#!/bin/bash
# Creates a new initiative folder from the template
# Usage: ./new-initiative.sh "initiative-name"

set -e

if [ -z "$1" ]; then
  echo "Usage: ./new-initiative.sh \"initiative-name\""
  echo "Example: ./new-initiative.sh checkout-redesign"
  exit 1
fi

NAME="$1"

# Find repo root (where template/ lives)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATE="$REPO_ROOT/template"

if [ ! -d "$TEMPLATE" ]; then
  echo "Error: template/ directory not found at $REPO_ROOT"
  exit 1
fi

# Determine PM name
PM_FILE="$REPO_ROOT/.pm-local"
if [ -f "$PM_FILE" ]; then
  PM="$(cat "$PM_FILE" | tr -d '[:space:]')"
else
  echo -n "Enter your name (will be saved to .pm-local): "
  read PM
  echo "$PM" > "$PM_FILE"
  echo "Saved: $PM_FILE"
fi

TARGET="$REPO_ROOT/$PM/$NAME"

if [ -d "$TARGET" ]; then
  echo "Error: initiative '$PM/$NAME' already exists"
  exit 1
fi

# Create PM directory if needed
mkdir -p "$REPO_ROOT/$PM"

# Copy template
cp -r "$TEMPLATE" "$TARGET"

# Replace placeholders in CONTEXT.md (macOS + Linux compatible).
# Escape sed metacharacters in user-provided values (/, &, \).
NAME_ESC=$(printf '%s' "$NAME" | sed -e 's/[\/&\\]/\\&/g')
PM_ESC=$(printf '%s' "$PM" | sed -e 's/[\/&\\]/\\&/g')
if [ -f "$TARGET/CONTEXT.md" ]; then
  sed -i.bak "s/\[INITIATIVE_NAME\]/$NAME_ESC/g; s/\[PM_NAME\]/$PM_ESC/g" "$TARGET/CONTEXT.md"
  rm -f "$TARGET/CONTEXT.md.bak"
fi

# Update status.json with PM and initiative name
if [ -f "$TARGET/output/status.json" ]; then
  python3 -c "
import json, sys
from datetime import date
with open(sys.argv[1], 'r') as f:
    d = json.load(f)
d['pm'] = sys.argv[2]
d['initiative'] = sys.argv[3]
d['created'] = str(date.today())
with open(sys.argv[1], 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
" "$TARGET/output/status.json" "$PM" "$NAME"
fi

# Initialize decisions.md
echo "# Decision Log: $NAME" > "$TARGET/output/decisions.md"

# Create CJM directory
mkdir -p "$TARGET/CJM"

echo ""
echo "Initiative created: $PM/$NAME"
echo ""
echo "Just tell Claude what you need — jobs work standalone:"
echo "  /hypotheses  -> break the problem into hypotheses"
echo "  /ingest      -> feed in a deck / export / page you were given"
echo "  /brief       -> brief for analyst or designer"
echo "  /validate    -> check hypotheses against data"
echo "  /solutions   -> solution hypotheses with scoring"
echo "  /next        -> what's the most valuable next action"
echo ""
echo "CONTEXT.md fills in incrementally as you work — no upfront checklist."
