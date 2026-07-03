---
name: experiment-design
description: Designs the validation experiment for a solution's riskiest assumption — AB test parameters (MDE, sample size, duration, guardrails, decision criteria) or a cheaper pre-test. The engine of /design-ab-test (step 14). Use for "спланируй AB-тест", "design the experiment", "sample size", "MDE", "как проверим решение", "критерии успеха теста".
---

# Experiment Design — `/design-ab-test` engine

Input: the top solution from `solution-scoring` and its **riskiest
assumption** (from the assumption map). The experiment tests THAT, not
"the feature in general".

## 0. Is an AB test even the right instrument?

Cheaper first: a concept test (user-testing skill) kills desirability
risks in days; a fake-door sizes demand; an ops pilot tests feasibility.
AB test is for causal measurement of the metric effect at scale — expensive
and slow; don't default to it. State the choice and why.

## 1. AB test parameters (with the analyst)

- **Hypothesis** in the falsifiable form: "If [change] for [segment], then
  [primary metric] moves from [baseline] by ≥[MDE], because [mechanism]."
  Baseline comes from the registry/CONTEXT.md, never from memory.
- **Primary metric** — exactly one; the same definition the dashboard uses
  (metric-definition mismatches are how gates die — see /challenge).
- **MDE** — the smallest effect worth shipping (business floor), not the
  effect you hope for.
- **Sample size & duration** — from baseline, MDE, power 0.8, α 0.05;
  respect weekly seasonality (full weeks only). If the segment is too small
  for the MDE — say the test is infeasible and go back to instrument choice.
- **Guardrails** — metrics that must NOT degrade (engagement, latency,
  support load) with explicit thresholds.
- **Decision criteria BEFORE launch**: ship / iterate / kill thresholds
  written down — no post-hoc goalpost moving.

## 2. Tracking readiness

Verify the events the test needs actually exist (tech-spec §tracking).
A test on unmeasured behavior is a dependency, not a test — create it in
status.json with the analyst as owner.

## 3. Output

`output/ab-test-design.md`: hypothesis, parameters table, guardrails,
decision criteria, experiment IDs placeholder. Create the AB-test
dependency (owner: analyst, deadline: launch + duration). Step 16
(`/analyze-ab-test`) reads this file as its contract — vague criteria here
become unfalsifiable results there.
