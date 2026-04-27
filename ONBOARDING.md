# PM Pipeline — Onboarding Guide

## Quick start

You have 3 tools:

| Tool | Purpose | Link |
|---|---|---|
| **Dashboard** | Initiative overview, progress, create new | `https://your-server/{your-login}/` |
| **Terminal** | Work with Claude Code — it guides you through the pipeline | `https://your-server/{your-login}/terminal/` |
| **Telegram bot** | Confirmations and reminders | (configured separately) |

> Browser may show a certificate warning. Click "Advanced" -> "Proceed" — this is normal, connection is encrypted.

Login and password are provided by the administrator.

---

## 0. Claude Code setup (first run)

On **first** terminal open, Claude Code will ask for authorization. This is done once.

### Step 1: Open terminal

Go to `https://your-server/{your-login}/terminal/` or click **"Claude Code"** on an initiative card in the dashboard.

### Step 2: Authorization

In the terminal you'll see a sign-in URL:

```
Welcome to Claude Code v2.x.x

Browser didn't open? Use the url below to sign in (c to copy)

https://claude.ai/oauth/authorize?code=true&client_id=...
```

1. **Copy the link** — select with mouse or press `c`
2. **Open in your browser** (not in the terminal)
3. **Sign in** to your Claude account (claude.ai)
4. Copy the **code** shown after authorization
5. **Return to terminal** and paste the code

> After successful auth, Claude Code remembers you. Re-authorization is needed only when the token expires (every few months).

### Step 3: Verify it works

After auth, Claude will greet you. Type something like:

```
show status
```

If Claude responds — you're all set.

---

## 1. Dashboard

Open `https://your-server/{your-login}/` to see all your initiatives.

### Main page

Each initiative is a card showing:
- **Progress**: how many steps completed (e.g., 5/21)
- **Current phase and step**: Phase 1 — Problem Research - /validate-problems
- **Pending tasks**: what needs your action
- **Claude Code**: button to launch Claude Code with initiative context
- **Archive**: button to move initiative to archive

### Create new initiative

1. Click **"New Initiative"** at top
2. **Step 1 — Name**: enter in lowercase with dashes (e.g., `checkout-redesign`)
3. **Step 2 — Context**: fill fields — metric, segment, baseline, target, etc. All fields are optional, but the more you fill now, the better Claude starts
4. **Step 3 — CJM**: drag & drop user journey screenshots (PNG, JPG, PDF). Can skip and add later

> Context and CJM can be edited anytime on the initiative page.

### Initiative page

Click an initiative name for the detail view:
- **Context**: metric, segment, progress + edit button
- **CJM gallery**: uploaded user journey screenshots
- **Step table**: all steps with statuses. Each step is clickable — opens Claude Code with that command
- **Pending tasks**: what needs your action
- **Recent decisions**: log entries
- **Pipeline config**: which template is active, which steps are enabled/disabled

---

## 2. Terminal — working with Claude Code

### How it works

When you open terminal from the dashboard:
1. System navigates to your initiative folder
2. Claude Code launches — AI assistant that guides you through the pipeline
3. Claude reads context: CONTEXT.md, status.json, recent decisions
4. Suggests next step (respecting your pipeline configuration)

### How to run a step

**Via dashboard** (recommended): click a step name (e.g., `/analyze-cjm`) — Claude Code opens with that command.

**Via terminal**: type the command manually:

```
/analyze-cjm
```

Or ask in natural language:

```
continue where we left off
show status
let's discuss the analytics results
```

### Session end

After each step or discussion, Claude **automatically**:
1. Updates `status.json` — which step completed, brief summary
2. Writes to `decisions.md` — what was discussed, decisions made, open questions
3. Git commits — everything is saved

**If you close the tab** — data isn't lost. Next time Claude reads the saved state and continues.

---

## 3. Context and CJM

### Initiative context (CONTEXT.md)

Context is filled during initiative creation (step 2) or via the edit button on the initiative page.

#### Context fields

