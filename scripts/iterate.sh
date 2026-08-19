#!/usr/bin/env bash
set -euo pipefail

# iterate.sh — mehmet'in standart iterasyon döngüsü.
#
# Her çalışmada:
#   1. Proje bütünlüğünü doğrular (validate.sh)
#   2. Olgunluk skorunu hesaplar ve kaçış durumunu günceller (maturity.sh)
#
# Kullanım: scripts/iterate.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== 1/2 Proje doğrulaması ==="
"$ROOT/scripts/validate.sh"

echo ""
echo "=== 2/2 Olgunluk ve kaçış durumu ==="
"$ROOT/scripts/maturity.sh"