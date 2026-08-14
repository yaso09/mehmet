#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

note() { echo "$*"; }

assert_eq() {
  local desc="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    PASS=$((PASS + 1)); note "PASS  $desc"
  else
    FAIL=$((FAIL + 1)); note "FAIL  $desc (expected '$expected', got '$actual')"
  fi
}

assert_exit() {
  local desc="$1" expected="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then actual=0; else actual=1; fi
  if [[ "$expected" == "$actual" ]]; then
    PASS=$((PASS + 1)); note "PASS  $desc"
  else
    FAIL=$((FAIL + 1)); note "FAIL  $desc (expected exit $expected, got $actual)"
  fi
}

make_complete_fixture() {
  local dir
  dir=$(mktemp -d)
  mkdir -p "$dir/docs" "$dir/tests" "$dir/.github/workflows"
  cat > "$dir/CHANGELOG.md" <<'EOF'
# Changelog

## [0.1.0] - 2026-07-04

### Added
- first

## [0.2.0] - 2026-07-04

### Added
- second

## [0.3.0] - 2026-08-14

### Added
- third
EOF
  cat > "$dir/README.md" <<'EOF'
# readme

Bu proje escape/kaçış mekanizması içerir.
EOF
  cat > "$dir/PERSONALITY.md" <<'EOF'
# Personality

## Kaçış Günlüğü

| Iterasyon | Tarih       | İlerleme |
|-----------|-------------|----------|
| 1         | 2026-07-04 | first    |
| 2         | 2026-07-04 | second   |
| 3         | 2026-08-14 | third    |
EOF
  echo "# design" > "$dir/docs/design.md"
  echo "echo ok" > "$dir/tests/sample.sh"
  cat > "$dir/.github/workflows/ci.yml" <<'EOF'
name: ci
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
EOF
  echo "all:" > "$dir/Makefile"
  echo "{}" > "$dir/opencode.json"
  echo "$dir"
}

make_empty_fixture() {
  mktemp -d
}

# --- bash syntax of the scripts ---
assert_exit "check-health.sh has valid bash syntax" 0 bash -n scripts/check-health.sh
assert_exit "run-tests.sh has valid bash syntax" 0 bash -n scripts/run-tests.sh

# --- complete fixture passes the escape gate ---
f_complete=$(make_complete_fixture)
out=$(bash scripts/check-health.sh --root "$f_complete")
assert_eq "complete fixture reports 95/100 (git tags skipped in root mode)" "MATURITY SCORE: 95/100" "$(printf '%s\n' "$out" | grep 'MATURITY SCORE' || true)"
assert_exit "complete fixture passes --gate" 0 bash scripts/check-health.sh --root "$f_complete" --gate
rm -rf "$f_complete"

# --- empty fixture fails the escape gate ---
f_empty=$(make_empty_fixture)
out=$(bash scripts/check-health.sh --root "$f_empty")
assert_eq "empty fixture reports 0/100" "MATURITY SCORE: 0/100" "$(printf '%s\n' "$out" | grep 'MATURITY SCORE' || true)"
assert_exit "empty fixture fails --gate" 1 bash scripts/check-health.sh --root "$f_empty" --gate
rm -rf "$f_empty"

# --- custom threshold works ---
f_empty=$(make_empty_fixture)
assert_exit "custom threshold=0 passes for empty fixture" 0 bash scripts/check-health.sh --root "$f_empty" --threshold 0
rm -rf "$f_empty"

echo "--------------------------------------------------"
echo "Tests: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]