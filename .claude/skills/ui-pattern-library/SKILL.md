---
name: ui-pattern-library
description: Picks UI patterns that address the mechanism of a solution hypothesis — for wireframing in /sketch. Use when sketching a solution, choosing between interface approaches, or when the user says "какой паттерн использовать", "what component to use", "UI pattern", "how should this screen work", "нарисуй экраны".
---

# UI Patterns for Solution Sketches

Serves the `/sketch` job: turn a solution hypothesis into concrete screens.
The question is never "which component is prettiest" — it's **"which
pattern delivers the mechanism this hypothesis promises"**.

## Method

1. **Start from the hypothesis mechanism.** Read the solution hypothesis
   (`output/solution-hypotheses.md`, linked ids in the registry): the
   "Formula: if X then Y because Z" line names the mechanism. The pattern
   must implement Z — everything else is decoration.
2. **Pick a pattern per mechanism**, e.g.:
   - reduce effort at a step → inline editing, smart defaults, one-tap
     confirm, progressive disclosure
   - build trust → social proof blocks, transparent pricing breakdown,
     recognizable payment affordances
   - create/capture intent → save-for-later, wishlists, follow/subscribe,
     re-engagement entry points
   - explain something new → empty states that teach, contextual tooltips,
     first-run checklists (NOT tours nobody reads)
   - surface at the right moment → contextual banners/sheets anchored to
     the user's current task, not global modals
3. **Respect platform conventions** the segment already knows (CONTEXT.md:
   platform). A familiar mediocre pattern usually beats a novel one — the
   novelty tax is real and shows up in concept tests.
4. **Name the risk per screen** — what the concept test (step 8.5) should
   probe: discoverability? comprehension? trust?

## Output — into `output/solution-sketch.md`

Per screen: purpose (which hypothesis/mechanism) → chosen pattern + why →
elements list top-to-bottom → user flow in/out → open risk for testing.
Text wireframes are fine; Figma via MCP when connected.

## Anti-patterns

- Design-system lectures (tokens, atomic design, component APIs) — that's
  the design team's domain, not a PM sketch.
- Patterns chosen by taste with no link to the hypothesis mechanism.
- Novel interactions where a platform convention exists — unless novelty
  IS the hypothesis.
