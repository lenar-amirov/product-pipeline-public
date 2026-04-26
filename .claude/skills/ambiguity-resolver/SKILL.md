---
name: ambiguity-resolver
description: Structures vague opportunities and unclear briefs into actionable
one-page problem statements. Use when user has a vague brief, undefined problem,
unclear opportunity, or says "we need to figure out what to do about X", "can
you help me make sense of this", or "I've been asked to look into Y".
metadata:
  author: Mohit Aggarwal
  version: 1.0.0
  category: discovery
  tags: [discovery, strategy, problem-framing, ambiguity]
  documentation: https://github.com/mohitagw15856/pm-claude-skills
---
# Ambiguity Resolver Skill

## Purpose
Turn vague briefs and half-formed opportunities into structured, actionable
problem statements — so you can reply with clarity instead of asking for three
more meetings.

## Three-Stage Process

### Stage 1: Reframe
- Restate the vague input as 3-5 explicit questions that need answering
- Identify the unstated assumptions hidden in the brief
- Surface the real decision this feeds into (what will someone do differently
  once this is resolved?)

### Stage 2: Scope
- Define what is explicitly IN scope
- Define what is explicitly OUT of scope (equally important)
- Identify the deadline pressure: is this urgent/important, important/not urgent,
  or unclear?
- Name who owns the final decision and who needs to be consulted

### Stage 3: Action
- Define the minimum viable research: 2-3 activities maximum that would give
  enough signal to move forward with confidence
- Time estimate for each activity
- What each activity would tell you (and what it wouldn't)
- Proposed check-in point: when to regroup before committing to more

## Output Format

### Problem Brief: [Opportunity Area]

**Restated as questions:**
1. [Question 1]
2. [Question 2]
3. [Question 3]

**Unstated assumptions we should surface:**
- [Assumption 1]
- [Assumption 2]

**In scope:** [Clear boundary]
**Out of scope:** [Clear boundary]
**Decision owner:** [Name/role]
**Timeline:** [Real deadline if known, or "unclear — recommend setting one"]

**Minimum viable research:**
| Activity | Time required | What it tells us |
|----------|--------------|------------------|
| [activity] | [time] | [insight] |

**Proposed check-in:** After [activity], regroup to decide whether to proceed
or pivot.

## Pipeline Integration

This skill is a **utility** — use it at any pipeline step when input is vague or contradictory.

### Common Triggers

| Step | Trigger | Output |
|------|---------|--------|
| **0. setup-initiative** | PM provides vague brief: "we need to do something about retention" | Full 3-stage process -> feeds into CONTEXT.md |
| **1. analyze-cjm** | CJM is incomplete or contradictory | Quick reframe -> clarify scope before hypothesis generation |
| **6. validate-problems** | Data partially confirms, partially contradicts | Scope stage -> define what's in/out for solution phase |
| **7. solution-hypotheses** | Multiple valid directions, PM can't choose | Reframe stage -> surface the real decision criteria |
| **Any step** | PM says "I'm not sure what we should do here" | Quick mode (below) |

### Quick Mode (3-Question Reframe)

For mid-step ambiguity when the full 3-stage process is too heavy:

1. **What specifically is unclear?** (Name the ambiguity — don't accept "everything")
2. **What would you do if you knew the answer?** (Reveals the real decision this feeds)
3. **What's the smallest thing we could do to get enough signal?** (Minimum viable research)

Write the answers to `output/decisions.md` as an ambiguity resolution entry:
```markdown
## YYYY-MM-DD — Ambiguity Resolution at Step N

**Ambiguity**: [What was unclear]
**Real decision**: [What knowing the answer enables]
**Resolution**: [What we decided / what we'll do to find out]
**Next step**: [Specific action]
```
