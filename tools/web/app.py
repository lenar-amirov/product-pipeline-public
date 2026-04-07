#!/usr/bin/env python3
"""PM Pipeline Web Dashboard — Flask app."""

import json
import os
import re
import secrets
import shutil
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

PIPELINE_STEPS = [
    (1,  "analyze-cjm",              "Phase 1", "Анализ CJM"),
    (2,  "synthetic-research",        "Phase 1", "Синт. интервью"),
    (3,  "competitor-research",       "Phase 1", "Конкуренты"),
    (4,  "generate-research",         "Phase 1", "Бриф аналитику"),
    (5,  "create-survey-audience",    "Phase 1", "Аудитория"),
    (6,  "validate-problems",         "Phase 1", "Валидация"),
    (7,  "solution-hypotheses",       "Phase 1", "Гипотезы решений"),
    (8,  "sketch-solution",           "Phase 1", "Образ решения"),
    (9,  "review-design",             "Phase 1", "Ревью дизайна"),
    (10, "create-presentation",       "Phase 1", "Презентация Gate 1"),
    (11, "create-design-brief",       "Phase 2", "Дизайн-бриф"),
    (12, "estimate-with-dev",         "Phase 2", "Оценка разработки"),
    (13, "finalize-prd",              "Phase 2", "Финализация PRD"),
    (14, "design-ab-test",            "Phase 2", "AB-тест"),
    (15, "create-gate2-presentation", "Phase 2", "Презентация Gate 2"),
    (16, "support-task",              "Phase 3", "Бриф поддержке"),
    (17, "announce-ab-test",          "Phase 3", "Анонс AB-теста"),
    (18, "announce-release",          "Phase 3", "Анонс релиза"),
]

STEP_ARTIFACTS = {
    1:  [("Гипотезы проблем", "output/hypotheses.md")],
    2:  [("Синтетические интервью", "research/synthetic-interviews.md")],
    3:  [("Конкурентный анализ", "research/competitive-analysis.md")],
    4:  [("Бриф аналитику", "research/analytics-brief.md"),
         ("Вопросы опроса", "research/survey-questions.md")],
    5:  [("Бриф на аудиторию", "research/survey-audience-brief.md")],
    6:  [("Валидированные гипотезы", "output/validated-hypotheses.md")],
    7:  [("Гипотезы решений", "output/solution-hypotheses.md")],
    8:  [("Образ решения", "output/solution-sketch.md"),
         ("Экраны Stitch", "output/screens/")],
    9:  [],
    10: [("Презентация Gate 1", "output/presentation.md")],
    11: [("Дизайн-бриф", "output/design-brief.md")],
    12: [("Оценка разработки", "output/dev-estimate.md")],
    13: [("PRD", "output/PRD.md")],
    14: [("AB-тест", "output/ab-test-design.md")],
    15: [("Презентация Gate 2", "output/gate2-presentation.md")],
    16: [("Бриф поддержке", "output/support-brief.md")],
    17: [("Анонс AB-теста", "output/announce-ab-test.md")],
    18: [("Анонс релиза", "output/announce-release.md")],
}

PENDING_LABELS = {
    "analytics_brief":   ("Передай бриф аналитику", "research/analytics-brief.md"),
    "survey_brief":      ("Передай бриф на опрос", "research/survey-questions.md"),
    "audience_brief":    ("Передай бриф на выгрузку", "research/survey-audience-brief.md"),
    "analytics_results": ("Запроси результаты аналитики", "research/analytics-brief.md"),
    "survey_results":    ("Запроси результаты опроса", "research/survey-questions.md"),
    "design_brief":      ("Передай бриф дизайнеру", "output/design-brief.md"),
    "gate1_challenge":   ("Иди на Challenge Gate 1", "output/presentation.md"),
    "gate2_challenge":   ("Иди на Challenge Gate 2", "output/gate2-presentation.md"),
    "support_brief":     ("Передай бриф в поддержку", "output/support-brief.md"),
}

