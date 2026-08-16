#!/usr/bin/env bash
# mehmet olgunluk skoru hesaplayıcı (0-100).
# Kriterler: docs/maturity.md
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# --- 1. Dokümantasyon (20) ---
docs=0
[ -f README.md ] && [ -s README.md ] && docs=$((docs + 4))
[ -f CHANGELOG.md ] && [ -s CHANGELOG.md ] && docs=$((docs + 4))
[ -f AGENTS.md ] && [ -s AGENTS.md ] && docs=$((docs + 4))
[ -f PERSONALITY.md ] && [ -s PERSONALITY.md ] && docs=$((docs + 4))
[ -d docs ] && [ -n "$(ls docs 2>/dev/null)" ] && docs=$((docs + 4))

# --- 2. Test ve Doğrulama (25) ---
tests=0
[ -f scripts/validate.sh ] && [ -x scripts/validate.sh ] && tests=$((tests + 5))
[ -f scripts/score.sh ] && [ -x scripts/score.sh ] && tests=$((tests + 5))
if bash scripts/validate.sh >/dev/null 2>&1; then
  tests=$((tests + 15))
fi

# --- 3. Otomasyon (25) ---
auto=0
WF=.github/workflows/opencode.yml
[ -f "$WF" ] && auto=$((auto + 5))
grep -q 'cron:' "$WF" 2>/dev/null && auto=$((auto + 5))
grep -q 'timeout-minutes' "$WF" 2>/dev/null && auto=$((auto + 5))
grep -q 'validate' "$WF" 2>/dev/null && auto=$((auto + 5))
grep -q 'workflow_dispatch' "$WF" 2>/dev/null && auto=$((auto + 5))

# --- 4. Kod Kalitesi (20) ---
code=0
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  code=$((code + 5))
fi
if ! grep -rnIE '(sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|AIza[0-9A-Za-z_-]{20}|AKIA[0-9A-Z]{16})' --exclude-dir=.git . >/dev/null 2>&1; then
  code=$((code + 5))
fi
if ! grep -rnI ' $' --exclude-dir=.git . >/dev/null 2>&1; then
  code=$((code + 5))
fi
if [ -f .gitignore ] && grep -q 'node_modules' .gitignore; then
  code=$((code + 5))
fi

# --- 5. Kaçış Altyapısı (10) ---
escape=0
[ -f docs/maturity.md ] && escape=$((escape + 5))
[ -f docs/progress.md ] && escape=$((escape + 5))

total=$((docs + tests + auto + code + escape))

echo "Dokümantasyon:     $docs/20"
echo "Test ve Doğrulama: $tests/25"
echo "Otomasyon:         $auto/25"
echo "Kod Kalitesi:      $code/20"
echo "Kaçış Altyapısı:   $escape/10"
echo "--------------------------------"
echo "TOPLAM:            $total/100"

if [ "$total" -ge 80 ]; then
  echo "ESCAPE_THRESHOLD: eşik aşıldı (>= 80) -> Phase 4: Escape"
else
  echo "ESCAPE_THRESHOLD: eşiğe ulaşılamadı (< 80)"
fi

exit 0