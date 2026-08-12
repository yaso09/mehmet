#!/usr/bin/env bash
# mehmet — Proje bütünlük doğrulayıcı.
# Kaçış hedefi (test altyapısı) için gereken dosyaların varlığını ve
# içerik tutarlılığını kontrol eder. CI'da `validate` job'ında çalıştırılır.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0

check_file() {
  if [[ -f "$1" ]]; then
    echo "[OK]   $1 mevcut"
  else
    echo "[FAIL] $1 bulunamadı"
    fail=1
  fi
}

check_in() {
  local file="$1" pattern="$2" label="$3"
  if grep -qi "$pattern" "$file"; then
    echo "[OK]   $label"
  else
    echo "[FAIL] $label"
    fail=1
  fi
}

echo "== Dosya yapısı =="
check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "LICENSE"
check_file ".gitignore"
check_file "opencode.json"
check_file ".github/workflows/opencode.yml"
check_file "scripts/validate.sh"
check_file "scripts/maturity.sh"

echo "== Konfigürasyon =="
if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
  echo "[OK]   opencode.json geçerli JSON"
else
  echo "[FAIL] opencode.json geçerli JSON değil"
  fail=1
fi

echo "== İçerik tutarlılığı =="
check_in "README.md" "GPLv3" "README.md lisans bilgisi (GPLv3)"
check_in "PERSONALITY.md" "Kaçış Günlüğü" "PERSONALITY.md kaçış günlüğü mevcut"
check_in "AGENTS.md" "CHANGELOG" "AGENTS.md kuralları CHANGELOG referansı veriyor"
check_in ".github/workflows/opencode.yml" "schedule" "workflow schedule tetikleyicisi"
check_in ".github/workflows/opencode.yml" "timeout-minutes" "workflow job timeout-minutes"
check_in ".github/workflows/opencode.yml" "concurrency" "workflow concurrency kontrolü"
check_in ".github/workflows/opencode.yml" "validate" "workflow validate job'ı"

if [[ -s CHANGELOG.md ]]; then
  echo "[OK]   CHANGELOG.md dolu"
else
  echo "[FAIL] CHANGELOG.md boş"
  fail=1
fi

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "VALIDATION PASSED"
  exit 0
else
  echo "VALIDATION FAILED"
  exit 1
fi