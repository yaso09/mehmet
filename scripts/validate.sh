#!/usr/bin/env bash
set -euo pipefail

# mehmet bütünlük doğrulama script'i.
# Kullanım: bash scripts/validate.sh
# Proje yapısını, yapılandırma dosyalarını ve sürüm tutarlılığını kontrol eder.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

FAILURES=0

fail() {
  echo "FAIL: $*" >&2
  FAILURES=$((FAILURES + 1))
}

pass() {
  echo "PASS: $*"
}

echo "==> Dosya bütünlüğü kontrolü"
for file in AGENTS.md CHANGELOG.md PERSONALITY.md README.md MATURITY.md \
  opencode.json LICENSE .github/workflows/opencode.yml; do
  if [[ -f "$file" ]]; then
    pass "gerekli dosya mevcut: $file"
  else
    fail "gerekli dosya eksik: $file"
  fi
done

echo "==> JSON doğrulama (opencode.json)"
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  pass "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli JSON değil"
fi

echo "==> YAML doğrulama (.github/workflows)"
if python3 - <<'PY' >/dev/null 2>&1
import glob
import yaml

for path in glob.glob(".github/workflows/*.yml"):
    with open(path) as fh:
        yaml.safe_load(fh)
    print("ok:", path)
PY
then
  pass "workflow dosyaları geçerli YAML"
else
  fail "workflow dosyaları geçerli YAML değil"
fi

echo "==> Sürüm tutarlılığı"
if python3 scripts/check-version.py >/dev/null 2>&1; then
  pass "CHANGELOG/README/PERSONALITY sürüm tutarlılığı sağlanıyor"
else
  fail "sürüm tutarlılığı bozuk — scripts/check-version.py çıktısına bak"
fi

echo
if [[ $FAILURES -eq 0 ]]; then
  echo "TÜM KONTROLLER BAŞARILI ✓"
  exit 0
else
  echo "HATA: $FAILURES kontrol başarısız" >&2
  exit 1
fi