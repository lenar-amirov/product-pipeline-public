#!/bin/bash
# Claude Code manages its own auth via ~/.claude/.credentials.json
# Do NOT set CLAUDE_CODE_OAUTH_TOKEN here — it overrides fresh tokens and causes 401s

STATE="/tmp/pm-session-$(whoami)"
if [ -f "$STATE" ]; then
    TARGET=$(cat "$STATE" 2>/dev/null)
    rm -f "$STATE" 2>/dev/null || true
    [ -n "$TARGET" ] && [ -d "$TARGET" ] && cd "$TARGET"
    claude
fi

exec bash -l
