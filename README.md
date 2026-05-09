# Product Discovery

**Run a product initiative as a tracked journey — from one-sentence problem to PRD, with persistent state across sessions.**

Not a toolbox of one-shot AI answers. A structured pipeline where every session adds to the same initiative — drill-down questions, evidence-typed hypotheses, a PRD that builds incrementally, and a decision log you can come back to next week.

Built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Powered by Double Diamond, Teresa Torres' Continuous Discovery, and Marty Cagan's Product Discovery.

> **Requires** Claude Code desktop app or CLI (not the web version — needs persistent local state).

---

## Why this, and not a PM skill toolbox?

There are great PM skill marketplaces (e.g. [pm-skills](https://github.com/phuryn/pm-skills)) that give you 60+ skills you can call ad-hoc: `/write-prd`, `/competitive-analysis`, `/personas`. They're excellent for one-shot answers.

**Product Discovery is different.** It's not a toolbox — it's a journey:

| | PM toolbox (e.g. pm-skills) | Product Discovery (this) |
|---|---|---|
| **Unit of work** | One question, one answer | One initiative, many sessions |
| **State** | Stateless — Claude forgets next time | Persistent: CONTEXT.md, status.json, decisions.md, PRD.md |
| **PRD** | Generated when you ask | Living document, builds across all 18 steps |
| **Evidence** | Free-form text | Typed: REAL / SYNTHETIC / INFERRED with confidence 0.0–1.0 |
| **Continuity** | Each session is a fresh start | Resume exactly where you stopped, with full context |
| **Best for** | Quick answers on any PM task | Working a real product initiative through to launch |

**Use a PM toolbox** when you want quick help with one specific task.
**Use Product Discovery** when you've committed to a real initiative and want a tracked path from problem to launch.

(They complement each other — you can install both.)

---

## Get started in 30 seconds

### 1. Install the plugin

In Claude Code:

```
/plugin marketplace add https://github.com/lenar-amirov/product-pipeline-public.git
/plugin install product-discovery
```

(Use the full HTTPS URL — the GitHub shorthand `lenar-amirov/product-pipeline-public` may try SSH and fail if your git is configured for SSH-only.)

Then in any project where you want to start a discovery:

```
/product-discovery:init
```

The plugin scaffolds `CLAUDE.md`, `template/`, and `.claude/` into your repo. After scaffolding:

```bash
pip3 install rich        # for the status dashboard (use pip3 on macOS)
```

Restart Claude Code in the scaffolded directory so the new `CLAUDE.md` loads.

### Alternative: clone the repo

If you don't want the plugin, clone directly:

```bash
git clone https://github.com/lenar-amirov/product-pipeline-public.git my-discovery
cd my-discovery && pip3 install rich
```

Open in [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

### 2. Describe your problem

You'll see:

```
╭────────────────────────────────────────╮
│                                        │
│  ◆ Product Discovery                   │
│  PM Copilot                            │
│                                        │
╰────────────────────────────────────────╯

  What product problem are you working on?
```

Type one sentence. For example:

> Users add items to cart but never complete checkout on mobile

### 3. Claude drills down — then creates an initiative

Claude won't immediately give you a polished consulting answer. Instead it asks 2–3 sharp follow-up questions to force specificity:

> "Where exactly do they drop — payment, address, cart? Which segment — new vs returning? What metric should move?"

Then it scaffolds an initiative folder, generates 3–5 problem hypotheses (marked `INFERRED` until validated), drafts a research plan, and shows you what's next.

The work is now persisted. Close Claude, come back tomorrow — the initiative resumes exactly where you left off.

---

## The pipeline

18 steps across 3 phases. Each step produces a concrete artifact and updates the living PRD.

```
   Problem Research              Solution Design + Validate         Launch
┌─────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────┐
│ CJM Analysis            │  │ Design Brief                 │  │ GTM Plan     │
│ Synthetic Research      │  │ Dev Estimate                 │  │ GTM Materials│
│ Competitor Research     │  │ Finalize PRD                 │  │ Support Brief│
│ Research Briefs         │  │ AB Test Design               │  └──────────────┘
│ Validate Problems       │  │ Solution Research Report ▶   │
│ Solution Hypotheses     │  │ AB Test Analysis             │
│ Sketch Solution         │  │  → Ship / Extend / Iterate   │
│ Design Review           │  └──────────────────────────────┘
│                         │
│   Problem Research      │
│       Report ▶          │
└─────────────────────────┘
```

### What you accumulate over the journey

| Artifact | What it is |
|----------|-----------|
| **CONTEXT.md** | The initiative's frame: metric, segment, baseline, constraints, OKR — never re-explained |
| **status.json** | Current step, pending tasks, pipeline config — Claude resumes from here |
| **decisions.md** | Log of every meaningful decision and discussion across sessions |
| **hypotheses.md** | Problem hypotheses with evidence typing (REAL/SYNTHETIC/INFERRED) |
| **PRD.md** | Living document — sections fill as you progress, not at the end |
| **Problem Research Report** | Presentation: validated problem + solution sketch (after step 10) |
| **Solution Research Report** | Presentation: designed solution + AB test plan (after step 15) |
| **tickets.md** | Dev tickets — pushed to Jira/Linear/GitHub via MCP if connected |

---

## What's bundled

| Component | Role |
|-----------|------|
| `CLAUDE.md` | Master prompt — session lifecycle, FIRST LAUNCH flow, intent matching |
| `.claude/settings.json` | `SessionStart` hook that auto-runs the dashboard at every session |
| `.claude/skills/` | 19 specialized skills — discovery, personas, funnels, PRD, design critique, pipeline-steps, etc. |
| `.claude/rules/` | Path-scoped rules: output formats, evidence typing |
| `template/` | Initiative scaffold copied for each new initiative |
| `tools/scripts/status.py` | Branded terminal dashboard with first-launch onboarding |
| `tools/scripts/new-initiative.sh` | Initiative scaffolder |
| `tools/scripts/generate-pptx.py` | Markdown → PowerPoint conversion |

### Your initiative folder

```
you/my-initiative/
├── CONTEXT.md              ← metric, segment, baseline, constraints
├── CJM/                    ← user journey screenshots
├── research/               ← analytics briefs, survey design, competitive analysis
└── output/                 ← hypotheses, PRD, presentations, decision log
```

### Configurable pipeline

Pick a template or compose your own. Mandatory steps stay locked.

| Template | Steps | Best for |
|----------|-------|----------|
| **Quick Discovery** | ~6 core steps | PM with existing data, tight timeline |
| **Full Discovery** | All steps | New problem space, full research |
| **Problem Only** | 5 steps | Just understand the problem |
| **Solution Only** | 7 steps | Problem known, design solution |
| **Custom** | Your choice | You know what's needed |

---

## Tracker integration

After Solution Research Report, push tickets to your tracker via MCP. Set the tracker in `CONTEXT.md` → `## Tracker` section, then connect the MCP server:

### Jira

Add to your Claude Code MCP settings (`.claude/settings.local.json`):

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
      "env": { "LINEAR_API_KEY": "your-api-key" }
    }
  }
}
```

API key: Linear → Settings → API → Personal API keys.

### GitHub Issues

No extra MCP — Claude Code uses `gh` CLI natively. Run `gh auth status` to verify you're logged in.

### No tracker

Skip MCP. `/create-tickets` writes `output/tickets.md` for manual copy-paste.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — CLI, desktop app, or IDE extension (not web)
- Python 3.10+
- `pip3 install rich` — for the terminal dashboard

Optional, install on demand:
- `pip3 install python-pptx` — when you reach `/create-presentation` (step 10) or `/create-gate2-presentation` (step 15)
- `pip3 install flask markdown` — only if you want the optional Flask web dashboard at `tools/web/app.py`

---

## Optional: Flask web dashboard

`tools/web/app.py` provides a visual dashboard:

```bash
pip3 install flask markdown
PM_USERS=$(cat .pm-local) python3 tools/web/app.py
# open http://localhost:5000/{your-name}/
```

Most users don't need this — `tools/scripts/status.py` (auto-run at session start) shows the same info in the terminal.

---

## FAQ

**How do I continue working?**
Open Claude Code in the project directory. The SessionStart hook runs `status.py` which loads your last state. Type "continue" and Claude picks up where you stopped.

**How do I change the pipeline configuration?**
Tell Claude: "reconfigure pipeline" or "switch to quick template" or "enable competitor research". The config lives in `output/status.json` → `pipeline_config`.

**Can I work on multiple initiatives in parallel?**
Yes. Each initiative is a separate folder with its own `CONTEXT.md`, `status.json`, `decisions.md`. Claude shows all initiatives at session start; you select one.

**What are Problem Research Report and Solution Research Report?**
Two presentations for stakeholders:
- **Problem Research Report** (after step 10) — validated problem + solution sketch
- **Solution Research Report** (after step 15) — designed solution + AB test plan

**What's the difference between step types?**
- **Core** — pipeline breaks without it
- **Recommended** — strongly suggested; skipping reduces confidence
- **Optional** — useful in specific contexts only

**Where are my personal preferences stored?**
- `pm-profile.md` — your role, company, working style (gitignored, personal)
- `.product-corrections.md` — accumulated corrections you've taught Claude (gitignored)
- `.initiatives-digest.md` — auto-generated overview of all your initiatives

---

## License

MIT
