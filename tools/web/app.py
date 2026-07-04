#!/usr/bin/env python3
"""Product Discovery Web Dashboard — Flask app."""

import json
import os
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

import markdown
from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   send_from_directory)

app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

# Server mode: PIPELINE_HOME=/home → /home/{pm}/pipeline/{initiative}
# Local mode: fallback to repo root → {root}/{pm}/{initiative}
_PIPELINE_HOME = os.environ.get("PIPELINE_HOME", "")
PIPELINE_ROOT = Path(__file__).parent.parent.parent


def pm_root(pm):
    """Return pipeline root dir for a given PM."""
    if _PIPELINE_HOME:
        return Path(_PIPELINE_HOME) / pm / "pipeline"
    return PIPELINE_ROOT / pm

# --- Constants ---

sys.path.insert(0, str(PIPELINE_ROOT / "tools" / "scripts"))
from pipeline_constants import MAIN_STEPS as PIPELINE_STEPS  # noqa: E402

STEP_ARTIFACTS = {
    1:  [("Problem Hypotheses", "output/hypotheses.md")],
    2:  [("Synthetic Interviews", "research/synthetic-interviews.md")],
    3:  [("Competitive Analysis", "research/competitive-analysis.md")],
    4:  [("Analytics Brief", "research/analytics-brief.md"),
         ("Survey Questions", "research/survey-questions.md")],
    5:  [("Audience Brief", "research/survey-audience-brief.md")],
    6:  [("Validated Hypotheses", "output/validated-hypotheses.md")],
    7:  [("Solution Hypotheses", "output/solution-hypotheses.md")],
    8:  [("Solution Sketch", "output/solution-sketch.md"),
         ("Screens", "output/screens/")],
    9:  [],
    10: [("Problem Research Report", "output/presentation.md")],
    11: [("Design Brief", "output/design-brief.md")],
    12: [("Dev Estimate", "output/dev-estimate.md")],
    13: [("PRD", "output/PRD.md")],
    14: [("AB Test Design", "output/ab-test-design.md")],
    15: [("Solution Research Report", "output/gate2-presentation.md")],
    16: [("AB Test Analysis", "output/ab-test-analysis.md")],
    17: [("GTM Plan", "output/gtm-plan.md")],
    18: [("GTM Materials", "output/gtm-materials.md")],
    19: [("Support Brief", "output/support-brief.md")],
}

PENDING_LABELS = {
    "analytics_brief":   ("Send brief to analyst", "research/analytics-brief.md"),
    "survey_brief":      ("Send survey brief", "research/survey-questions.md"),
    "audience_brief":    ("Send audience brief", "research/survey-audience-brief.md"),
    "analytics_results": ("Request analytics results", "research/analytics-brief.md"),
    "survey_results":    ("Request survey results", "research/survey-questions.md"),
    "design_brief":      ("Send brief to designer", "output/design-brief.md"),
    "gate1_challenge":   ("Present Problem Research Report", "output/presentation.md"),
    "gate2_challenge":   ("Present Solution Research Report", "output/gate2-presentation.md"),
    "support_brief":     ("Send brief to support", "output/support-brief.md"),
}

EXCLUDED_DIRS = {
    "template", "_template", ".claude", "tools", "config", "docs",
    "logs", "slides",
}

USERS = os.environ.get("PM_USERS", "alice,bob").split(",")
ADMIN_USER = os.environ.get("PM_ADMIN", USERS[0])

MD = markdown.Markdown(extensions=["extra", "tables", "fenced_code"])

