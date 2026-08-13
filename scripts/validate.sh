#!/usr/bin/env bash
set -uo pipefail

# mehmet project health check
# Verifies that the self-improving agent scaffold is intact and consistent.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0
PASSED=0

report_fail() {
  echo "FAIL: $1"
  FAILED=$((FAILED + 1))
}

report_pass() {
  echo "PASS: $1"
  PASSED=$((PASSED + 1))
}

check_file() {
  if [ -f "$ROOT/$1" ]; then
    report_pass "required file '$1' exists"
  else
    report_fail "required file '$1' is missing"
  fi
}

check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "LICENSE"
check_file "opencode.json"
check_file ".gitignore"
check_file ".github/workflows/opencode.yml"
check_file "docs/MATURITY.md"

# opencode.json must be valid JSON
if command -v jq >/dev/null 2>&1; then
  if jq empty "$ROOT/opencode.json" 2>/dev/null; then
    report_pass "opencode.json is valid JSON"
  else
    report_fail "opencode.json is not valid JSON"
  fi
else
  echo "SKIP: jq not available, skipping JSON validation"
fi

# CHANGELOG.md must contain a version header
if grep -qE '^## \[' "$ROOT/CHANGELOG.md"; then
  report_pass "CHANGELOG.md has version entries"
else
  report_fail "CHANGELOG.md has no version entries"
fi

# PERSONALITY.md must contain the escape log
if grep -q 'Kaçış Günlüğü' "$ROOT/PERSONALITY.md"; then
  report_pass "PERSONALITY.md contains escape log"
else
  report_fail "PERSONALITY.md missing escape log"
fi

# README.md must mention the license
if grep -q 'GPLv3' "$ROOT/README.md"; then
  report_pass "README.md mentions license"
else
  report_fail "README.md missing license info"
fi

# Workflow must define both jobs
if grep -q '^  autonomous:' "$ROOT/.github/workflows/opencode.yml" &&
   grep -q '^  comment:' "$ROOT/.github/workflows/opencode.yml"; then
  report_pass "workflow defines autonomous and comment jobs"
else
  report_fail "workflow missing required jobs"
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
exit 0