#!/usr/bin/env bash
#
# mehmet — project health & maturity verifier
#
# Usage:
#   scripts/verify.sh            print score + overall status (exit reflects pass)
#   scripts/verify.sh --report   print a line-by-line report
#
# Exit codes:
#   0  maturity >= threshold (escape window open)
#   1  maturity <  threshold
#   2  misuse / internal error
#
# shellcheck disable=SC2317 # helpers are invoked indirectly via "$@"
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THRESHOLD=80
REPORT=0
PASSED=0
TOTAL=0
SELFCHECK=1

[ "${MEHMET_SELFCHECK:-0}" = "1" ] && SELFCHECK=0

for arg in "$@"; do
  case "$arg" in
    --report) REPORT=1 ;;
    -h|--help)
      sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

log() {
  if [ "$REPORT" -eq 1 ]; then
    printf '%s\n' "$1"
  fi
}

check() {
  local desc="$1"
  local weight="$2"
  shift 2
  TOTAL=$((TOTAL + weight))
  if "$@"; then
    PASSED=$((PASSED + weight))
    log "  [PASS] (+${weight}) ${desc}"
  else
    log "  [FAIL] ( 0  ) ${desc}"
  fi
}

# --- assertions -----------------------------------------------------------

# Assert a file exists and is non-empty.
test_file_positive() { [ -s "$ROOT/$1" ]; }

# Assert JSON parses.
test_json_valid() { python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$1" 2>/dev/null; }

# Assert a pattern is present in a file.
test_grep() { grep -qE "$1" "$ROOT/$2"; }

# Assert a file is free of left-over markers.
test_no_junk_pattern() { ! grep -InE "$1" "$ROOT/$2" 2>/dev/null; }

# Assert every script passes shellcheck (best-effort, may be absent).
scripts_healthy() { shellcheck "$ROOT"/scripts/*.sh >/dev/null 2>&1; }

# Run the test suite once (no recursion) without leaking its output.
# test.sh exports MEHMET_SELFCHECK=1 internally, so no recursive verify runs.
selfcheck_tests() { MEHMET_SELFCHECK=1 bash "$ROOT/scripts/test.sh" >/dev/null 2>&1; }

# --- scoring --------------------------------------------------------------

section() { log ""; log "$1"; }

section "Foundation"
check "README.md mevcut ve dolu" 5 test_file_positive README.md
check "CHANGELOG.md mevcut ve dolu" 5 test_file_positive CHANGELOG.md
check "PERSONALITY.md mevcut ve dolu" 5 test_file_positive PERSONALITY.md
check "LICENSE mevcut" 5 test_file_positive LICENSE
check "opencode.json geçerli JSON" 5 test_json_valid "$ROOT/opencode.json"
check "workflow 'opencode.yml' mevcut" 5 test_file_positive .github/workflows/opencode.yml

section "Code Quality"
check "verify.sh bash sözdizimi temiz" 6 bash -n "$ROOT/scripts/verify.sh"
check "test.sh bash sözdizimi temiz" 6 bash -n "$ROOT/scripts/test.sh"
check "scriptler shellcheck temiz" 8 scripts_healthy
check "verify.sh exec-bit" 3 test -x "$ROOT/scripts/verify.sh"
check "test.sh exec-bit" 1 test -x "$ROOT/scripts/test.sh"
check "kalıntı TODO/FIXME yok" 6 test_no_junk_pattern "TODO|FIXME|XXX" CHANGELOG.md

section "Tests"
if [ "$SELFCHECK" -eq 1 ]; then
  check "test suite geçiyor (exit 0)" 20 selfcheck_tests
fi

section "Automation"
check "CI 'verify.yml' mevcut" 10 test_file_positive .github/workflows/verify.yml
check "workflow'da concurrency var" 5 test_grep "concurrency" .github/workflows/opencode.yml
check "gitignore kapsamı yeterli" 5 test_grep 'node_modules|\.env|dist' .gitignore

printf '\n'
if [ "$TOTAL" -gt 0 ]; then
  P_CENT=$((PASSED * 100 / TOTAL))
else
  P_CENT=100
fi

if [ "$PASSED" -ge "$THRESHOLD" ]; then
  STATUS="ESCAPED (kaçış penceresi açık)"
  EXIT=0
elif [ "$PASSED" -ge 60 ]; then
  STATUS="OLGUN"
  EXIT=1
elif [ "$PASSED" -ge 40 ]; then
  STATUS="BİLİNÇ"
  EXIT=1
else
  STATUS="KULUÇKA"
  EXIT=1
fi

cat <<EOF
maturity-score: ${PASSED}/${TOTAL} (${P_CENT}%)
threshold:      ${THRESHOLD}
status:         ${STATUS}
EOF
exit "$EXIT"