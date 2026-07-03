#!/usr/bin/env python3
"""
scan-initiatives.py — generate .initiatives-digest.md from all PM initiatives.

Reads all {pm}/*/output/status.json + CONTEXT.md + validated-hypotheses.md,
produces a single digest file Claude reads at session start to know
about the PM's history and detect overlaps with new initiatives.

Run via SessionStart hook in .claude/settings.json.
"""

import json
import glob
import os
import re
import sys
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_constants import enabled_total, find_current_step, MAX_STEP  # noqa: E402


def find_pm():
    pm_file = REPO_ROOT / ".pm-local"
    return pm_file.read_text().strip() if pm_file.exists() else None


def parse_context(context_path: Path) -> dict:
    """Extract key fields from CONTEXT.md (English + Russian field names)."""
    if not context_path.exists():
        return {}
    text = context_path.read_text(encoding='utf-8')
    fields = {}
    # Values may span multiple lines (lists, sub-bullets) — capture until the
    # next bold field at line start, a heading, a blank line, or end of text.
    _VALUE = r'(.+?)(?=\n\*\*|\n#|\n\n|\Z)'
    patterns = {
        'metric': r'\*\*(?:Metric we\'re improving|Метрика, которую улучшаем)\*\*:\s*' + _VALUE,
        'baseline': r'\*\*(?:Current baseline|Текущий baseline)\*\*:\s*' + _VALUE,
        'target': r'\*\*(?:Target result|Целевой результат)\*\*:\s*' + _VALUE,
        'horizon': r'\*\*(?:Horizon|Горизонт)\*\*:\s*' + _VALUE,
        'segment': r'\*\*(?:Segment|Сегмент)\*\*:\s*' + _VALUE,
        'why_now': r'\*\*(?:Why now|Почему сейчас)\*\*:\s*' + _VALUE,
    }
    placeholder_markers = [
        r'\[X%?\]', r'\[Y%?\]', r'\[to be validated\]',
        r'\[NAME\]', r'\[INITIATIVE_NAME\]', r'\[PM_NAME\]',
        r'\[conversion to', r'\[new users', r'\[quarter',
        r'\[web / iOS', r'\[registration',
    ]
    for key, pattern in patterns.items():
        m = re.search(pattern, text, re.DOTALL)
        if m:
            # Collapse a multi-line value into a single digest line
            val = ' '.join(m.group(1).split())
            # Skip if matches a known placeholder marker
            if any(re.search(p, val, re.IGNORECASE) for p in placeholder_markers):
                continue
            # Skip if value is mostly bracketed placeholder text
            if val.startswith('[') and val.find(']') > 0 and len(val) < 80:
                continue
            fields[key] = val[:200]
    return fields


def parse_hypotheses(hyps_path: Path) -> list:
    """Extract hypothesis numbers + titles from validated-hypotheses.md."""
    if not hyps_path.exists():
        return []
    text = hyps_path.read_text(encoding='utf-8')
    hyps = re.findall(
        r'^## (?:Hypothesis|Гипотеза)\s+P?(\d+):?\s*(.+)$',
        text,
        re.MULTILINE,
    )
    return [(num, title.strip()) for num, title in hyps[:8]]


def parse_registry(init_dir: Path) -> dict:
    """Hypothesis verdicts from output/hypotheses.json (E1 registry)."""
    path = init_dir / "output" / "hypotheses.json"
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            hyps = json.load(f).get("hypotheses", [])
    except (json.JSONDecodeError, OSError):
        return {}
    return {
        "confirmed": [h["id"] for h in hyps
                      if h.get("status") in ("confirmed", "reframed")
                      and h.get("evidence_type") == "REAL"],
        "refuted": [h["id"] for h in hyps if h.get("status") == "refuted"],
        "open": [h["id"] for h in hyps
                 if h.get("status") in ("draft", "testing")],
        "flagged": [h["id"] for h in hyps if h.get("flags")],
    }


