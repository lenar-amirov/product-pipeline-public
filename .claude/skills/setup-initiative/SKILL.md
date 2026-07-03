---
name: setup-initiative
description: Guides the PM through an initiative alignment checklist — metric, baseline, target, stakeholders, success/kill criteria, pipeline config. Use at the start of a new initiative, when the PM says "setup initiative", "set the target", "define success criteria", "align on goals", "configure the pipeline", or when CONTEXT.md is full of [to be validated] placeholders.
---

# Setup Initiative

Step 0 of the PM Pipeline. Guides the PM through an alignment checklist before any work begins.

## Purpose

Ensure explicit alignment on goals, constraints, stakeholders, and success criteria before investing time in research and solution design. Prevents the #1 cause of wasted work: misaligned expectations.

## When to use

- At the very start of a new initiative (after `template/` is copied)
- When PM says "create initiative" — this runs automatically after scaffolding
- When PM wants to reconfigure the pipeline mid-initiative

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
- This determines which steps can be accelerated or skipped
- If rich data exists: suggest `quick` or `solution-only` template

### 9. Tracker
**Ask**: "Where do you want dev tickets to land — Jira, Linear, GitHub Issues, or none?"
- Get: tracker system, project key/board name, standard labels
- If they say "I'll figure it out later" — set `None`, can be changed before `/create-tickets`
- Mention: "If you want me to push tickets directly, you'll need to connect the MCP — see Tracker integration section in README.md"

### 10. Pipeline Configuration
**Ask**: "How thorough should we be?" Then present template options:

```
Templates:
1. Quick Discovery (6 steps) — you have data, need structure
2. Full Discovery (all steps) — new problem space, need research
3. Problem Only (5 steps) — just understand the problem
4. Solution Only (7 steps) — problem is known, design the solution
5. Custom — pick steps yourself
```

For custom: show all steps with Core/Recommended/Optional labels. Core can't be disabled.

If PM picks a template with disabled recommended steps, show warning for each:
```
Note: Competitor research is disabled. Your solution may unknowingly duplicate existing products.
```

## Output

1. **CONTEXT.md** — all checklist answers written to appropriate fields
2. **pipeline_config in status.json** — template name + per-step enabled/type config

## Tips

- Don't make this feel like a bureaucratic form. It's a conversation.
- If PM has already filled some fields in CONTEXT.md — acknowledge and skip those.
- If PM wants to skip the checklist: "I understand, but 5 minutes now saves hours later. Let me ask the 3 most critical questions: metric, segment, and stakeholders."
- Adapt language to PM's style — if they're brief, be brief. If they elaborate, explore.
