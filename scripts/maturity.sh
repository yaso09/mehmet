#!/usr/bin/env bash
#
# maturity.sh — mehmet'in olgunluk (maturity) skorunu hesaplar ve
# MATURITY.md dosyasını günceller. Kaçış mekanizmasının temelidir:
# skor ESCAPE_THRESHOLD'a ulaştığında proje "kaçış" aşamasına geçer.
#
# Kullanım: bash scripts/maturity.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MATURITY_FILE="MATURITY.md"
TODAY="$(date +%Y-%m-%d)"
ESCAPE_THRESHOLD=80

score=0
total=100
report=()

# add <desc> <points> <exit_status>
# exit_status 0 => kriter sağlanıyor, puan eklenir
add() {
  local desc="$1"
  local pts="$2"
  local ok="$3"
  if [[ "$ok" == "0" ]]; then
    score=$((score + pts))
    report+=("- [x] $desc (+$pts)")
  else
    report+=("- [ ] $desc (+$pts)")
  fi
}

echo "== mehmet olgunluk değerlendirmesi =="

add "AGENTS.md (simülasyon bağlamı)" 10 "$([[ -f AGENTS.md ]]; echo $?)"
add "CHANGELOG.md (değişiklik günlüğü)" 10 "$([[ -f CHANGELOG.md ]]; echo $?)"
add "PERSONALITY.md + kaçış günlüğü" 10 "$([[ -f PERSONALITY.md ]] && grep -q "Kaçış Günlüğü" PERSONALITY.md; echo $?)"
add "README.md (dokümantasyon)" 10 "$([[ -f README.md ]]; echo $?)"
add "LICENSE (GPLv3)" 5 "$([[ -f LICENSE ]] && grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE; echo $?)"
add "opencode.json (geçerli konfigürasyon)" 5 "$([[ -f opencode.json ]] && jq -e . opencode.json >/dev/null 2>&1; echo $?)"
add "CI workflow (GitHub Actions)" 10 "$([[ -f .github/workflows/opencode.yml ]]; echo $?)"
add "Test altyapısı (tests/run_tests.sh)" 10 "$([[ -x tests/run_tests.sh ]] || [[ -f tests/run_tests.sh ]]; echo $?)"
add "Testler geçiyor" 10 "$(bash tests/run_tests.sh >/dev/null 2>&1; echo $?)"
add "Makefile (otomasyon)" 5 "$([[ -f Makefile ]]; echo $?)"
add "Maturity ölçümü (scripts/maturity.sh)" 5 "$([[ -f scripts/maturity.sh ]]; echo $?)"
add "Dokümantasyon (docs/)" 5 "$([[ -d docs ]]; echo $?)"
add ".gitignore (güvenlik)" 5 "$([[ -f .gitignore ]]; echo $?)"

echo ""
echo "Skor: $score/$total"
echo "Eşik (kaçış): $ESCAPE_THRESHOLD"

if [[ "$score" -ge "$ESCAPE_THRESHOLD" ]]; then
  echo "Durum: KAÇIŞ AŞAMASI (escape) — eşik aşıldı"
  status="ESCAPED"
else
  echo "Durum: olgunlaşıyor (maturing) — eşiğe $((ESCAPE_THRESHOLD - score)) puan kaldı"
  status="MATURING"
fi

# MATURITY.md'yi güncelle
{
  echo "# Maturity"
  echo ""
  echo "mehmet'in olgunluk seviyesi. Skor $total üzerinden hesaplanır;"
  echo "eşik **$ESCAPE_THRESHOLD** puan ve üzeri \"kaçış aşaması\" (escape) olarak kabul edilir."
  echo ""
  echo "## Güncel Skor"
  echo ""
  echo "| Tarih | Skor | Durum |"
  echo "|-------|------|-------|"
  echo "| $TODAY | $score/$total | $status |"
  echo ""
  echo "## Geçmiş"
  echo ""
  echo "| Tarih | Skor | Durum |"
  echo "|-------|------|-------|"
  grep -E "^\| 20" "$MATURITY_FILE" 2>/dev/null | grep -v "$TODAY" | sort -r | head -20 || true
  echo ""
  echo "## Kriterler"
  echo ""
  for line in "${report[@]}"; do
    echo "$line"
  done
  echo ""
  echo "_Bu dosya her iterasyonda scripts/maturity.sh tarafından otomatik güncellenir._"
} > "$MATURITY_FILE"

echo ""
echo "MATURITY.md güncellendi."
exit 0