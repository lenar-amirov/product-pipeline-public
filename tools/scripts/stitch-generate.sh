#!/bin/bash
# stitch-generate.sh — wrapper for Stitch CLI tools
# Usage:
#   stitch-generate.sh create-project "Project Title"
#   stitch-generate.sh generate <projectId> "<prompt>" [MOBILE|DESKTOP]
#   stitch-generate.sh get-image <projectId> <screenId> <output.png>
#   stitch-generate.sh get-html <projectId> <screenId> <output.html>
#   stitch-generate.sh edit <projectId> <screenId> "<prompt>"
#   stitch-generate.sh list-screens <projectId>

set -euo pipefail

export STITCH_API_KEY="${STITCH_API_KEY:-AQ.Ab8RN6IpxqG82DMPPv2VXVsIVUdjsWCfohbc8Db82q9mA3qecQ}"

CMD="${1:-help}"
shift || true

case "$CMD" in
  create-project)
    TITLE="${1:-New Project}"
    RESULT=$(stitch-mcp tool create_project -d "{\"title\":\"$TITLE\"}" 2>/dev/null)
    PROJECT_ID=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['name'].split('/')[-1])")
    echo "$PROJECT_ID"
    ;;

  generate)
    PROJECT_ID="$1"
    PROMPT="$2"
    DEVICE="${3:-MOBILE}"
    # Build JSON safely with Python
    JSON_DATA=$(python3 -c "import json,sys; print(json.dumps({'projectId':'$PROJECT_ID','prompt':sys.argv[1],'deviceType':'$DEVICE'}))" "$PROMPT")
    RESULT=$(stitch-mcp tool generate_screen_from_text -d "$JSON_DATA" 2>/dev/null)
    # Extract screen ID from response
    SCREEN_ID=$(echo "$RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
comps = data.get('outputComponents', [])
for c in comps:
    if 'design' in c:
        screens = c['design'].get('screens', [])
        if screens:
            print(screens[0]['id'])
            sys.exit(0)
print('NO_SCREEN')
" 2>/dev/null)
    echo "$SCREEN_ID"
    ;;

  get-image)
    PROJECT_ID="$1"
    SCREEN_ID="$2"
    OUTPUT="$3"
    TMPJSON=$(mktemp /tmp/stitch-img-XXXXX.json)
    stitch-mcp tool get_screen_image -d "{\"projectId\":\"$PROJECT_ID\",\"screenId\":\"$SCREEN_ID\"}" 2>/dev/null > "$TMPJSON"
    python3 -c "
import json, sys, base64
with open('$TMPJSON') as f:
    d = json.load(f)
with open('$OUTPUT', 'wb') as out:
    out.write(base64.b64decode(d['imageContent']))
print(f'Saved: $OUTPUT')
"
    rm -f "$TMPJSON"
    ;;

  get-html)
    PROJECT_ID="$1"
    SCREEN_ID="$2"
    OUTPUT="$3"
    TMPJSON=$(mktemp /tmp/stitch-html-XXXXX.json)
    stitch-mcp tool get_screen_code -d "{\"projectId\":\"$PROJECT_ID\",\"screenId\":\"$SCREEN_ID\"}" 2>/dev/null > "$TMPJSON"
    python3 -c "
import json
with open('$TMPJSON') as f:
    d = json.load(f)
with open('$OUTPUT', 'w') as out:
    out.write(d.get('codeContent', ''))
print(f'Saved: $OUTPUT')
"
    rm -f "$TMPJSON"
    ;;

  edit)
    PROJECT_ID="$1"
    SCREEN_ID="$2"
    PROMPT="$3"
    JSON_DATA=$(python3 -c "import json,sys; print(json.dumps({'projectId':'$PROJECT_ID','selectedScreenIds':['$SCREEN_ID'],'prompt':sys.argv[1]}))" "$PROMPT")
    RESULT=$(stitch-mcp tool edit_screens -d "$JSON_DATA" 2>/dev/null)
    NEW_SCREEN_ID=$(echo "$RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
comps = data.get('outputComponents', [])
for c in comps:
    if 'design' in c:
        screens = c['design'].get('screens', [])
        if screens:
            print(screens[0]['id'])
            sys.exit(0)
print('NO_SCREEN')
" 2>/dev/null)
    echo "$NEW_SCREEN_ID"
    ;;

  list-screens)
    PROJECT_ID="$1"
    stitch-mcp tool get_project -d "{\"name\":\"projects/$PROJECT_ID\"}" 2>/dev/null | \
      python3 -c "
import json, sys
data = json.load(sys.stdin)
for s in data.get('screenInstances', []):
    sid = s.get('sourceScreen','').split('/')[-1] if s.get('sourceScreen') else s.get('screenInstanceId','?')
    label = s.get('label', 'no-label')
    print(f'{sid} {label}')
"
    ;;

  help|*)
    echo "Usage: stitch-generate.sh <command> [args...]"
    echo "Commands: create-project, generate, get-image, get-html, edit, list-screens"
    ;;
esac
