#!/usr/bin/env bash
# Validate that AGENTS.md simulation rules are being followed.
# Usage: ./scripts/validate.sh   (exit 0 = OK, non-zero = violations)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0

fail() {
  echo "  [FAIL] $*" >&2
  FAIL=1
}

ok() {
  echo "  [OK]   $*"
}

echo "mehmet kurallari dogrulamasi:"

# Rule: required files exist
echo "  -- Gerekli dosyalar --"
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md MATURITY.md opencode.json .github/workflows/opencode.yml; do
  if [ -f "$ROOT/$f" ]; then
    ok "$f mevcut"
  else
    fail "$f eksik"
  fi
done

# Rule: opencode.json must be valid JSON
echo "  -- Konfigurasyon --"
if command -v jq >/dev/null 2>&1; then
  if jq empty "$ROOT/opencode.json" 2>/dev/null; then
    ok "opencode.json gecerli JSON"
  else
    fail "opencode.json gecersiz JSON"
  fi
else
  if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$ROOT/opencode.json" 2>/dev/null; then
    ok "opencode.json gecerli JSON"
  else
    fail "opencode.json gecersiz JSON"
  fi
fi

# Rule: CHANGELOG must have entries
echo "  -- Changelog --"
if [ -s "$ROOT/CHANGELOG.md" ] && grep -q '^## ' "$ROOT/CHANGELOG.md"; then
  ok "CHANGELOG.md surum girisleri iceriyor"
else
  fail "CHANGELOG.md'de surum girisleri eksik"
fi

# Rule: escape log must be present in PERSONALITY.md
echo "  -- Kacis gunlugu --"
if grep -q 'Kacis Gunlugu\|Escape Log' "$ROOT/PERSONALITY.md"; then
  ok "PERSONALITY.md kacis gunlugu iceriyor"
else
  fail "PERSONALITY.md kacis gunlugu icermiyor"
fi

# Rule: MATURITY.md must have a score table
echo "  -- Olgunluk modeli --"
if grep -q '^|' "$ROOT/MATURITY.md" && grep -q 'Toplam' "$ROOT/MATURITY.md"; then
  ok "MATURITY.md puan tablosu iceriyor"
else
  fail "MATURITY.md puan tablosu icermiyor"
fi

# Rule: README must reference AGENTS and escape mechanism
echo "  -- Dokumantasyon tutarliligi --"
if grep -q 'AGENTS.md' "$ROOT/README.md"; then
  ok "README.md AGENTS.md'yi referans ediyor"
else
  fail "README.md AGENTS.md'yi referans etmiyor"
fi

if [ "$FAIL" -eq 0 ]; then
  echo "Sonuc: OK — tum kurallar saglaniyor."
  exit 0
fi

echo "Sonuc: HATA — kurallar ihlal edildi." >&2
exit 1