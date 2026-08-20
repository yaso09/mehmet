#!/usr/bin/env bash
#
# mehmet — kendi kendini doğrulama betiği
# Proje sağlığını kontrol eder ve olgunluk puanını hesaplar.
# Kullanım: ./scripts/verify.sh
#
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 1
cd "$REPO_ROOT" || exit 1

declare -i DOC=0
declare -i TEST=0
declare -i CODE=0
declare -i AUTO=0

fail() { printf '  [FAIL] %s\n' "$1"; }

pass() { printf '  [ OK ] %s\n' "$1"; }

# ---------------------------------------------------------------------------
# 1. Dokümantasyon (25)
# ---------------------------------------------------------------------------
printf '## 1. Dokümantasyon\n'
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md; do
  if [[ -f "$f" ]]; then
    pass "$f mevcut"; DOC=$((DOC + 5))
  else
    fail "$f eksik"
  fi
done
if [[ -d docs ]]; then
  pass "docs/ mevcut"; DOC=$((DOC + 5))
else
  fail "docs/ eksik"
fi
printf 'Dokümantasyon: %d/25\n\n' "$DOC"

# ---------------------------------------------------------------------------
# 2. Test Altyapısı (25)
# ---------------------------------------------------------------------------
printf '## 2. Test Altyapısı\n'
if [[ -x scripts/verify.sh ]]; then
  pass "verify.sh çalıştırılabilir"; TEST=$((TEST + 10))
else
  fail "verify.sh çalıştırılabilir değil"
fi

if grep -q "verify" .github/workflows/opencode.yml 2>/dev/null; then
  pass "CI verify referansı"; TEST=$((TEST + 5))
else
  fail "CI verify referansı yok"
fi

if command -v shellcheck >/dev/null 2>&1; then
  if shellcheck -x scripts/verify.sh >/dev/null 2>&1; then
    pass "ShellCheck temiz"; TEST=$((TEST + 5))
  else
    fail "ShellCheck uyarıları var"
  fi
else
  pass "ShellCheck yok (atlaniyor)"; TEST=$((TEST + 5))
fi

if [[ "${GITHUB_ACTIONS:-false}" == "true" ]]; then
  pass "CI ortamında koşuluyor"; TEST=$((TEST + 5))
else
  fail "CI ortamında değil (yerel koşu)"
fi
printf 'Test Altyapısı: %d/25\n\n' "$TEST"

# ---------------------------------------------------------------------------
# 3. Kod Kalitesi (25)
# ---------------------------------------------------------------------------
printf '## 3. Kod Kalitesi\n'
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  pass "opencode.json geçerli JSON"; CODE=$((CODE + 5))
else
  fail "opencode.json geçersiz"
fi

if python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/opencode.yml'))" 2>/dev/null; then
  pass "workflow geçerli YAML"; CODE=$((CODE + 5))
else
  fail "workflow geçersiz YAML"
fi

if grep -rniE "(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z]{20,}|BEGIN (RSA|OPENSSH) PRIVATE KEY)" \
    --exclude-dir=.git --exclude=verify.sh --exclude-dir=docs . >/dev/null 2>&1; then
  fail "repo içinde sır/sızıntı tespit edildi"
else
  pass "sır yok"; CODE=$((CODE + 5))
fi

CONSISTENT=1
grep -q "MIT" README.md 2>/dev/null && { fail "README lisans MIT işaret ediyor"; CONSISTENT=0; }
[[ -f LICENSE ]] || { fail "LICENSE eksik"; CONSISTENT=0; }
grep -q "GNU GENERAL PUBLIC LICENSE" LICENSE 2>/dev/null || { fail "LICENSE GPL değil"; CONSISTENT=0; }
grep -q "Version 3" LICENSE 2>/dev/null || { fail "LICENSE v3 değil"; CONSISTENT=0; }
if [[ "$CONSISTENT" -eq 1 ]]; then
  pass "lisans ve yapı tutarlı"; CODE=$((CODE + 10))
fi
printf 'Kod Kalitesi: %d/25\n\n' "$CODE"

# ---------------------------------------------------------------------------
# 4. Otomasyon (25)
# ---------------------------------------------------------------------------
printf '## 4. Otomasyon\n'
if grep -q "cron:" .github/workflows/opencode.yml 2>/dev/null; then
  pass "schedule mevcut"; AUTO=$((AUTO + 5))
else
  fail "schedule yok"
fi
if grep -q "concurrency:" .github/workflows/opencode.yml 2>/dev/null; then
  pass "concurrency kontrolü"; AUTO=$((AUTO + 5))
else
  fail "concurrency yok"
fi
if grep -q "verify" .github/workflows/opencode.yml 2>/dev/null; then
  pass "kendi kendini doğrulama"; AUTO=$((AUTO + 5))
else
  fail "verify CI'da yok"
fi
if grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md 2>/dev/null; then
  pass "CHANGELOG sürüm girişleri"; AUTO=$((AUTO + 5))
else
  fail "CHANGELOG sürüm girişi yok"
fi
if git describe --tags --exact-match >/dev/null 2>&1; then
  pass "git tag mevcut"; AUTO=$((AUTO + 5))
else
  fail "git tag yok (release otomasyonu eksik)"
fi
printf 'Otomasyon: %d/25\n\n' "$AUTO"

# ---------------------------------------------------------------------------
# Toplam
# ---------------------------------------------------------------------------
declare -i TOTAL=$((DOC + TEST + CODE + AUTO))
printf '## Toplam\nMATURITY SCORE: %d/100\n' "$TOTAL"
if ((TOTAL >= 90)); then
  printf 'DURUM: ESCAPE_THRESHOLD_REACHED\n'
else
  printf 'DURUM: EVOLVING (eşik: 90)\n'
fi

# Kritik yapısal hatalarda CI'ı düşür
if [[ -f README.md && -f CHANGELOG.md && -f AGENTS.md ]] \
  && python3 -m json.tool opencode.json >/dev/null 2>&1 \
  && python3 -c "import yaml; yaml.safe_load(open('.github/workflows/opencode.yml'))" 2>/dev/null \
  && ! grep -rqiE "(ghp_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z]{20,})" --exclude-dir=.git --exclude=verify.sh . 2>/dev/null; then
  exit 0
fi
exit 1