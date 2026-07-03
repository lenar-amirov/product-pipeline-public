"""
pipeline_constants.py — single source of truth for pipeline structure (E3).

Every consumer (status.py, scan-initiatives.py, tools/web/app.py,
tools/web/static_export.py) imports from here. Before E3 each of them kept
its own diverged copy (0-19 vs 1-19, fallback totals 18 vs 19 vs 21).

Sub-steps 5.5 and 8.5 exist in status.json but never count toward totals.
"""

# (num, command, phase, label)
PIPELINE_STEPS = [
    (0, "setup-initiative", "Phase 1", "Setup"),
    (1, "analyze-cjm", "Phase 1", "CJM Analysis"),
    (2, "synthetic-research", "Phase 1", "Synthetic Research"),
    (3, "competitor-research", "Phase 1", "Competitor Research"),
    (4, "generate-research", "Phase 1", "Research Briefs"),
    (5, "create-survey-audience", "Phase 1", "Survey Audience"),
    (5.5, "customer-research-pause", "Phase 1", "Customer Research Pause"),
    (6, "validate-problems", "Phase 1", "Validate Problems"),
    (7, "solution-hypotheses", "Phase 1", "Solution Hypotheses"),
    (8, "sketch-solution", "Phase 1", "Sketch Solution"),
    (8.5, "user-test-concept", "Phase 1", "Concept Test"),
    (9, "review-design", "Phase 1", "Design Review"),
    (10, "create-presentation", "Phase 1", "Problem Research Report (Gate 1)"),
    (11, "create-design-brief", "Phase 2", "Design Brief"),
    (12, "estimate-with-dev", "Phase 2", "Dev Estimate"),
    (13, "finalize-prd", "Phase 2", "Finalize PRD"),
    (14, "design-ab-test", "Phase 2", "AB Test Design"),
    (15, "create-gate2-presentation", "Phase 2", "Solution Research Report (Gate 2)"),
    (16, "analyze-ab-test", "Phase 2", "AB Test Analysis"),
    (17, "plan-gtm", "Phase 3", "GTM Plan"),
    (18, "create-gtm-materials", "Phase 3", "GTM Materials"),
    (19, "support-task", "Phase 3", "Support Brief"),
]

SUB_STEPS = {5.5, 8.5}

# Main steps only — what totals and progress bars count
MAIN_STEPS = [s for s in PIPELINE_STEPS if s[0] not in SUB_STEPS]

STEP_LABELS = {num: label for num, _cmd, _phase, label in PIPELINE_STEPS}
STEP_COMMANDS = {num: cmd for num, cmd, _phase, _label in PIPELINE_STEPS}

MAX_STEP = 19
DEFAULT_TOTAL = len(MAIN_STEPS)  # 20


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


def enabled_total(pipeline_config: dict) -> int:
    """Number of enabled steps from pipeline_config, or the default total."""
    config_steps = (pipeline_config or {}).get("steps", {})
    if config_steps:
        return sum(1 for v in config_steps.values()
                   if isinstance(v, dict) and v.get("enabled"))
    return DEFAULT_TOTAL


def find_current_step(steps: dict):
    """Walk main steps from the end: first in_progress/paused wins, else the
    step after the last done one. None if `steps` is empty; 0 for a fresh
    initiative."""
    if not steps:
        return None
    for num, _cmd, _phase, _label in reversed(MAIN_STEPS):
        s = steps.get(str(num), {})
        if isinstance(s, dict) and s.get("status") in ("in_progress", "paused"):
            return num
        if isinstance(s, dict) and s.get("status") == "done":
            return min(num + 1, MAX_STEP)
    return 0
