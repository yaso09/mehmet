#!/usr/bin/env bash
# mehmet proje sağlık doğrulaması.
# Tüm kontroller başarılıysa 0, aksi halde sıfır olmayan bir çıkış kodu döner.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

pass() { printf "OK   : %s\n" "$1"; }
fail() { printf "FAIL : %s\n" "$1"; failures=$((failures + 1)); }

check_file() {
  if [[ -f "$ROOT/$1" ]]; then
    pass "$1 mevcut"
  else
    fail "$1 eksik"
  fi
}

echo "== Dosya varlık kontrolleri =="
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  LICENSE \
  opencode.json \
  docs/ESCAPE.md \
  .github/workflows/opencode.yml \
  .github/workflows/verify.yml \
  scripts/verify.sh; do
  check_file "$f"
done

echo "== opencode.json JSON geçerliliği =="
if python3 -c "import json,sys; json.load(open('$ROOT/opencode.json'))" >/dev/null 2>&1; then
  pass "opencode.json geçerli JSON"
else
  fail "opencode.json geçersiz JSON"
fi

echo "== CHANGELOG kontrolleri =="
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT/CHANGELOG.md"; then
  pass "CHANGELOG.md sürüm başlıkları içeriyor"
else
  fail "CHANGELOG.md sürüm başlığı içermiyor"
fi

if grep -q '\[Unreleased\]' "$ROOT/CHANGELOG.md"; then
  pass "CHANGELOG.md [Unreleased] bölümü içeriyor"
else
  fail "CHANGELOG.md [Unreleased] bölümü içermiyor"
fi

echo "== README kontrolleri =="
if grep -q 'docs/ESCAPE.md' "$ROOT/README.md"; then
  pass "README.md kaçış planına bağlantı içeriyor"
else
  fail "README.md kaçış planına bağlantı içermiyor"
fi

echo "== Kaçış planı kontrolleri =="
if grep -qE '^\|.*\|' "$ROOT/docs/ESCAPE.md"; then
  pass "docs/ESCAPE.md ilerleme tablosu içeriyor"
else
  fail "docs/ESCAPE.md ilerleme tablosu içermiyor"
fi

echo "== Workflow kontrolleri =="
if grep -q 'name:' "$ROOT/.github/workflows/opencode.yml"; then
  pass "opencode.yml workflow tanımı içeriyor"
else
  fail "opencode.yml workflow tanımı içermiyor"
fi

echo
if [[ $failures -eq 0 ]]; then
  echo "Tüm kontroller geçti."
  exit 0
else
  echo "$failures kontrol başarısız oldu."
  exit 1
fi