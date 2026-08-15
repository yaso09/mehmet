#!/usr/bin/env bash
# verify-project.sh - mehmet proje bütünlüğünü doğrular.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check_file() {
  local path="$1"
  if [ -f "$path" ]; then
    echo "[OK] $path"
  else
    echo "[FAIL] $path eksik"
    failures=$((failures + 1))
  fi
}

check_grep() {
  local pattern="$1" file="$2" label="$3"
  if grep -q "$pattern" "$file"; then
    echo "[OK] $label"
  else
    echo "[FAIL] $label ($file)"
    failures=$((failures + 1))
  fi
}

echo "== Dosya bütünlüğü =="
check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "MATURITY.md"
check_file "LICENSE"
check_file "opencode.json"
check_file ".github/workflows/opencode.yml"
check_file "scripts/verify-project.sh"

echo "== Tutarlılık =="
check_grep "GPLv3" "README.md" "README lisansı GPLv3 ile tutarlı"
check_grep "Kaçış Günlüğü" "PERSONALITY.md" "Kaçış günlüğü mevcut"
check_grep "## \[" "CHANGELOG.md" "CHANGELOG girişi mevcut"
check_grep "Kaçış Eşiği" "MATURITY.md" "Maturity eşiği tanımlı"

echo "== opencode.json geçerliliği =="
if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
  echo "[OK] opencode.json geçerli JSON"
else
  echo "[FAIL] opencode.json geçerli JSON değil"
  failures=$((failures + 1))
fi

echo ""
if [ "$failures" -gt 0 ]; then
  echo "Sonuç: $failures sorun bulundu."
  exit 1
fi
echo "Sonuç: tüm kontroller geçti."