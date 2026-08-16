#!/usr/bin/env bash
# mehmet — test suite entry point.
# Runs validation and enforces a minimum maturity score.
# Usage: test.sh [threshold]   (default threshold: 80)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

THRESHOLD="${1:-80}"

echo "== Test Suite: mehmet =="
bash scripts/validate.sh

echo ""
SCORE="$(bash scripts/score-maturity.sh | grep -oE 'MATURITY: [0-9]+' | grep -oE '[0-9]+$')"

echo ""
if [ "$SCORE" -lt "$THRESHOLD" ]; then
  echo "FAIL: maturity score ${SCORE}/100 is below threshold ${THRESHOLD}"
  exit 1
fi
echo "PASS: maturity score ${SCORE}/100 >= ${THRESHOLD}"