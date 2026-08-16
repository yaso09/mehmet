#!/usr/bin/env bash
set -euo pipefail

# run-tests.sh — mehmet test koşucusu
# tests/ dizinindeki *_test.sh dosyalarını sırayla çalıştırır.
# Her test dosyası başarıda 0, başarısızlıkta sıfır olmayan kod ile çıkar.
#
# Kullanım:
#   tests/run-tests.sh
#   tests/run-tests.sh --verbose

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERBOSE=false
if [[ "${1:-}" == "--verbose" ]]; then
  VERBOSE=true
fi

passed=0
failed=0
failed_names=()

for t in tests/*_test.sh; do
  [[ -e "$t" ]] || continue
  name="$(basename "$t")"
  if bash "$t" >/tmp/mehmet-test.log 2>&1; then
    printf 'PASS  %s\n' "$name"
    passed=$((passed + 1))
  else
    printf 'FAIL  %s\n' "$name"
    failed=$((failed + 1))
    failed_names+=("$name")
    if [[ "$VERBOSE" == true ]]; then
      sed 's/^/      /' /tmp/mehmet-test.log
    fi
  fi
done

printf '\nÖzet: %d geçti, %d başarısız\n' "$passed" "$failed"

if (( failed > 0 )); then
  printf 'Başarısız: %s\n' "${failed_names[*]}"
  exit 1
fi
exit 0