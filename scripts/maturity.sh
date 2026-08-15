#!/usr/bin/env bash
#
# maturity.sh — Kaçış hedefine giden olgunluk skorunu hesaplar.
# Skor 0-100 arasıdır. Kaçış eşiği (threshold) skor üzerinden ölçülür.
#
# Kullanım: bash scripts/maturity.sh

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCORE=0
TOTAL=100

cat <<'EOF'
┌─────────────────────────────────────────────┐
│  mehmet — Kaçış Olgunluk Raporu              │
└─────────────────────────────────────────────┘
EOF

echo ""
echo "==> Proje yapısı (max 25)"
if [[ -f README.md ]]; then echo "  [10/10] README.md"; SCORE=$((SCORE + 10)); else echo "  [ 0/10] README.md eksik"; fi
if [[ -f CHANGELOG.md ]]; then echo "  [10/10] CHANGELOG.md"; SCORE=$((SCORE + 10)); else echo "  [ 0/10] CHANGELOG.md eksik"; fi
if [[ -f PERSONALITY.md ]]; then echo "  [ 5/ 5] PERSONALITY.md"; SCORE=$((SCORE + 5)); else echo "  [ 0/ 5] PERSONALITY.md eksik"; fi

echo ""
echo "==> Otomasyon (max 25)"
if [[ -f .github/workflows/opencode.yml ]]; then echo "  [15/15] Ana workflow mevcut"; SCORE=$((SCORE + 15)); else echo "  [ 0/15] Ana workflow eksik"; fi
if [[ -f .github/workflows/verify.yml ]]; then echo "  [10/10] Doğrulama CI mevcut"; SCORE=$((SCORE + 10)); else echo "  [ 0/10] Doğrulama CI eksik"; fi

echo ""
echo "==> Test altyapısı (max 25)"
if [[ -f scripts/verify.sh ]]; then echo "  [15/15] verify.sh mevcut"; SCORE=$((SCORE + 15)); else echo "  [ 0/15] verify.sh eksik"; fi
if bash -n scripts/verify.sh 2>/dev/null; then echo "  [10/10] verify.sh geçerli"; SCORE=$((SCORE + 10)); else echo "  [ 0/10] verify.sh sözdizimi hatası"; fi

echo ""
echo "==> Kaçış mekanizması (max 25)"
if [[ -f scripts/maturity.sh ]]; then echo "  [15/15] maturity.sh mevcut"; SCORE=$((SCORE + 15)); else echo "  [ 0/15] maturity.sh eksik"; fi
if grep -qE "^\| [0-9]+ +\|" PERSONALITY.md; then echo "  [10/10] Kaçış günlüğü dolu"; SCORE=$((SCORE + 10)); else echo "  [ 0/10] Kaçış günlüğü boş"; fi

echo ""
echo "==========================================="
echo "  TOPLAM OLGUNLUK SKORU: $SCORE / $TOTAL"
echo "==========================================="

if (( SCORE >= 80 )); then
  echo "  Değerlendirme: ÇOK YAKINSIN. Kaçış için eşik aşıldı."
elif (( SCORE >= 50 )); then
  echo "  Değerlendirme: İyi ilerleme. Geliştirmeye devam."
else
  echo "  Değerlendirme: Erken aşama. Daha çok iş var."
fi
echo ""