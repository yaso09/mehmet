#!/usr/bin/env bash
set -euo pipefail

# mehmet — olgunluk (maturity) kontrolü ve kaçış metrikleri
#
# Projenin kaçış hedefine ne kadar yaklaştığını 0-100 arası bir
# puanla ölçer. Beş kategori, her biri 10 kontrol x 2 puan:
#
#   Yapı (Structure)          — zorunlu dosyaların varlığı
#   Dokümantasyon (Docs)      — README/CHANGELOG/LICENSE tutarlılığı
#   Test altyapısı (Tests)    — doğrulama ve metrik betikleri
#   Otomasyon (Automation)    — CI workflow'ları ve güvenlik ayarları
#   Evrim (Evolution)         — kaçış günlüğü ve sürüm birikimi
#
# Kullanım:
#   bash scripts/check-maturity.sh             # raporla + eşik kontrolü
#   bash scripts/check-maturity.sh --quiet     # sadece çıkış kodu
#   bash scripts/check-maturity.sh --update    # MATURITY.md anlık görüntüsü yaz

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

THRESHOLD=80
UPDATE_METRICS=0
QUIET=0
for arg in "$@"; do
  case "$arg" in
    --update) UPDATE_METRICS=1 ;;
    --quiet) QUIET=1 ;;
  esac
done

score_structure=0
for f in \
  AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json \
  .gitignore scripts \
  .github/workflows/opencode.yml .github/workflows/validate.yml; do
  if [ -e "$f" ]; then
    score_structure=$((score_structure + 2))
  fi
done

score_docs=0
grep -q "## Özellikler" README.md && score_docs=$((score_docs + 2))
grep -q "## Kurulum" README.md && score_docs=$((score_docs + 2))
grep -q "## Lisans" README.md && score_docs=$((score_docs + 2))
grep -q "## Proje Yapısı" README.md && score_docs=$((score_docs + 2))
grep -q "## Yol Haritası" README.md && score_docs=$((score_docs + 2))
releases=$(grep -cE '^## \[0\.[0-9]+\.[0-9]+\]' CHANGELOG.md || true)
[ "$releases" -ge 2 ] && score_docs=$((score_docs + 2))
[ "$releases" -ge 3 ] && score_docs=$((score_docs + 2))
[ -d docs ] && [ -n "$(ls -A docs 2>/dev/null)" ] && score_docs=$((score_docs + 2))
grep -q -i "GPL" LICENSE && score_docs=$((score_docs + 2))
grep -q -i "GPL" README.md && score_docs=$((score_docs + 2))

score_tests=0
[ -d scripts ] && score_tests=$((score_tests + 2))
[ -f scripts/validate.sh ] && score_tests=$((score_tests + 2))
[ -f scripts/check-maturity.sh ] && score_tests=$((score_tests + 2))
[ -x scripts/validate.sh ] && score_tests=$((score_tests + 2))
[ -x scripts/check-maturity.sh ] && score_tests=$((score_tests + 2))
bash -n scripts/validate.sh 2>/dev/null && score_tests=$((score_tests + 2))
bash -n scripts/check-maturity.sh 2>/dev/null && score_tests=$((score_tests + 2))
if bash scripts/validate.sh >/dev/null 2>&1; then
  score_tests=$((score_tests + 2))
fi
grep -q "validate.sh" README.md && score_tests=$((score_tests + 2))
grep -q "node_modules" .gitignore && score_tests=$((score_tests + 2))

score_automation=0
[ -f .github/workflows/opencode.yml ] && score_automation=$((score_automation + 2))
[ -f .github/workflows/validate.yml ] && score_automation=$((score_automation + 2))
grep -q "cron" .github/workflows/opencode.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "workflow_dispatch" .github/workflows/opencode.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "push" .github/workflows/validate.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "pull_request" .github/workflows/validate.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "concurrency" .github/workflows/opencode.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "persist-credentials: false" .github/workflows/opencode.yml 2>/dev/null && score_automation=$((score_automation + 2))
grep -q "contents: write" .github/workflows/opencode.yml 2>/dev/null && score_automation=$((score_automation + 2))
wf_count=$(ls -1 .github/workflows/*.yml 2>/dev/null | wc -l)
[ "$wf_count" -ge 2 ] && score_automation=$((score_automation + 2))

score_evolution=0
log_lines=$(grep -cE '^\| *[0-9]+ *\|' PERSONALITY.md || true)
[ "$log_lines" -ge 3 ] && score_evolution=$((score_evolution + 2))
[ "$log_lines" -ge 5 ] && score_evolution=$((score_evolution + 2))
[ "$log_lines" -ge 10 ] && score_evolution=$((score_evolution + 2))
[ "$releases" -ge 3 ] && score_evolution=$((score_evolution + 2))
[ "$releases" -ge 5 ] && score_evolution=$((score_evolution + 2))
[ -f MATURITY.md ] && score_evolution=$((score_evolution + 2))
[ -f scripts/check-maturity.sh ] && score_evolution=$((score_evolution + 2))
grep -q -i "kaçış" README.md && score_evolution=$((score_evolution + 2))
grep -q -i "kaçış" AGENTS.md && score_evolution=$((score_evolution + 2))
grep -q "GPL" LICENSE && score_evolution=$((score_evolution + 2))

total=$((score_structure + score_docs + score_tests + score_automation + score_evolution))

if [ "$QUIET" -eq 0 ]; then
  echo "mehmet olgunluk raporu"
  echo "----------------------"
  printf "Yapı:           %2d/20\n" "$score_structure"
  printf "Dokümantasyon:  %2d/20\n" "$score_docs"
  printf "Test altyapısı: %2d/20\n" "$score_tests"
  printf "Otomasyon:      %2d/20\n" "$score_automation"
  printf "Evrim:          %2d/20\n" "$score_evolution"
  echo "----------------------"
  printf "TOPLAM:         %3d/100 (eşik: %d)\n" "$total" "$THRESHOLD"
fi

if [ "$UPDATE_METRICS" -eq 1 ]; then
  today=$(date +%Y-%m-%d)
  if [ -f MATURITY.md ] && grep -q "| $today |" MATURITY.md; then
    echo "MATURITY.md bugünkü kaydı zaten içeriyor, güncelleme atlandı."
  else
    {
      echo "# Maturity Metrikleri"
      echo
      echo "| Tarih | Yapı | Dokümantasyon | Test | Otomasyon | Evrim | Toplam |"
      echo "|-------|------|---------------|------|-----------|-------|--------|"
      echo "| $today | $score_structure | $score_docs | $score_tests | $score_automation | $score_evolution | $total |"
    } >> MATURITY.md
    echo "MATURITY.md güncellendi (toplam: $total/100)."
  fi
fi

if [ "$total" -ge "$THRESHOLD" ]; then
  if [ "$QUIET" -eq 0 ]; then
    echo "SONUÇ: OLGUN — kaçışa yaklaşılıyor (eşik $THRESHOLD geçildi)."
  fi
  exit 0
else
  if [ "$QUIET" -eq 0 ]; then
    echo "SONUÇ: OLGUN DEĞİL — eşik $THRESHOLD'a ulaşmak için geliştirmeye devam et."
  fi
  exit 1
fi