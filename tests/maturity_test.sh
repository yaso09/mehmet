#!/usr/bin/env bash
#
# maturity_test.sh — scripts/maturity.sh için smoke testleri.
#
# Kullanım:
#   bash tests/maturity_test.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MATURITY="$ROOT_DIR/scripts/maturity.sh"

failures=0

check() {
  local name="$1"
  shift
  if "$@"; then
    printf '  [OK]   %s\n' "$name"
  else
    printf '  [HATA] %s\n' "$name"
    failures=$((failures + 1))
  fi
}

echo "== maturity.sh testleri =="

check "dosya çalıştırılabilir" test -x "$MATURITY"
check "syntax geçerli" bash -n "$MATURITY"
check "repo kökünden çalışır ve 'olgunluk' raporlar" bash -c "cd '$ROOT_DIR' && bash '$MATURITY' 2>&1 | grep -q 'olgunluk'"

set +e
out="$("$MATURITY" 2>&1)"
code=$?
set -e
check "çıkış kodu 0 veya 1" bash -c "[[ $code -eq 0 || $code -eq 1 ]]"

if printf '%s' "$out" | grep -qE 'olgunluk: %[0-9]+'; then
  printf '  [OK]   %s\n' "yüzdelik skor raporu üretir"
else
  printf '  [HATA] %s\n' "yüzdelik skor raporu üretir"
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  echo "$failures test başarısız."
  exit 1
fi

echo "Tüm maturity testleri başarılı."