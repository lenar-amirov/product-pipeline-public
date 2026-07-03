---
name: setup-initiative
description: Guides the PM through an initiative alignment checklist — metric, baseline, target, stakeholders, success/kill criteria. Use before a gate, when the PM says "setup initiative", "set the target", "define success criteria", "align on goals", or when the coverage map shows Frame incomplete. NOT a prerequisite for starting work — jobs run without it.
---

# Setup Initiative

Fills the **Frame phase** of the coverage map. NOT a gatekeeper for starting
work — jobs run without it (zero-setup principle); this skill earns its
place before the first gate or whenever the PM asks about targets.

## Purpose

Explicit alignment on goals, constraints, stakeholders, and success criteria.
The coverage map (`coverage.py`) shows `Frame N/4` until metric, baseline,
target and kill criteria are recorded — gates are blocked while Frame is
incomplete.

## When to use

- Before assembling a Gate presentation (gate preconditions require Frame)
- When the PM asks about targets / success criteria
- When `/next` recommends it (Frame gaps + a gate is near)
- NEVER as a forced first step of a new initiative

## Checklist

Guide the PM through these 10 areas. For each area, ask a focused question, then write the answer to CONTEXT.md.

### 1. Outcome
**Ask**: "What metric are we trying to improve, and by how much?"
- Get: metric name, current baseline, target, measurement horizon
- If PM doesn't know exact numbers: "Give your best estimate — we'll refine after step 1"
- **Required**: at minimum the metric name and direction (up/down)

### 2. Stakeholders
**Ask**: "Who needs to approve this at Report presentation, and who might block it?"
- Get: decision-maker, influencers, potential blockers
- Map: name -> role -> concern/interest
- If PM says "just me": note that, but ask about dev lead and designer

### 3. OKR Alignment
**Ask**: "Which company or team OKR does this serve?"
- Get: specific OKR text or "exploratory / not tied to OKR"
- If no OKR: flag as risk for report presentation ("needs strategic framing")

### 4. Constraints
**Ask**: "What can't we change, and what's our timeline?"
- Get: timeline, budget, team capacity, tech limitations, political constraints
- Distinguish hard constraints (deadline) from soft (preference)

### 5. Success Criteria
**Ask**: "If this initiative goes perfectly, what does the world look like in 3 months?"
- Get: specific, measurable outcome
- Push back on vague answers: "more users" -> "X% increase in Y metric"

### 6. Kill Criteria
**Ask**: "Under what conditions should we stop this initiative?"
- Get: specific threshold (e.g., "if validation shows <5% of users affected")
- If PM resists: "This protects your time. What would make you say 'this isn't worth it'?"
- Default suggestion: "If step 6 validation confirms none of the hypotheses"

### 7. User Segment
**Ask**: "Who specifically are we building this for?"
- Get: segment definition, size, platform, key behavior
- Push for specificity: "all users" -> "users who [specific behavior]"

### 8. Available Data
**Ask**: "What do we already know? Analytics, research, customer feedback?"
- Get: inventory of existing data sources
- If rich data exists: suggest `/ingest` right after the checklist — it will
  move hypotheses to REAL fastest

### 9. Tracker
**Ask**: "Where do you want dev tickets to land — Jira, Linear, GitHub Issues, or none?"
- Get: tracker system, project key/board name, standard labels
- If they say "I'll figure it out later" — set `None`, can be changed before `/create-tickets`
- Mention: "If you want me to push tickets directly, you'll need to connect the MCP — see Tracker integration section in README.md"

(Pipeline templates are **deprecated** — do not offer them. The PM runs the
jobs they need; the coverage map shows what evidence is still missing. If
the PM explicitly wants to disable an Optional/Recommended step, toggle it
in `pipeline_config.steps` with a one-line warning about what it costs.)

## Output

1. **CONTEXT.md** — all checklist answers written to appropriate fields
2. Re-run the coverage check (`python3 tools/scripts/coverage.py <dir>`) and
   show the PM the Frame line before/after — the visible payoff of 5 minutes
   of alignment

## Tips

- Don't make this feel like a bureaucratic form. It's a conversation.
- If PM has already filled some fields in CONTEXT.md — acknowledge and skip those.
- If PM wants to skip the checklist: "I understand, but 5 minutes now saves hours later. Let me ask the 3 most critical questions: metric, segment, and stakeholders."
- Adapt language to PM's style — if they're brief, be brief. If they elaborate, explore.
