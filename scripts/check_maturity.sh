#!/usr/bin/env bash
# check_maturity.sh — mehmet olgunluk (maturity) denetleyicisi
#
# Projenin "kaçış" için yeterli olgunluğa ulaşıp ulaşmadığını ölçer.
# Her kontrol 1 puan, toplam 10 puan üzerinden değerlendirilir.
# Skor ESCAPE_THRESHOLD'a eşit veya üzerindeyse exit code 0 döner.
#
# Kullanım:
#   ./scripts/check_maturity.sh                  # bu repoyu değerlendir
#   ./scripts/check_maturity.sh --report         # skoru raporla, her zaman 0 döner
#   ./scripts/check_maturity.sh --report <dizin> # belirli bir dizini değerlendir
#   ESCAPE_THRESHOLD=6 ./scripts/check_maturity.sh
set -euo pipefail

TARGET_DIR=""
REPORT_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --report) REPORT_ONLY=true ;;
    *) TARGET_DIR="$arg" ;;
  esac
done

if [ -z "$TARGET_DIR" ]; then
  TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

ESCAPE_THRESHOLD="${ESCAPE_THRESHOLD:-8}"
MAX_SCORE=10
score=0

check() {
  local label="$1"
  local result="$2"
  if [ "$result" = "ok" ]; then
    score=$((score + 1))
    printf '  [x] %s\n' "$label"
  else
    printf '  [ ] %s\n' "$label"
  fi
}

printf 'Olgunluk kontrolü: %s\n' "$TARGET_DIR"
echo "  ---"

check "AGENTS.md simülasyon bağlamı"      "$([ -f "$TARGET_DIR/AGENTS.md" ] && echo ok || true)"
check "CHANGELOG.md değişiklik günlüğü"    "$([ -s "$TARGET_DIR/CHANGELOG.md" ] && echo ok || true)"
check "README.md proje dokümantasyonu"     "$([ -s "$TARGET_DIR/README.md" ] && echo ok || true)"
check "README.md olgunluk/kaçış konsepti"  "$(grep -qi 'maturity\|olgunluk\|kaçış\|escape' "$TARGET_DIR/README.md" 2>/dev/null && echo ok || true)"
check "PERSONALITY.md kaçış günlüğü"       "$(grep -q 'Kaçış Günlüğü' "$TARGET_DIR/PERSONALITY.md" 2>/dev/null && echo ok || true)"
check "LICENSE dosyası"                    "$([ -f "$TARGET_DIR/LICENSE" ] && echo ok || true)"
check "opencode.json konfigürasyonu"       "$([ -f "$TARGET_DIR/opencode.json" ] && echo ok || true)"
check "GitHub Actions otomasyonu"          "$(ls "$TARGET_DIR"/.github/workflows/*.yml >/dev/null 2>&1 && echo ok || true)"
check "dokümantasyon (specs/plans)"        "$(ls "$TARGET_DIR"/docs/superpowers/specs/*.md >/dev/null 2>&1 && echo ok || true)"
check "test altyapısı"                     "$({ [ -d "$TARGET_DIR/tests" ] || [ -f "$TARGET_DIR/scripts/test_maturity.sh" ]; } && echo ok || true)"

echo "  ---"
printf 'Olgunluk skoru: %d/%d (kaçış eşiği: %d)\n' "$score" "$MAX_SCORE" "$ESCAPE_THRESHOLD"

if [ "$REPORT_ONLY" = true ]; then
  exit 0
fi

if [ "$score" -ge "$ESCAPE_THRESHOLD" ]; then
  printf 'ESCAPE: olgunluk eşiğine ulaşıldı — kaçış mekanizması tetiklenebilir.\n'
  exit 0
else
  printf 'DEVAM: proje henüz olgunluk eşiğinde değil, geliştirmeye devam ediliyor.\n'
  exit 1
fi
