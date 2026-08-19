#!/usr/bin/env bash
set -uo pipefail

# Test: validate.sh temiz bir projede başarıyla çalışır (çıkış kodu 0).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if "$ROOT/scripts/validate.sh" >/dev/null 2>&1; then
  echo "validate.sh temiz projede geçti."
else
  echo "HATA: validate.sh temiz projede başarısız oldu."
  exit 1
fi