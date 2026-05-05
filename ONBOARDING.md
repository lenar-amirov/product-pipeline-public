# AI Diamond — Getting Started

## Quick start

```bash
git clone https://github.com/lenar-amirov/product-pipeline-public.git
cd product-pipeline-public
```

Open the repo in [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI, desktop app, or IDE extension) and say:

```
create initiative checkout-redesign
```

Claude will:
1. Ask your name and save it to `.pm-local`
2. Copy `template/` into `{your-name}/checkout-redesign/`
3. Run `/setup-initiative` — alignment checklist (metric, segment, stakeholders, etc.)
4. Suggest the next step

That's it. You're in the pipeline.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — CLI, desktop app, or IDE extension
- Python 3.10+ (for status dashboard and PPTX generation)
- `pip install rich` — for the branded terminal dashboard (shown at session start)

Optional:
```bash
pip install -r requirements.txt   # rich, flask, markdown, python-pptx
```

---

## How it works

### 1. Claude Code is your co-pilot

When you open Claude Code in the repo, it reads:
- `CLAUDE.md` — master prompt with the full pipeline
- `.claude/skills/` — 19 specialized skills (discovery, personas, funnels, PRD, pipeline-steps, etc.)
- Your initiative's `CONTEXT.md`, `status.json`, and `decisions.md`

Claude knows where you are in the pipeline and suggests the next step.

### 2. Run pipeline steps

Type a command:

```
/analyze-cjm
```

Or ask in natural language:

```
continue where we left off
show status
let's discuss the analytics results
```

### 3. Session end

After each step, Claude **automatically**:
1. Updates `status.json` — which step completed, brief summary
2. Writes to `decisions.md` — what was discussed, decisions made, open questions
3. Commits to git — everything is saved

If you close the window — data isn't lost. Next time Claude reads the saved state and continues.

---

## Initiative context

### CONTEXT.md

Filled during `/setup-initiative` or manually. Key fields:

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

Without metric, baseline, and segment, Claude will refuse to start step 1 — and rightfully so. Without them, hypotheses aren't grounded in reality.

### CJM — user journey screenshots

Put screenshots in `{initiative}/CJM/`:
- Format: `01_step-name.png`, `02_step-name.png`
- Supported: PNG, JPG, PDF, Figma files
- If a step has states: `03a_form-empty.png`, `03b_form-error.png`

---

## Configurable pipeline

### Templates

When setting up (step 0), choose a template:

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

Reconfigure anytime: tell Claude "reconfigure pipeline" or "enable competitor research".

---

## All pipeline steps

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

After Solution Research Report: `/create-tickets` to generate dev tickets and push them to Jira/Linear/GitHub Issues via MCP.

### Phase 3: Launch Preparation
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 16 | `/support-task` | Optional | Support brief: FAQ, scenarios |
| 17 | `/announce-ab-test` | Optional | AB test announcement |
| 18 | `/announce-release` | Optional | Release announcement |

### Validation branching (step 6)

- All confirmed -> proceed to step 7
- Partially confirmed -> narrow focus, proceed to step 7
- None confirmed -> return to step 1 with new data
- Insufficient data -> repeat data collection

---

## What the pipeline creates

```
my-initiative/
├── CONTEXT.md                     <- filled via step 0 or manually
├── CJM/                           <- user journey screenshots
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

## Optional: Web dashboard

A Flask dashboard is included for visual tracking (`tools/web/app.py`):

```bash
pip install -r requirements.txt
PM_USERS=$(cat .pm-local) python tools/web/app.py
# Open http://localhost:5000/{your-name}/
```

By default the app expects users `alice,bob`. Pass `PM_USERS=<your-name>` so it uses your `.pm-local` name.

Features:
- Initiative list with progress tracking
- Context editing and CJM upload
- Step-by-step navigation
- Artifact viewer (PRD, hypotheses, presentations)

---

## Optional: Tracker integration (Jira / Linear / GitHub Issues)

After Solution Research Report, AI Diamond can push tickets directly to your tracker via MCP.

### Jira

Add to your Claude Code MCP settings (`.claude/settings.local.json` or via Claude Code settings UI):

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["@anthropic/mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "you@company.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

Get your API token: https://id.atlassian.com/manage-profile/security/api-tokens

### Linear

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["@anthropic/mcp-linear"],
      "env": {
        "LINEAR_API_KEY": "your-api-key"
      }
    }
  }
}
```

Get your API key: Linear Settings → API → Personal API keys

### GitHub Issues

No extra MCP needed — Claude Code uses `gh` CLI natively.

```bash
gh auth status   # make sure you're logged in
```

Set in your initiative's `CONTEXT.md`:
```
## Tracker
**System**: GitHub Issues
**Project/Board**: owner/repo
**Labels**: initiative:checkout-redesign
```

### No tracker? No problem.

AI Diamond generates tickets as markdown in `output/tickets.md`. Copy-paste or create manually.

---

## FAQ

**How to continue working?**
Open Claude Code in the repo. Claude reads `status.json` and continues from where you left off.

**How to change pipeline configuration?**
Tell Claude: "reconfigure pipeline" or "enable step 5" or "switch to quick template".

**Can I work on multiple initiatives?**
Yes. Each initiative is a separate folder with its own status. Claude shows a list at session start.

**What are Problem Research Report and Solution Research Report?**
Presentations for your team/leadership:
- **Problem Research Report** (after step 10): problem validated + solution sketch
- **Solution Research Report** (after step 15): solution designed (design, PRD, AB test plan)

**What's the difference between step types?**
- **Core**: mandatory, pipeline breaks without them
- **Recommended**: strongly suggested, skipping may reduce quality
- **Optional**: use when relevant to your context
