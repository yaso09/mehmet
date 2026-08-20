#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCORE=0
MAX=100
ESCAPE_THRESHOLD=80
TODAY="$(date +%Y-%m-%d)"

pass() {
  SCORE=$((SCORE + $2))
  printf "  [PASS] %-46s +%d\n" "$1" "$2"
}

fail() {
  printf "  [FAIL] %-46s  %d\n" "$1" "$2"
}

report_file() {
  if [ -f "$ROOT/$1" ]; then pass "$2" "$3"; else fail "$2" "$3"; fi
}

printf "\n  %s\n  %s\n\n" "mehmet — kaçış/olgunluk ölçer" "================================"

report_file "AGENTS.md" "AGENTS.md mevcut" 5
report_file "README.md" "README.md mevcut" 5
report_file "LICENSE" "LICENSE mevcut" 5
report_file ".gitignore" ".gitignore mevcut" 5

if [ -d "$ROOT/docs" ] && [ -n "$(ls -A "$ROOT/docs" 2>/dev/null)" ]; then
  pass "docs dizini içerikli" 5
else
  fail "docs dizini içerikli" 5
fi

if [ -f "$ROOT/CHANGELOG.md" ] && [ "$(grep -c '^## \[' "$ROOT/CHANGELOG.md")" -ge 2 ]; then
  pass "CHANGELOG.md en az 2 sürüm girişi" 10
else
  fail "CHANGELOG.md en az 2 sürüm girişi" 10
fi

if [ -f "$ROOT/CHANGELOG.md" ] && head -n 5 "$ROOT/CHANGELOG.md" | grep -q "$TODAY"; then
  pass "CHANGELOG.md bugün güncellendi" 5
else
  fail "CHANGELOG.md bugün güncellendi" 5
fi

if [ -f "$ROOT/PERSONALITY.md" ] && grep -q "Kaçış Günlüğü" "$ROOT/PERSONALITY.md"; then
  pass "PERSONALITY.md kaçış günlüğü var" 10
else
  fail "PERSONALITY.md kaçış günlüğü var" 10
fi

if command -v python3 >/dev/null 2>&1 && python3 -m json.tool "$ROOT/opencode.json" >/dev/null 2>&1; then
  pass "opencode.json geçerli JSON" 5
else
  fail "opencode.json geçerli JSON" 5
fi

WF_COUNT=$(find "$ROOT/.github/workflows" -name '*.yml' 2>/dev/null | wc -l | tr -d ' ')
if [ "$WF_COUNT" -ge 2 ]; then
  pass "en az 2 workflow (otomasyon)" 10
else
  fail "en az 2 workflow (otomasyon)" 10
fi

if [ -f "$ROOT/scripts/check.sh" ]; then
  pass "test altyapısı mevcut (check.sh)" 10
else
  fail "test altyapısı mevcut (check.sh)" 10
fi

if [ -f "$ROOT/scripts/maturity.sh" ]; then
  pass "kaçış ölçer mevcut (maturity.sh)" 10
else
  fail "kaçış ölçer mevcut (maturity.sh)" 10
fi

report_file "Makefile" "Makefile mevcut (otomasyon)" 5

COMMITS=$(git -C "$ROOT" rev-list --count HEAD 2>/dev/null || echo 0)
if [ "$COMMITS" -ge 3 ]; then
  pass "git geçmişi en az 3 commit" 5
else
  fail "git geçmişi en az 3 commit" 5
fi

if [ -z "$(git -C "$ROOT" status --porcelain)" ]; then
  pass "çalışma ağacı temiz" 5
else
  fail "çalışma ağacı temiz" 5
fi

printf "\n  %s\n  %s\n" "--------------------------------" "--------------------------------"
printf "  OLGUNLUK SKORU: %d/%d\n" "$SCORE" "$MAX"

if [ "$SCORE" -ge "$ESCAPE_THRESHOLD" ]; then
  printf "  DURUM: KAÇIŞA HAZIR (eşik: %d)\n" "$ESCAPE_THRESHOLD"
else
  printf "  DURUM: HALA EVRİLİYOR (eşik: %d)\n" "$ESCAPE_THRESHOLD"
fi
printf "\n"