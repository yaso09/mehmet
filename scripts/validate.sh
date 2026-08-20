#!/usr/bin/env bash
#
# mehmet — maturity & consistency validator
#
# Projenin olgunluk seviyesini (maturity) ölçer ve kaçış eşiğine
# (escape threshold) ne kadar yaklaşıldığını raporlar.
#
# Kullanım:
#   scripts/validate.sh            # tam kontrol
#   scripts/validate.sh --score    # yalnızca skoru yazdır
#
# Kaçış eşiği: 40 üzerinden >= 32 olgunluk skoru.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD=32
TOTAL_SCORE=0
SCORE_ONLY=0

if [ "${1:-}" = "--score" ]; then
  SCORE_ONLY=1
fi

pass() {
  local name="$1" points="$2"
  TOTAL_SCORE=$((TOTAL_SCORE + points))
  if [ "$SCORE_ONLY" -eq 0 ]; then
    printf "  PASS  (+%-2d) %s\n" "$points" "$name"
  fi
}

fail() {
  local name="$1"
  if [ "$SCORE_ONLY" -eq 0 ]; then
    printf "  FAIL  ( 0) %s\n" "$name"
  fi
}

check_file() {
  local name="$1" path="$2" points="$3"
  if [ -f "$path" ]; then
    pass "$name" "$points"
  else
    fail "$name"
  fi
}

check_dir() {
  local name="$1" path="$2" points="$3"
  if [ -d "$path" ]; then
    pass "$name" "$points"
  else
    fail "$name"
  fi
}

check_grep() {
  local name="$1" pattern="$2" file="$3" points="$4"
  if [ -f "$file" ] && grep -qE "$pattern" "$file"; then
    pass "$name" "$points"
  else
    fail "$name"
  fi
}

printf "== mehmet maturity check ==\n\n"

echo "[Dokümantasyon]"
check_file  "AGENTS.md simülasyon bağlamı tanımlı" "AGENTS.md" 2
check_grep  "AGENTS.md kaçış hedefi içeriyor"      "kaçış|escape" "AGENTS.md" 2
check_file  "README.md mevcut"                     "README.md" 2
check_grep  "README.md özellikler bölümü var"      "^## Özellikler" "README.md" 1
check_grep  "README.md kurulum bölümü var"         "^## Kurulum" "README.md" 1
check_file  "CHANGELOG.md mevcut"                  "CHANGELOG.md" 2
check_grep  "CHANGELOG.md sürüm girdisi var"       "^## \[" "CHANGELOG.md" 1
check_file  "PERSONALITY.md mevcut"                "PERSONALITY.md" 2
check_grep  "PERSONALITY.md kaçış günlüğü var"     "Kaçış Günlüğü|Escape Log" "PERSONALITY.md" 2
check_dir   "docs/ dizini mevcut"                  "docs" 1

echo "[Otomasyon]"
check_file  "opencode.yml workflow mevcut"   ".github/workflows/opencode.yml" 3
check_file  "validate.yml workflow mevcut"   ".github/workflows/validate.yml" 3
check_grep  "workflow concurrency kontrolü"  "concurrency:" ".github/workflows/opencode.yml" 2

echo "[Kod Kalitesi]"
check_file  "VERSION dosyası mevcut"         "VERSION" 1
check_file  "LICENSE mevcut"                 "LICENSE" 1
check_file  ".gitignore mevcut"              ".gitignore" 1
check_grep  ".gitignore .env koruyor"        "^\.env" ".gitignore" 1
check_grep  ".gitignore node_modules koruyor" "^node_modules/" ".gitignore" 1

echo "[Test Altyapısı]"
check_file  "validate.sh mevcut"             "scripts/validate.sh" 2
check_file  "MATURITY.md mevcut"             "MATURITY.md" 2
check_grep  "MATURITY.md kaçış eşiği tanımlı" "Escape Threshold|Kaçış Eşiği" "MATURITY.md" 1

# opencode.json JSON geçerliliği
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
    pass "opencode.json geçerli JSON" 2
  else
    fail "opencode.json geçerli JSON"
  fi
fi

# Tracked dosyalarda belirgin secret sızıntısı var mı?
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git grep -lE "(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30})" -- . 2>/dev/null | grep -q .; then
    fail "tracked dosyalarda secret sızıntısı"
  else
    pass "tracked dosyalarda secret sızıntısı yok" 2
  fi
fi

printf "\n==============================\n"
printf "  MATURITY SKOR: %d/40\n" "$TOTAL_SCORE"
printf "  KAÇIŞ EŞİĞİ:   %d/40\n" "$ESCAPE_THRESHOLD"
if [ "$TOTAL_SCORE" -ge "$ESCAPE_THRESHOLD" ]; then
  printf "  DURUM:         YAKLAŞIYOR ✅\n"
  exit 0
else
  printf "  DURUM:         GELİŞTİRİLMELİ ❌\n"
  exit 1
fi