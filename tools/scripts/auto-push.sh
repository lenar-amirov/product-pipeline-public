#!/bin/bash
# Auto-push: watches the repo for changes and pushes automatically.
# Usage: ./tools/scripts/auto-push.sh (or via launchd)
# Checks every 30 seconds, pushes if there are new commits.

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
INTERVAL=30

cd "$REPO_DIR" || exit 1

echo "[auto-push] Watching $REPO_DIR every ${INTERVAL}s..."

while true; do
    # Check if there are unpushed commits
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse origin/main 2>/dev/null)

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[auto-push] $(date '+%H:%M:%S') Unpushed commits found, pushing..."
        git pull --rebase origin main 2>&1
        if git push origin main 2>&1; then
            echo "[auto-push] Done, pushed successfully"
        else
            echo "[auto-push] Push failed, will retry in ${INTERVAL}s"
        fi
    fi

    sleep "$INTERVAL"
done
