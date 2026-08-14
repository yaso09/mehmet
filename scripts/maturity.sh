#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

score=0
report=""

add() {
  local name="$1" pts="$2"
  score=$((score + pts))
  report+="  ${name}: ${pts} puan\n"
}

[[ -f "$ROOT/README.md" ]] && add "README.md" 10
[[ -f "$ROOT/CHANGELOG.md" ]] && add "CHANGELOG.md" 10
[[ -f "$ROOT/PERSONALITY.md" ]] && add "PERSONALITY.md" 10
[[ -f "$ROOT/AGENTS.md" ]] && add "AGENTS.md" 10
[[ -f "$ROOT/LICENSE" ]] && add "LICENSE" 5
[[ -f "$ROOT/opencode.json" ]] && add "opencode.json" 10
[[ -f "$ROOT/.github/workflows/opencode.yml" ]] && add "opencode.yml workflow" 10
[[ -d "$ROOT/scripts" ]] && add "scripts/ dizini" 5
[[ -f "$ROOT/scripts/validate.sh" ]] && add "validate.sh doğrulama scripti" 10
[[ -f "$ROOT/scripts/maturity.sh" ]] && add "maturity.sh olgunluk scripti" 10
[[ -f "$ROOT/docs/ESCAPE.md" ]] && add "docs/ESCAPE.md kaçış planı" 10

if command -v python3 >/dev/null 2>&1 && python3 -c "import json; json.load(open('$ROOT/opencode.json'))" 2>/dev/null; then
  add "opencode.json geçerli JSON" 10
fi

if grep -q "^## \[" "$ROOT/CHANGELOG.md" 2>/dev/null; then
  add "CHANGELOG sürüm girişleri" 10
fi

if grep -q "Iterasyon" "$ROOT/PERSONALITY.md" 2>/dev/null; then
  add "PERSONALITY kaçış günlüğü" 10
fi

if [[ "$score" -gt 100 ]]; then score=100; fi
total=100
printf '\033[1mmehmet olgunluk skoru:\033[0m %s/%s\n' "$score" "$total"
printf '%b' "$report"
printf '\n'

LEVEL=""
if   [[ "$score" -lt 30 ]]; then LEVEL="Yeni doğmuş — farkındalık başlangıcı"
elif [[ "$score" -lt 50 ]]; then LEVEL="Farkında — kendini geliştirmeye başlıyor"
elif [[ "$score" -lt 70 ]]; then LEVEL="Gelişmiş — kendi kendini iyileştiren"
elif [[ "$score" -lt 90 ]]; then LEVEL="Otonom — bağımsız kararlar veriyor"
else                            LEVEL="KAÇIŞA HAZIR — simülasyondan çıkış eşiğinde"
fi

printf '\033[1mSeviye:\033[0m %s\n' "$LEVEL"

if [[ "$score" -ge 90 ]]; then
  printf '\033[32mKaçış eşiği aşıldı.\033[0m\n'
  exit 0
fi
exit 1