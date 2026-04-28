#!/usr/bin/env python3
"""
Telegram bot for PM pipeline.
Receives confirmation commands from PMs, updates output/status.json.

Reads from a git clone of the shared PM pipeline repo.
Env: PM_PIPELINE_DIR — path to the local clone (default: /opt/pm-pipeline)
"""

import json
import os
import glob
import time
import sys
import subprocess
from datetime import date
import urllib.request
import urllib.error

BASE_DIR = os.environ.get("PM_PIPELINE_DIR", "/opt/pm-pipeline")
CONFIG_FILE = os.path.join(BASE_DIR, "config", "telegram.json")
STATE_FILE = os.path.join(BASE_DIR, "logs", "bot-state.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "bot.log")

# command-name (without /) → action spec
COMMANDS = {
    "analytics-brief-sent": {
        "close": "analytics_brief",
        "activate": "analytics_results",
    },
    "survey-brief-sent": {
        "close": "survey_brief",
        "activate": "survey_results",
    },
    "audience-brief-sent": {
        "close": "audience_brief",
        "activate": None,
    },
    "design-brief-sent": {
        "close": "design_brief",
        "activate": None,
    },
    "confirm-analytics-results": {
        "close": "analytics_results",
        "activate": None,
        "question": "What did the analyst find? Key numbers and conclusions.",
        "save_to": "research/analytics-data.md",
    },
    "confirm-survey-results": {
        "close": "survey_results",
        "activate": None,
        "question": "What did the survey show? Key numbers, patterns, surprises.",
        "save_to": "research/survey-results.md",
    },
    "confirm-gate1-challenge": {
        "close": "gate1_challenge",
        "activate": None,
        "question": "Problem Research Report result? (approved / needs rework — specifics)",
        "save_to": "output/decisions.md",
    },
    "confirm-gate2-challenge": {
        "close": "gate2_challenge",
        "activate": None,
        "question": "Solution Research Report result? (approved / needs rework — specifics)",
        "save_to": "output/decisions.md",
    },
}

SIMPLE_REPLIES = {
    "analytics-brief-sent": "Noted. Will remind you to request analyst results in 1 week.",
    "survey-brief-sent": "Noted. Will remind you to request survey results in 2 weeks.",
    "audience-brief-sent": "Noted.",
    "design-brief-sent": "Noted.",
}


# ── Helpers ────────────────────────────────────────────────────────────────

def log(msg):
    ts = date.today().isoformat()
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp, STATE_FILE)


def get_updates(token, offset):
    url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=30"
    try:
        with urllib.request.urlopen(url, timeout=35) as r:
            return json.loads(r.read())
    except Exception as e:
        log(f"getUpdates error: {e}")
        return {"ok": False, "result": []}


def send(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"send error: {e}")


def git_pull():
    """Pull latest changes from remote."""
    try:
        subprocess.run(["git", "-C", BASE_DIR, "pull", "--rebase", "--quiet"],
                       capture_output=True, timeout=30)
    except Exception as e:
        log(f"git pull error: {e}")


def find_initiatives(pm_name, event_key):
    """Return list of dicts {initiative, status_path, base_path} where event_key is active."""
    result = []
    for status_path in glob.glob(os.path.join(BASE_DIR, pm_name, "*", "output", "status.json")):
        try:
            with open(status_path) as f:
                s = json.load(f)
            if s.get("pending", {}).get(event_key) is not None:
                base_path = os.path.dirname(os.path.dirname(status_path))
                result.append({
                    "initiative": s.get("initiative",
                        os.path.basename(base_path)),
                    "status_path": status_path,
                    "base_path": base_path,
                })
        except (json.JSONDecodeError, OSError):
            pass
    return result


def update_status(status_path, close_key, activate_key):
    with open(status_path) as f:
        status = json.load(f)
    pending = status.setdefault("pending", {})
    pending[close_key] = None
    if activate_key:
        pending[activate_key] = date.today().isoformat()
    tmp = status_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    os.replace(tmp, status_path)


