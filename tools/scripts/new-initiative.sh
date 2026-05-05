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

# Replace placeholders in CONTEXT.md (macOS + Linux compatible)
if [ -f "$TARGET/CONTEXT.md" ]; then
  sed -i.bak "s/\[INITIATIVE_NAME\]/$NAME/g; s/\[PM_NAME\]/$PM/g" "$TARGET/CONTEXT.md"
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
echo "Next steps:"
echo "  1. Fill in $PM/$NAME/CONTEXT.md"
echo "  2. Add CJM screenshots to $PM/$NAME/CJM/ (format: 01_step-name.png, 02_step-name.png...)"
echo "  3. Open Claude Code in the repo root"
echo "  4. Say: \"work on $NAME\" or run /setup-initiative"
echo ""
echo "Pipeline commands:"
echo ""
echo "  -- Phase 1: Problem Research --> Problem Research Report --"
echo "  0.  /setup-initiative        -> alignment checklist + pipeline config"
echo "  1.  /analyze-cjm             -> problem hypotheses from CJM"
echo "  2.  /synthetic-research      -> synthetic interviews or real research brief"
echo "  3.  /competitor-research     -> competitive analysis"
echo "  4.  /generate-research       -> analytics brief + survey design"
echo "  5.  /create-survey-audience  -> survey audience selection"
echo "  6.  /validate-problems       -> validate hypotheses with data"
echo "  7.  /solution-hypotheses     -> solution hypotheses with ICE"
echo "  8.  /sketch-solution         -> wireframes + user flow"
echo "  9.  /review-design           -> heuristic evaluation"
echo "  10. /create-presentation     -> Problem Research Report (.md + .pptx)"
echo ""
echo "  -- Phase 2: Solution Development --> Solution Research Report --"
echo "  11. /create-design-brief     -> brief for designer"
echo "  12. /estimate-with-dev       -> dev estimate"
echo "  13. /finalize-prd            -> finalize PRD"
echo "  14. /design-ab-test          -> AB test design"
echo "  15. /create-gate2-presentation -> Solution Research Report (.md + .pptx)"
echo ""
echo "  -- Phase 3: Launch Preparation --"
echo "  16. /support-task            -> support team brief"
echo "  17. /announce-ab-test        -> AB test announcement"
echo "  18. /announce-release        -> release announcement"
echo ""
echo "      /create-tickets          -> push tickets to Jira/Linear/GitHub via MCP (after Solution Research Report)"
