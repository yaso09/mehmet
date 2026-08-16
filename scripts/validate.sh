#!/usr/bin/env bash
# mehmet - proje sağlık kontrolü / doğrulama scripti.
#
# Kullanım: bash scripts/validate.sh
# Çıkış kodu 0 = tüm kontroller geçti, 1 = en az bir kontrol başarısız.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0

pass() {
  printf 'PASS: %s\n' "$1"
}

fail() {
  printf 'FAIL: %s\n' "$1"
  FAILED=1
}

check_file() {
  local desc="$1" path="$2"
  if test -f "$path"; then
    pass "$desc"
  else
    fail "$desc"
  fi
}

# 1. Kritik dosyalar mevcut mu?
echo "== Dosya varlığı =="
for f in \
  AGENTS.md \
  README.md \
  CHANGELOG.md \
  PERSONALITY.md \
  MATURITY.md \
  LICENSE \
  VERSION \
  opencode.json \
  .github/workflows/opencode.yml \
  .github/workflows/ci.yml; do
  check_file "Gerekli dosya mevcut: $f" "$f"
done

# 2. opencode.json geçerli JSON mu?
echo "== Konfigürasyon =="
if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' opencode.json 2>/dev/null; then
  pass "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli JSON"
fi

# 3. Sürüm tutarlılığı: VERSION <-> CHANGELOG <-> README
echo "== Sürüm tutarlılığı =="
VERSION="$(tr -d '[:space:]' < VERSION)"
if grep -q "^## \[$VERSION\]" CHANGELOG.md; then
  pass "CHANGELOG.md'de v$VERSION kaydı var"
else
  fail "CHANGELOG.md'de v$VERSION kaydı yok"
fi

if grep -q "$VERSION" README.md; then
  pass "README.md v$VERSION'dan bahsediyor"
else
  fail "README.md v$VERSION'dan bahsetmiyor"
fi

# 4. Kaçış günlüğü en az 3 iterasyon içeriyor mu?
echo "== Kaçış günlüğü =="
ROWS="$(grep -c '^| [0-9]' PERSONALITY.md || true)"
if test "$ROWS" -ge 3; then
  pass "Kaçış günlüğü en az 3 iterasyon içeriyor ($ROWS kayıt)"
else
  fail "Kaçış günlüğü yetersiz ($ROWS kayıt, en az 3 gerekli)"
fi

if grep -q '^## Kaçış Günlüğü' PERSONALITY.md; then
  pass "Kaçış Günlüğü başlığı mevcut"
else
  fail "Kaçış Günlüğü başlığı eksik"
fi

# 5. Workflow OPENCODE_API_KEY secret'ını kullanıyor mu?
echo "== Workflow =="
if grep -q 'OPENCODE_API_KEY' .github/workflows/opencode.yml; then
  pass "opencode.yml OPENCODE_API_KEY kullanıyor"
else
  fail "opencode.yml OPENCODE_API_KEY kullanmıyor"
fi

# 6. MATURITY.md skoru hesaplanabiliyor mu? (en az bir "Toplam" satırı)
echo "== Olgunluk =="
if grep -q '^## Skor Kartı' MATURITY.md; then
  pass "MATURITY.md skor kartı mevcut"
else
  fail "MATURITY.md skor kartı eksik"
fi

echo ""
if test "$FAILED" -eq 0; then
  echo "ALL CHECKS PASSED"
  exit 0
else
  echo "VALIDATION FAILED"
  exit 1
fi