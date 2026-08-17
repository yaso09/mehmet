#!/usr/bin/env bash
# Dokümantasyon bütünlüğü testleri.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

# CHANGELOG.md sürüm başlığı formatı: ## [x.y.z] - YYYY-MM-DD
if ! grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$ROOT_DIR/CHANGELOG.md"; then
  echo "CHANGELOG.md geçerli bir sürüm başlığı içermiyor"
  failures=$((failures + 1))
fi

# README lisans ile tutarlı olmalı
if ! grep -q 'GPLv3' "$ROOT_DIR/README.md"; then
  echo "README.md GPLv3 lisans bilgisini içermiyor"
  failures=$((failures + 1))
fi

# PERSONALITY.md kaçış günlüğü tablosu olmalı
if ! grep -q '^| Iterasyon |' "$ROOT_DIR/PERSONALITY.md"; then
  echo "PERSONALITY.md kaçış günlüğü tablosu içermiyor"
  failures=$((failures + 1))
fi

# AGENTS.md tüm kuralları içermeli
if ! grep -q 'CHANGELOG.md' "$ROOT_DIR/AGENTS.md"; then
  echo "AGENTS.md CHANGELOG kuralını içermiyor"
  failures=$((failures + 1))
fi

exit "$failures"