---
name: problem-structuring
description: MECE issue trees, pyramid principle and 80/20 prioritization for breaking a product problem into testable hypotheses — the structuring engine behind /hypotheses and /validate. Use for "разложи проблему", "issue tree", "MECE", "почему падает метрика", "structure this problem", "root cause".
---

# Problem Structuring (MECE for the pipeline)

The structuring engine of `/hypotheses` (step 1) and the synthesis logic of
`/validate` (step 6). Extracted from the full consulting framework — for a
partner-led, deliverable-heavy consulting engagement use
`consulting-problem-solving` instead.

## MECE issue tree

1. **Root = the metric gap**, phrased as a question with a number:
   "Why do only X% of [segment] reach [outcome]?" — from CONTEXT.md.
2. **First split — choose ONE dimension** and stick to it: funnel stages,
   user segments, or jobs-to-be-done. Mixing dimensions is the #1 MECE
   violation.
3. **Branches must be mutually exclusive, collectively exhaustive.** Test:
   every lost user lands in exactly one branch. If a case fits two branches
   — re-split. If no branch fits — add "other/unknown" and size it.
4. **Leaves become hypotheses** (`hypotheses.py add`): each leaf = a
   falsifiable claim about WHY users are lost there, with a segment size
   estimate. 5–15 hypotheses is the healthy range.
5. **Name the blind spots explicitly** — branches you cannot size with
   current data. These become research questions for `/brief`.

## Pyramid principle (for validated findings)

Answer first, then grouped support, then evidence: conclusion → 2–3 insight
groups → data per group with sources from the registry. Used in
`/validate` outputs and gate presentations — never a data walk-through that
ends with "so, in conclusion".

## 80/20 prioritization

Size every branch before drilling: 80% of the metric gap usually sits in
2–3 leaves. Depth-first into the biggest branch beats breadth-first
completeness. The registry's segment-size fields carry the sizing;
priorities follow SIF (Severity × Impact × Frequency) per
output-formats.md.

## Anti-patterns

- A "tree" that is really a list (no exclusivity test performed)
- Solution leaves in a problem tree ("нет кнопки X" is a solution in
  disguise — rephrase as the user problem)
- Drilling into a branch nobody sized
