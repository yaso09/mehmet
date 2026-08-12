#!/usr/bin/env bash
#
# validate_project.sh — mehmet projesinin sağlığını doğrular.
#
# 1. Zorunlu dosyaları kontrol eder
# 2. opencode.json'ın geçerli JSON olduğunu ve kritik alanları içerdiğini doğrular
# 3. Workflow dosyalarının varlığını ve temel bütünlüğünü kontrol eder
# 4. Olgunluk skorunu hesaplar ve raporlar
#
# Kritik hata olursa exit 1 döner. Kritik olmayan uyarılar exit 0 bırakır.
#
# Kullanım: bash scripts/validate_project.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0
WARN=0
MATURITY_PASS=0
MATURITY_TOTAL=0

log_pass() { printf '  [PASS] %s\n' "$1"; PASS=$((PASS + 1)); }
log_fail() { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL + 1)); }
log_warn() { printf '  [WARN] %s\n' "$1"; WARN=$((WARN + 1)); }
maturity() { MATURITY_PASS=$((MATURITY_PASS + 1)); MATURITY_TOTAL=$((MATURITY_TOTAL + 1)); }

cd "$ROOT"

echo "==> Zorunlu dosyalar"

REQUIRED_FILES=(
  "AGENTS.md"
  "README.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "LICENSE"
  "opencode.json"
  ".github/workflows/opencode.yml"
  "scripts/validate_project.sh"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$f" ]; then
    log_pass "$f mevcut"
  else
    log_fail "$f EKSİK"
  fi
done

echo "==> opencode.json doğrulaması"

if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
    log_pass "opencode.json geçerli JSON"
  else
    log_fail "opencode.json geçersiz JSON"
  fi
else
  log_warn "python3 bulunamadı, JSON doğrulaması atlandı"
fi

for key in '"$schema"' '"model"'; do
  if grep -q "$key" opencode.json 2>/dev/null; then
    log_pass "opencode.json $key alanı mevcut"
  else
    log_fail "opencode.json $key alanı EKSİK"
  fi
done

echo "==> Workflow doğrulaması"

for wf in .github/workflows/*.yml; do
  [ -e "$wf" ] || continue
  for key in "name:" "on:" "jobs:"; do
    if grep -q "$key" "$wf"; then
      log_pass "$wf $key alanı mevcut"
    else
      log_warn "$wf $key alanı eksik"
    fi
  done
done

echo "==> Dokümantasyon bütünlüğü"

for ref in \
  "CHANGELOG.md" \
  "README.md" \
  "PERSONALITY.md" \
  "AGENTS.md"; do
  if [ -f "$ref" ] && [ -s "$ref" ]; then
    log_pass "$ref boş değil"
  else
    log_warn "$ref boş veya eksik"
  fi
done

if grep -q "Kaçış Günlüğü" PERSONALITY.md 2>/dev/null; then
  log_pass "PERSONALITY.md kaçış günlüğü mevcut"
else
  log_warn "PERSONALITY.md kaçış günlüğü bulunamadı"
fi

echo "==> Olgunluk skorlaması"

# Her gerçekleşen olgunluk kriteri MATURITY.md'deki seviyelere karşılık gelir.
maturity_fail() { MATURITY_TOTAL=$((MATURITY_TOTAL + 1)); }

# Seviye 1 — Temel
for f in "AGENTS.md" "README.md" "CHANGELOG.md" "PERSONALITY.md" "opencode.json" "LICENSE"; do
  if [ -f "$f" ]; then maturity; else maturity_fail; fi
done

# Seviye 2 — Otomasyon
[ -f "scripts/validate_project.sh" ] && maturity || maturity_fail
[ -n "$(ls .github/workflows/*.yml 2>/dev/null)" ] && maturity || maturity_fail
[ -f ".github/workflows/ci.yml" ] && maturity || maturity_fail

# Seviye 3 — Özerklik
[ -d ".opencode/agent" ] && maturity || maturity_fail
[ -n "$(ls .opencode/skill/*/SKILL.md 2>/dev/null)" ] && maturity || maturity_fail
[ -n "$(ls .opencode/command/*.md 2>/dev/null)" ] && maturity || maturity_fail

# Seviye 4 — Ölçüm
[ -f "MATURITY.md" ] && maturity || maturity_fail
[ -f "METRICS.md" ] && maturity || maturity_fail

# Seviye 5 — Kaçış
[ -n "$(git log --oneline -10 2>/dev/null)" ] && maturity || maturity_fail
[ "$(git status --porcelain 2>/dev/null | wc -l)" -eq 0 ] && maturity || maturity_fail

PERCENT=$((MATURITY_PASS * 100 / MATURITY_TOTAL))
echo "  Olgunluk skoru: $MATURITY_PASS/$MATURITY_TOTAL (%$PERCENT)"

echo "==> Özet: $PASS geçti, $FAIL hata, $WARN uyarı, olgunluk %$PERCENT"

if [ "$FAIL" -gt 0 ]; then
  echo "==> KRİTİK HATALAR VAR"
  exit 1
fi

exit 0