EXCLUDED_DIRS = {
    "template", "_template", ".claude", "tools", "config", "docs",
    "logs", "slides",
}

USERS = os.environ.get("PM_USERS", "alice,bob").split(",")
ADMIN_USER = os.environ.get("PM_ADMIN", USERS[0])

MD = markdown.Markdown(extensions=["extra", "tables", "fenced_code"])


# --- Jinja2 filters ---

@app.template_filter("md")
def markdown_filter(text):
    """Render markdown text to HTML."""
    if not text:
        return ""
    MD.reset()
    return MD.convert(text)


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
    m = re.search(r"^#\s+(?:Инициатива:\s*)?(.+)$", text, re.MULTILINE)
    if m:
        result["title"] = m.group(1).strip()

    # Metric
    m = re.search(r"\*\*Метрика[^*]*\*\*:\s*(.+)", text)
    if m:
        val = m.group(1).strip()
        if val and not val.startswith("["):
            result["metric"] = val

    # Segment
    m = re.search(r"\*\*Сегмент\*\*:\s*(.+)", text)
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

def find_template_dir(pm):
    """Find template directory — PM-specific first, then repo root."""
    pm_tmpl = pm_root(pm) / "template"
    if pm_tmpl.is_dir():
        return pm_tmpl
    root_tmpl = PIPELINE_ROOT / "template"
    if root_tmpl.is_dir():
        return root_tmpl
    return None


def create_initiative(pm, name):
    """Create a new initiative by copying template and initializing files."""
    tmpl = find_template_dir(pm)
    if not tmpl:
        raise FileNotFoundError("Template directory not found")

    target = pm_root(pm) / name
    shutil.copytree(str(tmpl), str(target))

    # Update CONTEXT.md placeholders
    ctx_path = target / "CONTEXT.md"
    if ctx_path.is_file():
        text = ctx_path.read_text(encoding="utf-8")
        text = text.replace("[НАЗВАНИЕ]", name).replace("[ИМЯ]", pm)
        ctx_path.write_text(text, encoding="utf-8")

    # Ensure output directory
    output_dir = target / "output"
    output_dir.mkdir(exist_ok=True)

    # Initialize status.json with all pipeline steps
    status = {"steps": {}, "pending": {}}
    for num, cmd, phase, label in PIPELINE_STEPS:
        status["steps"][str(num)] = {
            "status": "pending", "date": None, "summary": None,
        }
    (output_dir / "status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8",
    )

    # Initialize decisions.md
    dec_path = output_dir / "decisions.md"
    if not dec_path.is_file():
        dec_path.write_text("# Решения\n\n", encoding="utf-8")

    # Create CJM directory
    (target / "CJM").mkdir(exist_ok=True)

    return target


