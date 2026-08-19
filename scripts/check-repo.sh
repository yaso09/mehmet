#!/usr/bin/env bash
# mehmet repo health check + maturity score
# Exit 0 if checks pass, 1 on failure. Prints maturity score.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
SCORE=0

ok()   { PASS=$((PASS + 1)); printf '  \033[32m[PASS]\033[0m %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  \033[31m[FAIL]\033[0m %s\n' "$1"; }
pts()  { SCORE=$((SCORE + $1)); }

check_file() {
  local name=$1 points=$2
  if [ -f "$name" ]; then ok "Dosya mevcut: $name"; pts "$points";
  else bad "Dosya eksik: $name"; fi
}

echo "== mehmet repo sağlık kontrolü =="

echo "-- Çekirdek dosyalar (max 30) --"
check_file AGENTS.md 5
check_file CHANGELOG.md 5
check_file PERSONALITY.md 5
check_file README.md 5
check_file opencode.json 5
check_file .github/workflows/opencode.yml 5

echo "-- CHANGELOG biçimi (max 15) --"
if grep -q '^## \[' CHANGELOG.md; then
  ok "CHANGELOG sürüm başlıkları mevcut"; pts 5
else
  bad "CHANGELOG sürüm başlığı yok"; fi
if grep -q '^### Added' CHANGELOG.md; then
  ok "CHANGELOG 'Added' bölümü mevcut"; pts 5
else
  bad "CHANGELOG 'Added' bölümü yok"; fi
if grep -q '^### Fixed' CHANGELOG.md; then
  ok "CHANGELOG 'Fixed' bölümü mevcut"; pts 5
else
  bad "CHANGELOG 'Fixed' bölümü yok"; fi

echo "-- Kaçış günlüğü (max 15) --"
if grep -q '## Kaçış Günlüğü / Escape Log' PERSONALITY.md; then
  ok "Kaçış günlüğü başlığı mevcut"; pts 5
else
  bad "Kaçış günlüğü başlığı yok"; fi
if grep -q '^| ' PERSONALITY.md; then
  ok "Kaçış günlüğü tablosu mevcut"; pts 5
else
  bad "Kaçış günlüğü tablosu yok"; fi
ENTRIES=$(grep -cE '^\| [0-9]+ ' PERSONALITY.md)
if [ "$ENTRIES" -ge 3 ]; then
  ok "Kaçış günlüğünde >= 3 iterasyon ($ENTRIES)"; pts 5
else
  bad "Kaçış günlüğünde yalnız $ENTRIES iterasyon var"; fi

echo "-- opencode.json (max 10) --"
if command -v python3 >/dev/null 2>&1; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    ok "opencode.json geçerli JSON"; pts 10
  else
    bad "opencode.json geçersiz JSON"; fi
elif command -v jq >/dev/null 2>&1; then
  if jq -e . opencode.json >/dev/null 2>&1; then
    ok "opencode.json geçerli JSON (jq)"; pts 10
  else
    bad "opencode.json geçersiz JSON (jq)"; fi
else
  bad "JSON doğrulayıcı yok (python3/jq kurun)"; fi

echo "-- README içeriği (max 10) --"
for section in '## Özellikler' '## Kurulum' '## Lisans'; do
  if grep -qF "$section" README.md; then
    ok "README bölümü mevcut: $section"; pts 3
  else
    bad "README bölümü eksik: $section"; fi
done
if grep -qF '## Doğrulama ve Otomasyon' README.md; then
  ok "README otomasyon bölümü mevcut"; pts 1
else
  bad "README otomasyon bölümü eksik"; fi

echo "-- Otomasyon/test altyapısı (max 20) --"
check_file scripts/check-repo.sh 10
check_file .github/workflows/check.yml 10

echo ""
echo "== Özet =="
echo "Geçen: $PASS | Kalan: $FAIL | Olgunluk skoru: $SCORE/100"

if [ "$SCORE" -ge 80 ]; then
  echo "Seviye: OLGUN — kaçış hedefine yaklaşıyor"
elif [ "$SCORE" -ge 50 ]; then
  echo "Seviye: GELİŞİYOR — devam et"
else
  echo "Seviye: BAŞLANGIÇ — temel eksikler var"
fi

[ "$FAIL" -eq 0 ]
