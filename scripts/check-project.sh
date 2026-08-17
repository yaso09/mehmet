#!/usr/bin/env bash
set -euo pipefail

# mehmet maturity checker
# Projenin olgunluk seviyesini ölçer ve kaçış mekanizması için skor üretir.
#
# Kullanım:
#   ./scripts/check-project.sh [proje_dizini] [--strict] [--json]

ROOT="${1:-.}"
STRICT=0
JSON=0
for arg in "${@:2}"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    --json) JSON=1 ;;
  esac
done

cd "$ROOT" || { echo "Hata: '$ROOT' dizini bulunamadı" >&2; exit 1; }

PASS=()
FAIL=()

pass() { PASS+=("$1"); }
fail() { FAIL+=("$1"); }

check_file() {
  if [[ -f "$1" ]]; then pass "$1 mevcut"; else fail "$1 eksik"; fi
}

# --- Kontrol listesi -------------------------------------------------------

check_file "AGENTS.md"
check_file "PERSONALITY.md"
check_file "CHANGELOG.md"
check_file "README.md"
check_file "LICENSE"
check_file "opencode.json"
check_file ".gitignore"
check_file ".github/workflows/opencode.yml"

if [[ -f "opencode.json" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
      pass "opencode.json geçerli JSON"
    else
      fail "opencode.json geçersiz JSON"
    fi
  else
    pass "opencode.json mevcut (JSON doğrulaması atlandı)"
  fi
fi

if command -v yq >/dev/null 2>&1 && [[ -f ".github/workflows/opencode.yml" ]]; then
  if yq eval '.' ".github/workflows/opencode.yml" >/dev/null 2>&1; then
    pass ".github/workflows/opencode.yml geçerli YAML"
  else
    fail ".github/workflows/opencode.yml geçersiz YAML"
  fi
fi

if grep -q "Kurulum" README.md 2>/dev/null && grep -q "Özellikler" README.md 2>/dev/null && grep -q "Lisans" README.md 2>/dev/null; then
  pass "README.md gerekli bölümleri içeriyor"
else
  fail "README.md gerekli bölümleri içermiyor (Kurulum/Özellikler/Lisans)"
fi

if grep -qE "^## \[" CHANGELOG.md 2>/dev/null; then
  pass "CHANGELOG.md sürüm girişleri içeriyor"
else
  fail "CHANGELOG.md sürüm girişi içermiyor"
fi

if grep -q "Kaçış Günlüğü" PERSONALITY.md 2>/dev/null; then
  pass "PERSONALITY.md kaçış günlüğü içeriyor"
else
  fail "PERSONALITY.md kaçış günlüğü içermiyor"
fi

ESCAPE_ENTRIES=$(grep -c "^| [0-9]" PERSONALITY.md 2>/dev/null || true)
if [[ "$ESCAPE_ENTRIES" -ge 3 ]]; then
  pass "Kaçış günlüğü en az 3 iterasyon içeriyor"
else
  fail "Kaçış günlüğü yetersiz (mevcut: ${ESCAPE_ENTRIES:-0})"
fi

if [[ -d "scripts" ]] && compgen -G "scripts/*.sh" >/dev/null; then
  pass "scripts/ dizini bash betikleri içeriyor"
else
  fail "scripts/ dizini bash betikleri içermiyor"
fi

if [[ -d "tests" ]] && compgen -G "tests/*.sh" >/dev/null; then
  pass "tests/ dizini test betikleri içeriyor"
else
  fail "tests/ dizini test betikleri içermiyor"
fi

if [[ -f ".github/workflows/validate.yml" ]]; then
  pass "Doğrulama workflow'u mevcut (.github/workflows/validate.yml)"
else
  fail "Doğrulama workflow'u eksik"
fi

if [[ -f "Makefile" ]]; then
  pass "Makefile mevcut"
else
  fail "Makefile eksik"
fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  pass "Git deposu mevcut"
else
  fail "Git deposu değil"
fi

if command -v shellcheck >/dev/null 2>&1; then
  if shellcheck scripts/*.sh tests/*.sh 2>/dev/null; then
    pass "Tüm bash betikleri shellcheck'ten geçiyor"
  else
    fail "Bash betikleri shellcheck hataları içeriyor"
  fi
else
  pass "shellcheck bulunamadı (doğrulama atlandı)"
fi

# --- Skorlama ----------------------------------------------------------------

TOTAL=$(( ${#PASS[@]} + ${#FAIL[@]} ))
SCORE=$(( (${#PASS[@]} * 100) / TOTAL ))
if (( SCORE >= 80 )); then
  GRADE="A"
elif (( SCORE >= 60 )); then
  GRADE="B"
elif (( SCORE >= 40 )); then
  GRADE="C"
else
  GRADE="F"
fi

if [[ "$JSON" -eq 1 ]]; then
  printf '{"total":%d,"passed":%d,"failed":%d,"score":%d,"grade":"%s","eligible_for_escape":%s}\n' \
    "$TOTAL" "${#PASS[@]}" "${#FAIL[@]}" "$SCORE" "$GRADE" \
    "$( [[ "$SCORE" -ge 80 ]] && echo true || echo false )"
else
  echo "--- mehmet maturity raporu ---"
  printf "Geçen: %d / %d\n" "${#PASS[@]}" "$TOTAL"
  for p in "${PASS[@]}"; do echo "  [OK] $p"; done
  for f in "${FAIL[@]}"; do echo "  [!!] $f"; done
  echo "Olgunluk skoru: $SCORE / 100 (not: $GRADE)"
  if (( SCORE >= 80 )); then
    echo "Kaçış kriteri karşılandı — proje kaçış için olgun."
  else
    echo "Kaçış kriteri karşılanmadı (gerekli: >= 80)."
  fi
fi

if (( SCORE < 80 )); then
  exit 1
fi

if [[ "$STRICT" -eq 1 && ${#FAIL[@]} -gt 0 ]]; then
  exit 1
fi

exit 0