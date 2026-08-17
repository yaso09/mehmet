#!/usr/bin/env bash
# Konfigürasyon dosyası geçerlilik testleri.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

# opencode.json geçerli JSON ve model alanı içermeli
if ! jq -e '.model' "$ROOT_DIR/opencode.json" >/dev/null 2>&1; then
  echo "opencode.json geçerli değil veya model alanı eksik"
  failures=$((failures + 1))
fi

# Workflow YAML dosyaları ayrıştırılabilir olmalı
for wf in "$ROOT_DIR"/.github/workflows/*.yml; do
  [[ -e "$wf" ]] || continue
  if ! yq e '.' "$wf" >/dev/null 2>&1; then
    echo "Geçersiz workflow YAML: $wf"
    failures=$((failures + 1))
  fi
done

# Workflow'ların tamamı boş jobs içermemeli
if ! grep -q 'jobs:' "$ROOT_DIR/.github/workflows/opencode.yml"; then
  echo "opencode.yml jobs tanımı içermiyor"
  failures=$((failures + 1))
fi

exit "$failures"