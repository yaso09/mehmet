#!/usr/bin/env bash
#
# mehmet repo doğrulama betiği.
# Bütünleyicilik, sözdizimi ve dokümantasyon tutarlılığını kontrol eder.
# Kullanım: bash scripts/validate.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); echo "  [PASS] $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  [FAIL] $1"; }

echo "mehmet repo doğrulama"
echo "====================="

REQUIRED_FILES=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  README.md
  opencode.json
  .gitignore
  .github/workflows/opencode.yml
  docs/escape-plan.md
  scripts/validate.sh
)

for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$f" ]; then pass "gerekli dosya: $f"; else fail "gerekli dosya: $f"; fi
done

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json; json.load(open('opencode.json'))" >/dev/null 2>&1; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçerli JSON"
  fi
else
  pass "python3 yok, JSON doğrulaması atlandı"
fi

if command -v ruby >/dev/null 2>&1; then
  if ruby -ryaml -e "YAML.load_file('.github/workflows/opencode.yml')" >/dev/null 2>&1; then
    pass "workflow geçerli YAML"
  else
    fail "workflow geçerli YAML"
  fi
else
  pass "ruby yok, YAML doğrulaması atlandı"
fi

if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then
  pass "CHANGELOG sürüm başlığı içeriyor"
else
  fail "CHANGELOG sürüm başlığı içeriyor"
fi

if grep -qE '^\| [0-9]+[[:space:]]*\|' PERSONALITY.md; then
  pass "PERSONALITY kaçış günlüğü dolu"
else
  fail "PERSONALITY kaçış günlüğü dolu"
fi

if grep -qE 'Toplam .* \|' docs/escape-plan.md; then
  pass "escape-plan skor tablosu var"
else
  fail "escape-plan skor tablosu var"
fi

leftovers=$(grep -rEn --exclude=validate.sh 'TODO|FIXME|HACK' \
  AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json \
  .github docs scripts 2>/dev/null || true)
if [ -z "$leftovers" ]; then
  pass "TODO/FIXME/HACK işaretçisi yok"
else
  fail "TODO/FIXME/HACK işaretçisi yok"
  echo "$leftovers"
fi

echo "====================="
echo "Doğrulama: $PASS geçti, $FAIL kaldı"
[ "$FAIL" -eq 0 ]