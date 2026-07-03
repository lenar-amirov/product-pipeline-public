---
name: user-testing
description: Designs user tests in two modes — quick 15-minute concept test on wireframes (3-5 users) or a full usability study (methodology, participants, tasks, severity coding). Use for "concept test", "проверить концепт на пользователях", "usability test", "юзабилити-тест", "user testing", "test the prototype", "план UX-исследования", "sample size for user test".
---

# User Testing — concept mode / study mode

One skill, two depths. Pick by what's at stake:

| | **Concept test** (quick) | **Usability study** (full) |
|---|---|---|
| When | after `/sketch` — validate direction before hi-fi | before/after launch — measure task performance |
| Duration | 15 min × 3–5 users, days to run | 30–60 min × 5–8/segment, weeks |
| Answers | "do users get it, do they want it" | "can users complete it, where does it break" |
| Output | keep / change / rethink per screen | severity-ranked issue list |

Default to **concept mode**; escalate to a study only when the decision
needs task-level measurement.

## Concept mode (step 8.5)

1. **Scenario** — realistic context from CONTEXT.md + job-to-be-done from
   the solution hypothesis. Don't lead toward the "right" answer.
2. **Questions per screen** (3–5 max): first impression (5 sec — "what is
   this?"), comprehension ("how would you [key action]?"), value ("better
   than how you do it today?"), friction ("anything confusing/missing?").
   Open-ended only; never explain the UI.
3. **Success/fail criteria BEFORE the sessions**, tied to the hypothesis:
   e.g. 4/5 understand the purpose in 5 sec; 3/5 complete the primary task
   unaided. Fail triggers (2+ misunderstand the core concept) mean back to
   `/sketch`, not "note it and proceed".
4. **Protocol**: setup ("we test the design, not you"; think-aloud) →
   screens → wrap-up rating. Write plan + empty results sections to
   `research/concept-test-results.md`.

## Study mode

1. **Research questions ≠ tasks**: 3–5 questions the business needs
   answered, each mapped to scenario-based tasks (real trigger, no UI
   vocabulary in the task text).
2. **Participants**: from the CONTEXT.md segment; 5–8 per distinct segment;
   screener excludes proxies (people who "know about" vs "do").
3. **Measures**: completion, time-on-task, error types + think-aloud
   coding. Moderated when exploring, unmoderated for benchmarks.
4. **Severity classification** for findings: blocker (task impossible) /
   major (workaround found, with pain) / minor (friction) / cosmetic —
   prioritized against segment share affected.
5. Plan → `research/ux-research-brief.md`; create a dependency
   (`kind: ux_research`, owner, deadline) — studies stall exactly like
   analyst briefs.

## Output to the registry (both modes)

Findings are REAL evidence: `hypotheses.py set <id> --type REAL
--confidence <C> --add-source "research/<results-file>::task N, M of K
users"` — confirm, downgrade or refute the touched solution/problem
hypotheses; then `hypotheses.py render`. Frequency honesty: "M of K users",
one user is not "users". Log the verdict in decisions.md.