# Defense-in-depth for rendered markdown: strip active content (scripts,
# event handlers, javascript: URLs). The dashboard is a local viewer of the
# PM's own files — this guards against pasted/imported content, it is not a
# substitute for a full sanitizer.
_BLOCK_RE = re.compile(
    r"<\s*(script|style|iframe|object|embed)\b.*?<\s*/\s*\1\s*>",
    re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(
    r"<\s*/?\s*(script|iframe|object|embed)\b[^>]*>", re.IGNORECASE)
_EVENT_RE = re.compile(
    r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", re.IGNORECASE)
_JSURL_RE = re.compile(
    r"(href|src)\s*=\s*([\"'])\s*javascript:[^\"']*\2", re.IGNORECASE)


def render_md(text):
    """Markdown → HTML with active content stripped."""
    if not text:
        return ""
    MD.reset()
    html = MD.convert(text)
    html = _BLOCK_RE.sub("", html)
    html = _TAG_RE.sub("", html)
    html = _EVENT_RE.sub("", html)
    html = _JSURL_RE.sub(r"\1=\2#\2", html)
    return html


def resolve_within(base, rel):
    """Resolve base/rel; return the path only if it stays inside base
    (symlink- and encoding-safe, unlike a '..' substring check)."""
    try:
        base_r = Path(base).resolve()
        full = (base_r / rel).resolve()
    except (OSError, ValueError):
        return None
    if full == base_r or base_r in full.parents:
        return full
    return None


# --- Jinja2 filters ---

@app.template_filter("md")
def markdown_filter(text):
    """Render markdown text to HTML (sanitized)."""
    return render_md(text)


# --- Helpers ---

def get_pm(req):
    return req.headers.get("X-PM-User", "")


def days_since(date_str):
    """Days since date_str (YYYY-MM-DD). 0 if today/future."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return max((date.today() - d).days, 0)
    except (ValueError, TypeError):
        return 0


def parse_context(base_path):
    """Extract key fields from CONTEXT.md."""
    ctx_path = os.path.join(base_path, "CONTEXT.md")
    result = {"metric": "—", "segment": "—", "title": "—"}
    try:
        with open(ctx_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return result

    # Title from first heading
    m = re.search(r"^#\s+(?:(?:Initiative|Инициатива):\s*)?(.+)$", text, re.MULTILINE)
    if m:
        result["title"] = m.group(1).strip()

    # Metric (English or Russian)
    m = re.search(r"\*\*(?:Metric[^*]*|Метрика[^*]*)\*\*:\s*(.+)", text)
    if m:
        val = m.group(1).strip()
        if val and not val.startswith("["):
            result["metric"] = val

    # Segment (English or Russian)
    m = re.search(r"\*\*(?:Segment|Сегмент)\*\*:\s*(.+)", text)
    if m:
        val = m.group(1).strip()
        if val and not val.startswith("["):
            result["segment"] = val

    return result


def parse_decisions(base_path, limit=None):
    """Parse decisions.md into list of {date, title, body}."""
    dec_path = os.path.join(base_path, "output", "decisions.md")
    try:
        with open(dec_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return []

    entries = []
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble
        lines = part.strip().split("\n", 1)
        header = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        # Parse "YYYY-MM-DD — Title"
        m = re.match(r"(\d{4}-\d{2}-\d{2})\s*[—–-]\s*(.+)", header)
        if m:
            entries.append({
                "date": m.group(1),
                "title": m.group(2).strip(),
                "body": body,
            })
        else:
            entries.append({"date": "", "title": header, "body": body})

    entries.reverse()  # newest first
    if limit:
        return entries[:limit]
    return entries


def get_initiative_data(pm, base_path):
    """Build initiative data dict from status.json + CONTEXT.md + decisions.md."""
    status_path = os.path.join(base_path, "output", "status.json")
    try:
        with open(status_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    name = os.path.basename(base_path)
    raw_steps = data.get("steps", {})
    raw_pending = data.get("pending", {})

    # Build steps
    steps = []
    steps_done = 0
    current_step = None
    current_phase = "Phase 1"

    for num, cmd, phase, label in PIPELINE_STEPS:
        step_data = raw_steps.get(str(num), {})
        status = step_data.get("status", "pending")
        step_date = step_data.get("date")
        summary = step_data.get("summary")

        if status == "done":
            steps_done += 1
        if status in ("paused", "in_progress") and current_step is None:
            current_step = num
            current_phase = phase
        if status == "pending" and current_step is None:
            current_step = num
            current_phase = phase

        # Artifacts for this step
        arts = []
        for art_label, art_path in STEP_ARTIFACTS.get(num, []):
            full_art = os.path.join(base_path, art_path)
            exists = os.path.isfile(full_art) and os.path.getsize(full_art) > 0
            arts.append({
                "label": art_label,
                "path": art_path,
                "exists": exists,
            })

        steps.append({
            "num": num,
            "command": cmd,
            "phase": phase,
            "label": label,
            "status": status,
            "date": step_date,
            "summary": summary,
            "artifacts": arts,
        })

    # Build pending
    pending_items = []
    for key, value in raw_pending.items():
        if value is not None and key in PENDING_LABELS:
            label, brief_path = PENDING_LABELS[key]
            days = days_since(value)
            pending_items.append({
                "key": key,
                "label": label,
                "brief_path": brief_path,
                "date": value,
                "days": days,
            })

    # Context
    context = parse_context(base_path)

    # Current step info
    if current_step is None:
        current_step = 18
        current_phase = "Phase 3"
    current_cmd = None
    current_status = "done"
    for s in steps:
        if s["num"] == current_step:
            current_cmd = s["command"]
            current_status = s["status"]
            break

    return {
        "name": name,
        "pm": pm,
        "steps": steps,
        "steps_done": steps_done,
        "total_steps": len(PIPELINE_STEPS),
        "current_step": current_step,
        "current_cmd": current_cmd,
        "current_status": current_status,
        "current_phase": current_phase,
        "pending": pending_items,
        "context": context,
        "path": base_path,
    }



def get_screens(base_path):
    """Return list of screen image files from output/screens/."""
    screens_dir = os.path.join(base_path, "output", "screens")
    if not os.path.isdir(screens_dir):
        return []
    screens = []
    for f in sorted(os.listdir(screens_dir)):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            screens.append({
                "filename": f,
                "label": f.rsplit(".", 1)[0].replace("_", " ").replace("-", " "),
            })
    return screens



def generate_context_md(name, pm, fields):
    """Generate CONTEXT.md content from form fields."""
    def v(key, placeholder):
        return fields.get(key) or placeholder

    desc = fields.get("description", "").strip()

    lines = [
        f"# Initiative: {v('title', name)}",
        "",
        f"**Product Manager**: {pm}",
    ]
    if desc:
        lines += ["", "## About", desc]
    lines += [
        "",
        "## Outcome",
        f"**Metric we're improving**: {v('metric', '[conversion to payment / retention D7 / NPS / ...]')}",
        f"**Current baseline**: {v('baseline', '[X%]')}",
        f"**Target result**: {v('target', '[Y%]')}",
        f"**Horizon**: {v('horizon', '[quarter / 6 weeks / ...]')}",
        "",
        "## User",
        f"**Segment**: {v('segment', '[new users / paying / churned / ...]')}",
        f"**Segment size**: {v('segment_size', '[DAU / MAU + share of total users]')}",
        f"**Platform**: {v('platform', '[web / iOS / Android / all]')}",
        f"**Key CJM scenario**: {v('scenario', '[registration / onboarding / checkout / ...]')}",
        "",
        "## Context",
        f"**Why now**: {v('why_now', '[what changed]')}",
        f"**What we tried before**: {v('tried', '[previous attempts]')}",
        "**Constraints**: " + v('constraints', "[can't touch X / no budget for Y / ...]"),
        f"**Related initiatives**: {v('links', '[what it affects / what it depends on]')}",
        "",
        "## CJM",
        "Materials in `/CJM/`. Supported formats:",
        "- **PNG/JPG screenshots**: `01_step-name.png`, `02_step-name.png` — export from Miro/Figma",
        "- **Figma file**: `*.fig` — read via Figma MCP",
        "- **PDF**: `*.pdf` — export from Miro/Notion",
        "",
        "If a step has states — separate files: `03a_form-empty.png`, `03b_form-error.png`",
    ]
    return "\n".join(lines) + "\n"


def parse_context_full(base_path):
    """Extract all fields from CONTEXT.md."""
    ctx_path = os.path.join(base_path, "CONTEXT.md")
    result = {
        "title": "", "description": "", "metric": "", "baseline": "",
        "target": "", "horizon": "", "segment": "", "segment_size": "",
        "platform": "", "scenario": "", "why_now": "",
        "tried": "", "constraints": "", "links": "",
    }
    try:
        with open(ctx_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return result

    m = re.search(r"^#\s+(?:(?:Initiative|Инициатива):\s*)?(.+)$", text, re.MULTILINE)
    if m:
        val = m.group(1).strip()
        if val and not val.startswith("["):
            result["title"] = val

    # Description — text between "## About" (or "## О чём инициатива") and next "##"
    m = re.search(
        r"^## (?:About|О чём инициатива)\s*\n(.*?)(?=^## |\Z)",
        text, re.MULTILINE | re.DOTALL,
    )
    if m:
        result["description"] = m.group(1).strip()

    field_map = {
        r"\*\*(?:Metric[^*]*|Метрика[^*]*)\*\*:\s*(.+)": "metric",
        r"\*\*(?:Current baseline|Текущий baseline)\*\*:\s*(.+)": "baseline",
        r"\*\*(?:Target result|Целевой результат)\*\*:\s*(.+)": "target",
        r"\*\*(?:Horizon|Горизонт)\*\*:\s*(.+)": "horizon",
        r"\*\*(?:Segment|Сегмент)\*\*:\s*(.+)": "segment",
        r"\*\*(?:Segment size|Размер сегмента)\*\*:\s*(.+)": "segment_size",
        r"\*\*(?:Platform|Платформа)\*\*:\s*(.+)": "platform",
        r"\*\*(?:Key CJM scenario|Ключевой сценарий на CJM)\*\*:\s*(.+)": "scenario",
        r"\*\*(?:Why now|Почему сейчас)\*\*:\s*(.+)": "why_now",
        r"\*\*(?:What we tried before|Что уже пробовали)\*\*:\s*(.+)": "tried",
        r"\*\*(?:Constraints|Ограничения)\*\*:\s*(.+)": "constraints",
        r"\*\*(?:Related initiatives|Связи с другими инициативами)\*\*:\s*(.+)": "links",
    }
    for pattern, key in field_map.items():
        m = re.search(pattern, text)
        if m:
            val = m.group(1).strip()
            if val and not val.startswith("["):
                result[key] = val

    return result


def get_cjm_files(base_path):
    """Return list of CJM files from CJM/ directory."""
    cjm_dir = os.path.join(base_path, "CJM")
    if not os.path.isdir(cjm_dir):
        return []
    files = []
    for f in sorted(os.listdir(cjm_dir)):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".pdf")):
            label = f.rsplit(".", 1)[0]
            label = re.sub(r"^\d+_", "", label)
            label = label.replace("_", " ").replace("-", " ")
            files.append({"filename": f, "label": label})
    return files


def list_initiatives(pm):
    """Return list of initiative data dicts."""
    root = pm_root(pm)
    initiatives = []
    if not root.is_dir():
        return []

    for entry in sorted(os.listdir(root)):
        if entry in EXCLUDED_DIRS or entry.startswith(".") or entry.startswith("_"):
            continue
        full = root / entry
        status_json = full / "output" / "status.json"
        if full.is_dir() and status_json.is_file():
            data = get_initiative_data(pm, str(full))
            if data:
                initiatives.append(data)

    return initiatives


def list_archived(pm):
    """Return list of archived initiative data dicts."""
    archive_dir = pm_root(pm) / "_archive"
    if not archive_dir.is_dir():
        return []
    result = []
    for entry in sorted(os.listdir(archive_dir)):
        full = archive_dir / entry
        status_json = full / "output" / "status.json"
        if full.is_dir() and status_json.is_file():
            data = get_initiative_data(pm, str(full))
            if data:
                result.append(data)
    return result


# --- Routes ---

@app.route("/<pm>/static/<path:filename>")
def pm_static(pm, filename):
    """Serve static files under /<pm>/static/ path."""
    return send_from_directory(app.static_folder, filename)


@app.route("/<pm>/")
def dashboard(pm):
    if pm not in USERS:
        abort(404)
    initiatives = list_initiatives(pm)
    return render_template("dashboard.html", pm=pm, initiatives=initiatives)



@app.route("/<pm>/initiative/<name>/screen/<filename>")
def screen_image(pm, name, filename):
    """Serve generated screen images."""
    if pm not in USERS:
        abort(404)
    if ".." in filename:
        abort(400)
    screens_dir = pm_root(pm) / name / "output" / "screens"
    if not (screens_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(screens_dir), filename)


@app.route("/<pm>/initiative/<name>")
def initiative_detail(pm, name):
    if pm not in USERS:
        abort(404)
    base_path = str(pm_root(pm) / name)
    if not os.path.isdir(base_path):
        abort(404)
    data = get_initiative_data(pm, base_path)
    decisions = parse_decisions(base_path)
    screens = get_screens(base_path)
    cjm_files = get_cjm_files(base_path)
    context_full = parse_context_full(base_path)
    return render_template(
        "initiative.html",
        pm=pm,
        initiative=data,
        decisions=decisions,
        screens=screens,
        cjm_files=cjm_files,
        context_full=context_full,
    )


@app.route("/<pm>/initiative/<name>/artifact")
def artifact_view(pm, name):
    """Return rendered markdown artifact as JSON."""
    if pm not in USERS:
        abort(404)
    rel_path = request.args.get("path", "")
    if not rel_path or ".." in rel_path or "/" in name or ".." in name:
        return jsonify({"error": "Invalid path"}), 400

    base_path = pm_root(pm) / name
    full_path = resolve_within(base_path, rel_path)

    if full_path is None or not full_path.is_file():
        return jsonify({"error": "File not found"})

    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception:
        return jsonify({"error": "Error reading file"})

    html = render_md(text)

    # Get file modification date
    try:
        mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
        updated = mtime.strftime("%Y-%m-%d")
    except Exception:
        updated = ""

    return jsonify({"html": html, "updated": updated})


@app.route("/<pm>/archive")
def archive_page(pm):
    """Show archived initiatives."""
    if pm not in USERS:
        abort(404)
    archived = list_archived(pm)
    return render_template("archive.html", pm=pm, initiatives=archived)


@app.route("/<pm>/initiative/<name>/archive", methods=["POST"])
def archive_initiative(pm, name):
    """Move initiative to _archive/."""
    if pm not in USERS:
        abort(404)
    root = pm_root(pm)
    src = root / name
    if not src.is_dir():
        abort(404)
    archive_dir = root / "_archive"
    archive_dir.mkdir(exist_ok=True)
    dst = archive_dir / name
    if dst.exists():
        return jsonify({"ok": False, "error": "Already archived"}), 409
    shutil.move(str(src), str(dst))
    return jsonify({"ok": True})


@app.route("/<pm>/initiative/<name>/restore", methods=["POST"])
def restore_initiative(pm, name):
    """Restore initiative from _archive/."""
    if pm not in USERS:
        abort(404)
    root = pm_root(pm)
    src = root / "_archive" / name
    if not src.is_dir():
        abort(404)
    dst = root / name
    if dst.exists():
        return jsonify({"ok": False, "error": "Name conflict"}), 409
    shutil.move(str(src), str(dst))
    return jsonify({"ok": True})


# --- Share (read-only public link) ---

@app.route("/<pm>/initiative/<name>/cjm/<filename>")
def cjm_file(pm, name, filename):
    """Serve or delete a CJM file."""
    if pm not in USERS:
        abort(404)
    if ".." in filename:
        abort(400)
    cjm_dir = pm_root(pm) / name / "CJM"
    path = cjm_dir / filename
    if not path.is_file():
        abort(404)
    return send_from_directory(str(cjm_dir), filename)


if __name__ == "__main__":
    # Local viewer by default. Set PIPELINE_HOST=0.0.0.0 only on a trusted
    # network — the app has no real authentication.
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    host = os.environ.get("PIPELINE_HOST", "127.0.0.1")
    debug = os.environ.get("PIPELINE_DEBUG", "") == "1"
    app.run(host=host, port=port, debug=debug)
