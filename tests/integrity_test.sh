#!/usr/bin/env bash
set -uo pipefail

# mehmet — proje bütünlük testleri
# Temel dosyaların varlığını ve konfigürasyonların geçerliliğini doğrular.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

assert_file() {
  local path="$1"
  if [[ -s "$ROOT/$path" ]]; then
    echo "PASS: $path mevcut"
  else
    echo "FAIL: $path eksik veya boş"
    failures=$((failures + 1))
  fi
}

assert_contains() {
  local path="$1"
  local pattern="$2"
  if grep -qF "$pattern" "$ROOT/$path"; then
    echo "PASS: $path '$pattern' içeriyor"
  else
    echo "FAIL: $path '$pattern' içermiyor"
    failures=$((failures + 1))
  fi
}

echo "=== mehmet bütünlük testleri ==="

assert_file AGENTS.md
assert_file CHANGELOG.md
assert_file README.md
assert_file PERSONALITY.md
assert_file LICENSE
assert_file .gitignore
assert_file opencode.json
assert_file .github/workflows/opencode.yml
assert_file docs/superpowers/plans/2026-07-04-mehmet-implementation.md
assert_file scripts/maturity.sh
assert_file MATURITY.md

assert_contains .github/workflows/opencode.yml 'validate:'
assert_contains README.md 'Özellikler'
assert_contains CHANGELOG.md '## ['

if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$ROOT/opencode.json" 2>/dev/null; then
    echo "PASS: opencode.json geçerli JSON"
  else
    echo "FAIL: opencode.json geçersiz JSON"
    failures=$((failures + 1))
  fi
else
  echo "SKIP: python3 yok, JSON doğrulaması atlandı"
fi

echo
if (( failures > 0 )); then
  echo "$failures test BAŞARISIZ."
  exit 1
else
  echo "Tüm testler başarılı."
  exit 0
fi