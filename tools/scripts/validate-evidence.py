#!/usr/bin/env python3
"""
validate-evidence.py — evidence audit across all initiatives (E2, roadmap 0.8).

Runs on SessionStart (hook in .claude/settings.json): for every initiative
that has a hypothesis registry (output/hypotheses.json), validates it against
the evidence-typing rules and prints a compact report — evidence summary plus
any violations. Silent-ish by design: one line per healthy initiative, details
only for problems.

Always exits 0 — a broken registry must not break session start; the report
itself is the signal.

Usage:
  validate-evidence.py            # audit all initiatives of the PM (.pm-local)
  validate-evidence.py <dir>      # audit one initiative folder
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hypotheses as registry  # noqa: E402


def find_pm():
    pm_file = REPO_ROOT / ".pm-local"
    return pm_file.read_text(encoding="utf-8").strip() if pm_file.exists() else None


def audit(initiative_dir: Path) -> None:
    data = registry.load(str(initiative_dir))
    hyps = data.get("hypotheses", [])
    if not hyps:
        return
    errors, warnings = registry.validate(data)

    confirmed_real = sum(
        1 for h in hyps
        if h.get("status") in ("confirmed", "reframed")
        and h.get("evidence_type") == "REAL")
    open_count = sum(1 for h in hyps if h.get("status") in ("draft", "testing"))
    refuted = sum(1 for h in hyps if h.get("status") == "refuted")
    flagged = sum(1 for h in hyps if h.get("flags"))

    line = (f"  {initiative_dir.name}: {len(hyps)} hypotheses — "
            f"{confirmed_real} confirmed REAL, {open_count} open, "
            f"{refuted} refuted")
    if flagged:
        line += f", {flagged} flagged"
    status = "OK" if not errors and not warnings else "ISSUES"
    print(f"{line} [{status}]")
    for e in errors:
        print(f"    ERROR {e}")
    for w in warnings:
        print(f"    WARN  {w}")


def main() -> int:
    if len(sys.argv) > 1:
        audit(Path(sys.argv[1]))
        return 0

    pm = find_pm()
    if not pm:
        return 0
    reg_files = sorted((REPO_ROOT / pm).glob("*/output/hypotheses.json"))
    if not reg_files:
        return 0
    print("Evidence audit:")
    for reg_path in reg_files:
        audit(reg_path.parent.parent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
