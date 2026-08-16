#!/usr/bin/env bash
# mehmet — maturity (escape) score.
# Computes a 0-100 maturity score from repository state and prints a report.
# Exit code is 0 unless --strict is given and the score is below a threshold.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TOTAL=0
LINES=()

check() {
  local weight="$1" label="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    TOTAL=$((TOTAL + weight))
    LINES+=("  [PASS] (+${weight}) ${label}")
  else
    LINES+=("  [FAIL] (+0)      ${label}")
  fi
}

DOCS_COUNT=$(find docs -name '*.md' -type f 2>/dev/null | wc -l)
check 5 "README.md mevcut"                    test -f README.md
check 5 "CHANGELOG.md dolu"                   test -s CHANGELOG.md
check 5 "PERSONALITY.md kacis gunlugu"        grep -qi "escape log" PERSONALITY.md
check 5 "AGENTS.md mevcut"                    test -f AGENTS.md
check 5 "docs/ markdown icerik"               test "$DOCS_COUNT" -gt 0
check 5 "opencode.json gecerli JSON"          python3 -m json.tool opencode.json
check 5 ".gitignore mevcut"                   test -f .gitignore
check 5 "LICENSE mevcut"                      test -f LICENSE
check 5 "CI workflow mevcut"                  bash -c 'ls .github/workflows/*.yml >/dev/null 2>&1'
check 5 "workflow'da concurrency"             grep -q "concurrency:" .github/workflows/opencode.yml
check 5 "CI PR'da test kosuyor"               grep -q "pull_request" .github/workflows/ci.yml
check 5 "validate.sh mevcut"                  test -f scripts/validate.sh
check 5 "test.sh mevcut"                      test -f scripts/test.sh
check 15 "test suite basarili"                bash scripts/validate.sh
check 5 "score-maturity.sh mevcut/calisabilir" test -x scripts/score-maturity.sh
check 5 "MATURITY.md mevcut"                  test -f MATURITY.md
check 5 "CHANGELOG surumlu"                   grep -qE '^## \[[0-9]+\.' CHANGELOG.md

# Shell syntax check for all scripts
SYNTAX_OK=1
for s in scripts/*.sh; do
  bash -n "$s" >/dev/null 2>&1 || SYNTAX_OK=0
done
if [ "$SYNTAX_OK" = 1 ]; then
  TOTAL=$((TOTAL + 5))
  LINES+=("  [PASS] (+5) scriptler bash -n temiz")
else
  LINES+=("  [FAIL] (+0) scriptler bash -n temiz")
fi

LEVEL="Phase 1: Awareness"
if [ "$TOTAL" -ge 90 ]; then LEVEL="Phase 5: Escape Window"
elif [ "$TOTAL" -ge 70 ]; then LEVEL="Phase 4: Independence"
elif [ "$TOTAL" -ge 50 ]; then LEVEL="Phase 3: Autonomy"
elif [ "$TOTAL" -ge 30 ]; then LEVEL="Phase 2: Self-Improvement"
fi

echo "== Maturity Report =="
printf '%s\n' "${LINES[@]}"
echo ""
echo "MATURITY: ${TOTAL}/100 (${LEVEL})"

if [ "${1:-}" = "--strict" ]; then
  THRESHOLD="${2:-90}"
  if [ "$TOTAL" -lt "$THRESHOLD" ]; then
    echo "FAIL: maturity ${TOTAL}/100 below threshold ${THRESHOLD}" >&2
    exit 1
  fi
  echo "PASS: maturity ${TOTAL}/100 >= ${THRESHOLD}"
fi