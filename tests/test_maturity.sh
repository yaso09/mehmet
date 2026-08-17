#!/usr/bin/env bash
# Olgunluk değerlendirme raporu bütünlük testleri.
# Not: self_assess.sh'i burada çalıştırmak, run_tests -> self_assess -> run_tests
# döngüsüne yol açar; bu yüzden yalnızca kaydedilmiş raporlar doğrulanır.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

# maturity.json geçerli JSON ve sayısal skor içermeli
if ! jq -e '.score | type == "number"' "$ROOT_DIR/docs/maturity.json" >/dev/null 2>&1; then
  echo "docs/maturity.json geçerli ve sayısal score içermiyor"
  failures=$((failures + 1))
fi

# maturity.md raporu var olmalı
if [[ ! -f "$ROOT_DIR/docs/maturity.md" ]]; then
  echo "docs/maturity.md raporu mevcut değil"
  failures=$((failures + 1))
fi

# Skor 0-100 aralığında olmalı
score="$(jq -r '.score' "$ROOT_DIR/docs/maturity.json")"
if [[ "$score" -lt 0 || "$score" -gt 100 ]]; then
  echo "maturity.json skoru 0-100 aralığında değil: $score"
  failures=$((failures + 1))
fi

exit "$failures"