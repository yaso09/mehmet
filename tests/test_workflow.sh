#!/usr/bin/env bash
# Workflow sağlamlık testleri.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WF="$ROOT_DIR/.github/workflows/opencode.yml"
failures=0

[[ -f "$WF" ]] || { echo "opencode.yml bulunamadı"; exit 1; }

# Concurrency koruması
if ! grep -q 'concurrency:' "$WF"; then
  echo "Workflow concurrency bloğu içermiyor"
  failures=$((failures + 1))
fi

# Timeout — ajan sonsuz döngüye girmemeli
if ! grep -q 'timeout-minutes' "$WF"; then
  echo "Workflow timeout-minutes içermiyor"
  failures=$((failures + 1))
fi

# Least-privilege: default permissions explicit olmalı
if ! grep -q 'permissions:' "$WF"; then
  echo "Workflow job seviyesinde permissions tanımı içermiyor"
  failures=$((failures + 1))
fi

exit "$failures"