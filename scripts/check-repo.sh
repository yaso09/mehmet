#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0
CHECKS=0

fail() {
  printf 'FAIL  %s\n' "$1"
  FAILURES=$((FAILURES + 1))
}

pass() {
  printf 'ok    %s\n' "$1"
  CHECKS=$((CHECKS + 1))
}

cd "$ROOT"

for file in AGENTS.md README.md CHANGELOG.md PERSONALITY.md opencode.json LICENSE .gitignore .github/workflows/opencode.yml; do
  if [[ -f "$file" ]]; then
    pass "required file exists: $file"
  else
    fail "required file missing: $file"
  fi
done

if [[ -s README.md ]]; then
  pass "README.md is non-empty"
else
  fail "README.md is empty"
fi

if [[ -s CHANGELOG.md ]] && grep -q '^## \[' CHANGELOG.md; then
  pass "CHANGELOG.md has at least one release entry"
else
  fail "CHANGELOG.md has no release entries"
fi

if grep -q 'GNU GENERAL PUBLIC LICENSE' LICENSE; then
  pass "LICENSE is GPLv3"
else
  fail "LICENSE is not GPLv3"
fi

if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
  pass "opencode.json is valid JSON"
else
  fail "opencode.json is not valid JSON"
fi

if grep -q '^## Kaçış Günlüğü' PERSONALITY.md || grep -q '^## Escape Log' PERSONALITY.md; then
  pass "PERSONALITY.md has escape log"
else
  fail "PERSONALITY.md missing escape log"
fi

if [[ -d docs/superpowers/plans ]] && [[ -d docs/superpowers/specs ]]; then
  pass "docs/superpowers structure present"
else
  fail "docs/superpowers structure missing"
fi

if find . -path ./.git -prune -o -name '*.md' -print | xargs grep -l $'[ \t]$' >/dev/null 2>&1; then
  fail "markdown files contain trailing whitespace"
else
  pass "markdown files have no trailing whitespace"
fi

printf -- '----\n%s/%s checks passed\n' "$CHECKS" "$((CHECKS + FAILURES))"
if ((FAILURES > 0)); then
  exit 1
fi