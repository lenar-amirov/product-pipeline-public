#!/usr/bin/env python3
"""
Telegram reminder script for PM pipeline.
Reads from a git clone of the shared PM pipeline repo.

Cron: 0 8 * * * cd /opt/pm-pipeline && git pull --quiet && python3 tools/scripts/remind.py
(8 UTC = 11 MSK)

Env: PM_PIPELINE_DIR — path to the local clone (default: /opt/pm-pipeline)
"""

import json
import os
import glob
import subprocess
from datetime import date, timedelta
import urllib.request
import urllib.error

BASE_DIR = os.environ.get("PM_PIPELINE_DIR", "/opt/pm-pipeline")
CONFIG_FILE = os.path.join(BASE_DIR, "config", "telegram.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "remind.log")

# --- Rules ---
# remind_after_days: первое напоминание через N дней после активации
# repeat_every_days: повторять каждые N дней (0 = только один раз)
# friday_digest: включить в пятничный дайджест аналитики
# remind_on: "next_monday" — специальное правило (один раз, в ближайший понедельник)

RULES = {
    "analytics_brief": {
        "emoji": "📊",
        "title": "Передай бриф аналитику",
        "body": "Бриф готов в <code>research/analytics-brief.md</code>",
        "hint": "Когда передашь → скажи в Cowork «аналитику передал»",
        "remind_after_days": 1,
        "repeat_every_days": 0,
        "friday_digest": True,
    },
    "survey_brief": {
        "emoji": "📝",
        "title": "Передай бриф на опрос",
        "body": "Бриф готов в <code>research/survey-questions.md</code>",
        "hint": "Когда передашь → скажи в Cowork «опрос передал»",
        "remind_after_days": 1,
        "repeat_every_days": 0,
        "friday_digest": True,
    },
    "audience_brief": {
        "emoji": "👥",
        "title": "Передай бриф на выгрузку аудитории",
        "body": "Бриф готов в <code>research/survey-audience-brief.md</code>",
        "hint": "Когда передашь → скажи в Cowork «выгрузку передал»",
        "remind_after_days": 1,
        "repeat_every_days": 0,
        "friday_digest": True,
    },
    "analytics_results": {
        "emoji": "📈",
        "title": "Запроси результаты у аналитика",
        "body": "Прошла неделя с момента передачи задач",
        "hint": "Когда получишь → открой Cowork и скажи «результаты аналитики: ...»",
        "remind_after_days": 7,
        "repeat_every_days": 7,
        "friday_digest": True,
    },
    "survey_results": {
        "emoji": "📋",
        "title": "Запроси результаты опроса",
        "body": "Прошло 2 недели с момента передачи опроса",
        "hint": "Когда получишь → открой Cowork и скажи «результаты опроса: ...»",
        "remind_after_days": 14,
        "repeat_every_days": 7,
        "friday_digest": True,
    },
    "design_brief": {
        "emoji": "🎨",
        "title": "Передай бриф дизайнеру",
        "body": "Бриф готов в <code>output/design-brief.md</code>",
        "hint": "Когда передашь → скажи в Cowork «бриф дизайнеру передал»",
        "remind_after_days": 1,
        "repeat_every_days": 0,
    },
    "gate1_challenge": {
        "emoji": "🎯",
        "title": "Иди на Problem Research Report",
        "body": "Презентация готова, пора защищать",
        "hint": "Когда сходишь → открой Cowork и скажи «Report прошёл: ...»",
        "remind_on": "next_monday",
    },
    "gate2_challenge": {
        "emoji": "🏁",
        "title": "Иди на Solution Research Report",
        "body": "Презентация готова, пора защищать",
        "hint": "Когда сходишь → открой Cowork и скажи «Report прошёл: ...»",
        "remind_on": "next_monday",
    },
}


def next_monday(from_date: date) -> date:
    """Ближайший понедельник строго после from_date."""
    days_ahead = -from_date.weekday() % 7
    if days_ahead == 0:
        days_ahead = 7
    return from_date + timedelta(days=days_ahead)


def should_remind(event_date: date, today: date, rule: dict) -> bool:
    if "remind_on" in rule:
        if rule["remind_on"] == "next_monday":
            return today == next_monday(event_date)
        return False

    days = (today - event_date).days
    after = rule.get("remind_after_days", 1)
    repeat = rule.get("repeat_every_days", 0)

    if days < after:
        return False
    if days == after:
        return True
    if repeat == 0:
        return False
    return (days - after) % repeat == 0


def send_telegram(bot_token: str, chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except urllib.error.URLError as e:
        log(f"  Telegram error: {e}")
        return False


def log(msg: str):
    ts = date.today().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def git_pull():
    """Pull latest changes from remote."""
    try:
        subprocess.run(["git", "-C", BASE_DIR, "pull", "--rebase", "--quiet"],
                       capture_output=True, timeout=30)
    except Exception as e:
        log(f"git pull error: {e}")


def main():
    git_pull()

    if not os.path.exists(CONFIG_FILE):
        log(f"Config not found: {CONFIG_FILE}")
        return

    with open(CONFIG_FILE) as f:
        config = json.load(f)

    bot_token = config.get("bot_token", "")
    pms_config = config.get("pms", {})

    if not bot_token or "YOUR_BOT_TOKEN" in bot_token:
        log("Bot token not configured")
        return

    today = date.today()
    is_friday = today.weekday() == 4
    sent = 0

    # pm → list of digest lines
    friday_digest: dict[str, list[str]] = {}

    for status_file in glob.glob(f"{BASE_DIR}/*/*/output/status.json"):
        try:
            with open(status_file) as f:
                status = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        pm = status.get("pm", "")
        initiative = status.get("initiative",
            os.path.basename(os.path.dirname(os.path.dirname(status_file)))
        )
        pending = status.get("pending", {})
        chat_id = pms_config.get(pm)

        if not chat_id or "YOUR_TELEGRAM" in str(chat_id):
            continue

        for event_type, event_date_str in pending.items():
            if not event_date_str:
                continue

            rule = RULES.get(event_type)
            if not rule:
                continue

            try:
                event_date = date.fromisoformat(event_date_str)
            except ValueError:
                continue

            days = (today - event_date).days

            # Friday digest: collect analytics items separately
            if is_friday and rule.get("friday_digest"):
                if pm not in friday_digest:
                    friday_digest[pm] = []
                friday_digest[pm].append(
                    f"{rule['emoji']} <b>{initiative}</b>: {rule['title']}"
                    + (f" ({days} дн.)" if days > 0 else "")
                )
                # Still fire individual reminder if due today (e.g. day 1)
                if not should_remind(event_date, today, rule):
                    continue
            else:
                if not should_remind(event_date, today, rule):
                    continue

            text = (
                f"{rule['emoji']} <b>{initiative}</b>\n\n"
                f"<b>{rule['title']}</b>\n"
                f"{rule['body']}\n\n"
                f"💡 {rule['hint']}"
            )

            if send_telegram(bot_token, chat_id, text):
                log(f"Sent to {pm}: {initiative} / {event_type} (day {days})")
                sent += 1

    # Check for stale initiatives (no active pending events + not updated for 14 days)
    for status_file in glob.glob(f"{BASE_DIR}/*/*/output/status.json"):
        try:
            with open(status_file) as f:
                status = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        pm = status.get("pm", "")
        initiative = status.get("initiative",
            os.path.basename(os.path.dirname(os.path.dirname(status_file)))
        )
        pending = status.get("pending", {})
        chat_id = pms_config.get(pm)

        if not chat_id or "YOUR_TELEGRAM" in str(chat_id):
            continue

        has_active = any(v is not None for v in pending.values())
        if has_active:
            continue

        mtime = date.fromtimestamp(os.path.getmtime(status_file))
        days_stale = (today - mtime).days

        if days_stale >= 14 and (days_stale - 14) % 14 == 0:
            text = (
                f"💤 <b>{initiative}</b>\n\n"
                f"<b>Инициатива не обновлялась {days_stale} дней</b>\n"
                f"Нет активных задач в пайплайне\n\n"
                f"💡 Продолжи работу над следующим шагом или закрой инициативу"
            )
            if send_telegram(bot_token, chat_id, text):
                log(f"Stale reminder → {pm}: {initiative} ({days_stale} days)")
                sent += 1

    # Send Friday digest
    if is_friday:
        for pm, items in friday_digest.items():
            chat_id = pms_config.get(pm)
            if not chat_id or not items:
                continue
            text = "📅 <b>Пятница: задачи у аналитика</b>\n\n" + "\n".join(items)
            if send_telegram(bot_token, chat_id, text):
                log(f"Friday digest → {pm}: {len(items)} item(s)")
                sent += 1

    log(f"Done. Sent {sent} reminder(s).")


if __name__ == "__main__":
    main()