| Field | Example | Why it matters |
|---|---|---|
| **Metric** | Conversion to purchase | What we're improving |
| **Baseline** | 2.3% | Current value (can be anonymized) |
| **Target** | 3.5% | Goal value |
| **Horizon** | Quarter | Timeframe |
| **Segment** | Buyers 18-35, mobile | Who our users are |
| **Segment size** | 12M MAU | Audience scale |
| **Platform** | Web / iOS / Android / All | Which platform |
| **Why now** | Competitor launched similar | What changed |
| **Constraints** | Don't touch the player | What can't be changed |
| **Stakeholders** | VP Product (approver) | Who's involved |
| **OKR** | Increase retention 15% | Strategic alignment |
| **Kill criteria** | <5% users affected | When to stop |

> Without metric, baseline, and segment, Claude will refuse to start step 1 — and rightfully so. Without them, hypotheses aren't grounded in reality.

### CJM — user journey screenshots

Upload via dashboard: drag files or click "Choose files". Formats: PNG, JPG, PDF.

**What to upload**: screenshots of the current user journey in order — home, card, payment, etc.

---

## 4. Configurable Pipeline

### Templates

When creating an initiative (step 0), you choose a pipeline template:

| Template | Steps | Best for |
|----------|-------|----------|
| **Quick Discovery** | ~6 core steps | Have data, need structure |
| **Full Discovery** | All steps | New problem, need full research |
| **Problem Only** | 5 steps | Just understand the problem |
| **Solution Only** | 7 steps | Problem known, design solution |
| **Custom** | Your choice | You know what's needed |

### Step types

- **Core** — can't be disabled, pipeline breaks without them
- **Recommended** — improves results, can be disabled with a warning
- **Optional** — useful in specific contexts, off by default in most templates

You can reconfigure at any time by telling Claude: "reconfigure pipeline" or "enable competitor research".

---

## 5. Pipeline — all steps

### Phase 0: Setup
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 0 | `/setup-initiative` | Core | Alignment: metric, stakeholders, OKR, constraints, kill criteria, pipeline config |

### Phase 1: Problem Research -> Problem Research Report
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 1 | `/analyze-cjm` | Core | Analyze CJM, formulate problem hypotheses |
| 2 | `/synthetic-research` | Recommended | Synthetic interviews for pre-validation |
| 3 | `/competitor-research` | Recommended | Scenario analogues and competitive analysis |
| 4 | `/generate-research` | Recommended | Analytics brief + survey design |
| 5 | `/create-survey-audience` | Optional | SQL for survey audience |
| 5.5 | Research pause | Recommended | Real research: analytics, survey, 5-8 interviews |
| 6 | `/validate-problems` | Core | Validate hypotheses (3 sub-steps: quick/survey/interviews) |
| 7 | `/solution-hypotheses` | Core | Solution hypotheses with ICE + business viability |
| 8 | `/sketch-solution` | Core | Wireframes, screens, user flow |
| 8.5 | `/user-test-concept` | Optional | Concept test with 3-5 real users |
| 9 | `/review-design` | Recommended | Heuristic evaluation + iteration |
| 10 | `/create-presentation` | Core | Problem Research Report |

### Phase 2: Solution Development -> Solution Research Report
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 11 | `/create-design-brief` | Recommended | Brief for designer |
| 12 | `/estimate-with-dev` | Core | Dev estimate and tech spec |
| 13 | `/finalize-prd` | Core | Complete PRD with user stories |
| 14 | `/design-ab-test` | Recommended | AB test: baseline, MDE, sample, guardrails |
| 15 | `/create-gate2-presentation` | Core | Solution Research Report |

After Solution Research Report: `/create-jira` for dev tickets.

### Phase 3: Launch Preparation
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 16 | `/support-task` | Optional | Support brief: FAQ, scenarios |
| 17 | `/announce-ab-test` | Optional | AB test announcement |
| 18 | `/announce-release` | Optional | Release announcement |

### Step types explained

- **Core** — Claude does it automatically or guides you through it. Can't skip.
- **Recommended** — Claude suggests it. You can skip, but Claude will note the risk.
- **Optional** — Available on demand. Disabled by default in most templates.
- **Pause** — waiting for external data (analytics, survey, interviews). Claude tracks what's pending.

### What if hypotheses aren't confirmed (step 6)

Possible outcomes:
- Confirmed -> proceed to step 7
- Partially confirmed -> narrow focus, proceed to step 7
- None confirmed -> return to step 1 with new data
- Insufficient data -> repeat data collection

---

## 6. What the pipeline creates

