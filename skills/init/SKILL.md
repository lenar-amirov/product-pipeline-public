---
description: Scaffold the Product Discovery pipeline into the current project. Creates CLAUDE.md, template/, .claude/skills/, .claude/rules/, tools/scripts/. Run this once per repository to bootstrap product discovery work. Trigger when the user says "init product discovery", "scaffold pipeline", "set up discovery", or invokes /product-discovery:init.
---

# Product Discovery — Init

Scaffold the full Product Discovery pipeline into the user's current project directory.

## What this does

Copies the plugin's bundled files into the user's repo so they can use the pipeline locally:

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

Once scaffolded, the user works with the pipeline as a normal local project — Claude reads CLAUDE.md on every session, runs status.py, and walks them through the discovery flow.

## How to run

When the user invokes `/product-discovery:init` (or asks to scaffold):

1. **Confirm location** — ask: "Scaffold Product Discovery into `<current-dir>`? (y/n)"
   - Show the absolute path so the user knows exactly where files will land
   - If user says no, ask which directory they want

2. **Check for conflicts** — if `CLAUDE.md`, `.claude/`, `template/`, or `tools/` already exist in the target, list them and ask:
   - "These files exist. (m)erge — keep existing, only add new files / (o)verwrite / (c)ancel?"
   - Default to merge (safer)

3. **Copy plugin files** — use the bash tool to copy from the plugin directory.
   The plugin's source files live alongside this skill. Use `${CLAUDE_PLUGIN_ROOT}` if available, otherwise resolve via the skill's location.

   ```bash
   PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname $(dirname "$0"))}"
   TARGET="${1:-.}"

   # Skip files the user already has unless they said overwrite
   cp -rn "$PLUGIN_ROOT/CLAUDE.md" "$TARGET/"
   cp -rn "$PLUGIN_ROOT/.claude" "$TARGET/"
   cp -rn "$PLUGIN_ROOT/template" "$TARGET/"
   cp -rn "$PLUGIN_ROOT/tools" "$TARGET/"
   ```

4. **Install dependencies hint** — after copying, tell the user:
   ```
   ✓ Product Discovery pipeline scaffolded.

   Next:
     pip install rich       # for the session-start dashboard
     claude                 # restart Claude Code to load CLAUDE.md

   Then describe your product problem and the pipeline will guide you.
   ```

5. **Don't auto-run anything else** — let the user restart Claude Code so CLAUDE.md is freshly loaded.

## Edge cases

- **No write access**: surface the OS error clearly, suggest `sudo` only if appropriate
- **Plugin files missing**: if `${CLAUDE_PLUGIN_ROOT}` doesn't contain CLAUDE.md, the plugin install is broken — tell user to reinstall via `/plugin install product-discovery`
- **User in their home directory**: warn before copying — ask "Are you sure you want to scaffold into `~`? Usually you want a project subdirectory."

## Why this exists

Product Discovery is a Claude Code-native pipeline. Its core lives in CLAUDE.md (auto-loaded by Claude on every session) and in skills/rules under `.claude/`. Plugins can ship those skills, but Claude Code doesn't auto-inject CLAUDE.md from a plugin into the user's project. So we use a one-time scaffold step to copy the necessary files locally — after that, the project works without further plugin involvement.
