#!/usr/bin/env bash
#
# run-tests.sh — runs the project test suite and the maturity score.
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Running integrity tests =="
if bash tests/test_project.sh; then
  echo "Integrity tests: PASS"
else
  echo "Integrity tests: FAIL"
  exit 1
fi

echo
echo "== Maturity / escape readiness =="
bash scripts/maturity.sh

exit 0