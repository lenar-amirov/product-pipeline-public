---
name: interview-analysis
description: Turns raw user-interview notes into coded patterns and registry verdicts — the method behind validation 6c and any qualitative debrief. Use for "вот заметки с интервью", "interview notes", "разбери интервью", "что сказали пользователи на интервью", "проанализируй звонки с клиентами".
---

# Interview Analysis — notes → codes → verdicts

Interviews are the highest-confidence qualitative REAL source (0.9–1.0 by
the evidence-typing scale) — and the easiest to cherry-pick. This method
keeps them honest.

## 1. Intake

Input: `research/interview-notes.md` (or pasted notes / transcripts).
Establish per interview: participant segment (matches CONTEXT.md segment?),
date, moderated by whom. Off-segment participants get analyzed separately —
their quotes must not launder into the main verdicts.

## 2. Coding (before any conclusions)

Walk the notes and tag utterances with codes — behaviors, pains,
workarounds, triggers ("compares prices elsewhere", "doesn't trust
payment"). Rules:
- Code what the user DID or experienced, not what they proposed ("add
  feature X" → code the underlying pain, not the feature)
- One utterance may carry several codes; keep participant id attached
- New code ≠ new hypothesis yet — codes are raw material

## 3. Patterns with frequency honesty

Group codes → patterns with explicit counts: "4 of 6 participants
mentioned…". Rules:
- A pattern needs ≥3 participants (of a typical 5–8 batch) — below that
  it's an anecdote; report it as such
- Actively look for DISCONFIRMING quotes for each pattern — one honest
  counter-example in the report beats ten confirmations
- Divergent answers may mean segmentation, not noise — say which

## 4. Verdicts to the registry

Map each pattern onto open hypotheses:
`hypotheses.py set <id> --status confirmed|refuted|testing --type REAL
--confidence 0.9 --add-source "research/interview-notes.md::N of M
participants, codes: <...>"`. Confidence scales with N/M and segment match
(0.9–1.0 full batch on-segment; 0.6–0.7 thin or mixed). Patterns matching
no hypothesis → candidate `hypotheses.py add` (ask the PM). Then
`hypotheses.py validate && hypotheses.py render`.

## 5. Deliver

Synthesis to `research/interview-notes.md` (append section): patterns with
counts and verbatim quotes (marked per participant), disconfirming
evidence, what interviews CANNOT tell us (quantification → analytics),
registry changes made. Update decisions.md. If the batch was synthetic
(personas, not people) — this skill does not apply; that's SYNTHETIC 0.2–0.4
territory in step 2.
