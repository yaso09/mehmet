#!/usr/bin/env bash
# test_validate.sh - validate.sh ve maturity.py için test suite'i
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 1
cd "$ROOT" || exit 1

PASS=0
FAIL=0

t() {
  local desc="$1"
  local expected="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    if [ "$expected" = "pass" ]; then
      PASS=$((PASS + 1)); printf 'PASS: %s\n' "$desc"
    else
      FAIL=$((FAIL + 1)); printf 'FAIL: %s (beklenen: hata, alınan: başarı)\n' "$desc"
    fi
  else
    if [ "$expected" = "fail" ]; then
      PASS=$((PASS + 1)); printf 'PASS: %s\n' "$desc"
    else
      FAIL=$((FAIL + 1)); printf 'FAIL: %s (beklenen: başarı, alınan: hata)\n' "$desc"
    fi
  fi
}

t "validate.sh temiz repo üzerinde başarılı olmalı" pass bash scripts/validate.sh
t "maturity.py insan okunabilir çalışmalı" pass python3 scripts/maturity.py
t "maturity.py --json geçerli JSON döndürmeli" pass python3 scripts/maturity.py --json
t "maturity.py JSON'u ayrıştırılabilir olmalı" pass python3 -c "
import json, subprocess
out = subprocess.check_output(['python3', 'scripts/maturity.py', '--json'])
data = json.loads(out)
assert 0 <= data['score'] <= 100, data
assert data['threshold'] > 0, data
"

# --json çıktısını validate et
echo ""
echo "Test sonucu: $PASS geçti, $FAIL başarısız"
[ "$FAIL" -eq 0 ] || exit 1
exit 0