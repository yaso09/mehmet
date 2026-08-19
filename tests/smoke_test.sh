#!/usr/bin/env bash
# mehmet — smoke tests for the tooling.
# Verifies that verify.sh and maturity.sh run cleanly and produce sane output.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0

assert_contains() { # assert_contains <haystack> <needle> <description>
  case "$1" in
    *"$2"*) printf '  ok   %s\n' "$3" ;;
    *)      printf '  FAIL %s\n' "$3"; FAILED=1 ;;
  esac
}

echo "== mehmet smoke tests =="

# --- verify.sh passes on a healthy repo ---
if bash scripts/verify.sh >/dev/null 2>&1; then
  printf '  ok   verify.sh exits 0 on healthy repo\n'
else
  printf '  FAIL verify.sh should exit 0 on healthy repo\n'; FAILED=1
fi

# --- maturity.sh outputs score and readiness ---
MATURITY_OUTPUT="$(bash scripts/maturity.sh)"
assert_contains "$MATURITY_OUTPUT" "MATURITY_SCORE=" "maturity.sh prints MATURITY_SCORE"
assert_contains "$MATURITY_OUTPUT" "ESCAPE_READINESS=" "maturity.sh prints ESCAPE_READINESS"

SCORE="$(printf '%s\n' "$MATURITY_OUTPUT" | sed -n 's/.*MATURITY_SCORE=\([0-9]*\)\/.*/\1/p')"
READINESS="$(printf '%s\n' "$MATURITY_OUTPUT" | sed -n 's/.*ESCAPE_READINESS=\([0-9]*\)%.*/\1/p')"

if [ -n "$SCORE" ] && [ "$SCORE" -gt 0 ] 2>/dev/null; then
  printf '  ok   maturity score is positive (score=%s)\n' "$SCORE"
else
  printf '  FAIL maturity score should be positive (score=%s)\n' "$SCORE"; FAILED=1
fi

if [ -n "$READINESS" ] && [ "$READINESS" -ge 0 ] 2>/dev/null && [ "$READINESS" -le 100 ] 2>/dev/null; then
  printf '  ok   escape readiness within 0-100 (readiness=%s%%)\n' "$READINESS"
else
  printf '  FAIL escape readiness out of range (readiness=%s)\n' "$READINESS"; FAILED=1
fi

echo
if [ "$FAILED" -eq 0 ]; then
  echo "All smoke tests passed."
else
  echo "Some smoke tests FAILED."
  exit 1
fi
