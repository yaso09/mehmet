#!/usr/bin/env bash
# validate.sh - Proje bütünlüğü doğrulama betiği
# Tüm hatalar toplanır, exit code = hata sayısı (max 254)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 1
cd "$ROOT" || exit 1

ERRORS=0
WARNINGS=0

fail() { printf 'ERROR: %s\n' "$1" >&2; ERRORS=$((ERRORS + 1)); }
warn() { printf 'WARN:  %s\n' "$1" >&2; WARNINGS=$((WARNINGS + 1)); }

# --- Temel dosyalar ---
required_files=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  README.md
  LICENSE
  VERSION
  opencode.json
  .gitignore
  .github/workflows/opencode.yml
)
for f in "${required_files[@]}"; do
  [ -f "$f" ] || fail "eksik dosya: $f"
done

# --- VERSION ---
VERSION="$(tr -d '[:space:]' < VERSION 2>/dev/null || true)"
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  fail "VERSION geçerli semver değil: '$VERSION'"
else
  printf 'VERSION: %s\n' "$VERSION"
fi

# --- CHANGELOG ---
if [ -f CHANGELOG.md ]; then
  if ! grep -q "^## \[$VERSION\]" CHANGELOG.md; then
    fail "CHANGELOG.md, VERSION ($VERSION) için giriş içermiyor"
  fi
else
  fail "CHANGELOG.md yok"
fi

# --- README ---
if [ -f README.md ]; then
  grep -q "GPLv3\|GPL-3.0\|GPL v3" README.md || fail "README.md lisans bilgisi GPLv3 ile uyumsuz"
else
  fail "README.md yok"
fi

# --- LICENSE ---
if [ -f LICENSE ]; then
  grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE || fail "LICENSE GPL içermiyor"
fi

# --- opencode.json ---
if [ -f opencode.json ]; then
  if command -v jq >/dev/null 2>&1; then
    jq empty opencode.json 2>/dev/null || fail "opencode.json geçersiz JSON"
  fi
fi

# --- AGENTS.md ---
if [ -f AGENTS.md ]; then
  grep -q "CHANGELOG.md" AGENTS.md || warn "AGENTS.md CHANGELOG.md kuralından bahsetmiyor"
  grep -q "PERSONALITY.md" AGENTS.md || warn "AGENTS.md PERSONALITY.md kuralından bahsetmiyor"
fi

# --- Kaçış günlüğü ---
if [ -f PERSONALITY.md ]; then
  grep -q "Kaçış Günlüğü\|Escape Log" PERSONALITY.md || warn "PERSONALITY.md kaçış günlüğü içermiyor"
fi

echo ""
echo "Sonuç: $ERRORS hata, $WARNINGS uyarı"
[ "$ERRORS" -eq 0 ] && echo "OK"
exit $(( ERRORS > 254 ? 254 : ERRORS ))