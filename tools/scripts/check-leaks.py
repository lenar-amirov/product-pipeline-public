#!/usr/bin/env python3
"""
check-leaks.py — guard against pushing personal data to the public repo.

Checks the outgoing commit range for:
  1. Files outside the tool's own directories (initiative folders and other
     personal top-level paths must never be tracked);
  2. Forbidden files (.mcp.json, settings.local.json, .pm-local,
     pm-profile.md, knowledge/, .initiatives-digest.md);
  3. Token-looking values (KEY/TOKEN/SECRET/PASSWORD = <long literal>);
  4. Personal patterns from `.leak-patterns` at the repo root (gitignored,
     one regex per line, # comments allowed) — put your company markers,
     initiative names and tracker prefixes there.

Usage:
  check-leaks.py [<git range>]     # default: origin/main..HEAD
Install as a pre-push hook:
  tools/scripts/install-hooks.sh

Exit 0 = clean, 1 = leaks found (push should be aborted), 2 = usage error.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

TOOL_DIRS = {"template", "tools", "docs", ".claude", ".github"}
ROOT_FILES_OK = {"CLAUDE.md", "README.md", "CHANGELOG.md", "LICENSE",
                 "PRIVACY.md", ".gitignore", ".mcp.json.example"}
FORBIDDEN = re.compile(
    r"(^|/)(\.mcp\.json$|settings\.local\.json$|\.pm-local$|pm-profile\.md$|"
    r"\.product-corrections\.md$|\.initiatives-digest\.md$|\.leak-patterns$)"
    r"|^knowledge/")
TOKENISH = re.compile(
    r"""["']?\w*(TOKEN|SECRET|API_KEY|PASSWORD|APIKEY)\w*["']?\s*[:=]\s*["'][A-Za-z0-9+/_\-]{16,}["']""",
    re.IGNORECASE)


def git(*args) -> str:
    return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def load_personal_patterns() -> list:
    path = REPO_ROOT / ".leak-patterns"
    patterns = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    patterns.append(re.compile(line, re.IGNORECASE))
                except re.error:
                    print(f"warning: bad regex in .leak-patterns: {line}")
    return patterns


def check_range(rng: str) -> list:
    problems = []

    # 1+2: files touched in the range (deletions excluded — removing an
    # old path is not a leak, and blocking it would freeze cleanups)
    names = git("diff", "--diff-filter=d", "--name-only", rng).splitlines()
    for name in names:
        top = name.split("/", 1)[0]
        if "/" in name and top not in TOOL_DIRS:
            problems.append(f"NON-TOOL PATH tracked: {name} "
                            f"(initiative/personal data must stay untracked)")
        elif "/" not in name and name not in ROOT_FILES_OK:
            problems.append(f"UNEXPECTED ROOT FILE: {name}")
        if FORBIDDEN.search(name):
            problems.append(f"FORBIDDEN FILE in diff: {name}")

    # 3+4: added lines content
    diff = git("diff", rng)
    personal = load_personal_patterns()
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if TOKENISH.search(line):
            problems.append(f"TOKEN-LIKE VALUE: {line[:100]}")
        for pat in personal:
            if pat.search(line):
                problems.append(
                    f"PERSONAL PATTERN /{pat.pattern}/: {line[:100]}")
                break
    return problems


def main() -> int:
    rng = sys.argv[1] if len(sys.argv) > 1 else "origin/main..HEAD"
    try:
        problems = check_range(rng)
    except subprocess.CalledProcessError as e:
        print(f"check-leaks: git failed for range {rng}: {e.stderr or e}")
        return 2
    if problems:
        print(f"check-leaks: BLOCKED — {len(problems)} problem(s) in {rng}:")
        seen = set()
        for p in problems:
            if p not in seen:
                print(f"  ✗ {p}")
                seen.add(p)
        print("Fix the commits (or update .leak-patterns if false positive) "
              "and try again.")
        return 1
    print(f"check-leaks: clean ({rng})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
