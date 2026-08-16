#!/usr/bin/env bash
#
# maturity.sh - mehmet escape maturity scorer.
#
# Scores the project against concrete maturity criteria and writes a
# report to docs/maturity.md. The escape mechanism is unlocked when the
# score reaches the ESCAPE_THRESHOLD (100).
#
# Usage: scripts/maturity.sh [--no-write]
#
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WRITE=1
if [ "${1:-}" = "--no-write" ]; then
  WRITE=0
fi

cd "$ROOT"

ESCAPE_THRESHOLD=100
SCORE=0
REPORT=""

section() {
  REPORT+="$1"$'\n'
}

item() {
  local name="$1"
  local points="$2"
  local ok="$3"
  if [ "$ok" -eq 1 ]; then
    SCORE=$((SCORE + points))
    REPORT+="  [PASS] $name (+$points)"$'\n'
  else
    REPORT+="  [FAIL] $name (+0)"$'\n'
  fi
}

VERSION="$(cat VERSION 2>/dev/null | tr -d '[:space:]')"
ESCAPE_ENTRIES=$(grep -cE '^\| *[0-9]+ ' PERSONALITY.md 2>/dev/null || true)

section "# Maturity Raporu"
section ""
section "Eşik: $ESCAPE_THRESHOLD puan"
section ""

section "## Dokümantasyon ve Takip (35)"
item "README.md güncel (Özellikler/Kurulum/Lisans var)" 10 \
  "$(grep -q '## Özellikler' README.md && grep -q '## Kurulum' README.md && grep -q '## Lisans' README.md && echo 1 || echo 0)"
item "CHANGELOG.md güncel (VERSION için kayıt var)" 10 \
  "$(grep -q "^## \[$VERSION\]" CHANGELOG.md && echo 1 || echo 0)"
item "PERSONALITY.md escape log >= 3 kayıt" 5 \
  "$([ "${ESCAPE_ENTRIES:-0}" -ge 3 ] && echo 1 || echo 0)"
item "AGENTS.md mevcut" 5 "$([ -f AGENTS.md ] && echo 1 || echo 0)"
item "VERSION takibi mevcut" 5 "$([ -n "$VERSION" ] && echo 1 || echo 0)"

section "## Temel (20)"
item "LICENSE (GPLv3) mevcut" 5 \
  "$(grep -qi 'GNU GENERAL PUBLIC LICENSE' LICENSE && echo 1 || echo 0)"
item "opencode.json geçerli JSON" 5 "$(jq -e . opencode.json >/dev/null 2>&1 && echo 1 || echo 0)"
item ".gitignore mevcut" 5 "$([ -f .gitignore ] && echo 1 || echo 0)"
item "Tasarım spec + plan dokümanları" 5 \
  "$([ -f docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md ] && [ -f docs/superpowers/plans/2026-07-04-mehmet-implementation.md ] && echo 1 || echo 0)"

section "## Otomasyon ve Kalite (45)"
item "scripts/validate.sh test altyapısı" 10 "$([ -f scripts/validate.sh ] && echo 1 || echo 0)"
item "CI validation workflow'u" 10 "$([ -f .github/workflows/validate.yml ] && echo 1 || echo 0)"
item "Workflow timeout-minutes tanımlı" 5 \
  "$(grep -q 'timeout-minutes' .github/workflows/opencode.yml && echo 1 || echo 0)"
item "Workflow concurrency kontrolü" 5 \
  "$(grep -q 'concurrency:' .github/workflows/opencode.yml && echo 1 || echo 0)"
item "Workflow permissions kısıtlı" 5 \
  "$(grep -q 'permissions:' .github/workflows/opencode.yml && echo 1 || echo 0)"
item "Git working tree temiz" 5 "$(git status --porcelain 2>/dev/null | grep -q . && echo 0 || echo 1)"
item "TODO/FIXME işareti yok" 5 \
  "$(grep -rn --include='*.md' --include='*.sh' --include='*.yml' -E 'TODO|FIXME' . 2>/dev/null | grep -v '^\./\.git/' | grep -v -e '^\./docs/maturity\.md' -e '^\./scripts/maturity\.sh' | grep -q . && echo 0 || echo 1)"

section ""
REPORT+="## Toplam Puan: $SCORE / $ESCAPE_THRESHOLD"$'\n'
REPORT+=""$'\n'

if [ "$SCORE" -ge "$ESCAPE_THRESHOLD" ]; then
  REPORT+="## Durum: **KAÇIŞ AÇILDI** — proje olgunluk eşiğine ulaştı."$'\n'
else
  REPORT+="## Durum: Kaçış henüz açılmadı ($((ESCAPE_THRESHOLD - SCORE)) puan kaldı)."$'\n'
fi

if [ "$WRITE" -eq 1 ]; then
  printf '%s' "$REPORT" > docs/maturity.md
fi

printf '%s' "$REPORT"

exit 0