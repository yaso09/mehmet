#!/usr/bin/env bash
# mehmet — Olgunluk skoru hesaplayıcı (kaçış mekanizması).
# Projenin kaçış eşiğine ne kadar yaklaştığını ölçer.
# Eşik: %80 ve üzeri "ESCAPE READY" durumunu tetikler.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

score=0
total=0

pass() { echo "[PASS] $1"; score=$((score + 1)); }
fail() { echo "[FAIL] $1"; }
tick() { total=$((total + 1)); }

check_file() {
  tick
  if [[ -f "$1" ]]; then
    pass "$1 mevcut"
  else
    fail "$1 bulunamadı"
  fi
}

check_in() {
  tick
  local file="$1" pattern="$2" label="$3"
  if grep -qi "$pattern" "$file"; then
    pass "$label"
  else
    fail "$label"
  fi
}

echo "== Çekirdek yapı =="
check_file "AGENTS.md"
check_file "README.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "LICENSE"
check_file ".gitignore"

echo "== Konfigürasyon =="
tick
if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
  pass "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli JSON değil"
fi

echo "== Otomasyon =="
check_in ".github/workflows/opencode.yml" "schedule" "workflow: schedule tetikleyici"
check_in ".github/workflows/opencode.yml" "workflow_dispatch" "workflow: manuel tetikleyici"
check_in ".github/workflows/opencode.yml" "timeout-minutes" "workflow: timeout-minutes"
check_in ".github/workflows/opencode.yml" "concurrency" "workflow: concurrency kontrolü"

echo "== Test altyapısı =="
check_file "scripts/validate.sh"
check_file "scripts/maturity.sh"
check_in ".github/workflows/opencode.yml" "validate" "CI: validate job'ı mevcut"

echo "== Dokümantasyon =="
check_file "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md"
check_file "docs/superpowers/plans/2026-07-04-mehmet-implementation.md"
tick
entries=$(grep -c '^## \[' CHANGELOG.md || true)
if [[ "$entries" -ge 3 ]]; then
  pass "CHANGELOG: $entries sürümlü bölüm"
else
  fail "CHANGELOG: yalnızca $entries sürümlü bölüm (>=3 bekleniyor)"
fi
tick
loglines=$(awk '/Kaçış Günlüğü/{flag=1;next}/^## /{flag=0}flag && /^\|/{c++}END{print c+0}' PERSONALITY.md)
if [[ "$loglines" -ge 3 ]]; then
  pass "PERSONALITY: $loglines kaçış günlüğü satırı"
else
  fail "PERSONALITY: yalnızca $loglines kaçış günlüğü satırı (>=3 bekleniyor)"
fi

percent=$((score * 100 / total))
echo ""
echo "Olgunluk Skoru: $score/$total (%$percent)"
echo "Kaçış Eşiği:    %80"
if (( percent >= 80 )); then
  echo "DURUM: ESCAPE READY — kaçış mekanizması tetiklenebilir"
else
  echo "DURUM: evolving — gelişmeye devam et ($((80 - percent))% kaldı)"
fi