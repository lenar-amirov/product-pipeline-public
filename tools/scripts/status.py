#!/usr/bin/env python3
"""
status.py — branded dashboard for Product Discovery pipeline.

Two modes:
  - First launch (no .pm-local): onboarding with example
  - Regular (has .pm-local): initiative status list
"""

import json
import glob
import os
import sys
from pathlib import Path
from typing import Optional
from datetime import date

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    Console = None


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
console = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_constants import (  # noqa: E402
    STEP_LABELS as PIPELINE_STEPS,
    PENDING_LABELS,
    enabled_total,
    find_current_step,
)
try:
    import hypotheses as _registry
except ImportError:
    _registry = None
try:
    import coverage as _coverage
except ImportError:
    _coverage = None


def _coverage_map(status_path: str) -> dict:
    """Coverage line + focus for the dashboard ({} if unavailable)."""
    if _coverage is None:
        return {}
    try:
        init_dir = Path(status_path).parent.parent
        phases = _coverage.compute_coverage(init_dir)
        focus = _coverage.focus_phase(phases)
        return {
            "line": _coverage.format_line(phases),
            "focus": focus["name"] if focus else None,
            "missing": (focus or {}).get("missing", []),
        }
    except Exception:
        return {}


def _count_evidence_issues(status_path: str) -> int:
    """Registry violations for the /next hint (0 if no registry)."""
    if _registry is None:
        return 0
    try:
        init_dir = Path(status_path).parent.parent
        errors, warnings = _registry.validate(_registry.load(str(init_dir)))
        return len(errors) + len(warnings)
    except Exception:
        return 0


def find_pm() -> Optional[str]:
    pm_file = REPO_ROOT / ".pm-local"
    if pm_file.exists():
        return pm_file.read_text().strip()
    return None


def load_initiatives(pm: str) -> list:
    initiatives = []
    pattern = str(REPO_ROOT / pm / "*" / "output" / "status.json")
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path) as f:
                status = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        name = status.get("initiative",
            os.path.basename(os.path.dirname(os.path.dirname(path))))

        steps = status.get("steps", {})
        config = status.get("pipeline_config", {})
        template_name = config.get("template", "full")
        pending = status.get("pending", {})

        done = sum(1 for s in steps.values()
                   if isinstance(s, dict) and s.get("status") == "done")

        total = enabled_total(config)

        current_cmd = None
        current_step = find_current_step(steps)

        if current_step is not None and current_step in PIPELINE_STEPS:
            current_cmd = PIPELINE_STEPS[current_step]

        # Legacy pending.* rendering — REMOVE IN 2.0 (dependencies[] is canon)
        pending_items = []
        today = date.today()
        for key, val in pending.items():
            if val is None:
                continue
            label = PENDING_LABELS.get(key, key)
            try:
                # value is either an ISO date or free text starting with one
                d = date.fromisoformat(str(val)[:10])
                days = (today - d).days
                pending_items.append({"label": label, "days": days})
            except (ValueError, TypeError):
                pending_items.append({"label": label, "days": 0})

        # dependencies[] (E8): external work with owner + deadline
        deps = []
        for dep in status.get("dependencies", []):
            if not isinstance(dep, dict) or dep.get("status") in ("done", "skipped"):
                continue
            overdue = 0
            try:
                overdue = (today - date.fromisoformat(dep.get("deadline", ""))).days
            except (ValueError, TypeError):
                pass
            deps.append({
                "id": dep.get("id", "?"),
                "owner": dep.get("owner", "?"),
                "jira": dep.get("jira"),
                "overdue": overdue,
                "blocks": dep.get("blocks", []),
            })

        initiatives.append({
            "name": name,
            "done": done,
            "total": total,
            "template": template_name,
            "current_step": current_step,
            "current_cmd": current_cmd,
            "pending": pending_items,
            "dependencies": deps,
            "evidence_issues": _count_evidence_issues(path),
            "coverage": _coverage_map(path),
        })

    return initiatives


def progress_bar(done: int, total: int, width: int = 20):
    if not HAS_RICH:
        return None
    if total == 0:
        return Text("?" * width, style="dim")
    filled = round(done / total * width)
    bar = Text()
    bar.append("\u2588" * filled, style="bright_blue")
    bar.append("\u2591" * (width - filled), style="bright_black")
    bar.append(f"  {done}/{total}", style="dim")
    return bar


def render_header():
    if not console:
        return
    title = Text()
    title.append("\u25c6 ", style="bright_blue bold")
    title.append("Product Discovery", style="bold white")
    subtitle = Text("PM Copilot", style="dim")

    header = Text.assemble(title, "\n", subtitle)
    console.print(Panel(header, box=box.ROUNDED, border_style="bright_blue",
                        padding=(1, 2)))


def render_onboarding():
    """First launch — show example and invite the user to start."""
    if not console:
        return
    console.print()

    # Example block
    example_title = Text("  Example:", style="bold white")
    console.print(example_title)
    console.print()
    console.print('  You say:', style="dim")
    console.print('  "Users add items to cart but never complete checkout on mobile"',
                  style="italic bright_white")
    console.print()
    console.print('  Product Discovery creates:', style="dim")
    console.print('    \u2192 Initiative [bold]mobile-checkout-drop[/bold]')
    console.print('    \u2192 5 problem hypotheses tied to the checkout funnel')
    console.print('    \u2192 Research plan: what data to collect, who to interview')
    console.print('    \u2192 Ready for deep CJM analysis with screenshots')
    console.print()

    # Separator
    console.print("  " + "\u2500" * 50, style="bright_black", highlight=False)
    console.print()

    # CTA
    console.print("  [bold]What product problem are you working on?[/bold]")
    console.print()
    console.print("  Or start with a job right away:", style="dim")
    console.print('    "read this deck"  ·  "I need an analyst brief"  ·  "break down problem X"',
                  style="dim italic")
    console.print()


