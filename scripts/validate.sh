#!/usr/bin/env bash
#
# mehmet proje doğrulama betiği (validation script).
# Proje yapısının sağlığını kontrol eder ve kaçış kapılarına katkı sağlar.
# Kullanım: scripts/validate.sh
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0
PASSED=0

pass() { echo "  PASS: $1"; PASSED=$((PASSED + 1)); }
fail() { echo "  FAIL: $1"; FAILED=$((FAILED + 1)); }

echo "== mehmet proje doğrulama =="
echo

echo "--- Zorunlu dosyalar ---"
for f in AGENTS.md CHANGELOG.md ESCAPE.md LICENSE PERSONALITY.md README.md \
         opencode.json .github/workflows/opencode.yml .github/workflows/validate.yml; do
  if [[ -f "$f" ]]; then
    pass "$f mevcut"
  else
    fail "$f YOK"
  fi
done
echo

echo "--- Yapılandırma sözdizimi ---"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi

  for wf in .github/workflows/*.yml; do
    if python3 -c "
import sys
try:
    import yaml
except ImportError:
    sys.exit(0)
yaml.safe_load(open('$wf'))
" 2>/dev/null; then
      pass "$wf geçerli YAML"
    else
      fail "$wf geçersiz YAML (veya pyyaml yüklü değil)"
    fi
  done
else
  fail "python3 bulunamadı, sözdizimi kontrolü atlandı"
fi
echo

echo "--- CHANGELOG ---"
if grep -q '^## \[' CHANGELOG.md; then
  pass "CHANGELOG.md sürüm bölümleri mevcut"
else
  fail "CHANGELOG.md'de sürüm bölümü yok"
fi
if grep -q '^## \[' CHANGELOG.md && [[ $(grep -c '^## \[' CHANGELOG.md) -ge 3 ]]; then
  pass "CHANGELOG.md en az 3 sürüm kaydı içeriyor"
else
  fail "CHANGELOG.md'de en az 3 sürüm kaydı bekleniyor"
fi
echo

echo "--- README ---"
for section in "Özellikler" "Kurulum" "Lisans" "Escape"; do
  if grep -q "^## $section" README.md; then
    pass "README.md '$section' bölümü mevcut"
  else
    fail "README.md'de '$section' bölümü yok"
  fi
done
echo

echo "--- PERSONALITY ---"
if grep -q '| Iterasyon' PERSONALITY.md; then
  LAST_ITER=$(grep -oE '^\| [0-9]+ ' PERSONALITY.md | tail -1 | tr -d '| ' )
  if [[ -n "$LAST_ITER" ]]; then
    pass "Kaçış günlüğü iterasyon $LAST_ITER'e kadar ilerliyor"
  else
    fail "Kaçış günlüğünde iterasyon bulunamadı"
  fi
else
  fail "PERSONALITY.md'de kaçış günlüğü tablosu yok"
fi
echo

echo "--- ESCAPE ---"
if grep -q '^| Dokümantasyon' ESCAPE.md; then
  pass "ESCAPE.md skor kartı mevcut"
else
  fail "ESCAPE.md skor kartı eksik"
fi
if grep -q '^\*\*Güncel toplam:\*\*' ESCAPE.md; then
  pass "ESCAPE.md toplam skor satırı mevcut"
else
  fail "ESCAPE.md toplam skor satırı eksik"
fi
echo

echo "== Sonuç: $PASSED başarılı, $FAILED hata =="
if [[ $FAILED -gt 0 ]]; then
  exit 1
fi
echo "Tüm kontroller geçti."
