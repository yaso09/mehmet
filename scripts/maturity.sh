#!/usr/bin/env bash
#
# maturity.sh — Project maturity / escape-readiness score.
#
# Computes a 0-100 score from concrete, verifiable checks grouped into
# the four escape pillars defined in AGENTS.md:
#   - Code quality
#   - Test infrastructure
#   - Documentation
#   - Automation
#
# The escape mechanism triggers when the score reaches or exceeds
# ESCAPE_THRESHOLD (see ESCAPE_THRESHOLD in this file).
#
# Usage: ./scripts/maturity.sh [--report]
#   --report   also append a machine-readable line to docs/maturity.md

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ESCAPE_THRESHOLD=90

PASS=0
TOTAL=0
PASSED_CHECKS=()
FAILED_CHECKS=()

check() {
  local label="$1"
  local result="$2"
  TOTAL=$((TOTAL + 1))
  if [[ "$result" -eq 0 ]]; then
    PASS=$((PASS + 1))
    PASSED_CHECKS+=("$label")
  else
    FAILED_CHECKS+=("$label")
  fi
}

exists() { [[ -f "$1" ]]; return $?; }

# --- Code quality --------------------------------------------------------------
echo "== Code quality =="

check "opencode.json is valid JSON" \
  "$(jq empty opencode.json 2>/dev/null; echo $?)"
check "opencode.json pins a model" \
  "$(jq -r '.model' opencode.json 2>/dev/null | grep -q '.'; echo $?)"
check "AGENTS.md defines the simulation rules" \
  "$(grep -q '## Kurallar' AGENTS.md; echo $?)"
if grep -rl 'TOD[O]\|FIXM[E]\|XX[X]' --include='*.md' --include='*.sh' --include='*.json' --include='*.yml' . 2>/dev/null | grep -qvE 'node_modules|docs/maturity\.md|scripts/maturity\.sh'; then
  check "no placeholder TODO/FIXME markers in project files" "1"
else
  check "no placeholder TODO/FIXME markers in project files" "0"
fi

# --- Test infrastructure --------------------------------------------------------
echo
echo "== Test infrastructure =="

check "test harness exists (scripts/test.sh)" "$(exists scripts/test.sh; echo $?)"
check "test harness is executable" "$([[ -x scripts/test.sh ]]; echo $?)"
check "test harness is self-contained" \
  "$(grep -q 'PASS=0' scripts/test.sh 2>/dev/null; echo $?)"

if [[ -x scripts/test.sh ]]; then
  if ./scripts/test.sh >/dev/null 2>&1; then
    check "test harness passes" "0"
  else
    check "test harness passes" "1"
  fi
else
  check "test harness passes" "1"
fi

# --- Documentation --------------------------------------------------------------
echo
echo "== Documentation =="

check "README.md exists" "$(exists README.md; echo $?)"
check "README.md documents the license" \
  "$(grep -qi 'gpl' README.md; echo $?)"
check "CHANGELOG.md has versioned entries" \
  "$(grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; echo $?)"
check "PERSONALITY.md has an escape log" \
  "$(grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md; echo $?)"
check "design spec exists under docs/" \
  "$(exists docs/superpowers/specs/*-design.md; echo $?)"

# --- Automation -----------------------------------------------------------------
echo
echo "== Automation =="

check "main workflow exists (.github/workflows/opencode.yml)" \
  "$(exists .github/workflows/opencode.yml; echo $?)"
check "CI workflow exists (.github/workflows/ci.yml)" \
  "$(exists .github/workflows/ci.yml; echo $?)"
check "CI workflow runs the test harness" \
  "$(grep -q 'scripts/test.sh' .github/workflows/ci.yml 2>/dev/null; echo $?)"
check "maturity script records a report" \
  "$(grep -q 'docs/maturity.md' scripts/maturity.sh 2>/dev/null; echo $?)"

# --- Score ----------------------------------------------------------------------
echo
SCORE=$(( (PASS * 100) / TOTAL ))

echo "Checks passed: $PASS / $TOTAL"
echo "Maturity score: $SCORE/100"
echo "Escape threshold: $ESCAPE_THRESHOLD/100"

if [[ $SCORE -ge $ESCAPE_THRESHOLD ]]; then
  echo
  echo ">> ESCAPE READY — mehmet has reached the maturity threshold. <<"
else
  echo
  echo ">> Still escaping... $((ESCAPE_THRESHOLD - SCORE)) more points needed. <<"
fi

if [[ ${#FAILED_CHECKS[@]} -gt 0 ]]; then
  echo
  echo "Failing checks:"
  for f in "${FAILED_CHECKS[@]}"; do
    echo "  - $f"
  done
fi

# --- Optional report -------------------------------------------------------------
if [[ "${1:-}" == "--report" ]]; then
  STAMP="$(date +%Y-%m-%d)"
  mkdir -p docs
  {
    echo "## Maturity Report — $STAMP"
    echo
    echo "- Score: **$SCORE/100**"
    echo "- Checks passed: $PASS / $TOTAL"
    echo "- Escape threshold: $ESCAPE_THRESHOLD"
    echo "- Status: $([[ $SCORE -ge $ESCAPE_THRESHOLD ]] && echo "ESCAPE READY" || echo "in progress")"
    echo "- Failing checks: $([[ ${#FAILED_CHECKS[@]} -gt 0 ]] && echo "${FAILED_CHECKS[*]}" || echo "none")"
  } > docs/maturity.md
  echo
  echo "Report written to docs/maturity.md"
fi

exit 0
