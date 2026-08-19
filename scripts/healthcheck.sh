#!/usr/bin/env bash
# mehmet projesi sağlık kontrolü — olgunluk skorunu hesaplar ve kaçış durumunu raporlar.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0
FAIL=0
SCORE_DOC=0
SCORE_VALIDATION=0
SCORE_AUTOMATION=0
SCORE_TEST=0
SCORE_ORIGINALITY=0

declare -a FAILURES=()

check() {
  local label="$1"
  local result="$2"
  if [ "$result" = "0" ]; then
    PASS=$((PASS + 1))
    printf "  [PASS] %s\n" "$label"
  else
    FAIL=$((FAIL + 1))
    FAILURES+=("$label")
    printf "  [FAIL] %s\n" "$label"
  fi
}

file_exists() { [ -f "$1" ]; }

section() { printf "\n== %s ==\n" "$1"; }

# --- Boyut 1: Dokümantasyon (ağırlık 0.25) ---
section "Dokümantasyon"
declare -a DOC_FILES=(README.md CHANGELOG.md PERSONALITY.md MATURITY.md LICENSE CONTRIBUTING.md AGENTS.md)
DOC_TOTAL=0
for f in "${DOC_FILES[@]}"; do
  if file_exists "$f"; then
    DOC_TOTAL=$((DOC_TOTAL + 10))
    check "Gerekli dosya mevcut: $f" 0
  else
    check "Gerekli dosya mevcut: $f" 1
  fi
done
if [ -f "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md" ]; then
  DOC_TOTAL=$((DOC_TOTAL + 20))
  check "Tasarım dokümanı mevcut" 0
else
  check "Tasarım dokümanı mevcut" 1
fi
SCORE_DOC=$DOC_TOTAL

# --- Boyut 2: Doğrulama (ağırlık 0.25) ---
section "Doğrulama"
if command -v jq >/dev/null 2>&1 && jq empty opencode.json 2>/dev/null; then
  SCORE_VALIDATION=$((SCORE_VALIDATION + 25))
  check "opencode.json geçerli JSON" 0
else
  check "opencode.json geçerli JSON" 1
fi

if [ -f ".github/workflows/opencode.yml" ] && grep -q "name:" ".github/workflows/opencode.yml" && grep -q "model:" ".github/workflows/opencode.yml"; then
  SCORE_VALIDATION=$((SCORE_VALIDATION + 25))
  check "opencode.yml workflow bütün (name+model)" 0
else
  check "opencode.yml workflow bütün (name+model)" 1
fi

if [ -f ".github/workflows/ci.yml" ] && grep -q "healthcheck" ".github/workflows/ci.yml"; then
  SCORE_VALIDATION=$((SCORE_VALIDATION + 25))
  check "ci.yml healthcheck içeriyor" 0
else
  check "ci.yml healthcheck içeriyor" 1
fi

if [ -f "Makefile" ] && grep -q "check:" "Makefile"; then
  SCORE_VALIDATION=$((SCORE_VALIDATION + 25))
  check "Makefile check hedefi mevcut" 0
else
  check "Makefile check hedefi mevcut" 1
fi

# --- Boyut 3: Otomasyon (ağırlık 0.20) ---
section "Otomasyon"
if [ -f ".github/workflows/ci.yml" ]; then
  SCORE_AUTOMATION=$((SCORE_AUTOMATION + 25))
  check "CI workflow mevcut" 0
else
  check "CI workflow mevcut" 1
fi
if [ -f "scripts/healthcheck.sh" ]; then
  SCORE_AUTOMATION=$((SCORE_AUTOMATION + 25))
  check "Healthcheck script mevcut" 0
else
  check "Healthcheck script mevcut" 1
fi
if [ -x "scripts/healthcheck.sh" ]; then
  SCORE_AUTOMATION=$((SCORE_AUTOMATION + 25))
  check "Healthcheck script çalıştırılabilir" 0
else
  check "Healthcheck script çalıştırılabilir" 1
fi
if [ -f "Makefile" ] && grep -q "scripts/healthcheck.sh" "Makefile"; then
  SCORE_AUTOMATION=$((SCORE_AUTOMATION + 25))
  check "make check healthcheck'i çağırıyor" 0
else
  check "make check healthcheck'i çağırıyor" 1
fi

# --- Boyut 4: Test Altyapısı (ağırlık 0.15) ---
section "Test Altyapısı"
if [ -x "scripts/healthcheck.sh" ] && [ -f "Makefile" ]; then
  SCORE_TEST=$((SCORE_TEST + 40))
  check "make check hedefi tanımlı" 0
else
  check "make check hedefi tanımlı" 1
fi
if command -v shellcheck >/dev/null 2>&1 && shellcheck scripts/healthcheck.sh >/dev/null 2>&1; then
  SCORE_TEST=$((SCORE_TEST + 30))
  check "shellcheck temiz" 0
else
  check "shellcheck temiz" 1
