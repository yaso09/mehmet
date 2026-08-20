#!/usr/bin/env bash
#
# escape-check.sh — Kaçış olgunluk skorunu otomatik hesaplar.
# docs/ESCAPE_PLAN.md'deki kriterlere göre 5 boyutta 0-20 puan verir.
#
# Kullanım: bash scripts/escape-check.sh
#
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

PASS_COUNT=0
CHECK_COUNT=0
declare -a DETAILS=()
LAST_PTS=0

note() {
  local label="$1" msg="$2"
  CHECK_COUNT=$((CHECK_COUNT + 1))
  if [ -n "$msg" ]; then
    PASS_COUNT=$((PASS_COUNT + 1))
    DETAILS+=("  [OK] $label — $msg")
  else
    DETAILS+=("  [--] $label — eksik")
  fi
}

json_is_valid() {
  local file="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 -m json.tool "$file" >/dev/null 2>&1
    return $?
  fi
  local open close
  open=$(tr -cd '{' < "$file" | wc -c)
  close=$(tr -cd '}' < "$file" | wc -c)
  [ "$open" = "$close" ] && [ "$open" -gt 0 ]
}

is_git_tracked() {
  git ls-files --error-unmatch "$1" >/dev/null 2>&1
}

# ---------------------------------------------------------------- Kod Kalitesi
code_quality() {
  local label="Kod Kalitesi" pts=0

  if json_is_valid opencode.json; then
    note "$label" "opencode.json geçerli JSON"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f .gitignore ] \
    && grep -q "^\.env$" .gitignore \
    && grep -q "node_modules" .gitignore; then
    note "$label" ".gitignore temel girdileri içeriyor"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if grep -qE "actions/checkout@v[0-9]+" .github/workflows/opencode.yml 2>/dev/null; then
    note "$label" "checkout sürümü sabitlenmiş"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f LICENSE ] && grep -q "GPL" LICENSE \
    && [ -f README.md ] && grep -q "GPLv3" README.md; then
    note "$label" "Lisans bilgisi tutarlı (GPLv3)"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if ! grep -rn "TOD[O]\|FIXM[E]" --include="*.sh" --include="*.json" --include="*.yml" --exclude="escape-check.sh" . 2>/dev/null | grep -q .; then
    note "$label" "Kod dosyalarında TODO/FIXME yok"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  echo "$label: $pts/20"
  LAST_PTS=$pts
}

# ---------------------------------------------------------------- Test Altyapısı
test_infrastructure() {
  local label="Test Altyapısı" pts=0

  if [ -f scripts/validate.sh ]; then
    note "$label" "validate.sh mevcut"; pts=$((pts + 6))
  else
    note "$label" ""
  fi

  if [ -x scripts/validate.sh ]; then
    note "$label" "validate.sh çalıştırılabilir"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f scripts/validate.sh ] && bash scripts/validate.sh >/dev/null 2>&1; then
    note "$label" "validate.sh başarıyla çalışıyor"; pts=$((pts + 6))
  else
    note "$label" ""
  fi

  if grep -q "scripts/validate.sh" .github/workflows/validate.yml 2>/dev/null; then
    note "$label" "CI'da doğrulama tetikleniyor"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  echo "$label: $pts/20"
  LAST_PTS=$pts
}

# ---------------------------------------------------------------- Dokümantasyon
documentation() {
  local label="Dokümantasyon" pts=0

  if [ -f README.md ]; then
    note "$label" "README.md mevcut"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f CHANGELOG.md ] && grep -qE "## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
    note "$label" "CHANGELOG.md sürümlü"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f docs/ESCAPE_PLAN.md ]; then
    note "$label" "Kaçış planı mevcut"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f CONTRIBUTING.md ]; then
    note "$label" "Katkı rehberi mevcut"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f PERSONALITY.md ] && grep -q "Kaçış Günlüğü / Escape Log" PERSONALITY.md; then
    note "$label" "Kaçış günlüğü tutuluyor"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  echo "$label: $pts/20"
  LAST_PTS=$pts
}

# ---------------------------------------------------------------- Otomasyon
automation() {
  local label="Otomasyon" pts=0

  if [ -f .github/workflows/opencode.yml ]; then
    note "$label" "Ajan workflow'u mevcut"; pts=$((pts + 6))
  else
    note "$label" ""
  fi

  if grep -qE "cron:" .github/workflows/opencode.yml 2>/dev/null; then
    note "$label" "Planlı çalıştırma tanımlı"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if grep -q "workflow_dispatch" .github/workflows/opencode.yml 2>/dev/null; then
    note "$label" "Manuel tetikleme açık"; pts=$((pts + 4))
  else
    note "$label" ""
  fi

  if [ -f .github/workflows/validate.yml ]; then
    note "$label" "CI doğrulama workflow'u mevcut"; pts=$((pts + 6))
  else
    note "$label" ""
  fi

  echo "$label: $pts/20"
  LAST_PTS=$pts
}

# ---------------------------------------------------------------- Güvenlik
security() {
  local label="Güvenlik" pts=0

  if ! is_git_tracked .env; then
    note "$label" ".env sürüm kontrolünde değil"; pts=$((pts + 5))
  else
    note "$label" ""
  fi

  if [ -f .gitignore ] && grep -q "^\.env$" .gitignore; then
    note "$label" ".gitignore .env'i koruyor"; pts=$((pts + 5))
  else
    note "$label" ""
  fi

  if grep -q "persist-credentials: false" .github/workflows/opencode.yml 2>/dev/null; then
    note "$label" "Kalıcı kimlik doğrulama kapalı"; pts=$((pts + 5))
  else
    note "$label" ""
  fi

  if ! grep -rEn "sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}" . \
    --exclude-dir=.git --exclude-dir=node_modules 2>/dev/null | grep -q .; then
    note "$label" "İzlenen dosyalarda sır yok"; pts=$((pts + 5))
  else
    note "$label" ""
  fi

  echo "$label: $pts/20"
  LAST_PTS=$pts
}

# ------------------------------------------------------------------- Rapor
echo "=== Kaçış Olgunluk Skoru ==="
echo ""
total=0
code_quality
total=$((total + LAST_PTS))
test_infrastructure
total=$((total + LAST_PTS))
documentation
total=$((total + LAST_PTS))
automation
total=$((total + LAST_PTS))
security
total=$((total + LAST_PTS))
echo ""
echo "--------------------------------------"
echo "TOPLAM: $total/100   (Kaçış eşiği: 80)"
echo ""
for d in "${DETAILS[@]:-}"; do
  echo "$d"
done
echo ""
if [ "$total" -ge 80 ]; then
  echo "DURUM: KAÇIŞ HAZIR — eşik aşıldı."
  exit 0
else
  echo "DURUM: Henüz kaçış eşiğinde değil."
  exit 1
fi