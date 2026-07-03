---
name: technical-spec-document
description: Translates PRD requirements into an implementation blueprint agreed with the dev team — scope by component, behavior-level contracts, acceptance mapping, estimate structure. Use at dev-estimate time or when the user says "tech spec", "implementation spec", "спецификация", "технический документ". Complements system-design-doc (that one captures constraints; this one specifies what gets built).
---

# Technical Spec (implementation blueprint)

Boundary: **this skill = what will be built for THIS initiative**, agreed
with the dev team. What the system already looks like and what constrains
us is `system-design-doc`.

The spec's customer is the dev team; its source of truth is PRD §6–8
(which traces to confirmed hypotheses in the registry). Nothing enters the
spec without tracing back to a requirement — and no requirement leaves
without acceptance criteria.

## Structure

1. **Scope by component** — for each affected component (from
   system-design-doc): what changes, and what explicitly does NOT change
   (the out-of-scope list prevents estimate creep).
2. **Contracts at behavior level** — new/changed interfaces described as
   inputs → outputs → errors. Enough for the dev team to design against;
   not pretending to be their design.
3. **Acceptance mapping** — every user story from PRD §8 → which
   component(s) deliver it → how we verify (feeds `/tickets`
   Given/When/Then directly).
4. **Tracking requirements** — events the solution must emit so the AB
   test (step 14) and post-launch review can measure it. A solution that
   ships unmeasurable is a spec bug.
5. **Estimate structure** — S/M/L per component with the dev lead's
   confidence; unknowns from system-design-doc widen ranges explicitly.

## Output

`output/dev-estimate.md` (spec section) + PRD §9–10 updates. Feeds
`/tickets` — Epics/Stories are generated from the acceptance mapping, so
sloppy mapping here becomes sloppy tickets there.

## Anti-patterns

- Duplicating system-design-doc content — link to it instead.
- Code-level detail (schemas, class names) — that's the dev team's design.
- Specs for features whose hypotheses are not confirmed in the registry —
  check `hypotheses.py show <dir>` before writing a line.
