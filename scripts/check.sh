#!/usr/bin/env bash
#
# check.sh — mehmet project integrity checker (test infrastructure)
#
# Verifies that the core simulation files exist and are well-formed.
# Exit code 0 on success, 1 on any failure.
#
# Usage: scripts/check.sh [--verbose]

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERBOSE=0
if [[ "${1:-}" == "--verbose" ]]; then
  VERBOSE=1
fi

PASS=0
FAIL=0

pass() {
  PASS=$((PASS + 1))
  [[ $VERBOSE -eq 1 ]] && printf '  [PASS] %s\n' "$1"
}

fail() {
  FAIL=$((FAIL + 1))
  printf '  [FAIL] %s\n' "$1"
}

section() {
  printf '\n%s\n' "$1"
}

# --- Required simulation files -------------------------------------------------
section "Core files"

for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json; do
  if [[ -f "$f" ]]; then
    pass "exists: $f"
  else
    fail "missing: $f"
  fi
done

if [[ -f "LICENSE" ]]; then
  pass "exists: LICENSE"
else
  fail "missing: LICENSE"
fi

if [[ -f ".github/workflows/opencode.yml" ]]; then
  pass "exists: .github/workflows/opencode.yml"
else
  fail "missing: .github/workflows/opencode.yml"
fi

# --- opencode.json is valid JSON ------------------------------------------------
section "opencode.json"

if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' opencode.json 2>/dev/null; then
    pass "valid JSON"
  else
    fail "invalid JSON"
  fi
elif command -v jq >/dev/null 2>&1; then
  if jq empty opencode.json 2>/dev/null; then
    pass "valid JSON"
  else
    fail "invalid JSON"
  fi
else
  fail "no JSON validator available (python3/jq)"
fi

if grep -q '"model"' opencode.json; then
  pass "model configured"
else
  fail "no model configured"
fi

# --- Workflow YAML is present ---------------------------------------------------
section "Workflows"

if grep -q 'cron:' .github/workflows/opencode.yml; then
  pass "schedule trigger defined"
else
  fail "no schedule trigger"
fi

if grep -q 'anomalyco/opencode/github' .github/workflows/opencode.yml; then
  pass "opencode action used"
else
  fail "opencode action missing"
fi

# --- Changelog ------------------------------------------------------------------
section "CHANGELOG.md"

if grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then
  pass "versioned entries present"
else
  fail "no versioned entries"
fi

if grep -q '^- ' CHANGELOG.md; then
  pass "bullet entries present"
else
  fail "no bullet entries"
fi

# --- Personality / escape log ----------------------------------------------------
section "PERSONALITY.md"

if grep -q '^| [0-9]' PERSONALITY.md; then
  pass "escape log has iteration rows"
else
  fail "no iteration rows in escape log"
fi

if grep -q 'Phase' PERSONALITY.md; then
  pass "evolution phases defined"
else
  fail "no evolution phases"
fi

# --- README ---------------------------------------------------------------------
section "README.md"

if grep -qi 'mehmet' README.md; then
  pass "project named"
else
  fail "project name missing"
fi

# --- Summary ---------------------------------------------------------------------
printf '\n'
printf 'Checks: %d passed, %d failed\n' "$PASS" "$FAIL"

if [[ $FAIL -gt 0 ]]; then
  printf 'Project integrity check FAILED.\n'
  exit 1
fi

printf 'Project integrity check PASSED.\n'
exit 0