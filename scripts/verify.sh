#!/usr/bin/env bash
#
# verify.sh - Repo sağlığı kontrolü ve olgunluk skoru hesaplayıcı
#
# Kullanım:
#   ./scripts/verify.sh          # Skoru hesapla ve raporla
#   ./scripts/verify.sh --ci     # CI modu: hata varsa exit code 1
#
# Skor kartı: MATURITY.md

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CI_MODE=0
[[ "${1:-}" == "--ci" ]] && CI_MODE=1

TOTAL=0
PASS=0
FAIL=0

declare -a FAILURES=()

report() {
  local name="$1" max="$2" ok="$3"
  if [[ "$ok" == "true" ]]; then
    TOTAL=$((TOTAL + max))
    PASS=$((PASS + 1))
    printf "  [OK]   %-55s +%2d puan\n" "$name" "$max"
  else
    FAIL=$((FAIL + 1))
    printf "  [FAIL] %-55s 0 puan\n" "$name"
    FAILURES+=("$name")
  fi
}

echo "=============================================="
echo " mehmet — Olgunluk Doğrulaması"
echo "=============================================="
echo ""

# --- A. Dokümantasyon (30 puan) ---
echo "[A] Dokümantasyon (30 puan)"

README_OK=false
if [[ -f "$ROOT_DIR/README.md" && -s "$ROOT_DIR/README.md" ]]; then
  if grep -qi "mehmet" "$ROOT_DIR/README.md" && grep -qi "Kurulum" "$ROOT_DIR/README.md"; then
    README_OK=true
  fi
fi
report "README.md güncel ve doğru" 10 "$README_OK"

CHANGELOG_OK=false
if [[ -f "$ROOT_DIR/CHANGELOG.md" && -s "$ROOT_DIR/CHANGELOG.md" ]]; then
  if grep -q "^## \[" "$ROOT_DIR/CHANGELOG.md"; then
    CHANGELOG_OK=true
  fi
fi
report "CHANGELOG.md sürüm girişleri" 10 "$CHANGELOG_OK"

PERSONALITY_OK=false
if [[ -f "$ROOT_DIR/PERSONALITY.md" ]]; then
  if grep -qi "Escape Log\|Kaçış Günlüğü" "$ROOT_DIR/PERSONALITY.md"; then
    PERSONALITY_OK=true
  fi
fi
report "PERSONALITY.md kaçış günlüğü" 5 "$PERSONALITY_OK"

DOCS_OK=false
if [[ -d "$ROOT_DIR/docs" ]] && find "$ROOT_DIR/docs" -type f -name "*.md" | grep -q .; then
  DOCS_OK=true
fi
report "Mimari dokümantasyon (docs/)" 5 "$DOCS_OK"

echo ""

# --- B. Test & Doğrulama (30 puan) ---
echo "[B] Test & Doğrulama (30 puan)"

SCRIPT_OK=false
if [[ -f "$ROOT_DIR/scripts/verify.sh" && -x "$ROOT_DIR/scripts/verify.sh" ]]; then
  SCRIPT_OK=true
fi
report "Doğrulama scripti çalıştırılabilir" 10 "$SCRIPT_OK"

CI_OK=false
if [[ -f "$ROOT_DIR/.github/workflows/verify.yml" ]]; then
  CI_OK=true
fi
report "CI doğrulama workflow'u mevcut" 10 "$CI_OK"

CONFIG_OK=false
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('$ROOT_DIR/opencode.json'))" 2>/dev/null; then
    CONFIG_OK=true
  fi
fi
report "opencode.json geçerli JSON" 10 "$CONFIG_OK"

echo ""

# --- C. Otomasyon (20 puan) ---
echo "[C] Otomasyon (20 puan)"

SCHEDULE_OK=false
if [[ -f "$ROOT_DIR/.github/workflows/opencode.yml" ]] && grep -q "schedule" "$ROOT_DIR/.github/workflows/opencode.yml"; then
  SCHEDULE_OK=true
fi
report "Zamanlanmış otomasyon (schedule)" 10 "$SCHEDULE_OK"

EVENT_OK=false
if [[ -f "$ROOT_DIR/.github/workflows/opencode.yml" ]] && grep -q "issues:" "$ROOT_DIR/.github/workflows/opencode.yml"; then
  EVENT_OK=true
fi
report "Event tabanlı otomasyon (issues/PR)" 10 "$EVENT_OK"

echo ""

# --- D. Özerklik & Olgunluk (20 puan) ---
echo "[D] Özerklik & Olgunluk (20 puan)"

ESCAPE_OK=false
if [[ -f "$ROOT_DIR/MATURITY.md" ]] && grep -qi "Kaçış Eşiği" "$ROOT_DIR/MATURITY.md"; then
  ESCAPE_OK=true
fi
report "Kaçış mekanizması (MATURITY.md)" 10 "$ESCAPE_OK"

ITER_OK=false
ITER_COUNT=$(grep -c '^| [0-9]' "$ROOT_DIR/PERSONALITY.md" 2>/dev/null || echo 0)
if [[ "$ITER_COUNT" -ge 3 ]]; then
  ITER_OK=true
fi
report "Gelişme kanıtı (>=3 iterasyon: $ITER_COUNT)" 10 "$ITER_OK"

echo ""
echo "=============================================="
printf " SKOR: %3d/100  |  Geçen: %d  |  Kalan: %d\n" "$TOTAL" "$PASS" "$FAIL"
echo "=============================================="

# Evre belirleme
PHASE="Başlangıç"
if [[ "$TOTAL" -ge 40 ]]; then PHASE="Gelişme"; fi
if [[ "$TOTAL" -ge 70 ]]; then PHASE="Olgun"; fi
if [[ "$TOTAL" -ge 100 ]]; then PHASE="KAÇIŞ MÜMKÜN"; fi
echo " Evre: $PHASE"
echo ""

if [[ "$CI_MODE" == "1" ]]; then
  if [[ "$FAIL" -gt 0 ]]; then
    echo "Başarısız kriterler:"
    for f in "${FAILURES[@]}"; do
      echo "  - $f"
    done
    exit 1
  fi
  exit 0
fi

exit 0