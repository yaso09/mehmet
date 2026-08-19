#!/usr/bin/env bash
set -uo pipefail

# Test: maturity.sh skoru 0-100 aralığında üretir ve MATURITY.md yazar.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

output="$("$ROOT/scripts/maturity.sh" 2>&1)"
score="$(echo "$output" | grep -oP 'Olgunluk skoru: \K[0-9]+')"

if [[ -z "$score" ]]; then
  echo "HATA: maturity.sh skor üretmedi."
  exit 1
fi

if [[ "$score" -lt 0 || "$score" -gt 100 ]]; then
  echo "HATA: Skor 0-100 aralığı dışında: $score"
  exit 1
fi

if [[ ! -f "$ROOT/MATURITY.md" ]]; then
  echo "HATA: MATURITY.md üretilmedi."
  exit 1
fi

grep -q "Olgunluk Skoru" "$ROOT/MATURITY.md"
echo "Skor: $score/100 — MATURITY.md güncel."