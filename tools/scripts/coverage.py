#!/usr/bin/env python3
"""
coverage.py — evidence coverage map (E11, roadmap 1.0).

Phases are a DIAGNOSTIC MAP, not a track: each phase has exit criteria
computed from actual state (hypothesis registry, CONTEXT.md, artifacts,
step statuses) — never from "which step number are we on". "Step 4/20"
is dead; "Evidence 2/3, missing: no validation issues" replaces it.

Usage:
  coverage.py <initiative_dir>       # print the map
As a module:
  compute_coverage(init_dir) -> list of phase dicts
  format_line(phases) -> compact one-line summary
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hypotheses as registry  # noqa: E402

CTX_FIELDS = {
    "metric": r"Metric we're improving|Метрика, которую улучшаем",
    "baseline": r"Current baseline|Текущий baseline",
    "target": r"Target result|Целевой результат",
    "kill criteria": r"Kill criteria|Kill-критерии",
}


def _ctx_filled(text: str, pattern: str) -> bool:
    m = re.search(r"\*\*(?:" + pattern + r")\*\*:\s*(.+?)(?=\n\*\*|\n#|\n\n|\Z)",
                  text, re.DOTALL)
    if not m:
        return False
    val = " ".join(m.group(1).split())
    return bool(val) and not val.startswith("[") and "to be validated" not in val


def _step_done(steps: dict, num) -> bool:
    s = steps.get(str(num), {})
    return isinstance(s, dict) and s.get("status") == "done"


def compute_coverage(init_dir) -> list:
    init_dir = Path(init_dir)

    ctx_text = ""
    ctx_path = init_dir / "CONTEXT.md"
    if ctx_path.exists():
        ctx_text = ctx_path.read_text(encoding="utf-8")

    steps = {}
    status_path = init_dir / "output" / "status.json"
    if status_path.exists():
        try:
            steps = json.loads(status_path.read_text(encoding="utf-8")).get("steps", {})
        except (json.JSONDecodeError, OSError):
            pass

    reg = registry.load(str(init_dir))
    hyps = reg.get("hypotheses", [])
    errors, warnings = registry.validate(reg) if hyps else ([], [])
    confirmed_real = [
        h for h in hyps
        if h.get("status") in ("confirmed", "reframed")
        and h.get("evidence_type") == "REAL"]
    has_solutions = any(h.get("solutions") for h in hyps)

    def artifact(rel, min_bytes=500):
        p = init_dir / rel
        return p.is_file() and p.stat().st_size >= min_bytes

    phases = []

    def phase(name, checks):
        done = [label for label, ok in checks if ok]
        missing = [label for label, ok in checks if not ok]
        phases.append({"name": name, "done": len(done),
                       "total": len(checks), "missing": missing})

    phase("Frame", [
        (label, _ctx_filled(ctx_text, pat)) for label, pat in CTX_FIELDS.items()
    ])
    phase("Evidence", [
        ("hypotheses exist", bool(hyps)),
        ("≥2 confirmed REAL", len(confirmed_real) >= 2),
        ("no validation issues", bool(hyps) and not errors and not warnings),
    ])
    phase("Solution", [
        ("solutions linked to hypotheses", has_solutions),
        ("solution-hypotheses.md substantial", artifact("output/solution-hypotheses.md")),
    ])
    phase("Bet", [
        ("Gate 1 presented (step 10)", _step_done(steps, 10)),
    ])
    phase("Build", [
        ("dev estimate (step 12)", _step_done(steps, 12)),
        ("PRD finalized (step 13)", _step_done(steps, 13)),
    ])
    phase("Launch", [
        ("Gate 2 presented (step 15)", _step_done(steps, 15)),
        ("experiment decided (step 16)", _step_done(steps, 16)),
        ("GTM planned (step 17)", _step_done(steps, 17)),
    ])
    phase("Learn", [
        ("post-launch review recorded", artifact("output/post-launch-review.md", 200)),
    ])
    return phases


def format_line(phases: list) -> str:
    parts = []
    for p in phases:
        if p["done"] == p["total"]:
            mark = "✓"
        elif p["done"] == 0:
            mark = "·"
        else:
            mark = "…"
        parts.append(f"{p['name']} {p['done']}/{p['total']}{mark if mark == '✓' else ''}")
    return " · ".join(parts)


def focus_phase(phases: list):
    for p in phases:
        if p["done"] < p["total"]:
            return p
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    phases = compute_coverage(sys.argv[1])
    print(format_line(phases))
    focus = focus_phase(phases)
    if focus:
        print(f"focus → {focus['name']}: missing " + "; ".join(focus["missing"]))
    else:
        print("all phases complete 🎉")
    return 0


if __name__ == "__main__":
    sys.exit(main())
