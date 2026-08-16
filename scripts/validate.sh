#!/usr/bin/env bash
#
# validate.sh - mehmet project health checks.
#
# Runs a set of automated checks against the repository and exits
# non-zero if any of them fail. Designed to be run locally and in CI.
#
# Usage: scripts/validate.sh [--quiet]
#
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUIET=0
if [ "${1:-}" = "--quiet" ]; then
  QUIET=1
fi

FAILURES=0
CHECKS=0

log() {
  if [ "$QUIET" -eq 0 ]; then
    printf '%s\n' "$1"
  fi
}

pass() {
  CHECKS=$((CHECKS + 1))
  log "  [PASS] $1"
}

fail() {
  CHECKS=$((CHECKS + 1))
  FAILURES=$((FAILURES + 1))
  log "  [FAIL] $1"
}

section() {
  log ""
  log "== $1 =="
}

check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    pass "command '$1' is available"
  else
    fail "command '$1' is not available"
  fi
}

cd "$ROOT"

section "Required files"
for f in AGENTS.md CHANGELOG.md LICENSE PERSONALITY.md README.md VERSION opencode.json .github/workflows/opencode.yml; do
  if [ -f "$f" ]; then
    pass "required file '$f' exists"
  else
    fail "required file '$f' is missing"
  fi
done

section "Version consistency"
VERSION="$(cat VERSION 2>/dev/null | tr -d '[:space:]')"
if [ -n "$VERSION" ]; then
  pass "VERSION is set to '$VERSION'"
else
  fail "VERSION file is empty"
fi

if grep -q "^## \[$VERSION\]" CHANGELOG.md 2>/dev/null; then
  pass "CHANGELOG.md has an entry for version $VERSION"
else
  fail "CHANGELOG.md is missing an entry for version $VERSION"
fi

section "JSON validity"
if [ -f opencode.json ]; then
  if jq -e . opencode.json >/dev/null 2>&1; then
    pass "opencode.json is valid JSON"
  else
    fail "opencode.json is not valid JSON"
  fi
fi

section "License consistency"
if grep -q "GPLv3" README.md 2>/dev/null && grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE 2>/dev/null; then
  pass "README.md and LICENSE both reference GPL"
else
  fail "README.md / LICENSE license mismatch"
fi

section "Trailing whitespace"
if ! grep -rn --include="*.md" --include="*.yml" --include="*.json" --include="*.sh" -E '[[:blank:]]+$' . 2>/dev/null | grep -v '^\./\.git/' | grep -q .; then
  pass "no trailing whitespace found"
else
  fail "trailing whitespace found in tracked text files"
fi

section "Markdown relative links"
BROKEN=0
for f in $(grep -rl --include="*.md" -E '\]\(\.?/' . 2>/dev/null | grep -v '^\./\.git/'); do
  while read -r target; do
    if [ -n "$target" ] && [ ! -e "$ROOT/$target" ]; then
      log "  broken link in $f -> $target"
      BROKEN=1
    fi
  done < <(grep -oE '\]\(\.?/[^)#]+' "$f" | sed -E 's/\]\(\.?\///; s/\)$//')
done
if [ "$BROKEN" -eq 0 ]; then
  pass "no broken relative markdown links"
else
  fail "broken relative markdown links found"
fi

section "Workflow sanity"
if grep -q "name: mehmet" .github/workflows/opencode.yml 2>/dev/null; then
  pass "opencode workflow named 'mehmet'"
else
  fail "opencode workflow name missing"
fi

if grep -q "OPENCODE_API_KEY" .github/workflows/opencode.yml 2>/dev/null; then
  pass "OPENCODE_API_KEY secret is wired"
else
  fail "OPENCODE_API_KEY secret not referenced"
fi

log ""
log "Checks: $CHECKS  Failures: $FAILURES"

if [ "$FAILURES" -gt 0 ]; then
  log "RESULT: FAIL"
  exit 1
fi

log "RESULT: PASS"
exit 0