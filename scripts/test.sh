#!/usr/bin/env bash
set -euo pipefail

# test.sh — proje doğrulama paketi. Test altyapısının kendini kanıtladığı yerdir.

cd "$(dirname "$0")/.."
ROOT="$PWD"
PASSED=0
FAILED=0

t() { # 1: ad, 2: komut
  if eval "$2" >/dev/null 2>&1; then
    echo "ok   $1"
    PASSED=$((PASSED + 1))
  else
    echo "FAIL $1"
    FAILED=$((FAILED + 1))
  fi
}

t "opencode.json geçerli JSON" \
  "python3 -c \"import json; json.load(open('$ROOT/opencode.json'))\""

t "maturity.sh --json çıktı üretiyor" \
  "bash '$ROOT/scripts/maturity.sh' --json | grep -q '\"score\"'"

t "maturity.sh --log günlüğe yazıyor" \
  "bash '$ROOT/scripts/maturity.sh' --log && [ -f '$ROOT/docs/escape-log/maturity.csv' ]"

t "AGENTS.md simülasyon kuralı içeriyor" \
  "grep -q 'CHANGELOG' '$ROOT/AGENTS.md'"

t "README MATURITY'a referans veriyor" \
  "grep -q 'MATURITY' '$ROOT/README.md'"

echo "---"
echo "Testler: $PASSED geçti, $FAILED başarısız."
[ "$FAILED" -eq 0 ] || exit 1