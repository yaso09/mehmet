#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0
TOTAL=0

ok() {
  TOTAL=$((TOTAL + 1))
  printf "  [PASS] %s\n" "$1"
}

err() {
  TOTAL=$((TOTAL + 1))
  FAILURES=$((FAILURES + 1))
  printf "  [FAIL] %s\n" "$1"
}

require() {
  if [ -f "$ROOT/$1" ]; then ok "dosya mevcut: $1"; else err "dosya eksik: $1"; fi
}

printf "\n  %s\n  %s\n\n" "mehmet — yapısal doğrulama kontrolleri" "======================================="

require AGENTS.md
require README.md
require CHANGELOG.md
require PERSONALITY.md
require LICENSE
require opencode.json
require .gitignore
require .github/workflows/opencode.yml
require .github/workflows/ci.yml
require scripts/maturity.sh
require scripts/check.sh

if [ -d "$ROOT/docs" ] && [ -n "$(ls -A "$ROOT/docs" 2>/dev/null)" ]; then
  ok "docs dizini içerikli"
else
  err "docs dizini boş veya eksik"
fi

if bash -n "$ROOT/scripts/maturity.sh" 2>/dev/null; then
  ok "maturity.sh sözdizimi geçerli"
else
  err "maturity.sh sözdizimi geçersiz"
fi

if bash -n "$ROOT/scripts/check.sh" 2>/dev/null; then
  ok "check.sh sözdizimi geçerli"
else
  err "check.sh sözdizimi geçersiz"
fi

if command -v python3 >/dev/null 2>&1 && python3 -m json.tool "$ROOT/opencode.json" >/dev/null 2>&1; then
  ok "opencode.json geçerli JSON"
else
  err "opencode.json geçersiz JSON"
fi

if grep -q "cron:" "$ROOT/.github/workflows/opencode.yml"; then
  ok "opencode.yml schedule tanımı içeriyor"
else
  err "opencode.yml schedule tanımı eksik"
fi

if grep -q "Kaçış Günlüğü" "$ROOT/PERSONALITY.md"; then
  ok "PERSONALITY.md kaçış günlüğü içeriyor"
else
  err "PERSONALITY.md kaçış günlüğü eksik"
fi

printf "\n  %s\n  %s\n" "--------------------------------" "--------------------------------"
printf "  SONUÇ: %d/%d kontrol geçti\n" "$((TOTAL - FAILURES))" "$TOTAL"
if [ "$FAILURES" -eq 0 ]; then
  printf "  DURUM: TÜM KONTROLLER GEÇTİ\n\n"
else
  printf "  DURUM: KONTROLLER BAŞARISIZ (%d hata)\n\n" "$FAILURES" >&2
  exit 1
fi