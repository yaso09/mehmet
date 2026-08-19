#!/usr/bin/env bash
# mehmet test koşucusu
# Gerçek mantığı doğrular: pozitif (temiz repo) ve negatif (bozuk repo) senaryolar.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS=0
FAILS=0

t() {
  local name="$1" cmd="$2"
  TESTS=$((TESTS + 1))
  if eval "$cmd"; then
    echo "PASS: $name"
  else
    echo "FAIL: $name"
    FAILS=$((FAILS + 1))
  fi
}

t "validate.sh temiz repoda geçer" "bash $ROOT/scripts/validate.sh"

tmp="$(mktemp -d)"
mkdir -p "$tmp/repo/scripts" "$tmp/repo/.github/workflows"
cp "$ROOT"/AGENTS.md "$ROOT"/CHANGELOG.md "$ROOT"/PERSONALITY.md "$ROOT"/README.md "$ROOT"/opencode.json "$ROOT"/LICENSE "$ROOT"/.gitignore "$tmp/repo/" 2>/dev/null || true
cp "$ROOT"/scripts/*.sh "$tmp/repo/scripts/"
cp "$ROOT"/.github/workflows/opencode.yml "$tmp/repo/.github/workflows/"
rm -f "$tmp/repo/AGENTS.md"
t "validate.sh eksik dosyada başarısız olur" "! bash $tmp/repo/scripts/validate.sh >/dev/null 2>&1"
rm -rf "$tmp"

t "maturity.sh 0-100 arası skor üretir" "MEHMET_RECURSION_GUARD=1 bash $ROOT/scripts/maturity.sh | grep -Eq 'MEHMET MATURITY SCORE: (100|[1-9][0-9]?)/100'"

echo ""
if [[ $FAILS -gt 0 ]]; then
  echo "TESTS FAILED: $FAILS/$TESTS"
  exit 1
fi
echo "ALL TESTS PASSED: $TESTS"
