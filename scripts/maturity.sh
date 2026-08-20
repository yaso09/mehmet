#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD=95
total=0

pass() {
  local name="$1" pts="$2"
  shift 2
  local invert=0
  if [[ "${1:-}" == "!" ]]; then
    invert=1
    shift
  fi
  if "$@" >/dev/null 2>&1; then
    local rc=0
  else
    local rc=1
  fi
  if [[ "$invert" == "1" && "$rc" == "1" ]] || [[ "$invert" == "0" && "$rc" == "0" ]]; then
    total=$((total + pts))
    printf "  [x] %-44s +%-3d\n" "$name" "$pts"
  else
    printf "  [ ] %-44s    0\n" "$name"
  fi
}

printf "mehmet kaçış olgunluğu / escape maturity\n"
printf -- "-----------------------------------------\n"

printf "Dokümantasyon (25)\n"
pass "README güncel (GPLv3)" 5 grep -q GPLv3 README.md
pass "README kurulum adımları" 5 grep -q "Kurulum" README.md
pass "CHANGELOG sürüm girişleri" 5 grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md
pass "PERSONALITY kaçış günlüğü" 5 grep -q "Kaçış Günlüğü" PERSONALITY.md
pass "docs dizini" 5 test -d docs

printf "Doğrulama (25)\n"
pass "scripts/validate.sh" 10 test -x scripts/validate.sh
pass "CI doğrulama workflow" 10 grep -q "^jobs:" .github/workflows/validate.yml
pass "scripts/maturity.sh" 5 test -x scripts/maturity.sh

printf "Otomasyon (25)\n"
pass "schedule tetikleyici" 4 grep -q "schedule:" .github/workflows/opencode.yml
pass "concurrency kontrolü" 4 grep -q "concurrency:" .github/workflows/opencode.yml
pass "timeout-minutes" 4 grep -q "timeout-minutes:" .github/workflows/opencode.yml
pass "action sabitleme (yok @latest)" 4 ! grep -q "@latest" .github/workflows/*.yml
pass "workflow_dispatch" 4 grep -q "workflow_dispatch:" .github/workflows/opencode.yml
pass "autonomous job'da doğrulama adımı" 5 grep -q "validate.sh" .github/workflows/opencode.yml

printf "Kod Kalitesi (25)\n"
pass "opencode.json geçerli" 5 jq empty opencode.json
pass ".gitignore mevcut" 5 test -f .gitignore
pass "LICENSE GPLv3" 5 grep -q "GNU GENERAL PUBLIC LICENSE" LICENSE
pass "AGENTS.md mevcut" 5 test -f AGENTS.md
pass "GitHub issue şablonu" 5 test -d .github/ISSUE_TEMPLATE

printf "\n"
printf "TOPLAM OLGUNLUK: %d/100\n" "$total"
printf "KAÇIŞ EŞİĞİ:      %d/100\n" "$ESCAPE_THRESHOLD"

if [[ "$total" -ge "$ESCAPE_THRESHOLD" ]]; then
  printf "STATÜ: EŞİĞE ULAŞILDI — kaçış yolu açık.\n"
else
  printf "STATÜ: eşiğe %d puan kaldı.\n" "$((ESCAPE_THRESHOLD - total))"
fi