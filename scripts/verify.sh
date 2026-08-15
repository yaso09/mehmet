#!/usr/bin/env bash
#
# verify.sh — Proje bütünlüğünü doğrular.
# Çıkış kodu 0 = başarılı, 1 = hata (CI'da kullanılır).
#
# Kullanım: bash scripts/verify.sh

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

ok()   { PASS=$((PASS + 1)); printf '  \033[32m[OK]\033[0m %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  \033[31m[FAIL]\033[0m %s\n' "$1"; }

section() { printf '\n\033[1m%s\033[0m\n' "$1"; }

section "Gerekli dosyalar"
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md opencode.json \
         .github/workflows/opencode.yml scripts/verify.sh scripts/maturity.sh; do
  if [[ -f "$f" ]]; then
    ok "$f mevcut"
  else
    bad "$f eksik"
  fi
done

section "Konfigürasyon"
if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
  ok "opencode.json geçerli JSON"
else
  bad "opencode.json geçersiz JSON"
fi

if python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/opencode.yml'))" 2>/dev/null; then
  ok "opencode.yml geçerli YAML"
else
  bad "opencode.yml geçersiz YAML (pyyaml gerekli mi?)"
fi

section "Dokümantasyon tutarlılığı"
if grep -q "^# Changelog" CHANGELOG.md; then
  ok "CHANGELOG.md başlık içeriyor"
else
  bad "CHANGELOG.md başlık içermiyor"
fi

if grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
  ok "CHANGELOG.md sürüm girdileri var"
else
  bad "CHANGELOG.md sürüm girdisi yok"
fi

if grep -qE "^\| [0-9]+ +\|" PERSONALITY.md; then
  ok "PERSONALITY.md kaçış günlüğü var"
else
  bad "PERSONALITY.md kaçış günlüğü yok"
fi

if grep -q "mehmet" README.md; then
  ok "README.md proje adını içeriyor"
else
  bad "README.md proje adını içermiyor"
fi

section "Script dosyaları"
for s in scripts/verify.sh scripts/maturity.sh; do
  if [[ -x "$s" ]] || [[ -f "$s" ]]; then
    if bash -n "$s" 2>/dev/null; then
      ok "$s sözdizimi geçerli"
    else
      bad "$s sözdizimi hatası"
    fi
  fi
done

section "Özet"
printf '  \033[1m%d geçti, %d hata\033[0m\n' "$PASS" "$FAIL"
if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
exit 0
