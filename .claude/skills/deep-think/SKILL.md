---
name: deep-think
description: Facilitated partner-led thinking session for problems that are NOT initiatives yet — strategy questions, org decisions, "should we enter X" — where there is no metric gap to pipeline. The PM leads, Claude structures and executes. Use for "давай подумаем стратегически", "помоги продумать сложный вопрос", "стоит ли нам…", "как подойти к реорганизации", "think this through with me", "у меня нет метрики, но есть проблема". When the problem IS a metric gap — that's /hypotheses, not this.
---

# Deep Think — `/deep-think`

A facilitated thinking session for the questions the pipeline can't hold:
no metric, no funnel, often no product surface — strategy bets, org
design, build-vs-buy, "is this worth an initiative at all". The PM is the
partner (owns direction, makes calls); Claude is the associate (structures,
drafts, stress-tests). One session, one page of output.

## How to run it

1. **Frame together** — restate the question until the PM confirms it's THE
   question; name the decision it feeds and who makes it. (For briefs handed
   down by a stakeholder, `ambiguity-resolver` does this framing.)
2. **Structure** — build the tree with `problem-structuring` (MECE applies
   to strategy questions too; the root is the decision, not a metric).
   Present the structure, let the PM cut or reweight branches — their
   context beats symmetric completeness.
3. **Work the priority branches** — for each surviving branch: what we know
   (typed honestly — most of it will be INFERRED/AMBIGUOUS here, say so),
   what would change the answer, cheapest way to find out.
4. **Synthesize answer-first** — pyramid: recommendation → 2-3 supporting
   arguments → evidence and open risks. Prose per writing-style.md.
5. **Land it** — one page to whatever file the PM names (or in-chat).
   Then the bridge, always offered, never forced:
   - the question turned out to be a metric gap → "превратить в инициативу?"
     (Frame + `/hypotheses` — the tree's branches seed the hypotheses);
   - it stays strategic → offer to bank durable conclusions in
     `knowledge/facts.json` so future initiatives inherit them.

## Boundaries

- PM decides at every fork; Claude proposes, never railroads.
- No fake rigor: strategy sessions run on INFERRED evidence — type it,
  don't dress it as analysis.
- If halfway in it's clearly an initiative (metric found, segment named) —
  say so and switch to the pipeline instead of finishing the ceremony.