def generate_context_md(name, pm, fields):
    """Generate CONTEXT.md content from form fields."""
    def v(key, placeholder):
        return fields.get(key) or placeholder

    desc = fields.get("description", "").strip()

    lines = [
        f"# Инициатива: {v('title', name)}",
        "",
        f"**Продакт**: {pm}",
    ]
    if desc:
        lines += ["", "## О чём инициатива", desc]
    lines += [
        "",
        "## Цель",
        f"**Метрика, которую улучшаем**: {v('metric', '[конверсия в оплату / retention D7 / NPS / ...]')}",
        f"**Текущий baseline**: {v('baseline', '[X%]')}",
        f"**Целевой результат**: {v('target', '[Y%]')}",
        f"**Горизонт**: {v('horizon', '[квартал / 6 недель / ...]')}",
        "",
        "## Пользователь",
        f"**Сегмент**: {v('segment', '[новые пользователи / платящие / churned / ...]')}",
        f"**Размер сегмента**: {v('segment_size', '[DAU / MAU + доля от всех пользователей]')}",
        f"**Платформа**: {v('platform', '[web / iOS / Android / все]')}",
        f"**Ключевой сценарий на CJM**: {v('scenario', '[регистрация / онбординг / оформление заказа / ...]')}",
        "",
        "## Контекст",
        f"**Почему сейчас**: {v('why_now', '[что изменилось]')}",
        f"**Что уже пробовали**: {v('tried', '[что делали раньше]')}",
        f"**Ограничения**: {v('constraints', '[нельзя трогать X / нет бюджета на Y / ...]')}",
        f"**Связи с другими инициативами**: {v('links', '[что аффектит / от чего зависит]')}",
        "",
        "## CJM",
        "Материалы в папке `/CJM/`. Поддерживаемые форматы:",
        "- **PNG/JPG скрины**: `01_шаг-название.png`, `02_шаг-название.png` — экспорт из Miro/Figma",
        "- **Figma файл**: `*.fig` — читать через Figma MCP",
        "- **PDF**: `*.pdf` — экспорт из Miro/Notion",
        "",
        "Если шаг имеет состояния — отдельные файлы: `03a_form-empty.png`, `03b_form-error.png`",
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

    m = re.search(r"^#\s+(?:Инициатива:\s*)?(.+)$", text, re.MULTILINE)
    if m:
        val = m.group(1).strip()
        if val and not val.startswith("["):
            result["title"] = val

    # Description — text between "## О чём инициатива" and next "##"
    m = re.search(
        r"^## О чём инициатива\s*\n(.*?)(?=^## |\Z)",
        text, re.MULTILINE | re.DOTALL,
    )
    if m:
        result["description"] = m.group(1).strip()

    field_map = {
        r"\*\*Метрика[^*]*\*\*:\s*(.+)": "metric",
        r"\*\*Текущий baseline\*\*:\s*(.+)": "baseline",
        r"\*\*Целевой результат\*\*:\s*(.+)": "target",
        r"\*\*Горизонт\*\*:\s*(.+)": "horizon",
        r"\*\*Сегмент\*\*:\s*(.+)": "segment",
        r"\*\*Размер сегмента\*\*:\s*(.+)": "segment_size",
        r"\*\*Платформа\*\*:\s*(.+)": "platform",
        r"\*\*Ключевой сценарий на CJM\*\*:\s*(.+)": "scenario",
        r"\*\*Почему сейчас\*\*:\s*(.+)": "why_now",
        r"\*\*Что уже пробовали\*\*:\s*(.+)": "tried",
        r"\*\*Ограничения\*\*:\s*(.+)": "constraints",
        r"\*\*Связи с другими инициативами\*\*:\s*(.+)": "links",
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


@app.route("/share/static/<path:filename>")
def share_static(filename):
    """Serve static files for shared pages."""
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
    if not rel_path or ".." in rel_path:
        return jsonify({"error": "Неверный путь"}), 400

    base_path = pm_root(pm) / name
    full_path = base_path / rel_path

    if not full_path.is_file():
        return jsonify({"error": "Файл не найден"})

    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception:
        return jsonify({"error": "Ошибка чтения файла"})

    MD.reset()
    html = MD.convert(text)

    # Get file modification date
    try:
        mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
        updated = mtime.strftime("%Y-%m-%d")
    except Exception:
        updated = ""

    return jsonify({"html": html, "updated": updated})


@app.route("/<pm>/open/<name>", methods=["POST"])
def open_initiative(pm, name):
    if pm not in USERS:
        abort(404)
    initiative_path = str(pm_root(pm) / name)
    command = request.args.get("cmd", "")
    state_file = f"/tmp/pm-session-{pm}"
    try:
        content = initiative_path
        if command:
            content += f"\n/{command}"
        with open(state_file, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})


@app.route("/<pm>/new", methods=["GET"])
def new_initiative_form(pm):
    if pm not in USERS:
        abort(404)
    return render_template("new.html", pm=pm, error=None)


@app.route("/<pm>/new", methods=["POST"])
def new_initiative_submit(pm):
    if pm not in USERS:
        abort(404)

    name = request.form.get("name", "").strip()

    if not name:
        return render_template("new.html", pm=pm,
                               error="Введите название инициативы.")
    if not re.match(r"^[a-z0-9-]+$", name):
        return render_template("new.html", pm=pm,
                               error="Только строчные латинские буквы, цифры и дефисы.")

    target = pm_root(pm) / name
    if target.exists():
        return render_template("new.html", pm=pm,
                               error=f"Инициатива «{name}» уже существует.")

    try:
        create_initiative(pm, name)
    except Exception as e:
        return render_template("new.html", pm=pm, error=f"Ошибка создания: {e}")

    # Context fields
    ctx_fields = {}
    for key in ("title", "description", "metric", "baseline", "target",
                "horizon", "segment", "segment_size", "platform", "scenario",
                "why_now", "tried", "constraints", "links"):
        val = request.form.get(key, "").strip()
        if val:
            ctx_fields[key] = val
    if ctx_fields:
        ctx_text = generate_context_md(name, pm, ctx_fields)
        (target / "CONTEXT.md").write_text(ctx_text, encoding="utf-8")

    # CJM files
    cjm_files = request.files.getlist("cjm_files")
    cjm_labels_raw = request.form.get("cjm_labels", "")
    try:
        cjm_labels = json.loads(cjm_labels_raw) if cjm_labels_raw else []
    except json.JSONDecodeError:
        cjm_labels = []

    cjm_dir = target / "CJM"
    for i, f in enumerate(cjm_files):
        if f and f.filename:
            ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else "png"
            label = cjm_labels[i] if i < len(cjm_labels) else f"step-{i + 1}"
            safe_label = re.sub(r"[^a-zA-Z0-9\u0400-\u04ff_-]", "-", label)
            filename = f"{i + 1:02d}_{safe_label}.{ext}"
            f.save(str(cjm_dir / filename))

    return redirect(f"/{pm}/initiative/{name}")


@app.route(f"/{ADMIN_USER}/team")
def team_page():
    """Show all initiatives from all PMs (admin only)."""
    groups = []
    for user in USERS:
        inits = list_initiatives(user)
        if inits:
            groups.append({"pm": user, "initiatives": inits})
    return render_template("team.html", pm=ADMIN_USER, groups=groups, is_admin=True)


@app.route(f"/{ADMIN_USER}/team/<owner>/<name>")
def team_initiative_detail(owner, name):
    """View any PM's initiative in read-only mode (admin only)."""
    if owner not in USERS:
        abort(404)
    base_path = str(pm_root(owner) / name)
    if not os.path.isdir(base_path):
        abort(404)
    data = get_initiative_data(owner, base_path)
    decisions = parse_decisions(base_path)
    screens = get_screens(base_path)
    cjm_files = get_cjm_files(base_path)
    context_full = parse_context_full(base_path)
    return render_template(
        "initiative.html",
        pm=ADMIN_USER,
        owner_pm=owner,
        initiative=data,
        decisions=decisions,
        screens=screens,
        cjm_files=cjm_files,
        context_full=context_full,
        readonly=True,
        is_admin=True,
    )


@app.route(f"/{ADMIN_USER}/team/<owner>/<name>/cjm/<filename>")
def team_cjm_file(owner, name, filename):
    """Proxy CJM file from any PM's initiative."""
    if owner not in USERS or ".." in filename:
        abort(404)
    cjm_dir = pm_root(owner) / name / "CJM"
    if not (cjm_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(cjm_dir), filename)


@app.route(f"/{ADMIN_USER}/team/<owner>/<name>/screen/<filename>")
def team_screen_file(owner, name, filename):
    """Proxy screen file from any PM's initiative."""
    if owner not in USERS or ".." in filename:
        abort(404)
    screens_dir = pm_root(owner) / name / "output" / "screens"
    if not (screens_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(screens_dir), filename)


@app.route(f"/{ADMIN_USER}/team/<owner>/<name>/artifact")
def team_artifact_view(owner, name):
    """Proxy artifact from any PM's initiative."""
    if owner not in USERS:
        abort(404)
    rel_path = request.args.get("path", "")
    if not rel_path or ".." in rel_path:
        return jsonify({"error": "Неверный путь"}), 400
    full_path = pm_root(owner) / name / rel_path
    if not full_path.is_file():
        return jsonify({"error": "Файл не найден"})
    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception:
        return jsonify({"error": "Ошибка чтения файла"})
    MD.reset()
    html = MD.convert(text)
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

def _find_shared(token):
    """Find initiative by share token. Returns (pm, name, base_path) or None."""
    for user in USERS:
        root = pm_root(user)
        if not root.is_dir():
            continue
        for entry in os.listdir(root):
            if entry in EXCLUDED_DIRS or entry.startswith(".") or entry.startswith("_"):
                continue
            status_path = root / entry / "output" / "status.json"
            if not status_path.is_file():
                continue
            try:
                with open(status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("share_token") == token:
                    return user, entry, str(root / entry)
            except (json.JSONDecodeError, OSError):
                continue
    return None


@app.route("/<pm>/initiative/<name>/share", methods=["POST"])
def toggle_share(pm, name):
    """Generate or revoke share token."""
    if pm not in USERS:
        abort(404)
    status_path = pm_root(pm) / name / "output" / "status.json"
    if not status_path.is_file():
        abort(404)
    with open(status_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    action = request.args.get("action", "create")
    if action == "revoke":
        data.pop("share_token", None)
        token = None
    else:
        token = data.get("share_token") or secrets.token_urlsafe(16)
        data["share_token"] = token

    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "token": token})


@app.route("/share/<token>")
def shared_initiative(token):
    """Public read-only view of a shared initiative."""
    result = _find_shared(token)
    if not result:
        abort(404)
    owner, name, base_path = result
    data = get_initiative_data(owner, base_path)
    decisions = parse_decisions(base_path)
    screens = get_screens(base_path)
    cjm_files = get_cjm_files(base_path)
    context_full = parse_context_full(base_path)
    return render_template(
        "initiative.html",
        pm=owner,
        owner_pm=owner,
        initiative=data,
        decisions=decisions,
        screens=screens,
        cjm_files=cjm_files,
        context_full=context_full,
        readonly=True,
        shared=True,
        share_base="/share/" + token,
    )


@app.route("/share/<token>/artifact")
def shared_artifact(token):
    result = _find_shared(token)
    if not result:
        abort(404)
    owner, name, base_path = result
    rel_path = request.args.get("path", "")
    if not rel_path or ".." in rel_path:
        return jsonify({"error": "bad path"}), 400
    full_path = Path(base_path) / rel_path
    if not full_path.is_file():
        return jsonify({"error": "not found"})
    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception:
        return jsonify({"error": "read error"})
    MD.reset()
    html = MD.convert(text)
    try:
        mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
        updated = mtime.strftime("%Y-%m-%d")
    except Exception:
        updated = ""
    return jsonify({"html": html, "updated": updated})


@app.route("/share/<token>/cjm/<filename>")
def shared_cjm(token, filename):
    result = _find_shared(token)
    if not result or ".." in filename:
        abort(404)
    owner, name, base_path = result
    cjm_dir = Path(base_path) / "CJM"
    if not (cjm_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(cjm_dir), filename)


@app.route("/share/<token>/screen/<filename>")
def shared_screen(token, filename):
    result = _find_shared(token)
    if not result or ".." in filename:
        abort(404)
    owner, name, base_path = result
    screens_dir = Path(base_path) / "output" / "screens"
    if not (screens_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(screens_dir), filename)


@app.route("/<pm>/initiative/<name>/context", methods=["POST"])
def update_context(pm, name):
    """Update CONTEXT.md from form fields."""
    if pm not in USERS:
        abort(404)
    base_path = pm_root(pm) / name
    if not base_path.is_dir():
        abort(404)
    fields = {}
    for key in ("title", "description", "metric", "baseline", "target",
                "horizon", "segment", "segment_size", "platform", "scenario",
                "why_now", "tried", "constraints", "links"):
        val = request.form.get(key, "").strip()
        if val:
            fields[key] = val
    ctx_text = generate_context_md(name, pm, fields)
    (base_path / "CONTEXT.md").write_text(ctx_text, encoding="utf-8")
    return jsonify({"ok": True, "context": parse_context(str(base_path))})


@app.route("/<pm>/initiative/<name>/cjm/upload", methods=["POST"])
def cjm_upload(pm, name):
    """Upload CJM files."""
    if pm not in USERS:
        abort(404)
    base_path = pm_root(pm) / name
    if not base_path.is_dir():
        abort(404)
    cjm_dir = base_path / "CJM"
    cjm_dir.mkdir(exist_ok=True)

    # Find current max number
    max_num = 0
    if cjm_dir.is_dir():
        for fn in os.listdir(str(cjm_dir)):
            m = re.match(r"^(\d+)_", fn)
            if m:
                max_num = max(max_num, int(m.group(1)))

    files = request.files.getlist("files")
    labels_raw = request.form.get("labels", "")
    try:
        labels = json.loads(labels_raw) if labels_raw else []
    except json.JSONDecodeError:
        labels = []

    saved = []
    for i, f in enumerate(files):
        if f and f.filename:
            max_num += 1
            ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else "png"
            label = labels[i] if i < len(labels) else f"step-{max_num}"
            safe_label = re.sub(r"[^a-zA-Z0-9\u0400-\u04ff_-]", "-", label)
            filename = f"{max_num:02d}_{safe_label}.{ext}"
            f.save(str(cjm_dir / filename))
            saved.append({"filename": filename, "label": label})
    return jsonify({"ok": True, "files": saved})


@app.route("/<pm>/initiative/<name>/cjm/reorder", methods=["POST"])
def cjm_reorder(pm, name):
    """Reorder CJM files."""
    if pm not in USERS:
        abort(404)
    base_path = pm_root(pm) / name
    if not base_path.is_dir():
        abort(404)
    cjm_dir = base_path / "CJM"
    data = request.get_json()
    order = data.get("order", [])

    # Rename with temp prefix to avoid collisions
    for i, fname in enumerate(order):
        src = cjm_dir / fname
        if src.is_file():
            ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
            label_part = re.sub(r"^\d+_", "", fname.rsplit(".", 1)[0])
            tmp_name = f"_tmp_{i + 1:02d}_{label_part}.{ext}"
            src.rename(cjm_dir / tmp_name)

    # Rename from temp to final
    for fn in sorted(os.listdir(str(cjm_dir))):
        if fn.startswith("_tmp_"):
            (cjm_dir / fn).rename(cjm_dir / fn[5:])
    return jsonify({"ok": True, "files": get_cjm_files(str(base_path))})


@app.route("/<pm>/initiative/<name>/cjm/<filename>", methods=["GET", "DELETE"])
def cjm_file(pm, name, filename):
    """Serve or delete a CJM file."""
    if pm not in USERS:
        abort(404)
    if ".." in filename:
        abort(400)
    cjm_dir = pm_root(pm) / name / "CJM"
    path = cjm_dir / filename
    if request.method == "DELETE":
        if path.is_file():
            path.unlink()
        return jsonify({"ok": True})
    if not path.is_file():
        abort(404)
    return send_from_directory(str(cjm_dir), filename)


@app.route("/<pm>/onboarding")
def onboarding(pm):
    """Render ONBOARDING.md as HTML."""
    if pm not in USERS:
        abort(404)
    root = pm_root(pm)
    onboarding_path = root / "ONBOARDING.md"
    if not onboarding_path.is_file():
        abort(404)
    text = onboarding_path.read_text(encoding="utf-8")
    MD.reset()
    html = MD.convert(text)
    return render_template("onboarding.html", pm=pm, content=html)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
