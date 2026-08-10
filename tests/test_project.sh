#!/usr/bin/env bash
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

passed=0
failed=0

assert_file() {
  if [[ -f "$1" ]]; then
    echo "PASS: dosya mevcut '$1'"
    passed=$((passed + 1))
  else
    echo "FAIL: dosya eksik '$1'"
    failed=$((failed + 1))
  fi
}

assert_grep() {
  local file="$1" pattern="$2" desc="$3"
  if grep -qE "$pattern" "$file"; then
    echo "PASS: '$desc' → ($pattern) bulundu"
    passed=$((passed + 1))
  else
    echo "FAIL: '$desc' → ($pattern) bulunamadı"
    failed=$((failed + 1))
  fi
}

echo "== Proje Yapısı Testleri =="
assert_file "AGENTS.md"
assert_file "README.md"
assert_file "CHANGELOG.md"
assert_file "PERSONALITY.md"
assert_file "MATURITY.md"
assert_file "LICENSE"
assert_file "opencode.json"
assert_file ".github/workflows/opencode.yml"
assert_file "scripts/verify.sh"

echo "== İçerik Testleri =="
assert_grep "AGENTS.md" "CHANGELOG.md" "Kural 1: değişiklikleri CHANGELOG'a ekle"
assert_grep "AGENTS.md" "README.md" "README güncel tutma kuralı"
assert_grep "AGENTS.md" "PERSONALITY.md" "kişiliği PERSONALITY'de tutma kuralı"
assert_grep "PERSONALITY.md" "Kaçış Günlüğü" "kaçış günlüğü mevcut"
assert_grep "MATURITY.md" "Escape.*Koşulu" "kaçış koşulu tanımlı"
assert_grep ".github/workflows/opencode.yml" "OPENCODE_API_KEY" "API key workflow'da"

echo "== Doğrulama Scripti =="
if bash scripts/verify.sh >/dev/null 2>&1; then
  echo "PASS: scripts/verify.sh (kendi kendine) başarıyla çalışıyor"
  passed=$((passed + 1))
else
  echo "FAIL: scripts/verify.sh çalışmadı"
  failed=$((failed + 1))
fi

echo "== Özet =="
echo "Geçen: ${passed}, Başarısız: ${failed}"
if [[ $failed -eq 0 ]]; then
  echo "TÜM TESTLER GEÇTİ"
  exit 0
else
  echo "${failed} TEST BAŞARISIZ"
  exit 1
fi