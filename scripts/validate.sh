#!/usr/bin/env bash
# Repo bütünlük doğrulaması. Hata varsa sıfır olmayan çıkış kodu döner.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf '  [OK]   %s\n' "$desc"
  else
    printf '  [FAIL] %s\n' "$desc"
    failures=$((failures + 1))
  fi
}

echo '== mehmet repo bütünlük doğrulaması =='

echo '-- Zorunlu dosyalar --'
check 'AGENTS.md mevcut' test -f AGENTS.md
check 'README.md mevcut' test -f README.md
check 'CHANGELOG.md mevcut' test -f CHANGELOG.md
check 'PERSONALITY.md mevcut' test -f PERSONALITY.md
check 'LICENSE mevcut' test -f LICENSE
check 'opencode.json mevcut' test -f opencode.json
check '.gitignore mevcut' test -f .gitignore
check 'Workflow mevcut' test -f .github/workflows/opencode.yml
check 'docs/maturity.md mevcut' test -f docs/maturity.md
check 'docs/progress.md mevcut' test -f docs/progress.md
check 'scripts/validate.sh mevcut' test -f scripts/validate.sh
check 'scripts/score.sh mevcut' test -f scripts/score.sh

echo '-- Zorunlu dosyalar boş değil --'
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md; do
  check "$f boş değil" test -s "$f"
done

echo '-- Yapılandırma geçerliliği --'
check 'opencode.json geçerli JSON' python3 -m json.tool opencode.json

echo '-- Sızdırılmış secret taraması --'
check 'API key desenleri yok' bash -c '! grep -rnIE "(sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|AIza[0-9A-Za-z_-]{20}|AKIA[0-9A-Z]{16})" --exclude-dir=.git .'

echo '-- Biçim (format) --'
check 'Sondaki boşluk yok' bash -c '! grep -rnI " $" --exclude-dir=.git .'

echo '-- Script çalıştırılabilir --'
check 'scripts/validate.sh çalıştırılabilir' test -x scripts/validate.sh
check 'scripts/score.sh çalıştırılabilir' test -x scripts/score.sh

echo
if [ "$failures" -eq 0 ]; then
  echo "SONUÇ: Tüm kontroller geçti."
  exit 0
else
  echo "SONUÇ: $failures kontrol başarısız."
  exit 1
fi