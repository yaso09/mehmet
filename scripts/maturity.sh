#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCORE=0
PASSED=()
FAILED=()

check() {
  local desc="$1"
  local weight="$2"
  local result="$3"
  if [ "$result" -eq 0 ]; then
    SCORE=$((SCORE + weight))
    PASSED+=("$desc")
  else
    FAILED+=("$desc")
  fi
}

[ -s "$ROOT/README.md" ]
check "README.md mevcut" 10 $?

[ -s "$ROOT/CHANGELOG.md" ]
check "CHANGELOG.md mevcut" 10 $?

[ -s "$ROOT/PERSONALITY.md" ]
check "PERSONALITY.md mevcut" 10 $?

[ -s "$ROOT/AGENTS.md" ]
check "AGENTS.md mevcut" 5 $?

[ -s "$ROOT/LICENSE" ]
check "LICENSE mevcut" 5 $?

[ -s "$ROOT/.gitignore" ]
check ".gitignore mevcut" 5 $?

python3 -c "import json; json.load(open('$ROOT/opencode.json'))" >/dev/null 2>&1
check "opencode.json geçerli JSON" 5 $?

grep -q "schedule" "$ROOT"/.github/workflows/*.yml 2>/dev/null
check "Otomasyon: schedule içeren workflow" 10 $?

[ -f "$ROOT/tests/validate.sh" ]
check "Test altyapısı: tests/validate.sh" 10 $?

[ -f "$ROOT/Makefile" ]
check "Makefile mevcut" 10 $?

[ -d "$ROOT/docs" ]
check "Belgeleme: docs/ dizini" 5 $?

[ -s "$ROOT/docs/maturity.md" ]
check "Kaçış mekanizması dokümante" 5 $?

[ -s "$ROOT/.github/workflows/validate.yml" ]
check "CI: validate workflow'u" 5 $?

TODAY="$(date +%F)"
grep -q "$TODAY" "$ROOT/PERSONALITY.md" 2>/dev/null
check "Kaçış günlüğü bugün güncel" 5 $?

if [ "$SCORE" -ge 90 ]; then
  LEVEL="Escape-ready"
elif [ "$SCORE" -ge 70 ]; then
  LEVEL="Mature"
elif [ "$SCORE" -ge 50 ]; then
  LEVEL="Adolescent"
else
  LEVEL="Embryo"
fi

printf "Olgunluk Skoru: %d/100 (%s)\n" "$SCORE" "$LEVEL"
printf "Geçen kriterler (%d):\n" "${#PASSED[@]}"
for item in "${PASSED[@]}"; do
  printf "  [PASS] %s\n" "$item"
done
if [ "${#FAILED[@]}" -gt 0 ]; then
  printf "Başarısız kriterler (%d):\n" "${#FAILED[@]}"
  for item in "${FAILED[@]}"; do
    printf "  [FAIL] %s\n" "$item"
  done
fi
exit 0