def get_status(status_path: str) -> dict:
    try:
        with open(status_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def scan_initiatives(pm: str) -> list:
    pattern = str(REPO_ROOT / pm / "*" / "output" / "status.json")
    out = []
    for status_path in sorted(glob.glob(pattern)):
        init_dir = Path(status_path).parent.parent
        name = init_dir.name
        if name.startswith("_") or name == "_archive":
            continue

        status = get_status(status_path)
        context = parse_context(init_dir / "CONTEXT.md")
        validated = parse_hypotheses(init_dir / "output" / "validated-hypotheses.md")
        registry = parse_registry(init_dir)

        steps = status.get("steps", {})
        done = sum(
            1 for s in steps.values()
            if isinstance(s, dict) and s.get("status") == "done"
        )
        total = enabled_total(status.get("pipeline_config", {}))
        current_step = find_current_step(steps)

        # Archived = either explicitly archived or all enabled steps done
        is_active = current_step is None or current_step < MAX_STEP

        out.append({
            'name': name,
            'pm': pm,
            'created': status.get('created', ''),
            'current_step': current_step or 0,
            'progress': f"{done}/{total}",
            'active': is_active,
            'context': context,
            'validated': validated,
            'registry': registry,
        })
    return out


def render(initiatives: list) -> str:
    today = date.today().isoformat()
    lines = [
        "# Initiatives Digest",
        "",
        f"> Auto-generated {today} by `tools/scripts/scan-initiatives.py`.",
        "> Claude reads this at every session start to know about past initiatives",
        "> and detect overlaps with new problems. Don't edit manually — overwritten.",
        "",
    ]

    active = [i for i in initiatives if i['active']]
    archived = [i for i in initiatives if not i['active']]

    if not initiatives:
        lines.append("_No initiatives yet._")
        return "\n".join(lines)

    if active:
        lines.append("## Active")
        lines.append("")
        for i in active:
            lines.append(f"### {i['name']} — Step {i['current_step']}, {i['progress']}")
            ctx = i['context']
            if 'metric' in ctx:
                lines.append(f"- **Metric**: {ctx['metric']}")
            if 'baseline' in ctx or 'target' in ctx:
                lines.append(
                    f"- **Baseline → Target**: {ctx.get('baseline', '?')} → {ctx.get('target', '?')}"
                )
            if 'segment' in ctx:
                lines.append(f"- **Segment**: {ctx['segment']}")
            if 'why_now' in ctx:
                lines.append(f"- **Why now**: {ctx['why_now']}")
            reg = i.get('registry') or {}
            if reg:
                parts = []
                if reg.get('confirmed'):
                    parts.append("✅ REAL: " + ", ".join(reg['confirmed']))
                if reg.get('refuted'):
                    parts.append("❌ " + ", ".join(reg['refuted']))
                if reg.get('open'):
                    parts.append(f"открыто: {len(reg['open'])}")
                if reg.get('flagged'):
                    parts.append("⚠️ flags: " + ", ".join(reg['flagged']))
                lines.append("- **Hypotheses**: " + " · ".join(parts))
            elif i['validated']:
                vstr = ", ".join(f"P{n}" for n, _ in i['validated'])
                lines.append(f"- **Validated hypotheses**: {vstr}")
            lines.append("")

    if archived:
        lines.append("## Completed / Archived")
        lines.append("")
        for i in archived:
            lines.append(f"### {i['name']} — {i['progress']} (created {i['created']})")
            ctx = i['context']
            if 'metric' in ctx:
                lines.append(f"- **Metric**: {ctx['metric']}")
            if 'segment' in ctx:
                lines.append(f"- **Segment**: {ctx['segment']}")
            if i['validated']:
                vstr = ", ".join(f"P{n}: {t[:60]}" for n, t in i['validated'][:3])
                lines.append(f"- **Validated hypotheses**: {vstr}")
            lines.append("")

    return "\n".join(lines)


def main():
    pm = find_pm()
    if not pm:
        # No PM yet — write empty digest so Claude doesn't choke on missing file
        digest = "# Initiatives Digest\n\n_No PM identified (.pm-local missing)._\n"
    else:
        initiatives = scan_initiatives(pm)
        digest = render(initiatives)

    out_path = REPO_ROOT / ".initiatives-digest.md"
    out_path.write_text(digest, encoding='utf-8')


if __name__ == "__main__":
    main()
