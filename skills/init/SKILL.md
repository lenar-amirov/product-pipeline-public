---
description: Scaffold the Product Discovery pipeline into the user's current project directory. Run when the user invokes /product-discovery:init or asks to "scaffold pipeline", "set up product discovery", "initialize discovery". Copies CLAUDE.md, template/, .claude/skills/, .claude/rules/, and tools/scripts/ from the plugin into the user's working directory, so Claude can run the discovery pipeline on every future session.
---

# Product Discovery — Init

Scaffold the full Product Discovery pipeline into the user's current project directory.

## What this skill does

Copies the plugin's bundled pipeline files into the user's working directory:

```
<user-repo>/
├── CLAUDE.md                       # Master prompt — pipeline lifecycle
├── .claude/
│   ├── skills/                     # 19 specialized skills
│   └── rules/                      # Output formats, evidence typing
├── template/                       # Initiative scaffold
└── tools/scripts/
    ├── status.py                   # Branded session-start dashboard
    ├── new-initiative.sh           # Initiative scaffolder
    └── generate-pptx.py            # Presentation builder
```

Once scaffolded, the user works with the pipeline as a normal local project — Claude reads CLAUDE.md at every session start, runs status.py, and walks them through the discovery flow.

## How to run

Follow these steps in order. **Don't skip the confirmation step** — the user needs to know exactly what's being copied where.

### Step 1: Confirm location

Run:
```bash
pwd
```

Show the absolute path to the user and ask:
> "Scaffold Product Discovery into `<absolute-path>`? (y/n)"

- If user says no, ask: "Which directory should I scaffold into?"
- If user is in `~` (home directory), warn: "This will copy files directly into your home directory. Usually you want a project subdirectory. Continue anyway?"

### Step 2: Check for existing files

Run:
```bash
ls -d CLAUDE.md .claude template tools 2>/dev/null
```

If any of those exist, list them and ask:
> "These files already exist: [list]. Choose: (m) merge — keep existing, only add new / (o) overwrite all / (c) cancel?"

Default to merge. Skip step 3 if user picks cancel.

**Special case for `.claude/settings.json`**: if the user already has `.claude/settings.json`, our SessionStart hook won't be added in merge mode. Tell them: "Your existing `.claude/settings.json` was kept. To get auto-launching of the welcome screen at session start, manually add this hook to your settings.json:"

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "python3 tools/scripts/status.py" } ] }
    ]
  }
}
```

### Step 3: Copy files

The plugin's bundled files live at `${CLAUDE_PLUGIN_ROOT}` — this environment variable is set by Claude Code when the plugin is loaded.

Run this single bash block:

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT not set — plugin install may be broken}"
TARGET="$(pwd)"

# Use -n (no-clobber) for merge, -f for overwrite. Default: merge.
COPY_FLAG="${COPY_FLAG:--n}"

cp -r $COPY_FLAG "$PLUGIN_ROOT/CLAUDE.md" "$TARGET/" 2>/dev/null || cp -r "$PLUGIN_ROOT/CLAUDE.md" "$TARGET/"
cp -r $COPY_FLAG "$PLUGIN_ROOT/.claude" "$TARGET/" 2>/dev/null || true
cp -r $COPY_FLAG "$PLUGIN_ROOT/template" "$TARGET/" 2>/dev/null || true
cp -r $COPY_FLAG "$PLUGIN_ROOT/tools" "$TARGET/" 2>/dev/null || true

# Verify the copy succeeded
ls "$TARGET/CLAUDE.md" "$TARGET/template" "$TARGET/.claude/skills" "$TARGET/tools/scripts" >/dev/null && echo "OK" || echo "MISSING"
```

For overwrite mode, set `COPY_FLAG=-f` before running.

### Step 4: Tell the user what to do next

After successful copy, show the user this exact set of next steps. **The cd step is critical** — Claude loads CLAUDE.md from the working directory, so the user MUST be in the scaffolded directory when they restart Claude Code.

```
✓ Product Discovery pipeline scaffolded into <ABSOLUTE_PATH>

NEXT STEPS — run these in your terminal:

  pip3 install rich                          # install dashboard (macOS often only has pip3)
  /exit                                       # exit this Claude Code session
  cd "<ABSOLUTE_PATH>" && claude              # ⚠ MUST cd into the scaffolded dir before launching claude

In the new Claude Code session, send any message —
Claude will show the welcome screen and ask:
  "What product problem are you working on?"
```

Substitute `<ABSOLUTE_PATH>` with the absolute path you scaffolded into. Use double quotes — the path may contain spaces.

**Why cd matters**: Claude Code loads `CLAUDE.md` from the current working directory at session start. If the user runs `claude` from anywhere else (like home), the pipeline's CLAUDE.md won't load and Claude won't know about Product Discovery. This is the #1 user error — emphasize it.

**If `pip3` also fails**: try `python3 -m pip install rich`.

### Step 5: Stop here

Don't run status.py, don't try to start the pipeline. CLAUDE.md only takes effect after Claude Code restarts. Tell the user to restart and end the response.

## Edge cases

- **`CLAUDE_PLUGIN_ROOT` is empty or unset**: tell the user "Plugin install appears broken. Try: `/plugin uninstall product-discovery && /plugin install product-discovery`"
- **No write permission**: surface the OS error verbatim. Don't suggest `sudo` automatically — that's risky for files going into a project directory.
- **Source files missing in plugin install**: if `ls "$PLUGIN_ROOT/CLAUDE.md"` fails, the plugin is corrupted. Tell user to reinstall.
- **User wants to update an already-scaffolded project**: suggest `cd` to a fresh directory or use `COPY_FLAG=-f` to overwrite (warning: overwrites their CLAUDE.md customizations).

## Why this skill exists

Product Discovery is a Claude Code-native pipeline. Its core lives in `CLAUDE.md` (auto-loaded by Claude on every session) and in `.claude/skills/` + `.claude/rules/`. Plugins ship those files, but Claude Code doesn't auto-inject `CLAUDE.md` from a plugin into the user's project — files in `.claude/` plugin directories are loaded into the plugin's own context, not the user's project.

So we use a one-time scaffold step to copy the necessary files into the user's project directory. After that, the project works as a standalone Product Discovery setup — the user can iterate without further plugin involvement, push to their own git repo, customize CLAUDE.md, etc.
