#!/usr/bin/env bash
set -euo pipefail

# mehmet — maturity checker tests
# check-maturity.sh betiğinin davranışını doğrular.
# Çalıştırma: make test  (veya: scripts/test-maturity.sh)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCRIPT="scripts/check-maturity.sh"
FAILURES=0
COUNT=0

t() {
  local desc="$1" expected="$2"
  shift 2
  COUNT=$((COUNT + 1))
  local rc=0
  "$@" >/dev/null 2>&1 || rc=$?
  if [ "$rc" -eq "$expected" ]; then
    printf "  [PASS] %s\n" "$desc"
  else
    printf "  [FAIL] %s (rc=%d, beklenen=%s)\n" "$desc" "$rc" "$expected"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "mehmet — betik testleri"
echo "========================"

t "check-maturity.sh mevcut"                    0 test -f "$SCRIPT"
t "check-maturity.sh çalıştırılabilir"          0 test -x "$SCRIPT"
t "check-maturity.sh bash -n geçer"             0 bash -n "$SCRIPT"
t "test betiği bash -n geçer"                   0 bash -n "$0"
t "--json çalışıyor"                            0 "$SCRIPT" --json

JSON_OUT="$("$SCRIPT" --json 2>/dev/null || true)"
t "JSON skor formatı geçerli"                   0 sh -c 'case "$1" in *"\"score\":"*"\"max\":40"*) exit 0;; *) exit 1;; esac' _ "$JSON_OUT"

PERCENT="$(printf '%s' "$JSON_OUT" | sed -n 's/.*"percent":\([0-9]*\).*/\1/p')"
THRESHOLD_ABOVE=$((PERCENT + 1))
t "THRESHOLD=0 ile başarılı"                    0 env THRESHOLD=0 "$SCRIPT"
t "THRESHOLD=percent+1 ile başarısız"           1 env THRESHOLD="$THRESHOLD_ABOVE" "$SCRIPT"

echo ""
echo "========================"
if [ "$FAILURES" -eq 0 ]; then
  printf "Tüm testler geçti (%d kontrol).\n" "$COUNT"
else
  printf "HATA: %d/%d test başarısız.\n" "$FAILURES" "$COUNT"
  exit 1
fi