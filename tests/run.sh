#!/usr/bin/env bash
# Minimal, dependency-free test suite for the mehmet project.
# Each test asserts a structural/integrity invariant of the repo.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0

report() {
  local status="$1"
  local name="$2"
  if [[ "$status" == "pass" ]]; then
    PASS=$((PASS + 1))
    printf 'ok   - %s\n' "$name"
  else
    FAIL=$((FAIL + 1))
    printf 'FAIL - %s\n' "$name" >&2
  fi
}

assert_file() {
  local name="$1" path="$2"
  if [[ -f "$ROOT/$path" ]]; then report pass "$name"; else report fail "$name"; fi
}

assert_dir() {
  local name="$1" path="$2"
  if [[ -d "$ROOT/$path" ]]; then report pass "$name"; else report fail "$name"; fi
}

assert_json() {
  local name="$1" path="$2"
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$ROOT/$path" 2>/dev/null; then
    report pass "$name"
  else
    report fail "$name"
  fi
}

echo "== core files =="
assert_file "AGENTS.md present" AGENTS.md
assert_file "README.md present" README.md
assert_file "CHANGELOG.md present" CHANGELOG.md
assert_file "PERSONALITY.md present" PERSONALITY.md
assert_file "opencode.json present" opencode.json
assert_file "LICENSE present" LICENSE

echo "== configuration validity =="
assert_json "opencode.json is valid JSON" opencode.json

echo "== workflows =="
assert_file "autonomous workflow present" .github/workflows/opencode.yml
assert_file "CI workflow present" .github/workflows/ci.yml

echo "== structure =="
assert_dir "docs present" docs
assert_dir "scripts present" scripts
assert_file "maturity scorer present" scripts/maturity.py
assert_file "test runner present" tests/run.sh

echo
echo "Summary: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]