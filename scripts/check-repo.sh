#!/usr/bin/env bash
# mehmet — repo yapısal tutarlılık kontrol betiği.
#
# Kritik dosyaların varlığını ve içerik tutarlılığını doğrular.
# Hata durumunda sıfır olmayan çıkış kodu döner (CI için).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0

require() {
  for f in "$@"; do
    if [ -f "$f" ]; then
      echo "  [OK] $f"
    else
      echo "  [HATA] $f yok"
      ERRORS=$((ERRORS + 1))
    fi
  done
}

grep_ok() {
  local pattern="$1" file="$2"
  if [ -f "$file" ] && grep -q "$pattern" "$file"; then
    echo "  [OK] $file -> '$pattern'"
  else
    echo "  [HATA] $file -> '$pattern' bulunamadı"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "== Repo yapısal kontrol =="
echo "-- Kritik dosyalar --"
require README.md CHANGELOG.md PERSONALITY.md AGENTS.md LICENSE opencode.json .gitignore
require .github/workflows/opencode.yml scripts/maturity.sh scripts/check-repo.sh scripts/run-tests.sh

echo "-- Tutarlılık --"
grep_ok "concurrency:" .github/workflows/opencode.yml
grep_ok "OPENCODE_API_KEY" .github/workflows/opencode.yml
grep_ok "GPLv3" README.md
grep_ok "GNU GENERAL PUBLIC LICENSE" LICENSE
grep_ok "Escape Log" PERSONALITY.md

echo
if [ "$ERRORS" -eq 0 ]; then
  echo "Sonuç: TÜM KONTROLLER GECTI"
  exit 0
else
  echo "Sonuç: $ERRORS hata"
  exit 1
fi