def render_initiatives(initiatives: list):
    """Regular launch — show initiative status."""
    if not console:
        return
    if not initiatives:
        console.print("  No initiatives yet.", style="dim")
        console.print("  Describe your product problem or say [bold]create initiative <name>[/bold]")
        console.print()
        return

    for init in initiatives:
        console.print(Text(f"  {init['name']}", style="bold white"))

        cov = init.get('coverage') or {}
        if cov.get('line'):
            console.print(f"    {cov['line']}", style="cyan")
            if cov.get('focus'):
                missing = "; ".join(cov.get('missing', [])[:3])
                console.print(f"    focus \u2192 {cov['focus']}: missing {missing}", style="dim")
        elif init['current_cmd']:
            console.print(f"    \u2192 Step {init['current_step']}: {init['current_cmd']}", style="dim")

        for p in init['pending']:
            days_str = f" ({p['days']}d)" if p['days'] > 0 else ""
            style = "yellow" if p['days'] > 7 else "dim yellow" if p['days'] > 0 else "dim"
            console.print(f"    \u23f3 {p['label']}{days_str}", style=style)

        for d in init.get('dependencies', []):
            jira = f" {d['jira']}" if d.get('jira') else ""
            blocks = f", blocks {', '.join(d['blocks'])}" if d.get('blocks') else ""
            if d['overdue'] > 0:
                console.print(f"    \u23f0 {d['id']}{jira} ({d['owner']}) \u2014 OVERDUE {d['overdue']}d{blocks}", style="red")
            else:
                console.print(f"    \u23f3 {d['id']}{jira} ({d['owner']}){blocks}", style="dim yellow")

        stale = sum(1 for p in init['pending'] if p['days'] >= 7)
        overdue_deps = sum(1 for d in init.get('dependencies', []) if d['overdue'] > 0)
        if init.get('evidence_issues') or stale or overdue_deps:
            parts = []
            if init.get('evidence_issues'):
                parts.append(f"{init['evidence_issues']} evidence issue(s)")
            if stale:
                parts.append(f"{stale} stale pending")
            if overdue_deps:
                parts.append(f"{overdue_deps} overdue dependency(ies)")
            console.print(f"    ! {', '.join(parts)} \u2014 ask /next", style="red")

        console.print()

    console.print("  Type a command or say [bold]continue[/bold]", style="dim")
    console.print()


def render_plain():
    """Plain-text fallback when `rich` is not installed."""
    pm = find_pm()
    print()
    print("  Product Discovery — PM Copilot")
    print("  " + "-" * 38)
    print()

    if not pm:
        print('  Example:')
        print('    You say: "Users add items to cart but never complete checkout on mobile"')
        print('    Product Discovery creates: initiative + 5 problem hypotheses + research plan')
        print()
        print("  What product problem are you working on?")
        print()
        print('  Or start with a job right away:')
        print('    "read this deck"  ·  "I need an analyst brief"  ·  "break down problem X"')
        print()
        print("  (Tip: install `rich` for a nicer dashboard — pip install rich)")
        return

    initiatives = load_initiatives(pm)
    if not initiatives:
        print(f"  PM: {pm}")
        print("  No initiatives yet. Describe your product problem to start.")
        print()
        return

    for init in initiatives:
        print(f"  {init['name']}")
        cov = init.get('coverage') or {}
        if cov.get('line'):
            print(f"    {cov['line']}")
            if cov.get('focus'):
                missing = "; ".join(cov.get('missing', [])[:3])
                print(f"    focus -> {cov['focus']}: missing {missing}")
        elif init['current_cmd']:
            print(f"    -> Step {init['current_step']}: {init['current_cmd']}")
        for p in init['pending']:
            days_str = f" ({p['days']}d)" if p['days'] > 0 else ""
            print(f"    [pending] {p['label']}{days_str}")
        for d in init.get('dependencies', []):
            jira = f" {d['jira']}" if d.get('jira') else ""
            blocks = f", blocks {', '.join(d['blocks'])}" if d.get('blocks') else ""
            mark = f"OVERDUE {d['overdue']}d" if d['overdue'] > 0 else "waiting"
            print(f"    [dep] {d['id']}{jira} ({d['owner']}) — {mark}{blocks}")
        stale = sum(1 for p in init['pending'] if p['days'] >= 7)
        overdue_deps = sum(1 for d in init.get('dependencies', []) if d['overdue'] > 0)
        if init.get('evidence_issues') or stale or overdue_deps:
            parts = []
            if init.get('evidence_issues'):
                parts.append(f"{init['evidence_issues']} evidence issue(s)")
            if stale:
                parts.append(f"{stale} stale pending")
            if overdue_deps:
                parts.append(f"{overdue_deps} overdue dependency(ies)")
            print(f"    ! {', '.join(parts)} — ask /next")
        print()
    print("  (Tip: install `rich` for a nicer dashboard — pip install rich)")


def main():
    global console
    if not HAS_RICH:
        render_plain()
        return

    console = Console()
    pm = find_pm()
    render_header()

    if pm:
        initiatives = load_initiatives(pm)
        render_initiatives(initiatives)
    else:
        render_onboarding()


if __name__ == "__main__":
    main()
