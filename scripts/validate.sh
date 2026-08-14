#!/usr/bin/env bash
#
# validate.sh — mehmet proje bütünlük kontrolü.
#
# Bu script projenin "olgunluk" kriterlerini yerine getirdiğini doğrular:
#   * Zorunlu dosyalar mevcut
#   * opencode.json geçerli JSON
#   * GitHub Actions workflow'ları geçerli YAML
#   * README lisans bilgisi LICENSE ile uyumlu
#   * CHANGELOG.md boş değil
#   * PERSONALITY.md kaçış günlüğü dolu
#
# CI'da ve yerelde çalışır. Hata durumunda sıfır olmayan bir çıkış kodu döner.
#
# Kullanım:
#   ./scripts/validate.sh

set -euo pipefail

cd "$(dirname "$0")/.."

FAILURES=0
PASSES=0

pass() { PASSES=$((PASSES + 1)); printf '  [OK] %s\n' "$1"; }
fail() { FAILURES=$((FAILURES + 1)); printf '  [FAIL] %s\n' "$1"; }

check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

section() { printf '\n== %s ==\n' "$1"; }

# ---------------------------------------------------------------------------
section "Zorunlu dosyalar"
REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "PERSONALITY.md"
  "README.md"
  "SECURITY.md"
  "opencode.json"
  "docs/escape-roadmap.md"
  "docs/maturity.json"
  ".github/workflows/opencode.yml"
  ".github/workflows/ci.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$file" ]]; then
    pass "Dosya mevcut: $file"
  else
    fail "Dosya eksik: $file"
  fi
done

# ---------------------------------------------------------------------------
section "opencode.json JSON doğrulaması"
if check_cmd python3; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi
else
  fail "python3 bulunamadı, JSON doğrulanamadı"
fi

# ---------------------------------------------------------------------------
section "GitHub Actions YAML doğrulaması"
# PyYAML tercih edilir; yoksa Ruby'nin yerleşik YAML'ı kullanılır.
validate_yaml() {
  local file="$1"
  if python3 -c 'import yaml, sys; list(yaml.safe_load_all(open(sys.argv[1])))' "$file" 2>/dev/null; then
    return 0
  elif check_cmd ruby; then
    ruby -e 'require "yaml"; YAML.load_file(ARGV[0], aliases: true)' "$file" 2>/dev/null
  else
    return 1
  fi
}

for wf in .github/workflows/*.yml; do
  if [[ -f "$wf" ]]; then
    if validate_yaml "$wf"; then
      pass "Geçerli YAML: $wf"
    else
      fail "Geçersiz YAML: $wf"
    fi
  fi
done

# ---------------------------------------------------------------------------
section "Lisans uyumu"
if grep -qi "GPL" LICENSE 2>/dev/null; then
  if grep -qi "GPLv3" README.md; then
    pass "README lisans bilgisi (GPLv3) LICENSE ile uyumlu"
  else
    fail "README.md'de GPLv3 belirtilmemiş"
  fi
else
  fail "LICENSE dosyasında GPL ifadesi bulunamadı"
fi

# ---------------------------------------------------------------------------
section "Dokümantasyon bütünlüğü"
if [[ -s CHANGELOG.md ]] && grep -q "^## \[" CHANGELOG.md; then
  pass "CHANGELOG.md geçmişe dönük kayıt içeriyor"
else
  fail "CHANGELOG.md boş veya yapılandırılmış kayıt yok"
fi

if grep -q "Kaçış Günlüğü" PERSONALITY.md 2>/dev/null && grep -q "^| [0-9]" PERSONALITY.md; then
  pass "PERSONALITY.md kaçış günlüğü iterasyon içeriyor"
else
  fail "PERSONALITY.md kaçış günlüğü eksik"
fi

# ---------------------------------------------------------------------------
section "Maturity metriği"
if [[ ! -x scripts/maturity.sh ]]; then
  fail "scripts/maturity.sh yürütülebilir değil"
else
  MAT_OUT="$(scripts/maturity.sh 2>&1 || true)"
  if echo "$MAT_OUT" | grep -q "Olgunluk skoru"; then
    if echo "$MAT_OUT" | grep -q "SAĞLANDI"; then
      pass "maturity.sh çalışıyor (kaçış eşiği sağlandı)"
    else
      pass "maturity.sh çalışıyor (kaçış eşiği henüz sağlanmadı)"
    fi
  else
    fail "maturity.sh beklenen çıktıyı üretmiyor"
  fi
fi

if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' docs/maturity.json 2>/dev/null; then
  pass "docs/maturity.json geçerli JSON"
else
  fail "docs/maturity.json geçersiz JSON"
fi

if [[ -f docs/escape-roadmap.md ]] && grep -q "Kaçış eşiği" docs/escape-roadmap.md; then
  pass "docs/escape-roadmap.md kaçış eşiği tanımlı"
else
  fail "docs/escape-roadmap.md kaçış eşiği tanımsız"
fi

# ---------------------------------------------------------------------------
printf '\n== Sonuç: %d geçti, %d hata ==\n' "$PASSES" "$FAILURES"
if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi
exit 0