#!/usr/bin/env bash
#
# mehmet test suite — scripts/validate.sh ve scripts/maturity.sh davranışlarını test eder.
#
# Kullanım: bash scripts/test.sh
# Çıkış kodu: 0 = tüm testler geçti, 1 = en az bir test başarısız

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASSED=0
FAILED=0

pass() { printf '[ PASS ] %s\n' "$*"; PASSED=$((PASSED + 1)); }
fail() { printf '[ FAIL ] %s\n' "$*"; FAILED=$((FAILED + 1)); }

section() { printf '\n== %s ==\n' "$*"; }

section "validate.sh — sağlıklı repo"

if bash "$ROOT_DIR/scripts/validate.sh" >/dev/null 2>&1; then
  pass "Sağlıklı repoda çıkış kodu 0"
else
  fail "Sağlıklı repoda çıkış kodu 0 olmalı"
fi

OUTPUT=$(bash "$ROOT_DIR/scripts/validate.sh")
case "$OUTPUT" in
  *"Repo sağlıklı"*) pass "Başarı mesajı üretiyor" ;;
  *) fail "Başarı mesajı bekleniyor ('Repo sağlıklı')" ;;
esac

section "validate.sh — bozuk repoyu yakalar"

TMP_DIR=$(mktemp -d)
mkdir -p "$TMP_DIR/.github/workflows" "$TMP_DIR/scripts"
cp "$ROOT_DIR/scripts/validate.sh" "$TMP_DIR/scripts/"
touch "$TMP_DIR/opencode.json"

if bash "$TMP_DIR/scripts/validate.sh" >/dev/null 2>&1; then
  fail "Eksik dosyalarla çıkış kodu 0 olmamalı"
else
  pass "Eksik dosyaları tespit ediyor (çıkış kodu 1)"
fi
rm -rf "$TMP_DIR"

section "maturity.sh — skor çıktısı"

SCORE_OUTPUT=$(bash "$ROOT_DIR/scripts/maturity.sh")
case "$SCORE_OUTPUT" in
  *"Olgunluk Skoru"*) pass "Skor satırı üretiyor" ;;
  *) fail "Skor satırı bekleniyor" ;;
esac
case "$SCORE_OUTPUT" in
  *"Seviye"*) pass "Seviye satırı üretiyor" ;;
  *) fail "Seviye satırı bekleniyor" ;;
esac

section "maturity.sh --write — MATURITY.md üretir"

MATURITY_TMP=$(mktemp -d)
OLD_MATURITY=""
if [[ -f "$ROOT_DIR/MATURITY.md" ]]; then
  OLD_MATURITY=$(cat "$ROOT_DIR/MATURITY.md")
fi

bash "$ROOT_DIR/scripts/maturity.sh" --write >/dev/null 2>&1

if [[ -f "$ROOT_DIR/MATURITY.md" ]]; then
  pass "MATURITY.md oluşturuluyor"
  grep -q "Olgunluk Skoru" "$ROOT_DIR/MATURITY.md" && pass "MATURITY.md skor içeriyor" || fail "MATURITY.md skor içermiyor"
else
  fail "MATURITY.md oluşturulamadı"
fi

if [[ -n "$OLD_MATURITY" ]]; then
  printf '%s\n' "$OLD_MATURITY" > "$ROOT_DIR/MATURITY.md"
fi
rm -rf "$MATURITY_TMP"

printf '\n== Sonuç ==\n'
printf 'Geçen: %d | Başarısız: %d\n' "$PASSED" "$FAILED"

if [[ "$FAILED" -gt 0 ]]; then
  exit 1
fi
exit 0