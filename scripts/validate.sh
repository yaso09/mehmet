#!/usr/bin/env bash
#
# validate.sh — Project health checks.
#
# Verifies that the repository stays structurally sound as mehmet evolves:
#   - JSON files parse correctly
#   - YAML files parse correctly
#   - CHANGELOG.md uses the expected format
#   - Required documentation files exist with expected sections
#
# Exit code 0 means everything passed.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check() {
  local description="$1"
  local result="$2"
  if [ "$result" -eq 0 ]; then
    echo "PASS: $description"
  else
    echo "FAIL: $description"
    failures=$((failures + 1))
  fi
}

echo "== JSON validation =="
for file in $(git ls-files '*.json' '*.jsonc'); do
  if node -e "require('fs'); JSON.parse(require('fs').readFileSync('$file', 'utf8'));" 2>/dev/null; then
    check "$file is valid JSON" 0
  else
    check "$file is valid JSON" 1
  fi
done

echo "== YAML validation =="
for file in $(git ls-files '*.yml' '*.yaml'); do
  if python3 -c "import yaml,sys; yaml.safe_load(open('$file'))" 2>/dev/null; then
    check "$file is valid YAML" 0
  else
    check "$file is valid YAML" 1
  fi
done

echo "== Shell script validation =="
for file in $(git ls-files 'scripts/*.sh'); do
  if bash -n "$file" 2>/dev/null; then
    check "$file syntax" 0
  else
    check "$file syntax" 1
  fi
done

echo "== CHANGELOG format =="
if [ -f CHANGELOG.md ]; then
  # Every version section must be a level-2 header matching [x.y.z] - YYYY-MM-DD
  bad_headers="$(grep -nE '^## ' CHANGELOG.md | grep -vE '^[0-9]+:## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$' || true)"
  if [ -z "$bad_headers" ]; then
    check "CHANGELOG.md version headers" 0
  else
    echo "$bad_headers"
    check "CHANGELOG.md version headers" 1
  fi
else
  check "CHANGELOG.md exists" 1
fi

echo "== Required docs =="
for file in README.md CHANGELOG.md PERSONALITY.md AGENTS.md MATURITY.md; do
  if [ -f "$file" ]; then
    check "$file exists" 0
  else
    check "$file exists" 1
  fi
done

echo
if [ "$failures" -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "$failures check(s) failed."
  exit 1
fi
