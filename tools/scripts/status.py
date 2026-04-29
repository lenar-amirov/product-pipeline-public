#!/usr/bin/env python3
"""
status.py — branded dashboard for AI Diamond pipeline.

Usage:
    python3 tools/scripts/status.py
    python3 tools/scripts/status.py --initiative checkout-redesign
"""

import json
import glob
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
except ImportError:
    print("rich not installed. Run: pip install rich")
    sys.exit(1)


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
    16: "Support Brief",
    17: "Announce AB Test",
    18: "Announce Release",
}

PENDING_LABELS = {
    "analytics_brief": "Send brief to analyst",
    "survey_brief": "Send survey brief",
    "audience_brief": "Send audience brief",
    "analytics_results": "Waiting for analytics results",
    "survey_results": "Waiting for survey results",
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


def load_initiatives(pm: str) -> list[dict]:
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
        enabled_steps = config.get("enabled_steps", {})
        pending = status.get("pending", {})

        # Count completed
        done = sum(1 for s in steps.values()
                   if isinstance(s, dict) and s.get("status") == "done")

        # Count total enabled steps
        if enabled_steps:
            total = sum(1 for v in enabled_steps.values() if v)
        else:
            total = 18

        # Find current step
        current_step = None
        current_cmd = None
        for num in range(18, -1, -1):
            s = steps.get(str(num), {})
            if isinstance(s, dict) and s.get("status") in ("in_progress", "paused"):
                current_step = num
                break
            elif isinstance(s, dict) and s.get("status") == "done":
                # Next step after this one
                current_step = num + 1
                break

        if current_step is not None and current_step in PIPELINE_STEPS:
            current_cmd = PIPELINE_STEPS[current_step]

        # Pending items
        pending_items = []
        from datetime import date
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
            "current_step": current_step,
            "current_cmd": current_cmd,
            "pending": pending_items,
            "path": os.path.dirname(os.path.dirname(path)),
        })

    return initiatives


def progress_bar(done: int, total: int, width: int = 20) -> Text:
    if total == 0:
        return Text("?" * width, style="dim")
    filled = round(done / total * width)
    bar = Text()
    bar.append("█" * filled, style="bright_blue")
    bar.append("░" * (width - filled), style="bright_black")
    bar.append(f"  {done}/{total}", style="dim")
    return bar


def render_header():
    title = Text()
    title.append("◆ ", style="bright_blue bold")
    title.append("AI Diamond", style="bold white")
    subtitle = Text("Product Discovery Copilot", style="dim")

    header = Text.assemble(title, "\n", subtitle)
    console.print(Panel(header, box=box.ROUNDED, border_style="bright_blue",
                        padding=(1, 2)))


def render_initiatives(initiatives: list[dict]):
    if not initiatives:
        console.print("  No initiatives yet. Say [bold]create initiative <name>[/bold] to start.\n")
        return

    for init in initiatives:
        # Initiative name + progress bar
        name_text = Text(f"  {init['name']}", style="bold white")
        console.print(name_text, end="  ")
        console.print(progress_bar(init['done'], init['total']))

        # Current step
        if init['current_cmd']:
            console.print(f"    → Step {init['current_step']}: {init['current_cmd']}",
                         style="dim")

        # Pending items
        for p in init['pending']:
            days_str = f" ({p['days']}d)" if p['days'] > 0 else ""
            style = "yellow" if p['days'] > 7 else "dim yellow" if p['days'] > 0 else "dim"
            console.print(f"    ⏳ {p['label']}{days_str}", style=style)

        console.print()


def render_footer():
    console.print("  Type a command or say [bold]continue[/bold]\n", style="dim")


def main():
    pm = find_pm()

    render_header()

    if pm:
        initiatives = load_initiatives(pm)
        render_initiatives(initiatives)
    else:
        console.print("  First time? Say [bold]create initiative <name>[/bold] to start.\n")

    render_footer()


if __name__ == "__main__":
    main()
