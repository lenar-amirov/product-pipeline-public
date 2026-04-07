#!/bin/bash
# Auto-push: следит за изменениями в репо и пушит автоматически.
# Запуск: ./tools/scripts/auto-push.sh (или через launchd)
# Проверяет каждые 30 секунд, пушит если есть новые коммиты.

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
INTERVAL=30

cd "$REPO_DIR" || exit 1

echo "[auto-push] Слежу за $REPO_DIR каждые ${INTERVAL}с..."

while true; do
    # Проверяем есть ли непушенные коммиты
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse origin/main 2>/dev/null)

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[auto-push] $(date '+%H:%M:%S') Есть непушенные коммиты, пушу..."
        git pull --rebase origin main 2>&1
        if git push origin main 2>&1; then
            echo "[auto-push] ✓ Запушено"
        else
            echo "[auto-push] ✗ Push не прошёл, попробую через ${INTERVAL}с"
        fi
    fi

    sleep "$INTERVAL"
done
