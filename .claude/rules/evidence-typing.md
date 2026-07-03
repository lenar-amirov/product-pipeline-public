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

## Operational rules (enforced by validate-evidence.py on SessionStart)

- **Contradictory sources** for the same metric → set the flag immediately:
  `hypotheses.py set <id> --flag data_inconsistency --note "source A says X, source B says Y"`.
  While flagged, confidence above 0.6 is a violation — downgrade or reconcile
  with the analyst before any gate. Clear with `--unflag data_inconsistency`
  once reconciled (history records both).
- **Upgrades and downgrades** go only through `hypotheses.py set --type ...
  --confidence ... --add-source ...` — never edit narrative markdown alone;
  the registry history must show every transition.
- Confidence outside the type's range is a violation the audit reports every
  session until fixed — retype the evidence or fix the number.

## Who writes to the registry

Any skill that produces a VERDICT, FINDING or PRIORITY about the product or
its users must record it in `output/hypotheses.json` — not only in prose:
- new insight → `hypotheses.py add <id> --title ... --type ... --confidence ...`
- evidence for/against an existing hypothesis → `hypotheses.py set <id>
  --status ... --type ... --confidence ... --add-source "file::where"`
- solution decided → `hypotheses.py set <id> --link-solution S<N>`
A finding that lives only in a markdown file is invisible to the coverage
map, the gates, and `/next`.
