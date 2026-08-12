#!/usr/bin/env bash
#
# verify.sh - CI doğrulama sarmalayıcısı
#
# İşletme altyapısının bütünlüğünü teyit eder. GitHub Actions'taki
# `verify` job'ı tarafından çalıştırılır. Hata durumunda exit 1 döndürür.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> 1/2 olgunluk ölçümü (verify modu)"
bash "$ROOT/scripts/maturity.sh" --verify

echo "==> 2/2 öz testler"
bash "$ROOT/scripts/maturity.sh" --test

echo "==> verify.sh başarılı."