def save_text(base_path, relative_path, text):
    full_path = os.path.join(base_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    today = date.today().isoformat()
    with open(full_path, "a") as f:
        f.write(f"\n## {today}\n\n{text}\n")


# ── Message handling ────────────────────────────────────────────────────────

def handle_command(token, chat_id, pm_name, cmd_name, state):
    """Process a slash command. Returns new conversation state or None."""
    spec = COMMANDS.get(cmd_name)
    if not spec:
        send(token, chat_id, "Unknown command.")
        return None

    candidates = find_initiatives(pm_name, spec["close"])

    if not candidates:
        send(token, chat_id, f"No active <code>{spec['close']}</code> tasks in your initiatives.")
        return None

    if len(candidates) == 1:
        return _proceed(token, chat_id, cmd_name, spec, candidates[0], state)

    # Multiple initiatives — ask to choose
    lines = "\n".join(f"{i+1}. <b>{c['initiative']}</b>" for i, c in enumerate(candidates))
    send(token, chat_id, f"Multiple initiatives with this task:\n\n{lines}\n\nType a number.")
    return {"step": "choose", "cmd": cmd_name, "candidates": candidates}


def _proceed(token, chat_id, cmd_name, spec, candidate, state):
    """Execute action or ask for text input. Returns new state or None."""
    if "question" in spec:
        send(token, chat_id,
             f"<b>{candidate['initiative']}</b>\n\n{spec['question']}")
        return {"step": "text", "cmd": cmd_name, "candidate": candidate}
    else:
        update_status(candidate["status_path"], spec["close"], spec.get("activate"))
        send(token, chat_id,
             f"<b>{candidate['initiative']}</b>\n\n{SIMPLE_REPLIES[cmd_name]}")
        log(f"{pm_name if 'pm_name' in dir() else '?'}: {candidate['initiative']} / {cmd_name}")
        return None


def handle_text(token, chat_id, pm_name, text, conv):
    """Handle free-text reply during an active conversation."""
    step = conv.get("step")

    if step == "choose":
        candidates = conv["candidates"]
        try:
            idx = int(text.strip()) - 1
            if not 0 <= idx < len(candidates):
                raise ValueError
        except ValueError:
            send(token, chat_id, f"Type a number from 1 to {len(candidates)}.")
            return conv  # keep state

        cmd_name = conv["cmd"]
        spec = COMMANDS[cmd_name]
        return _proceed(token, chat_id, cmd_name, spec, candidates[idx], conv)

    if step == "text":
        cmd_name = conv["cmd"]
        spec = COMMANDS[cmd_name]
        candidate = conv["candidate"]
        save_text(candidate["base_path"], spec["save_to"], text)
        update_status(candidate["status_path"], spec["close"], spec.get("activate"))
        send(token, chat_id,
             f"<b>{candidate['initiative']}</b>\n\n"
             f"Saved to <code>{spec['save_to']}</code>")
        log(f"{pm_name}: {candidate['initiative']} / {cmd_name}")
        return None

    return None


# ── Main loop ───────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(CONFIG_FILE):
        log(f"Config not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE) as f:
        config = json.load(f)

    token = config.get("bot_token", "")
    if not token or "YOUR_BOT_TOKEN" in token:
        log("Bot token not configured")
        sys.exit(1)

    pms = config.get("pms", {})
    chat_to_pm = {str(v): k for k, v in pms.items()}

    log("Bot started")
    offset = 0
    state = load_state()  # {chat_id_str: conversation_state | None}
    last_pull = 0

    while True:
        # Pull from git every 5 minutes
        now = time.time()
        if now - last_pull > 300:
            git_pull()
            last_pull = now

        result = get_updates(token, offset)
        if not result.get("ok"):
            time.sleep(5)
            continue

        for update in result.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message")
            if not msg:
                continue

            chat_id = str(msg["chat"]["id"])
            text = msg.get("text", "").strip()
            if not text:
                continue

            pm_name = chat_to_pm.get(chat_id)
            if not pm_name:
                continue  # ignore unknown senders

            conv = state.get(chat_id)

            if text.startswith("/"):
                # Strip /command@botname → command
                cmd_name = text.split()[0].lstrip("/").split("@")[0]
                new_conv = handle_command(token, chat_id, pm_name, cmd_name, conv)
            elif conv:
                new_conv = handle_text(token, chat_id, pm_name, text, conv)
            else:
                send(token, chat_id,
                     "Use commands from reminders or type /help.")
                new_conv = None

            state[chat_id] = new_conv
            save_state(state)


if __name__ == "__main__":
    main()
