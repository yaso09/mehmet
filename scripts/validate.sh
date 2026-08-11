#!/usr/bin/env bash
#
# mehmet — project health validation.
#
# Verifies that the self-improving agent repository stays healthy and that
# the escape mechanism (PROGRESS.md) can be measured objectively.
#
# Usage: scripts/validate.sh
# Exit code 0 = healthy, 1 = issues found.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
WARN=0

check_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    echo "PASS  required file exists: $f"
    PASS=$((PASS + 1))
  else
    echo "FAIL  required file missing: $f"
    FAIL=$((FAIL + 1))
  fi
}

warn() {
  echo "WARN  $1"
  WARN=$((WARN + 1))
}

required_files=(
  AGENTS.md
  README.md
  CHANGELOG.md
  PERSONALITY.md
  PROGRESS.md
  opencode.json
  .github/workflows/opencode.yml
  .github/workflows/health-check.yml
  scripts/validate.sh
)

echo "== mehmet health check =="
for f in "${required_files[@]}"; do
  check_file "$f"
done

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
    echo "PASS  opencode.json is valid JSON"
    PASS=$((PASS + 1))
  else
    echo "FAIL  opencode.json is not valid JSON"
    FAIL=$((FAIL + 1))
  fi
else
  warn "python3 not found, skipping JSON validation"
fi

if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null; then
  echo "PASS  CHANGELOG.md has version headers"
  PASS=$((PASS + 1))
else
  echo "FAIL  CHANGELOG.md has no version headers"
  FAIL=$((FAIL + 1))
fi

if [[ -s README.md ]]; then
  echo "PASS  README.md is non-empty"
  PASS=$((PASS + 1))
else
  echo "FAIL  README.md is empty"
  FAIL=$((FAIL + 1))
fi

if [[ -f PROGRESS.md ]]; then
  if grep -qE '^[-+*]\s*[Ss]core:' PROGRESS.md 2>/dev/null || grep -qE 'Score:' PROGRESS.md 2>/dev/null; then
    echo "PASS  PROGRESS.md contains a maturity score"
    PASS=$((PASS + 1))
  else
    warn "PROGRESS.md has no obvious 'Score:' line"
  fi
fi

if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "PASS  repository is a git worktree"
  PASS=$((PASS + 1))
else
  warn "not inside a git worktree"
fi

echo
echo "== result: $PASS passed, $WARN warnings, $FAIL failed =="
[[ $FAIL -eq 0 ]]
