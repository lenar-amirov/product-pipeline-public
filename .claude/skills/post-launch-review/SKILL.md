---
name: post-launch-review
description: Closes the loop after launch — compares actual metric movement against the target set in Frame, issues production verdicts to hypotheses, and banks reusable facts into the PM's knowledge base. Use when the PM says "post-launch review", "прошло N месяцев после запуска", "метрика сдвинулась?", "подведём итоги инициативы", or when a post_launch_review dependency comes due.
---

# Post-Launch Review — `/post-launch-review`

Discovery without this step never learns: hypotheses get "confirmed" by
analytics, solutions ship, and nobody checks whether the metric actually
moved. This job is the difference between a pipeline and a feedback system.

## When it fires

- The `post_launch_review` dependency (created at ship decision, deadline
  launch + 90 days) comes due — the dashboard will show it.
- Or the PM asks directly.

## 1. Fact vs promise

- Target from `CONTEXT.md` (Frame): metric, baseline → target.
- Actual: ask the PM for current numbers or `/ingest` the fresh export.
- Verdict: **hit / partial / miss** — with the honest delta, not adjectives.

## 2. Production verdicts for hypotheses

For every hypothesis that drove shipped work:
`hypotheses.py set <id> --confidence 0.95 --note "confirmed in production:
<actual effect>"` — or downgrade/refute if production disagreed with the
discovery signal. REAL production data beats everything (evidence-typing).

## 3. Bank the knowledge — `knowledge/facts.json`

The PM-level knowledge base lives at the repo root in `knowledge/`
(personal, gitignored automatically). Append facts a FUTURE initiative
would want on day one:

```json
{
  "fact": "connected online payment multiplies checkout CR severalfold",
  "metric_effect": "+N% CR",
  "initiative": "<slug>",
  "source": "post-launch review YYYY-MM-DD",
  "date": "YYYY-MM-DD",
  "tags": ["checkout", "payments"]
}
```

Format: `{"version": 1, "facts": [ ... ]}`. Create the file if missing.
Facts must be product truths ("X drives Y"), not initiative trivia.

## 4. Calibration

Count from registry history across initiatives: how often did INFERRED
hypotheses survive REAL validation? Report the ratio — it calibrates how
much to trust the next INFERRED batch.

## 5. Record and close

`output/post-launch-review.md`: promise vs fact, verdicts, banked facts,
calibration note, and the one-paragraph retrospective (what discovery step
earned its keep, what was ceremony). Update decisions.md. Set the
`post_launch_review` dependency in status.json to `status: "done"` — this
completes the Learn phase on the coverage map.
