#!/usr/bin/env bash
set -uo pipefail

# validate.sh — proje bütünlüğünü ve tutarlılığını doğrular.
# CI'da (validate workflow'u) ve her iterasyonda çalıştırılır.
# Herhangi bir kontrol başarısız olursa sıfır olmayan çıkış kodu döner.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0

check() {
  local name="$1"
  local result="$2"
  if [[ "$result" -eq 0 ]]; then
    printf '  [OK]   %s\n' "$name"
  else
    printf '  [FAIL] %s\n' "$name"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "Proje doğrulaması başladı: $ROOT"

# 1. opencode.json geçerli JSON olmalı
if command -v python3 >/dev/null 2>&1; then
  python3 -m json.tool "$ROOT/opencode.json" >/dev/null 2>&1
  check "opencode.json geçerli JSON" $?
else
  node -e "JSON.parse(require('fs').readFileSync('$ROOT/opencode.json','utf8'))" >/dev/null 2>&1
  check "opencode.json geçerli JSON" $?
fi

# 2. Workflow YAML dosyaları geçerli olmalı (sözdizimi kontrolü)
for wf in "$ROOT"/.github/workflows/*.yml; do
  [[ -f "$wf" ]] || continue
  base="$(basename "$wf")"
  python3 -c "import yaml,sys; yaml.safe_load(open('$wf'))" >/dev/null 2>&1
  check "$base YAML sözdizimi" $?
done

# 3. Çekirdek dosyalar mevcut olmalı
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json; do
  [[ -f "$ROOT/$f" ]]
  check "$f mevcut" $?
done

# 4. README zorunlu bölümleri içermeli
for section in "Özellikler" "Kurulum" "Lisans"; do
  grep -q "$section" "$ROOT/README.md" 2>/dev/null
  check "README '$section' bölümü" $?
done

# 5. Scriptler shellcheck ile doğrulanmalı
if command -v shellcheck >/dev/null 2>&1; then
  for s in "$ROOT"/scripts/*.sh; do
    [[ -f "$s" ]] || continue
    shellcheck "$s" >/dev/null 2>&1
    check "$(basename "$s") shellcheck" $?
  done
fi

echo ""
if [[ "$FAILURES" -eq 0 ]]; then
  echo "Doğrulama başarılı — tüm kontroller geçti."
  exit 0
else
  echo "Doğrulama başarısız — $FAILURES kontrol hatası."
  exit 1
fi