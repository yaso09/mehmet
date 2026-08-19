#!/usr/bin/env bash
# mehmet maturity scorer — Python modülünü çağırır.
# MATURITY.md yol haritasını ayrıştırır ve kaçış eşiğine göre skoru raporlar.
#
# Usage: bash scripts/maturity.sh [--strict]

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHONPATH="$ROOT/src" python3 -m mehmet.maturity "$@"