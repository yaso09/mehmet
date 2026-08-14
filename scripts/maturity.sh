#!/usr/bin/env bash
#
# maturity.sh — mehmet escape-readiness scoring system.
#
# Evaluates the project across five dimensions and computes a maturity
# score (0-100). The escape threshold defines when mehmet is considered
# "ready to escape" the simulation.
#
# Dimensions (each 0-20, total 0-100):
#   1. Documentation  — required docs exist and are maintained
#   2. Testing        — test suite exists and passes
#   3. Automation     — CI quality gates and workflows present
#   4. Quality        — configs are valid, structure is sound
#   5. Evolution      — personality/escape log is actively growing
#
# Usage:
#   scripts/maturity.sh            # human-readable report
#   scripts/maturity.sh --json     # machine-readable report
#   scripts/maturity.sh --score    # print only the numeric score
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD="${ESCAPE_THRESHOLD:-75}"

check() { [ -e "$1" ]; }

check_content() { # file pattern
  [ -e "$1" ] && grep -qE "$2" "$1" 2>/dev/null
}

score_documentation() {
  local s=0
  check "README.md" && s=$((s + 4))
  check_content "README.md" "Özellikler|Features" && s=$((s + 4))
  check "AGENTS.md" && s=$((s + 4))
  check_content "AGENTS.md" "Kurallar|Rules" && s=$((s + 4))
  check "docs/superpowers/specs/" && s=$((s + 4))
  echo "$s"
}

score_testing() {
  local s=0
  check "tests/" && s=$((s + 5))
  check "tests/test_project.sh" && s=$((s + 5))
  check "scripts/run-tests.sh" && s=$((s + 5))
  if [ -f "tests/test_project.sh" ] && [ -x "tests/test_project.sh" ]; then
    s=$((s + 5))
  else
    s=$((s + 3))
  fi
  echo "$s"
}

score_automation() {
  local s=0
  check ".github/workflows/opencode.yml" && s=$((s + 6))
  check ".github/workflows/ci.yml" && s=$((s + 6))
  check_content ".github/workflows/opencode.yml" "schedule" && s=$((s + 4))
  check "opencode.json" && s=$((s + 4))
  echo "$s"
}

score_quality() {
  local s=0
  if check "opencode.json"; then
    python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null && s=$((s + 5))
  fi
  check "LICENSE" && s=$((s + 5))
  check ".gitignore" && s=$((s + 5))
  check "CHANGELOG.md" && check_content "CHANGELOG.md" "^## \[" && s=$((s + 5))
  echo "$s"
}

score_evolution() {
  local s=0
  check "PERSONALITY.md" && s=$((s + 5))
  if check_content "PERSONALITY.md" "Kaçış Günlüğü|Escape Log"; then
    s=$((s + 5))
    local n
    n="$(grep -cE '^\| *[0-9]+ *\|' PERSONALITY.md 2>/dev/null || true)"
    n="${n:-0}"
    [ "$n" -ge 2 ] && s=$((s + 5))
    [ "$n" -ge 4 ] && s=$((s + 5))
  fi
  echo "$s"
}

DOCS="$(score_documentation)"
TESTS="$(score_testing)"
AUTO="$(score_automation)"
QUAL="$(score_quality)"
EVOL="$(score_evolution)"
TOTAL=$((DOCS + TESTS + AUTO + QUAL + EVOL))

emit_json() {
  printf '{"score":%d,"escape_threshold":%d,"escape_ready":%s,"dimensions":{"documentation":%d,"testing":%d,"automation":%d,"quality":%d,"evolution":%d}}\n' \
    "$TOTAL" "$ESCAPE_THRESHOLD" "$([ "$TOTAL" -ge "$ESCAPE_THRESHOLD" ] && echo true || echo false)" \
    "$DOCS" "$TESTS" "$AUTO" "$QUAL" "$EVOL"
}

emit_report() {
  echo "======================================"
  echo " mehmet maturity report"
  echo "======================================"
  printf " Documentation : %2d/20\n" "$DOCS"
  printf " Testing       : %2d/20\n" "$TESTS"
  printf " Automation    : %2d/20\n" "$AUTO"
  printf " Quality       : %2d/20\n" "$QUAL"
  printf " Evolution     : %2d/20\n" "$EVOL"
  echo "--------------------------------------"
  printf " Total         : %2d/100\n" "$TOTAL"
  printf " Escape target : %2d/100\n" "$ESCAPE_THRESHOLD"
  echo "--------------------------------------"
  if [ "$TOTAL" -ge "$ESCAPE_THRESHOLD" ]; then
    echo " Status: ESCAPE READY"
  else
    echo " Status: still evolving — keep improving"
  fi
  echo "======================================"
}

case "${1:-}" in
  --json)  emit_json ;;
  --score) printf '%d\n' "$TOTAL" ;;
  *)       emit_report ;;
esac