#!/usr/bin/env bash
set -euo pipefail

# mehmet — yapısal doğrulama betiği
#
# Projenin temel bütünlüğünü kontrol eder: zorunlu dosyaların varlığı,
# lisans tutarlılığı, sürüm günlüğü, kaçış günlüğü ve betik sağlığı.
#
# Kullanım:
#   bash scripts/validate.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILURES=0

pass() { printf 'PASS  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; FAILURES=$((FAILURES + 1)); }

require_file() {
  if [ -f "$1" ]; then
    pass "Dosya var: $1"
  else
    fail "Dosya eksik: $1"
  fi
}

echo "== Zorunlu dosyalar =="
require_file AGENTS.md
require_file README.md
require_file CHANGELOG.md
require_file PERSONALITY.md
require_file LICENSE
require_file opencode.json
require_file .github/workflows/opencode.yml

echo "== Lisans tutarlılığı =="
if grep -q -i "GPL" LICENSE; then
  pass "LICENSE GPL içeriyor"
else
  fail "LICENSE GPL içermiyor"
fi

if grep -q -i "GPLv3" README.md; then
  pass "README lisans bilgisi GPLv3"
else
  fail "README lisans bilgisi GPLv3 değil"
fi

echo "== Sürüm ve kaçış günlüğü =="
if grep -qE '^## \[0\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then
  pass "CHANGELOG sürüm girişi var"
else
  fail "CHANGELOG sürüm girişi yok"
fi

if grep -q "Kaçış Günlüğü" PERSONALITY.md; then
  pass "PERSONALITY kaçış günlüğü var"
else
  fail "PERSONALITY kaçış günlüğü yok"
fi

echo "== Betik sağlığı =="
for script in scripts/validate.sh scripts/check-maturity.sh; do
  if [ -f "$script" ] && [ -x "$script" ]; then
    pass "$script çalıştırılabilir"
  else
    fail "$script çalıştırılabilir değil"
  fi
  if bash -n "$script" 2>/dev/null; then
    pass "$script sözdizimi geçerli"
  else
    fail "$script sözdizimi hatalı"
  fi
done

echo
if [ "$FAILURES" -eq 0 ]; then
  echo "TÜM KONTROLLER BAŞARILI"
  exit 0
else
  echo "$FAILURES KONTROL BAŞARISIZ"
  exit 1
fi