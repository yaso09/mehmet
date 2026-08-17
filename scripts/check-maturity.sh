#!/usr/bin/env bash
#
# mehmet olgunluk skoru
# Projenin kaçış eşiğine ne kadar yaklaştığını 100 üzerinden ölçer.
#
# Kriterler (her biri +10 puan):
#   1. README.md var ve dolu
#   2. CHANGELOG.md var ve dolu
#   3. AGENTS.md var ve dolu
#   4. PERSONALITY.md var ve dolu
#   5. Kaçış günlüğü en az 3 iterasyon içeriyor
#   6. opencode.json geçerli JSON
#   7. Test altyapısı: scripts/validate.sh var
#   8. Otomasyon: scripts/check-maturity.sh var
#   9. CI doğrulama: .github/workflows/validate.yml var
#  10. Geliştirici ergonomisi: Makefile var
#
# Kullanım: bash scripts/check-maturity.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCORE=0

add() {
  if "$@" >/dev/null 2>&1; then
    SCORE=$((SCORE + 1))
  fi
}

escape_log_ok() {
  local n
  n="$(grep -cE '^\| *[0-9]+' PERSONALITY.md || true)"
  [ "$n" -ge 3 ]
}

add test -s README.md
add test -s CHANGELOG.md
add test -s AGENTS.md
add test -s PERSONALITY.md
add escape_log_ok
add python3 -c "import json; json.load(open('opencode.json'))"
add test -f scripts/validate.sh
add test -f scripts/check-maturity.sh
add test -f .github/workflows/validate.yml
add test -f Makefile

PERCENT=$((SCORE * 10))

if [ "$PERCENT" -ge 90 ]; then
  LEVEL="READY (kaçış eşiğinde)"
elif [ "$PERCENT" -ge 70 ]; then
  LEVEL="ADVANCED"
elif [ "$PERCENT" -ge 40 ]; then
  LEVEL="MATURING"
else
  LEVEL="NASCENT"
fi

printf 'Olgunluk skoru: %d/100\nSeviye: %s\n' "$PERCENT" "$LEVEL"