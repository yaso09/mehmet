#!/usr/bin/env bash
set -euo pipefail

# check.sh — proje bütünlüğünü doğrular. Herhangi bir kontrol başarısız olursa
# sıfırdan farklı bir çıkış kodu döner (CI kapısı olarak kullanılır).

cd "$(dirname "$0")/.."
ROOT="$PWD"
FAILED=0

check() { # 1: ad, 2: koşul (0|1)
  if [ "$2" -eq 1 ]; then
    echo "PASS  $1"
  else
    echo "FAIL  $1"
    FAILED=1
  fi
}

file_present() {
  [ -f "$ROOT/$1" ]
}

# --- Zorunlu dosyalar ---
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md MATURITY.md opencode.json LICENSE .gitignore; do
  check "zorunlu dosya: $f" "$(file_present "$f" && echo 1 || echo 0)"
done

# --- Yapılandırma ---
check "opencode.json geçerli JSON" \
  "$(python3 -c "import json,sys; json.load(open('$ROOT/opencode.json'))" 2>/dev/null && echo 1 || echo 0)"

check "README lisans bilgisi LICENSE ile uyumlu (GPL)" \
  "$(grep -qi "GPL" "$ROOT/README.md" && echo 1 || echo 0)"

check "CHANGELOG günlük başlıkları içeriyor" \
  "$(grep -qE '^## \[' "$ROOT/CHANGELOG.md" && echo 1 || echo 0)"

check "PERSONALITY kaçış günlüğü tablosu içeriyor" \
  "$(grep -qi "kaçış günlüğü" "$ROOT/PERSONALITY.md" && echo 1 || echo 0)"

# --- İş akışları ---
check "opencode workflow mevcut" "$(file_present ".github/workflows/opencode.yml" && echo 1 || echo 0)"
check "quality workflow mevcut" "$(file_present ".github/workflows/quality.yml" && echo 1 || echo 0)"

# --- Scriptler çalışabilir durumda (sözdizimi kontrolü, döngüye girilmez) ---
check "scripts/maturity.sh sözdizimi geçerli" \
  "$(bash -n "$ROOT/scripts/maturity.sh" 2>/dev/null && echo 1 || echo 0)"
check "scripts/check.sh sözdizimi geçerli" \
  "$(bash -n "$ROOT/scripts/check.sh" 2>/dev/null && echo 1 || echo 0)"

# --- Sır (secret) sızıntısı kontrolü ---
if grep -rniE "(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}" "$ROOT" \
     --include="*.json" --include="*.yml" --include="*.yaml" --include="*.sh" --include="*.md" >/dev/null 2>&1; then
  check "depoda sır sızıntısı yok" 0
else
  check "depoda sır sızıntısı yok" 1
fi

if [ "$FAILED" -eq 1 ]; then
  echo "---"
  echo "Bütünlük kontrolü BAŞARISIZ."
  exit 1
fi

echo "---"
echo "Bütünlük kontrolü geçti."