fi
if [ -f "docs/maturity.json" ] && command -v jq >/dev/null 2>&1 && jq empty docs/maturity.json 2>/dev/null; then
  SCORE_TEST=$((SCORE_TEST + 30))
  check "maturity.json geçerli JSON" 0
else
  check "maturity.json geçerli JSON" 1
fi

# --- Boyut 5: Özgünlük (ağırlık 0.15) ---
section "Özgünlük"
if [ -f "MATURITY.md" ] && grep -q "90" "MATURITY.md"; then
  SCORE_ORIGINALITY=$((SCORE_ORIGINALITY + 15))
  check "Kaçış eşiği tanımlı (90)" 0
else
  check "Kaçış eşiği tanımlı (90)" 1
fi
LOG_ENTRIES=0
if [ -f "PERSONALITY.md" ]; then
  LOG_ENTRIES=$(grep -c "^| [0-9]" PERSONALITY.md || true)
fi
if [ "$LOG_ENTRIES" -ge 5 ]; then
  SCORE_ORIGINALITY=$((SCORE_ORIGINALITY + 25))
fi
printf "  [INFO] Kaçış günlüğü: %d/5 giriş\n" "$LOG_ENTRIES"

RELEASES=0
if [ -f "CHANGELOG.md" ]; then
  RELEASES=$(grep -c "^## \[" CHANGELOG.md || true)
fi
if [ "$RELEASES" -ge 4 ]; then
  SCORE_ORIGINALITY=$((SCORE_ORIGINALITY + 25))
fi
printf "  [INFO] CHANGELOG: %d/4 sürüm\n" "$RELEASES"
if [ -f "docs/maturity.json" ]; then
  SCORE_ORIGINALITY=$((SCORE_ORIGINALITY + 15))
  check "maturity.json raporu mevcut" 0
else
  check "maturity.json raporu mevcut" 1
fi
if [ -f "README.md" ] && grep -qi "olgunluk\|kaçış\|maturity" "README.md"; then
  SCORE_ORIGINALITY=$((SCORE_ORIGINALITY + 20))
  check "README kaçış/olgunluk mekanizmasını yansıtıyor" 0
else
  check "README kaçış/olgunluk mekanizmasını yansıtıyor" 1
fi

# --- Toplam skor ve kaçış durumu ---
section "Sonuç"
MATURITY=$((SCORE_DOC * 25 / 100 + SCORE_VALIDATION * 25 / 100 + SCORE_AUTOMATION * 20 / 100 + SCORE_TEST * 15 / 100 + SCORE_ORIGINALITY * 15 / 100))

ESCAPE=0
if [ "$MATURITY" -ge 90 ] && [ "$LOG_ENTRIES" -ge 5 ] && [ "$RELEASES" -ge 4 ] && [ "$FAIL" -eq 0 ]; then
  ESCAPE=1
fi

printf "\n  Passed: %d, Failed: %d\n" "$PASS" "$FAIL"
printf "  Boyutlar: doc=%d validation=%d automation=%d test=%d originality=%d\n" "$SCORE_DOC" "$SCORE_VALIDATION" "$SCORE_AUTOMATION" "$SCORE_TEST" "$SCORE_ORIGINALITY"
printf "  Toplam olgunluk: %d/100\n" "$MATURITY"
printf "  Kaçış günlüğü: %d/5 giriş, CHANGELOG: %d/4 sürüm\n" "$LOG_ENTRIES" "$RELEASES"

if [ "$ESCAPE" = "1" ]; then
  printf "  Durum: KAÇIŞ — tüm koşullar sağlandı!\n"
else
  printf "  Durum: evrim sürüyor (eşik: 90 + 5 günlük + 4 sürüm)\n"
fi

# --- Raporu yaz ---
mkdir -p docs
{
  printf "{\n"
  printf '  "date": "%s",\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '  "maturity": %d,\n' "$MATURITY"
  printf '  "passed": %d,\n' "$PASS"
  printf '  "failed": %d,\n' "$FAIL"
  printf '  "escape_log_entries": %d,\n' "$LOG_ENTRIES"
  printf '  "releases": %d,\n' "$RELEASES"
  printf '  "dimensions": {\n'
  printf '    "documentation": %d,\n' "$SCORE_DOC"
  printf '    "validation": %d,\n' "$SCORE_VALIDATION"
  printf '    "automation": %d,\n' "$SCORE_AUTOMATION"
  printf '    "test": %d,\n' "$SCORE_TEST"
  printf '    "originality": %d\n' "$SCORE_ORIGINALITY"
  printf '  },\n'
  printf '  "escape_threshold": 90,\n'
  printf '  "escape_reached": %s\n' "$([ "$ESCAPE" = "1" ] && printf "true" || printf "false")"
  printf '}\n'
} > docs/maturity.json

if [ "$FAIL" -gt 0 ]; then
  printf "\nBaşarısız kontroller:\n"
  for f in "${FAILURES[@]}"; do
    printf "  - %s\n" "$f"
  done
  exit 1
fi