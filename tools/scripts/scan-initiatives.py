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

        steps = status.get("steps", {})
        config_steps = status.get("pipeline_config", {}).get("steps", {})
        done = sum(
            1 for s in steps.values()
            if isinstance(s, dict) and s.get("status") == "done"
        )
        if config_steps:
            total = sum(
                1 for v in config_steps.values()
                if isinstance(v, dict) and v.get("enabled")
            )
        else:
            total = 19

        # Find current step
        current_step = None
        for num in range(19, -1, -1):
            s = steps.get(str(num), {})
            if isinstance(s, dict) and s.get("status") in ("in_progress", "paused"):
                current_step = num
                break
            elif isinstance(s, dict) and s.get("status") == "done":
                current_step = num + 1
                break

        # Fresh initiative (all pending) — current step is 0
        if current_step is None and steps:
            current_step = 0

        # Archived = either explicitly archived or all enabled steps done
        is_active = current_step is None or current_step < 19

        out.append({
            'name': name,
            'pm': pm,
            'created': status.get('created', ''),
            'current_step': current_step or 0,
            'progress': f"{done}/{total}",
            'active': is_active,
            'context': context,
            'validated': validated,
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
            if i['validated']:
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
