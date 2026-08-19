#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAIL=0

check() {
  local desc="$1"
  local status="$2"
  if [ "$status" -eq 0 ]; then
    printf '  \033[32m✓\033[0m %s\n' "$desc"
  else
    printf '  \033[31m✗\033[0m %s\n' "$desc"
    FAIL=1
  fi
}

echo "== Gerekli dosyalar =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json \
         .github/workflows/opencode.yml docs/maturity.md scripts/validate.sh VERSION; do
  [ -f "$f" ]
  check "$f mevcut" $?
done

echo "== YAML/JSON sözdizimi =="
python3 -c 'import yaml,sys; yaml.safe_load(open(".github/workflows/opencode.yml")); print("workflow YAML OK")' >/dev/null 2>&1
check ".github/workflows/opencode.yml geçerli YAML" $?

jq empty opencode.json >/dev/null 2>&1
check "opencode.json geçerli JSON" $?

echo "== Tutarlılık =="
VERSION="$(cat VERSION)"
grep -q "## \[$VERSION\]" CHANGELOG.md
check "CHANGELOG.md $VERSION sürümünü içeriyor" $?

grep -qi "GPLv3\|GNU General Public" LICENSE
check "LICENSE GPLv3" $?

grep -qi "GPLv3" README.md
check "README.md lisans bilgisi GPLv3" $?

[ -s PERSONALITY.md ]
check "PERSONALITY.md boş değil" $?

[ -s docs/maturity.md ]
check "docs/maturity.md boş değil" $?

echo "== Script sözdizimi =="
bash -n scripts/validate.sh
check "scripts/validate.sh sözdizimi geçerli" $?

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -s bash scripts/validate.sh >/dev/null 2>&1
  check "shellcheck temiz" $?
else
  check "shellcheck mevcut değil (atlandı)" 0
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "Sonuç: TÜM KONTROLLER BAŞARILI"
  exit 0
else
  echo "Sonuç: BAŞARISIZ - yukarıdaki hataları düzeltin"
  exit 1
fi