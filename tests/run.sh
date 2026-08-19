#!/usr/bin/env bash
set -uo pipefail

# tests/run.sh — mehmet test çalıştırıcısı.
# tests/ altındaki tüm test_*.sh dosyalarını sırayla çalıştırır.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$ROOT/tests"
PASSED=0
FAILED=0

for t in "$TEST_DIR"/test_*.sh; do
  [[ -f "$t" ]] || continue
  name="$(basename "$t")"
  if bash "$t"; then
    printf '  [OK]   %s\n' "$name"
    PASSED=$((PASSED + 1))
  else
    printf '  [FAIL] %s\n' "$name"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "Sonuç: $PASSED geçti, $FAILED başarısız."
[[ "$FAILED" -eq 0 ]]