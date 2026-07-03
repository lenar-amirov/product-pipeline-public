# Evidence Typing

Every piece of evidence in hypotheses, validation, and PRD must be typed by source.

## Types and confidence ranges

| Type | Confidence | Sources |
|------|-----------|---------|
| **REAL** | 0.6–1.0 | Analytics data, survey results, user interviews, A/B test results |
| **SYNTHETIC** | 0.2–0.4 | AI-generated interviews, synthetic research, persona simulations |
| **INFERRED** | 0.3–0.5 | Logical deductions from other evidence, competitive analogues |
| **AMBIGUOUS** | 0.1–0.3 | Contradictory signals, unclear data, unverified claims |

## Registry

Types and confidence live in `output/hypotheses.json` — the single source of
truth, managed via `tools/scripts/hypotheses.py` (`set` records history
automatically, `validate` enforces the ranges above and requires sources for
REAL). Narrative markdown must not contradict the registry.

## Rules

- When REAL contradicts SYNTHETIC — REAL wins. Document the delta.
- Frequency ranking: "N out of M sources mention this" (inspired by PMRead pattern)
- Confidence upgrades when validated: SYNTHETIC → REAL after user interviews confirm
- Never present SYNTHETIC evidence as fact — always mark explicitly
- In presentations: only REAL evidence in "proof" slides. SYNTHETIC goes in speaker notes as context.
