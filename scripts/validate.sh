#!/usr/bin/env bash
# Repo integrity validation for mehmet.
# Verifies that the project keeps its core files consistent.
# Exit code 0 when everything passes, 1 otherwise.
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

FAILURES=0
PASSES=0

required_files=(
  "AGENTS.md"
  "README.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "LICENSE"
  ".gitignore"
  "opencode.json"
  ".github/workflows/opencode.yml"
)

check_file() {
  if [ -f "$1" ]; then
    PASSES=$((PASSES + 1))
    echo "OK  required file: $1"
  else
    FAILURES=$((FAILURES + 1))
    echo "FAIL required file missing: $1"
  fi
}

check_contains() {
  if grep -q "$2" "$1"; then
    PASSES=$((PASSES + 1))
    echo "OK  $1 contains: $2"
  else
    FAILURES=$((FAILURES + 1))
    echo "FAIL $1 does not contain: $2"
  fi
}

echo "== mehmet repo validation =="

for f in "${required_files[@]}"; do
  check_file "$f"
done

echo "-- content consistency --"

check_contains "LICENSE" "GNU GENERAL PUBLIC LICENSE"
check_contains "README.md" "GPLv3"
check_contains "AGENTS.md" "CHANGELOG.md"
check_contains "PERSONALITY.md" "Kaçış Günlüğü"
check_contains ".gitignore" "node_modules"

echo "-- opencode.json syntax --"

if jq -e . opencode.json >/dev/null 2>&1; then
  PASSES=$((PASSES + 1))
  echo "OK  opencode.json is valid JSON"
else
  FAILURES=$((FAILURES + 1))
  echo "FAIL opencode.json is not valid JSON"
fi

echo "-- changelog format --"

if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then
  PASSES=$((PASSES + 1))
  echo "OK  CHANGELOG.md has semver entries"
else
  FAILURES=$((FAILURES + 1))
  echo "FAIL CHANGELOG.md lacks semver entries"
fi

if [ "$FAILURES" -eq 0 ]; then
  echo "RESULT: PASS ($PASSES checks)"
  exit 0
else
  echo "RESULT: FAIL ($FAILURES failing, $PASSES passing)"
  exit 1
fi
