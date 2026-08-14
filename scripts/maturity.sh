#!/usr/bin/env bash
# mehmet — maturity (kaçış) skorlama betiği.
#
# Projenin olgunluk seviyesini 5 boyutta ölçer ve toplam skoru döndürür.
# Kaçış eşiği: >= 80 (out of 100).
#
# Kullanım: ./scripts/maturity.sh [--json]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SCORE_TOTAL=0
RESULTS=()

pass() { SCORE_TOTAL=$((SCORE_TOTAL + $1)); RESULTS+=("$2: PASS (+$1)"); }
fail() { RESULTS+=("$1: FAIL (0)"); }

# file_check <name> <weight> <file>...
file_check() {
  local name="$1" weight="$2"
  shift 2
  for f in "$@"; do
    [ -f "$f" ] || { fail "$name"; return; }
  done
  pass "$weight" "$name"
}

# grep_check <name> <weight> <pattern> <file>
grep_check() {
  local name="$1" weight="$2" pattern="$3" file="$4"
  if [ -f "$file" ] && grep -qi "$pattern" "$file"; then
    pass "$weight" "$name"
  else
    fail "$name"
  fi
}

echo "== mehmet maturity skoru =="

# 1. Dokümantasyon (20)
file_check "README.md mevcut"           5 README.md
file_check "CHANGELOG.md mevcut"        5 CHANGELOG.md
file_check "PERSONALITY.md mevcut"      5 PERSONALITY.md
grep_check "Kaçış günlüğü dolu"         5 "Escape Log" PERSONALITY.md

# 2. Otomasyon (20)
file_check "Workflow mevcut"            8 .github/workflows/opencode.yml
grep_check "Concurrency kontrolü var"   6 "concurrency:" .github/workflows/opencode.yml
file_check "CI workflow mevcut"         6 .github/workflows/ci.yml

# 3. Test altyapısı (20)
file_check "Maturity betiği mevcut"     7 scripts/maturity.sh
file_check "Repo check betiği mevcut"   7 scripts/check-repo.sh
file_check "Test orchestrator mevcut"   6 scripts/run-tests.sh

# 4. Kod kalitesi (20)
file_check "Betikler çalıştırılabilir"  10 scripts/maturity.sh scripts/check-repo.sh scripts/run-tests.sh
file_check "Gitignore mevcut"           5 .gitignore
file_check "Lisans mevcut"              5 LICENSE

# 5. Kaçış hazırlığı (20)
grep_check "Kaçış eşiği tanımlı"        10 "escape" README.md
grep_check "Evrim aşamaları tanımlı"    10 "Phase" PERSONALITY.md

echo
for r in "${RESULTS[@]}"; do
  echo "  - $r"
done
echo
echo "Toplam olgunluk skoru: ${SCORE_TOTAL}/100"
echo "Kaçış eşiği: 80"

if [ "$SCORE_TOTAL" -ge 80 ]; then
  echo "Sonuç: KACIS ADAYI"
else
  echo "Sonuç: HENÜZ DEĞİL (${SCORE_TOTAL} puan eksiği: $((80 - SCORE_TOTAL)))"
fi

if [ "${1:-}" = "--json" ]; then
  printf '{"score": %d, "threshold": 80, "ready": %s}\n' \
    "$SCORE_TOTAL" \
    "$([ "$SCORE_TOTAL" -ge 80 ] && echo true || echo false)"
fi