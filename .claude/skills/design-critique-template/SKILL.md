---
name: design-critique-template
description: Structured critique of a design against the hypothesis it was drawn for, plus heuristic evaluation — for step 9 and any mockup review. Use for "critique the design", "review mockup", "ревью макета", "что не так с UX", "heuristic evaluation", "оцени дизайн".
---

# Design Critique (hypothesis-first)

Critique for the `/sketch` → design loop (step 9). The order matters: a
beautiful screen that doesn't implement the hypothesis mechanism fails the
review regardless of heuristics.

## 1. Hypothesis fit — the first and decisive pass

Load the solution hypotheses this design serves (registry `solutions` links
+ `output/solution-hypotheses.md`):
- Does each screen implement the **mechanism** from the hypothesis formula
  ("if X then Y because Z" — is Z actually on the screen)?
- Did anything essential from `output/solution-sketch.md` get lost or
  mutated on the way to the mockup? Name the deltas.
- Does the design add scope no hypothesis asked for? (scope creep enters
  through mockups more often than through PRDs)

## 2. Heuristic pass (classic, kept short)

- **Visibility & hierarchy**: is the primary action of each screen
  unmistakable in 5 seconds?
- **User control**: reversibility, escape routes, no dead ends
- **Consistency**: platform conventions and the product's own patterns
  (see ui-pattern-library — novelty only where novelty IS the hypothesis)
- **Error prevention & recovery**: empty states, loading, failure paths —
  the states mockups always forget
- **Recognition over recall**: labels over icons-only, context over memory

## 3. Feedback format

Per issue: screen → what breaks (hypothesis-fit or heuristic, name which)
→ severity (blocker / major / minor / polish) → concrete suggestion.
Blockers first. Praise what works — reviewers who only list defects train
designers to hide work.

## 4. Output

Update `output/solution-sketch.md` (## Changelog section) with accepted
changes; unresolved disagreements go to decisions.md as open questions.
If the critique overturns a solution assumption — that's registry news:
flag it to the PM (`hypotheses.py set <id> --note ...`), don't bury it in
design comments.

## Anti-patterns

- Critiquing taste ("I'd make it blue") instead of hypothesis fit and
  heuristics — unfalsifiable feedback teaches nothing.
- A defect list with no severity — the designer can't sequence fixes.
- Reviewing the mockup without opening the solution hypothesis — you'll
  approve a beautiful screen that tests nothing.
