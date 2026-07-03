---
name: ingest
description: First-class intake of external data the PM was given — a deck (PDF/PPTX), analytics export (xlsx/csv), Confluence page, or pasted numbers. Extracts key metrics with exact locations, maps them onto open hypotheses in the registry, proposes upgrades/refutations. Use when the PM says "мне принесли дек", "вот данные/выгрузка", "прочитай этот PDF", "ingest this", "here's a deck from the analyst".
---

# Ingest — `/ingest <file | Confluence pageID | pasted data>`

In real corporate work the most valuable data arrives through the side door
— someone else's deck, an ad-hoc export, a wiki page. This job turns such an
artifact into typed evidence in the registry instead of a manual retyping
exercise.

## 1. Acquire

- **PDF** (deck, report): render pages to images —
  `python3 tools/scripts/render-pdf.py <file.pdf> <scratch_dir> [first] [last]`
  — then Read the images (batch 5-10 pages per pass).
- **PPTX**: convert to PDF first if possible (`soffice --convert-to pdf`), or
  ask the PM for a PDF export.
- **xlsx/csv**: read directly (xlsx skill if available).
- **Confluence page**: fetch via MCP (`confluence_get_page` with pageID).
- **Pasted text/numbers**: work with it as-is.

## 2. Extract

Pull out every **number and finding** relevant to the initiative's tracks:
metric, value, definition (exactly as the source states it), and location
("слайд 17", "стр. 3, таблица 2"). Note the data window (dates) — it goes
into the source record.

## 3. Map onto hypotheses (the core of the job)

Load open hypotheses: `python3 tools/scripts/hypotheses.py show <dir>`.
For each extracted finding, classify:

- **Supports Hx** → propose upgrade:
  `hypotheses.py set Hx --status confirmed --type REAL --confidence 0.N
  --add-source "<file>::слайд NN — <what it says>"`
- **Contradicts Hx** → propose refutation (`--status refuted`) and say
  explicitly that REAL beats the previous INFERRED/SYNTHETIC — document the
  delta in the narrative file.
- **Contradicts ANOTHER source already in the registry** → do NOT silently
  average: `hypotheses.py set Hx --flag data_inconsistency --note "source A
  vs source B: X vs Y"` and add the reconciliation question to the open
  questions for the analyst.
- **Relevant but matches no hypothesis** → candidate NEW hypothesis
  (`hypotheses.py add`) — ask the PM before adding.
- **Not mapped** → append to `research/inbox-notes.md` with source refs, so
  nothing is lost.

## 4. Typing discipline

Internal analytics/dashboards/decks of your own product = REAL. External
benchmarks and competitor numbers = INFERRED (0.3–0.5) — they are analogies,
not facts about your product. Surveys of your users = REAL. Someone's
opinion slide without data = AMBIGUOUS (0.1–0.3).

Source quality check before typing anything REAL: who produced it, what
data window, does its total reconcile with numbers already in the registry?
A REAL source with an unknown window or an unreconciled total enters at the
bottom of the REAL range (0.6), not the top.

## 5. Deliver

Summary to the PM: what was ingested (N pages/rows), which hypotheses moved
(before → after), which contradictions were flagged, what landed in
inbox-notes, and the updated registry table (`hypotheses.py render`).
Then: `research/analytics-data.md` (or a new file under `research/`) gets
the extracted numbers with locations — future jobs cite it, not the raw
artifact.

If no initiative exists: do steps 1–2 and 5 in-chat, then offer to persist
(FIRST LAUNCH flow).
