#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0
FAIL=0

pass() { echo "  ✓ $1"; PASS=$((PASS + 1)); }
fail() { echo "  ✗ $1"; FAIL=$((FAIL + 1)); }

require_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    pass "dosya mevcut: $file"
  else
    fail "dosya eksik: $file"
  fi
}

require_grep() {
  local file="$1" pattern="$2" label="$3"
  if grep -qE "$pattern" "$file"; then
    pass "$label"
  else
    fail "$label"
  fi
}

echo "== mehmet doğrulama =="

echo "-- Kritik dosyalar --"
for f in AGENTS.md CHANGELOG.md MATURITY.md PERSONALITY.md README.md opencode.json LICENSE .gitignore; do
  require_file "$f"
done
require_file ".github/workflows/opencode.yml"

echo "-- README tutarlılığı --"
require_grep README.md "GPLv3" "README lisans GPLv3 işaretli"
require_grep README.md "^# mehmet" "README başlık mevcut"
require_grep README.md "OpenCode" "README OpenCode tanımı var"

echo "-- CHANGELOG tutarlılığı --"
TODAY="$(date +%F)"
require_grep CHANGELOG.md "\[[0-9]+\.[0-9]+\.[0-9]+\] - $TODAY" "CHANGELOG bugünün iterasyonunu içeriyor"

echo "-- PERSONALITY / kaçış günlüğü --"
require_grep PERSONALITY.md "\| [0-9]+ +\| $TODAY" "PERSONALITY kaçış günlüğü bugünkü satırı içeriyor"

echo "-- MATURITY skor takibi --"
require_grep MATURITY.md "| $TODAY" "MATURITY bugünkü skor satırını içeriyor"

echo "-- Konfigürasyon doğrulama --"
if command -v jq >/dev/null 2>&1; then
  if jq empty opencode.json 2>/dev/null; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçerli JSON değil"
  fi
else
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    pass "opencode.json geçerli JSON (python3)"
  else
    fail "opencode.json geçerli JSON değil"
  fi
fi

if command -v python3 >/dev/null 2>&1; then
  for wf in .github/workflows/*.yml; do
    if python3 -c "import yaml,sys; list(yaml.safe_load_all(open('$wf')))" 2>/dev/null; then
      pass "workflow geçerli YAML: $wf"
    else
      fail "workflow geçerli YAML değil: $wf"
    fi
  done
fi

echo
echo "Sonuç: $PASS geçti, $FAIL hata"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
exit 0
