---
name: challenge
description: Adversarial gate rehearsal — a hostile stakeholder attacks the presentation against the hypothesis registry before the real gate does. Use when the PM says "завтра защита", "порепетируем гейт", "challenge my deck", "attack this presentation", "прогони как злой стейкхолдер", or before any Gate 1 / Gate 2 review.
---

# Challenge — `/challenge [gate1|gate2|<file>]`

The cheapest place to lose a gate is in rehearsal. Attack the PM's deck the
way the real audience will — armed with the registry, which knows exactly
where the evidence is thin.

## 0. Preconditions first

Run `python3 tools/scripts/validate-evidence.py --gate <dir>`. If GATE
BLOCKED — stop: report the blockers and the fastest way to clear each one.
Rehearsing a deck built on unreconciled numbers wastes the PM's time.

## 1. Load the ammunition

- The deck: `output/presentation.md` (Gate 1) or `output/gate2-presentation.md`
- The registry: `hypotheses.py show <dir>` — statuses, confidences, flags,
  sources per hypothesis
- `CONTEXT.md` — the promised metric/target
- Last decisions.md entries — anything promised earlier and not delivered

## 2. Attack in three personas (in order)

**CFO / sponsor** — attacks the money and the sizing:
- Where does the effect estimate come from? Which registry source backs
  each number on the sizing slide?
- What's the cost of being wrong? Kill criteria defined?
- "Why this and not the other initiative competing for the same team?"

**VP Product** — attacks the problem-solution link:
- Which slide claims rest on SYNTHETIC/INFERRED evidence presented as fact?
  (cross-check every proof slide against the registry — this is the
  highest-yield attack)
- Refuted or flagged hypotheses: does the deck quietly rely on any?
- Segment sizes: do funnel numbers on different slides agree?

**Skeptic engineer / analyst** — attacks the data:
- Metric definitions: same metric, same definition on every slide?
- data_inconsistency flags: "these two numbers contradict — which is true?"
- Baseline windows and seasonality; sample sizes for any test claims.

## 3. Report

For each hit: **slide/claim → the attack question → severity (fatal /
painful / cosmetic) → how to fix before the gate** (patch the slide, move
to speaker notes, reconcile the number, downgrade the claim). Fatal =
presentation should not go out; list fatals first. End with the 3 questions
most likely to actually be asked, and suggested answers backed by registry
sources.
