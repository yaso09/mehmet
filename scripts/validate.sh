#!/usr/bin/env bash
#
# mehmet proje sağlık kontrolü
# Zorunlu dosyaların varlığını, JSON/YAML geçerliliğini ve
# kaçış günlüğü gibi belge bütünlüğünü doğrular.
#
# Kullanım: bash scripts/validate.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILURES=0

pass() { printf '  [PASS] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; FAILURES=$((FAILURES + 1)); }
skip() { printf '  [SKIP] %s\n' "$1"; }

check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    pass "$desc"
  else
    fail "$desc"
  fi
}

echo "== mehmet proje sağlık kontrolü =="

echo "-- Zorunlu dosyalar --"
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md opencode.json .github/workflows/opencode.yml; do
  check "dosya mevcut ve boş değil: $f" test -s "$f"
done

echo "-- Konfigürasyon --"
check "opencode.json geçerli JSON" python3 -c "import json; json.load(open('opencode.json'))"

echo "-- Belge bütünlüğü --"
check "PERSONALITY.md kaçış günlüğü başlığı var" grep -q "Kaçış Günlüğü" PERSONALITY.md
count_iterations() {
  local n
  n="$(grep -cE '^\| *[0-9]+' PERSONALITY.md || true)"
  [ "$n" -ge 3 ]
}
check "PERSONALITY.md en az 3 iterasyon kaydı" count_iterations
check "CHANGELOG.md sürüm başlığı var" grep -qE '^## \[' CHANGELOG.md
check "README.md proje adını içeriyor" grep -qi "mehmet" README.md

echo "-- YAML iş akışları --"
if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" >/dev/null 2>&1; then
  for wf in .github/workflows/*.yml; do
    check "geçerli YAML: $wf" python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]))" "$wf"
  done
else
  skip "YAML doğrulaması (PyYAML kurulu değil)"
fi

echo
if [ "$FAILURES" -gt 0 ]; then
  echo "== $FAILURES kontrol BAŞARISIZ =="
  exit 1
fi
echo "== Tüm kontroller geçti =="