As you work, artifacts appear in the initiative folder:

```
my-initiative/
├── CONTEXT.md                     <- filled via dashboard or step 0
├── CJM/                           <- uploaded via dashboard
│   ├── 01_home.png
│   └── 02_card.png
├── research/                      <- research artifacts
│   ├── synthetic-interviews.md    <- step 2
│   ├── competitive-analysis.md    <- step 3
│   ├── analytics-brief.md         <- step 4
│   ├── survey-questions.md        <- step 4
│   ├── survey-audience-brief.md   <- step 5
│   ├── analytics-data.md          <- from analyst
│   ├── survey-results.md          <- from researcher
│   ├── interview-notes.md         <- from PM (step 5.5)
│   └── concept-test-results.md    <- step 8.5
├── output/                        <- results
│   ├── status.json                <- pipeline status + config
│   ├── decisions.md               <- decision log
│   ├── hypotheses.md              <- step 1
│   ├── validated-hypotheses.md    <- step 6
│   ├── solution-hypotheses.md     <- step 7
│   ├── solution-sketch.md         <- step 8
│   ├── PRD.md                     <- built incrementally
│   ├── presentation.md            <- step 10
│   ├── presentation.pptx          <- step 10
│   ├── design-brief.md            <- step 11
│   ├── dev-estimate.md            <- step 12
│   ├── ab-test-design.md          <- step 14
│   ├── gate2-presentation.md      <- step 15
│   ├── gate2-presentation.pptx    <- step 15
│   ├── support-brief.md           <- step 16
│   ├── announce-ab-test.md        <- step 17
│   └── announce-release.md        <- step 18
└── CLAUDE.md                      <- instructions for Claude
```

---

## 7. Telegram bot

The bot handles two things:
1. **You confirm** you've handed off a task (brief to analyst, survey, design)
2. **Bot reminds** you when it's time to check for results

### Confirmation commands

When you've **sent a brief**:

| Situation | Bot command |
|---|---|
| Sent brief to analyst | `/analytics-brief-sent` |
| Sent survey brief | `/survey-brief-sent` |
| Sent audience brief | `/audience-brief-sent` |
| Sent brief to designer | `/design-brief-sent` |
| Sent brief to support | `/support-brief-sent` |

When you've **received results**:

| Situation | Bot command |
|---|---|
| Got analytics data | `/confirm-analytics-results` |
| Got survey results | `/confirm-survey-results` |
| Problem report passed | `/confirm-gate1-challenge` |
| Solution report passed | `/confirm-gate2-challenge` |

### Reminder schedule

- **Briefs** (analytics, survey, audience, design) -> reminder next day if not sent
- **Analytics results** -> reminder after 1 week, then weekly
- **Survey results** -> reminder after 2 weeks, then weekly
- **Gate Challenge** -> reminder next Monday
- **Friday digest** -> summary of all open tasks

---

## 8. Archive

Initiatives that are no longer active can be archived:
1. On the main dashboard page, click the archive button on the initiative card
2. Confirm in the modal
3. Initiative moves to **"Archive"** section (accessible via header)

From the archive, you can **restore** an initiative back to the main page.

---

## FAQ

**I closed the tab — is everything lost?**
No. Claude saves progress in git after every session. Reopen the initiative — it continues from the same place.

**How to continue working?**
Open initiative via dashboard -> click **"Claude Code"** or click a step. Claude reads status.json and continues.

**How to change pipeline configuration?**
Tell Claude: "reconfigure pipeline" or "enable step 5" or "switch to quick template".

**Bot doesn't respond to a command?**
Check: (1) command is typed exactly as in the table, with `/` prefix; (2) you're messaging the bot, not another chat.

**Can I work on multiple initiatives?**
Yes. Each initiative is a separate folder with its own status. Switch via dashboard.

**What are Problem Research Report and Solution Research Report?**
Presentations for your team/leadership:
- **Problem Research Report** (after step 10): problem validated + solution sketch
- **Solution Research Report** (after step 15): solution designed (design, PRD, AB test plan)

After Solution Research Report -> Phase 3: launch preparation.

**What's the difference between step types?**
- **Core**: mandatory, pipeline breaks without them
- **Recommended**: strongly suggested, skipping may reduce quality
- **Optional**: use when relevant to your context
