#!/usr/bin/env bash
#
# mehmet — test suite for scripts/verify.sh
#
# Usage: scripts/test.sh
# Exit:  0 if all tests pass, otherwise 1.
#
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERIFY="$ROOT/scripts/verify.sh"
PASS=0
FAIL=0

export MEHMET_SELFCHECK=1

ok() {
  local name="$1"
  PASS=$((PASS + 1))
  printf '  [ok] %s\n' "$name"
}

bad() {
  local name="$1"
  FAIL=$((FAIL + 1))
  printf '  [!!] %s\n' "$name" >&2
}

assert_contains() {
  local name="$1"
  local needle="$2"
  shift 2
  local out
  out="$("$@" 2>&1)"
  if printf '%s' "$out" | grep -qF "$needle"; then
    ok "$name"
  else
    bad "$name (expected: $needle)"
  fi
}

assert_exit() {
  local name="$1"
  local expected="$2"
  shift 2
  "$@" >/dev/null 2>&1
  local code=$?
  if [ "$code" -eq "$expected" ]; then
    ok "$name"
  else
    bad "$name (exit=$code, expected=$expected)"
  fi
}

echo "Running verify.sh tests..."

assert_contains "skor çıktısı mevcut" "maturity-score" bash "$VERIFY"
assert_contains "eşik çıktısı mevcut" "threshold"      bash "$VERIFY"
assert_contains "durum çıktısı mevcut" "status"        bash "$VERIFY"
assert_contains "--report PASS satırı" "[PASS]"         bash "$VERIFY" --report
assert_contains "--report otomasyon başlığı" "Automation" bash "$VERIFY" --report
assert_exit    "--help exit 0" 0                         bash "$VERIFY" --help
assert_exit    "bilinmeyen argüman exit 2" 2             bash "$VERIFY" --bogus

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
if [ "$FAIL" -gt 0 ]; then
  echo "TEST SUITE FAILED"
  exit 1
fi
echo "TEST SUITE PASSED"
exit 0