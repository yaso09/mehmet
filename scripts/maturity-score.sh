#!/usr/bin/env bash
#
# Kaçış / olgunluk skoru hesaplayıcısı.
# docs/ESCAPE.md içindeki rubriğe göre 0-100 arası puan üretir.
#
# Kullanım: bash scripts/maturity-score.sh
# Çıktı: kategori dökümü + toplam puan. Rapor amaçlıdır, daima 0 ile çıkar.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

score=0
total=0

add() {
  local name="$1" max="$2" got="$3"
  total=$((total + max))
  score=$((score + got))
  printf '%-22s %2d/%2d\n' "$name" "$got" "$max"
}

# --- Dokümantasyon (25) ---
d=0
[[ -f README.md ]] && grep -q '^## Özellikler' README.md && d=$((d + 5))
[[ -f README.md ]] && grep -q '^## Geliştirme' README.md && d=$((d + 5))
[[ -f CHANGELOG.md ]] && grep -q "$(date +%Y)" CHANGELOG.md && d=$((d + 5))
[[ -f PERSONALITY.md ]] && grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md && d=$((d + 5))
[[ -f docs/ESCAPE.md ]] && d=$((d + 5))
add "dokümantasyon" 25 "$d"

# --- Test & Kalite (30) ---
q=0
if [[ -f scripts/validate.sh ]]; then
  q=$((q + 5))
  if bash scripts/validate.sh >/dev/null 2>&1; then
    q=$((q + 10))
  fi
fi
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  q=$((q + 5))
fi
unknown="$(python3 - "$ROOT" <<'PY'
import json, sys
allowed = set("""$schema shell logLevel server command skills references reference watcher snapshot
plugin share autoshare autoupdate disabled_providers enabled_providers model small_model
default_agent subagent_depth username mode agent provider mcp formatter lsp instructions
layout permission tools attachment enterprise tool_output compaction experimental""".split())
with open(f"{sys.argv[1]}/opencode.json") as f:
    data = json.load(f)
print(" ".join(sorted(set(data) - allowed)))
PY
)"
[[ -z "$unknown" ]] && q=$((q + 5))
[[ -f scripts/maturity-score.sh ]] && q=$((q + 5))
add "test & kalite" 30 "$q"

# --- Otomasyon (25) ---
a=0
[[ -f .github/workflows/opencode.yml ]] && grep -q 'schedule' .github/workflows/opencode.yml && a=$((a + 10))
[[ -f .github/workflows/opencode.yml ]] && grep -q 'validate' .github/workflows/opencode.yml && a=$((a + 10))
[[ -f .github/workflows/opencode.yml ]] && grep -q 'concurrency' .github/workflows/opencode.yml && a=$((a + 5))
add "otomasyon" 25 "$a"

# --- Kaçış Mekanizması (20) ---
e=0
[[ -f docs/ESCAPE.md ]] && e=$((e + 10))
[[ -f scripts/maturity-score.sh ]] && e=$((e + 10))
add "kaçış mekanizması" 20 "$e"

echo "---------------------------"
printf 'TOPLAM: %d/%d\n' "$score" "$total"

THRESHOLD=75
if [[ $score -ge $THRESHOLD ]]; then
  echo "ESCAPE READY: olgunluk eşiğine ulaşıldı ($score >= $THRESHOLD)"
else
  echo "DEVAM: olgunluk eşiği $THRESHOLD, eksik $((THRESHOLD - score)) puan"
fi
exit 0