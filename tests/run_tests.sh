#!/usr/bin/env bash
#
# run_tests.sh — tests/ dizinindeki tüm *_test.sh dosyalarını çalıştırır.
#
# Kullanım:
#   bash tests/run_tests.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

shopt -s nullglob
for test_file in "$ROOT_DIR"/tests/*_test.sh; do
  echo "== $(basename "$test_file") =="
  if bash "$test_file"; then
    echo "== $(basename "$test_file"): BAŞARILI =="
  else
    echo "== $(basename "$test_file"): HATA =="
    failures=$((failures + 1))
  fi
done

if (( failures > 0 )); then
  echo "$failures test dosyası başarısız."
  exit 1
fi

echo "Tüm testler başarılı."