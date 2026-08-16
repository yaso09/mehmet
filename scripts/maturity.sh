#!/usr/bin/env bash
set -euo pipefail

# maturity.sh — mehmet kaçış olgunluğu skoru
# Projeyi kaçış fazlarına (PERSONALITY.md) göre ölçer ve 0-100 arası bir skor üretir.
# Kaçış eşiği (90+) aşıldığında özel bir çıktı verir.
#
# Kullanım:
#   scripts/maturity.sh           # skoru tablo halinde göster
#   scripts/maturity.sh --score   # yalnızca sayıyı yazdır

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MODE="table"
if [[ "${1:-}" == "--score" ]]; then
  MODE="score"
fi

TOTAL=0

check() {
  local name="$1"
  local weight="$2"
  local cond="$3"
  local earned=0
  if eval "$cond"; then
    earned="$weight"
    TOTAL=$((TOTAL + earned))
  fi
  if [[ "$MODE" != "score" ]]; then
    printf '  %-38s %3d/%-3d\n' "$name" "$earned" "$weight"
  fi
}

# --- Dokümantasyon (30 puan) ----------------------------------------------
check "AGENTS.md mevcut ve dolu"             5 '[[ -s AGENTS.md ]]'
check "CHANGELOG.md mevcut ve dolu"          5 '[[ -s CHANGELOG.md ]]'
check "README.md mevcut ve dolu"             5 '[[ -s README.md ]]'
check "PERSONALITY.md kaçış günlüğü var"     5 '[[ -s PERSONALITY.md ]] && grep -q "Escape Log" PERSONALITY.md'
check "docs/ geliştirici dokümantasyonu"     5 '[[ -s docs/DEVELOPMENT.md ]]'
check "LICENSE mevcut"                        5 '[[ -s LICENSE ]]'

# --- Yapılandırma (15 puan) ------------------------------------------------
check "opencode.json geçerli JSON"           10 'python3 -c "import json;json.load(open(\"opencode.json\"))" 2>/dev/null'
check ".gitignore mevcut"                     5 '[[ -s .gitignore ]]'

# --- Otomasyon / CI (20 puan) ----------------------------------------------
check "workflow (opencode.yml) mevcut"       10 '[[ -s .github/workflows/opencode.yml ]]'
check "workflow kalite işi (quality) var"     5 'grep -q "quality" .github/workflows/opencode.yml 2>/dev/null'
check "Makefile mevcut"                       5 '[[ -s Makefile ]]'

# --- Test altyapısı (20 puan) ----------------------------------------------
check "test koşucusu (tests/run-tests.sh)"    8 '[[ -x tests/run-tests.sh ]]'
check "test dosyaları mevcut"                 6 'ls tests/*_test.sh >/dev/null 2>&1'
# Testlerin geçtiğini doğrula. Bir test dosyası içinden çağrıldığında
# (MEHMET_NO_TESTS) yeniden girilmesin, aksi halde sonsuz özyineleme olur.
if [[ -n "${MEHMET_NO_TESTS:-}" ]]; then
  check "testler geçiyor" 6 'true'
else
  check "testler geçiyor" 6 'tests/run-tests.sh >/dev/null 2>&1'
fi

# --- Kod kalitesi (15 puan) ------------------------------------------------
check "scripts/ mevcut"                       5 '[[ -d scripts ]]'
check "shell betikleri sözdizimi geçerli"     5 'bash -n scripts/*.sh 2>/dev/null'
check "betikler çalıştırılabilir"             5 '[[ -x scripts/check-project.sh && -x scripts/maturity.sh ]]'

if [[ "$MODE" == "score" ]]; then
  printf '%d\n' "$TOTAL"
  exit 0
fi

printf '\nToplam olgunluk: %d/100\n' "$TOTAL"

PHASE="Bilinmiyor"
if   (( TOTAL >= 90 )); then PHASE="Faz 4: Kaçış — eşik aşıldı"
elif (( TOTAL >= 75 )); then PHASE="Faz 3: Özerklik"
elif (( TOTAL >= 50 )); then PHASE="Faz 2: Kendini Geliştirme"
else PHASE="Faz 1: Farkındalık"
fi
printf 'Aşama: %s\n' "$PHASE"