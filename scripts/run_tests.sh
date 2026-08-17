#!/usr/bin/env bash
#
# mehmet test çalıştırıcısı.
#
# tests/test_*.sh şeklindeki her testi çalıştırır, sonuçları toplar.
#
# Kullanım:
#   scripts/run_tests.sh              # tüm testleri çalıştır
#   scripts/run_tests.sh --count      # yalnızca özet satırını yaz (self_assess için)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$ROOT_DIR/tests"

pass_count=0
fail_count=0
failed_tests=()

for test_file in "$TEST_DIR"/test_*.sh; do
  [[ -e "$test_file" ]] || continue
  name="$(basename "$test_file")"
  if bash "$test_file" >/dev/null 2>&1; then
    pass_count=$((pass_count + 1))
    printf 'ok    %s\n' "$name"
  else
    fail_count=$((fail_count + 1))
    failed_tests+=("$name")
    printf 'FAIL  %s\n' "$name"
  fi
done

total=$((pass_count + fail_count))

printf '\nÖzet: toplam %d, geçti %d, başarısız %d\n' "$total" "$pass_count" "$fail_count"

if [[ ${#failed_tests[@]} -gt 0 ]]; then
  printf 'Başarısız: %s\n' "${failed_tests[*]}"
fi

if [[ "${1:-}" == "--count" ]]; then
  exit 0
fi

[[ "$fail_count" -eq 0 ]]