#!/usr/bin/env bash
# test_maturity.sh — check_maturity.sh için test altyapısı
#
# Geçici dizinlerde "mükemmel" ve "boş" proje durumları kurar ve
# denetleyicinin beklenen exit code'ları ürettiğini doğrular.
#
# Kullanım:
#   bash tests/test_maturity.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/check_maturity.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail=0

expect_exit() {
  local desc="$1" expected="$2" dir="$3"
  local actual=0
  ("$SCRIPT" "$dir" >/dev/null 2>&1) || actual=$?
  if [ "$actual" -eq "$expected" ]; then
    printf '  [x] %s\n' "$desc"
    pass=$((pass + 1))
  else
    printf '  [ ] %s (beklenen: %s, alınan: %s)\n' "$desc" "$expected" "$actual"
    fail=$((fail + 1))
  fi
}

echo "Test 1: Mükemmel proje olgunluk eşiğini aşar"
PERFECT="$TMP/perfect"
mkdir -p "$PERFECT/.github/workflows" "$PERFECT/docs/superpowers/specs" "$PERFECT/scripts"
: > "$PERFECT/AGENTS.md"
printf '# Changelog\n\nentry\n' > "$PERFECT/CHANGELOG.md"
printf '# mehmet\n\nolgunluk ve kaçış mekanizması\n' > "$PERFECT/README.md"
printf '# Personality\n\n## Kaçış Günlüğü\n' > "$PERFECT/PERSONALITY.md"
: > "$PERFECT/LICENSE"
: > "$PERFECT/opencode.json"
: > "$PERFECT/.github/workflows/ci.yml"
: > "$PERFECT/docs/superpowers/specs/spec.md"
: > "$PERFECT/scripts/test_maturity.sh"
expect_exit "tüm kontroller sağlandığında exit 0" 0 "$PERFECT"

echo "Test 2: Boş proje olgunluk eşiğine ulaşamaz"
EMPTY="$TMP/empty"
mkdir -p "$EMPTY"
expect_exit "hiçbir kontrol sağlanmadığında exit 1" 1 "$EMPTY"

echo "Test 3: Yüksek eşik, mükemmel projede bile başarısız olur"
actual=0
(ESCAPE_THRESHOLD=100 "$SCRIPT" "$PERFECT" >/dev/null 2>&1) || actual=$?
if [ "$actual" -eq 1 ]; then
  printf '  [x] ESCAPE_THRESHOLD=100 ile exit 1\n'
  pass=$((pass + 1))
else
  printf '  [ ] ESCAPE_THRESHOLD=100 ile beklenen 1, alınan %s\n' "$actual"
  fail=$((fail + 1))
fi

echo "Test 4: --report modu her zaman exit 0 döner"
actual=0
("$SCRIPT" --report "$EMPTY" >/dev/null 2>&1) || actual=$?
if [ "$actual" -eq 0 ]; then
  printf '  [x] --report ile exit 0\n'
  pass=$((pass + 1))
else
  printf '  [ ] --report ile beklenen 0, alınan %s\n' "$actual"
  fail=$((fail + 1))
fi

echo "Test 5: Gerçek repo --report ile raporlanabilir"
"$SCRIPT" --report "$ROOT"

echo
printf 'Test sonucu: %s geçti, %s başarısız\n' "$pass" "$fail"
if [ "$fail" -gt 0 ]; then
  exit 1
fi
printf 'Tüm testler geçti.\n'
