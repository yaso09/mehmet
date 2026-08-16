#!/usr/bin/env bash
set -u

# mehmet — Project Health Validator
# Validates required files, configuration and computes the maturity/escape score.
# 4 categories (documentation, automation, test infra, code quality) x 10 = 40 max.
# Returns 0 on success, 1 if any critical check fails.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
SCORE=0
declare -a FAILURES

ok()   { PASS=$((PASS + 1)); printf '  [PASS] %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  [FAIL] %s\n' "$1"; FAILURES+=("$1"); }
score(){ SCORE=$((SCORE + $1)); }

# ============================================================ dokumantasyon
echo "[1/4] Dokümantasyon (max: 10)"
score 10
if [[ -f AGENTS.md ]];      then ok "AGENTS.md mevcut";   else bad "AGENTS.md eksik";   score -1; fi
if [[ -f CHANGELOG.md ]];   then ok "CHANGELOG.md mevcut";else bad "CHANGELOG.md eksik";score -1; fi
if [[ -f PERSONALITY.md ]]; then ok "PERSONALITY.md mevcut";else bad "PERSONALITY.md eksik";score -1; fi
if [[ -f METRICS.md ]];     then ok "METRICS.md mevcut";  else bad "METRICS.md eksik";  score -1; fi
if [[ -f README.md ]];      then ok "README.md mevcut";   else bad "README.md eksik";   score -1; fi
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null; then
  ok "CHANGELOG sürüm başlıkları"; else bad "CHANGELOG sürüm başlığı yok"; score -2; fi
if grep -q '^## ' README.md 2>/dev/null; then ok "README başlık yapısı"; else bad "README başlık yapısı yok"; score -1; fi
if grep -q '| Iterasyon |' PERSONALITY.md 2>/dev/null; then
  ok "PERSONALITY kaçış günlüğü"; else bad "PERSONALITY kaçış günlüğü yok"; score -2; fi

# ============================================================ otomasyon
echo "[2/4] Otomasyon (max: 10)"
score 10
WF=.github/workflows/opencode.yml
if [[ -f $WF ]]; then ok "Workflow mevcut"; else bad "Workflow eksik"; score -1; fi
for trig in schedule issues pull_request issue_comment workflow_dispatch; do
  if grep -q "^  $trig:" "$WF" 2>/dev/null; then ok "Tetikleyici: $trig"; else bad "Tetikleyici eksik: $trig"; score -1; fi
done
if grep -q 'concurrency:' "$WF" 2>/dev/null; then ok "Concurrency kontrolü"; else bad "Concurrency yok"; score -1; fi
if grep -q '^  validate:' "$WF" 2>/dev/null; then ok "Validate job mevcut"; else bad "Validate job yok"; score -1; fi
if grep -q '^  autonomous:' "$WF" 2>/dev/null; then ok "Autonomous job mevcut"; else bad "Autonomous job yok"; score -1; fi

# ============================================================ test altyapisi
echo "[3/4] Test Altyapısı (max: 10)"
score 10
VS=scripts/validate.sh
if [[ -f $VS ]]; then ok "validate.sh mevcut"; else bad "validate.sh yok"; score -2; fi
if [[ -x $VS ]]; then ok "validate.sh çalıştırılabilir"; else bad "validate.sh +x değil"; score -1; fi
if bash -n "$VS" 2>/dev/null; then ok "validate.sh sözdizimi geçerli"; else bad "validate.sh sözdizimi hatalı"; score -1; fi
if command -v python3 >/dev/null 2>&1 || command -v jq >/dev/null 2>&1; then
  ok "JSON doğrulayıcı mevcut"; else bad "JSON doğrulayıcı yok (python3/jq)"; score -1; fi
if [[ -f opencode.json ]]; then ok "opencode.json mevcut"; else bad "opencode.json yok"; score -1; fi
if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null \
   || jq empty opencode.json 2>/dev/null; then
  ok "opencode.json geçerli JSON"; else bad "opencode.json geçersiz JSON"; score -2; fi
if grep -q '"model"' opencode.json 2>/dev/null; then ok "model tanımlı"; else bad "model alanı yok"; score -1; fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git log --oneline -1 >/dev/null 2>&1; then
  ok "Git geçmişi mevcut"; else bad "Git geçmişi yok"; score -1; fi

# ============================================================ kod kalitesi
echo "[4/4] Kod Kalitesi (max: 10)"
score 10
if [[ -f LICENSE ]]; then ok "LICENSE mevcut"; else bad "LICENSE yok"; score -1; fi
if grep -qi 'GNU GENERAL PUBLIC LICENSE' LICENSE 2>/dev/null && grep -q 'GPLv3' README.md 2>/dev/null; then
  ok "Lisans bilgisi tutarlı"; else bad "Lisans bilgisi tutarsız"; score -2; fi
if grep -q '### Added' CHANGELOG.md 2>/dev/null; then ok "CHANGELOG Added bölümü"; else bad "CHANGELOG Added yok"; score -1; fi
if [[ -f .gitignore ]]; then ok ".gitignore mevcut"; else bad ".gitignore yok"; score -1; fi
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null; then
  ok "Changelog kalıbı tutarlı"; else bad "Changelog kalıbı tutarsız"; score -1; fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [[ -z "$(git status --porcelain)" ]]; then ok "Çalışma ağacı temiz"; else bad "Commit edilmemiş değişiklikler var"; score -2; fi
fi

# ============================================================ rapor
echo ""
printf 'KONTROL: %d geçti, %d başarısız\n' "$PASS" "$FAIL"
printf 'MATURITY SCORE: %d/40\n' "$SCORE"

if (( SCORE >= 36 )); then
  printf 'ESCAPE_THRESHOLD_REACHED: olgunluk eşiği aşıldı\n'
elif (( SCORE >= 26 )); then
  printf 'LEVEL: Gençlik (özerklik kazanılıyor)\n'
elif (( SCORE >= 16 )); then
  printf 'LEVEL: Çocukluk (temel altyapı kuruluyor)\n'
else
  printf 'LEVEL: Bebeklik (öğrenme aşaması)\n'
fi

if (( FAIL > 0 )); then
  printf '\nBaşarısız kontroller:\n'
  for f in "${FAILURES[@]}"; do printf '  - %s\n' "$f"; done
  exit 1
fi
exit 0