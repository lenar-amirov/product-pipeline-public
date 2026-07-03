#!/bin/bash
# Installs the pre-push leak guard into .git/hooks.
# Usage: tools/scripts/install-hooks.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOK="$REPO_ROOT/.git/hooks/pre-push"

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "Error: $REPO_ROOT is not a git repository"
  exit 1
fi

cat > "$HOOK" << 'EOF'
#!/bin/bash
# pre-push leak guard (installed by tools/scripts/install-hooks.sh)
# Checks every outgoing range with tools/scripts/check-leaks.py.
while read -r local_ref local_sha remote_ref remote_sha; do
  # skip branch deletions
  if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
    continue
  fi
  if [ "$remote_sha" = "0000000000000000000000000000000000000000" ]; then
    range="origin/main..$local_sha"   # new branch: compare against main
  else
    range="$remote_sha..$local_sha"
  fi
  python3 "$(git rev-parse --show-toplevel)/tools/scripts/check-leaks.py" "$range" || exit 1
done
exit 0
EOF
chmod +x "$HOOK"

echo "pre-push leak guard installed → $HOOK"
echo "Personal markers: put regexes (one per line) into .leak-patterns at the repo root (gitignored)."
