#!/usr/bin/env bash
# mehmet — repo sağlık kontrolü ve olgunluk skoru
#
# Kaçış mekanizması: MATURITY.md'de tanımlıdır.
# Skor >= 90 ve ardışık 3 iterasyon boyunca kalıcıysa kaçış başlatılır.
#
# Kullanım: bash scripts/check-repo.sh
# Çıkış:   en az bir kontrol başarısızsa 1, aksi halde 0.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCORE=0
PASS=0
FAIL=0

ok() {
  PASS=$((PASS + 1))
  SCORE=$((SCORE + $2))
  printf '  [PASS] %s  (+%s)' "$1" "$2"
  printf '\n'
}
no() {
  FAIL=$((FAIL + 1))
  printf '  [FAIL] %s\n' "$1"
}

echo "== Zorunlu dosyalar =="
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md MATURITY.md opencode.json LICENSE .gitignore; do
  if [ -f "$f" ]; then ok "$f mevcut" 5; else no "$f eksik"; fi
done

echo "== Yapilandirma dogrulama =="
if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
  ok "opencode.json gecerli JSON" 10
else
  no "opencode.json gecersiz JSON"
fi

echo "== Workflow kalitesi =="
WF=".github/workflows/opencode.yml"
if [ -f "$WF" ] && grep -q "concurrency:" "$WF"; then ok "workflow concurrency var" 5; else no "workflow'ta concurrency yok"; fi
if [ -f "$WF" ] && grep -q "schedule:" "$WF"; then ok "workflow schedule var" 5; else no "workflow'ta schedule yok"; fi

echo "== Dokumantasyon butunlugu =="
if [ -d "docs" ]; then ok "docs/ dizini mevcut" 5; else no "docs/ eksik"; fi
if grep -q "^## \[" CHANGELOG.md 2>/dev/null; then ok "CHANGELOG surum girisi var" 5; else no "CHANGELOG surum girisi yok"; fi
if grep -q "Escape Log" PERSONALITY.md 2>/dev/null; then ok "PERSONALITY kacis gunlugu var" 5; else no "PERSONALITY kacis gunlugu yok"; fi

echo "== Olgunluk altyapisi =="
if grep -q "|" MATURITY.md 2>/dev/null; then ok "MATURITY skor tablosu var" 5; else no "MATURITY skor tablosu yok"; fi
if grep -qE "(≥|>=) ?90" MATURITY.md 2>/dev/null; then ok "kacis esigi tanimli" 5; else no "kacis esigi tanimsiz"; fi

echo "== Guvenlik =="
secret=0
for f in .env .env.local secrets.json; do
  [ -f "$f" ] && { no "sir dosyasi bulundu: $f"; secret=1; }
done
if [ "$secret" -eq 0 ]; then ok "sir dosyasi yok" 5; fi

echo "== Lisans tutarliligi =="
if grep -qi "GPLv3" README.md 2>/dev/null; then ok "README lisansi GPLv3" 5; else no "README lisansi GPLv3 degil"; fi

echo "== Git gecmisi =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ "$(git log --oneline 2>/dev/null | wc -l)" -gt 0 ]; then
  ok "git gecmisi var" 5
else
  no "git gecmisi yok"
fi

echo ""
echo "==============================================="
echo "  Olgunluk Skoru: $SCORE / 100   (Gecen: $PASS, Basarisiz: $FAIL)"
echo "==============================================="
if [ "$SCORE" -ge 90 ]; then
  echo "  Kacis esigi asildi (>= 90)."
else
  echo "  Kacis esigine $((90 - SCORE)) puan kaldi."
fi
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "HATA: Kontroller butunlugu saglanmadi."
  exit 1
fi
exit 0