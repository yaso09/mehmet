#!/usr/bin/env bash
# Güvenlik testleri — depoda sır bulunmamalı.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

# Potansiyel API anahtarı / sır kalıpları.
# Not: Secret ADININ referansı (ör. `OPENCODE_API_KEY`) meşrudur; yalnızca
# gerçek anahtar değerleri ya da sabitlenmiş (literal) anahtar ataması aranır.
SECRET_PATTERN='(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|OPENCODE_API_KEY[=:]["'"'"']?[A-Za-z0-9]{12,})'
EXPR_SECRET_REF="\\\${{ *secrets\\."
EXPR_DOC_EXAMPLE='OPENCODE_API_KEY.*Secrets.*olarak ekle'

if grep -rInE "$SECRET_PATTERN" \
    --include='*.sh' --include='*.json' --include='*.yml' --include='*.yaml' \
    --include='*.md' --include='*.toml' --include='*.py' "$ROOT_DIR" \
    | grep -v "$EXPR_SECRET_REF" | grep -v "$EXPR_DOC_EXAMPLE" ; then
  echo "Depoda potansiyel sır bulundu"
  failures=$((failures + 1))
fi

# .gitignore temel güvenlik girdilerini içermeli
for pattern in '.env' '*.log'; do
  if ! grep -qF "$pattern" "$ROOT_DIR/.gitignore"; then
    echo ".gitignore eksik girdi: $pattern"
    failures=$((failures + 1))
  fi
done

exit "$failures"