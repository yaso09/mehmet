#!/usr/bin/env bash
set -euo pipefail

# maturity_test.sh — scripts/maturity.sh için testler

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

assert() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf '  ok: %s\n' "$desc"
  else
    printf '  HATA: %s\n' "$desc"
    failures=$((failures + 1))
  fi
}

# Bu test dosyasından çağrıldığında maturity.sh test koşucusunu yeniden
# çalıştırmasın (sonsuz özyinelemeyi önlemek için).
export MEHMET_NO_TESTS=1

assert "maturity.sh tablo modunda çalışıyor" scripts/maturity.sh
assert "maturity.sh --score çalışıyor" scripts/maturity.sh --score

# --score çıktısı 0-100 arası bir tam sayı olmalı
score="$(scripts/maturity.sh --score 2>/dev/null)"
if [[ "$score" =~ ^[0-9]+$ ]] && (( score >= 0 && score <= 100 )); then
  printf '  ok: skor geçerli aralıkta (%s)\n' "$score"
else
  printf '  HATA: skor geçersiz (%s)\n' "$score"
  failures=$((failures + 1))
fi

# Betikler çalıştırılabilir olmalı
assert "check-project.sh çalıştırılabilir" test -x scripts/check-project.sh
assert "maturity.sh çalıştırılabilir" test -x scripts/maturity.sh

# Betikler sözdizimi açısından geçerli olmalı
assert "check-project.sh sözdizimi geçerli" bash -n scripts/check-project.sh
assert "maturity.sh sözdizimi geçerli" bash -n scripts/maturity.sh

if (( failures > 0 )); then
  printf 'maturity_test.sh: %d hata\n' "$failures"
  exit 1
fi

printf 'maturity_test.sh: tüm testler geçti\n'
exit 0