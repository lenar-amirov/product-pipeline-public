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


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PIPELINE_STEPS = {
    0: "Setup",
    1: "CJM Analysis",
    2: "Synthetic Research",
    3: "Competitor Research",
    4: "Research Briefs",
    5: "Survey Audience",
    6: "Validate Problems",
    7: "Solution Hypotheses",
    8: "Sketch Solution",
    9: "Design Review",
    10: "Problem Research Report",
    11: "Design Brief",
    12: "Dev Estimate",
    13: "Finalize PRD",
    14: "AB Test Design",
    15: "Solution Research Report",
    16: "AB Test Analysis",
    17: "GTM Plan",
    18: "GTM Materials",
    19: "Support Brief",
}

PENDING_LABELS = {
    "analytics_brief": "Send brief to analyst",
    "survey_brief": "Send survey brief",
    "audience_brief": "Send audience brief",
    "analytics_results": "Waiting for analytics results",
    "survey_results": "Waiting for survey results",
    "ab_test_analysis": "Waiting for AB test data",
    "gtm_materials_review": "GTM materials awaiting PM review",
    "design_brief": "Send brief to designer",
    "support_brief": "Send brief to support",
    "gate1_challenge": "Present Problem Research Report",
    "gate2_challenge": "Present Solution Research Report",
}

console = Console()


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
        config_steps = config.get("steps", {})
        template_name = config.get("template", "full")
        pending = status.get("pending", {})

        done = sum(1 for s in steps.values()
                   if isinstance(s, dict) and s.get("status") == "done")

        if config_steps:
            total = sum(1 for v in config_steps.values()
                        if isinstance(v, dict) and v.get("enabled"))
        else:
            total = 18

        current_step = None
        current_cmd = None
        for num in range(18, -1, -1):
            s = steps.get(str(num), {})
            if isinstance(s, dict) and s.get("status") in ("in_progress", "paused"):
                current_step = num
                break
            elif isinstance(s, dict) and s.get("status") == "done":
                current_step = num + 1
                break

        # Fresh initiative — no step started yet, point to 0
        if current_step is None and steps:
            current_step = 0

        if current_step is not None and current_step in PIPELINE_STEPS:
            current_cmd = PIPELINE_STEPS[current_step]

        pending_items = []
        today = date.today()
        for key, val in pending.items():
            if val is None:
                continue
            label = PENDING_LABELS.get(key, key)
            try:
                d = date.fromisoformat(val)
                days = (today - d).days
                pending_items.append({"label": label, "days": days})
            except (ValueError, TypeError):
                pending_items.append({"label": label, "days": 0})

        initiatives.append({
            "name": name,
            "done": done,
            "total": total,
            "template": template_name,
            "current_step": current_step,
            "current_cmd": current_cmd,
            "pending": pending_items,
        })

    return initiatives


def progress_bar(done: int, total: int, width: int = 20) -> Text:
    if total == 0:
        return Text("?" * width, style="dim")
    filled = round(done / total * width)
    bar = Text()
    bar.append("\u2588" * filled, style="bright_blue")
    bar.append("\u2591" * (width - filled), style="bright_black")
    bar.append(f"  {done}/{total}", style="dim")
    return bar


def render_header():
    title = Text()
    title.append("\u25c6 ", style="bright_blue bold")
    title.append("Product Discovery", style="bold white")
    subtitle = Text("PM Copilot", style="dim")

    header = Text.assemble(title, "\n", subtitle)
    console.print(Panel(header, box=box.ROUNDED, border_style="bright_blue",
                        padding=(1, 2)))


def render_onboarding():
    """First launch — show example and invite the user to start."""
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


def render_initiatives(initiatives: list):
    """Regular launch — show initiative status."""
    if not initiatives:
        console.print("  No initiatives yet.", style="dim")
        console.print("  Describe your product problem or say [bold]create initiative <name>[/bold]")
        console.print()
        return

    for init in initiatives:
        name_text = Text(f"  {init['name']}", style="bold white")
        console.print(name_text, end="  ")
        console.print(progress_bar(init['done'], init['total']))

        template_label = init.get('template', 'full')
        if init['current_cmd']:
            console.print(f"    \u2192 Step {init['current_step']}: {init['current_cmd']}  ({template_label} template)",
                         style="dim")
        else:
            console.print(f"    ({template_label} template)", style="dim")

        for p in init['pending']:
            days_str = f" ({p['days']}d)" if p['days'] > 0 else ""
            style = "yellow" if p['days'] > 7 else "dim yellow" if p['days'] > 0 else "dim"
            console.print(f"    \u23f3 {p['label']}{days_str}", style=style)

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
        print("  (Tip: install `rich` for a nicer dashboard — pip install rich)")
        return

    initiatives = load_initiatives(pm)
    if not initiatives:
        print(f"  PM: {pm}")
        print("  No initiatives yet. Describe your product problem to start.")
        print()
        return

    for init in initiatives:
        bar_filled = round(init['done'] / max(init['total'], 1) * 20) if init['total'] else 0
        bar = "#" * bar_filled + "." * (20 - bar_filled)
        print(f"  {init['name']}  [{bar}]  {init['done']}/{init['total']}  ({init.get('template', 'full')} template)")
        if init['current_cmd']:
            print(f"    -> Step {init['current_step']}: {init['current_cmd']}")
        for p in init['pending']:
            days_str = f" ({p['days']}d)" if p['days'] > 0 else ""
            print(f"    [pending] {p['label']}{days_str}")
        print()
    print("  (Tip: install `rich` for a nicer dashboard — pip install rich)")


def main():
    if not HAS_RICH:
        render_plain()
        return

    pm = find_pm()
    render_header()

    if pm:
        initiatives = load_initiatives(pm)
        render_initiatives(initiatives)
    else:
        render_onboarding()


if __name__ == "__main__":
    main()
