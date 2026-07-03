---
name: tracking-and-funnels
description: Designs what to track and how to read funnels — event schema derived from open hypotheses, funnel/cohort analysis for validation and briefs. Use for "воронка", "funnel analysis", "drop-off", "where are users dropping", "что трекать", "event schema", "tracking plan", "cohort analysis", "трекинг событий".
---

# Tracking & Funnels

One skill for both directions of the same loop: **what to instrument** (so
hypotheses become measurable) and **how to read the funnel** (so
measurements become verdicts). Serves `/brief` (steps 4–5), `/validate`
(step 6) and experiment-design (step 14/16).

## Design tracking FROM the hypotheses

For every testing/draft hypothesis in `output/hypotheses.json`, name the
event/metric that would confirm or refute it — that mapping IS the
acceptance test of the schema. An event no hypothesis needs is noise; a
hypothesis no event can test is a research gap → into the analytics brief.

Schema conventions:
- `object_action` naming (`checkout_started`, not `click_btn_3`), snake_case
- Properties over event proliferation: one `order_completed` with
  `payment_method` beats three payment events
- Every event: user id, timestamp, platform, session id; funnel events
  additionally carry the entry surface/source
- Define each metric once, in writing, with its window ("CTR" without a
  definition is how gate presentations die — see /challenge)

## Read the funnel

- **Sequential windows**: a funnel is ordered events within a window per
  user — state the window and whether re-entry counts; unstated windows
  make numbers incomparable across sources (→ `data_inconsistency`).
- **Segment before averaging**: an aggregate drop-off hides opposite
  behaviors; split by the CONTEXT.md segments and by entry surface first.
- **Cohorts for time effects**: compare users by start week when the
  product changes underneath them.
- Skeleton (adapt to the PM's warehouse; pseudo-SQL is fine in briefs):

```sql
SELECT step, COUNT(DISTINCT user_id) AS users,
       ROUND(100.0 * COUNT(DISTINCT user_id) /
             FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (ORDER BY step), 1) AS pct
FROM funnel_events           -- events pre-mapped to ordered steps
GROUP BY step ORDER BY step;
-- splitting by segment/platform? add PARTITION BY to the window fn,
-- or pct will be computed against the wrong base
```

## Quality checks before trusting numbers

Totals reconcile across sources (same metric, same definition, same
window)? Bot/internal traffic excluded? Event fired once per action
(dedup)? A funnel built on unverified events produces confident nonsense —
flag first, analyze second.

## Output to the registry

A drop-off finding is evidence: `hypotheses.py set <id> --type REAL
--confidence <C> --add-source "research/analytics-data.md::<funnel, step>"`.
A drop-off matching no hypothesis → candidate `hypotheses.py add` (ask the
PM). Contradicting sources → `--flag data_inconsistency`, never silent
averaging.
