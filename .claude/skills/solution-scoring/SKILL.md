---
name: solution-scoring
description: Assumption mapping, ICE/SIF scoring and business viability check for solution hypotheses — the scoring engine of /solutions (step 7). Use for "какое решение выбрать", "ICE scoring", "assumption map", "prioritize solutions", "оцени решения", "риски этого решения".
---

# Solution Scoring — assumption map + ICE + viability

The scoring engine of `/solutions`: turns "we could do A, B or C" into a
ranked, risk-aware bet. Input: ✅/🎯 problems from the registry
(`hypotheses.py show <dir>`), never from prose.

## 1. Assumption map (per solution)

List what must be TRUE for the solution to work; classify each:

| Assumption | Type | Risk | Cheapest validation |
|---|---|---|---|
| users will notice the entry point | desirability | high | concept test (step 8.5) |
| sellers can fulfil in 48h | feasibility | med | ops interview |
| unit economics survive the discount | viability | high | spreadsheet + finance review |

Rule: the **riskiest assumption gets validated first and cheapest** —
that's what `experiment-design` takes as input. A solution whose riskiest
assumption is untestable is a faith project; say so.

## 2. Scoring — ICE by default, SIF if the PM's profile says so

- **Impact**: expected movement of the initiative metric — anchor in
  registry numbers (segment sizes, measured effects), not vibes.
- **Confidence** — numeric, staged by validation depth (REAL-backed
  problems justify confidence in the PROBLEM, not the solution):
  0.1–0.3 untested idea or external analogy · 0.4–0.6 after a concept
  test or a competitive analogue with the same mechanism on a comparable
  audience · 0.7+ only after an experiment on OUR users. A number outside
  its stage is the same violation as evidence-typing ranges.
- **Ease**: S/M/L from the dev lead when available, gut S/M/L otherwise
  (mark INFERRED).

Comparative table, top-1 recommendation with one-paragraph reasoning.
Honesty rule: don't inflate Confidence without evidence — the anti-generic
self-check applies.

## 3. Business viability (quick pass, before design)

Unit economics sketch · cannibalization risk · dependencies (teams/systems
→ candidates for status.json `dependencies[]`) · compliance flags · effort
S/M/L. Verdict per solution:
- **RED** — any single disqualifier: unit economics negative at target
  scale, hard compliance blocker, or effort L with confidence ≤0.3.
  One red parks the solution regardless of its ICE score (a great score
  on a non-viable solution is how teams burn quarters).
- **YELLOW** — proceed with a NAMED risk and an owner for it.
- **GREEN** — no known disqualifiers.

## 4. Output

`output/solution-hypotheses.md` per output-formats.md (S-ids, Formula,
win criteria) + link every survivor to its problem:
`hypotheses.py set <problem-id> --link-solution S<N>` — the OST and the
Solution phase of the coverage map are built from these links. Parked
solutions stay in the file with their red reason — they will be asked
about at the gate.
