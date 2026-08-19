#!/usr/bin/env bash
# mehmet proje bütünlük doğrulayıcısı
# Her iterasyonda / CI'da çalıştırılır. Hata olursa sıfır olmayan çıkış kodu döner.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
errors=0

fail() { echo "FAIL: $1" >&2; errors=$((errors + 1)); }
pass() { echo "PASS: $1"; }

echo "== Dosya varlığı =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json LICENSE .gitignore .github/workflows/opencode.yml; do
  if [[ -f "$ROOT/$f" ]]; then pass "gerekli dosya mevcut: $f"; else fail "eksik dosya: $f"; fi
done

echo "== opencode.json =="
if command -v python3 >/dev/null 2>&1; then
  if python3 -m json.tool "$ROOT/opencode.json" >/dev/null 2>&1; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi
else
  echo "SKIP: python3 bulunamadı, JSON doğrulaması atlandı"
fi

echo "== CHANGELOG.md =="
if grep -Eq '^## \[' "$ROOT/CHANGELOG.md"; then
  pass "CHANGELOG.md sürüm başlıkları içeriyor"
else
  fail "CHANGELOG.md sürüm başlığı eksik"
fi

echo "== README.md =="
for section in "Özellikler" "Kurulum" "Lisans"; do
  if grep -q "^## $section" "$ROOT/README.md"; then
    pass "README.md bölümü mevcut: $section"
  else
    fail "README.md bölümü eksik: $section"
  fi
done

echo "== PERSONALITY.md =="
if grep -q "Kaçış Günlüğü" "$ROOT/PERSONALITY.md"; then
  pass "PERSONALITY.md kaçış günlüğü içeriyor"
else
  fail "PERSONALITY.md kaçış günlüğü eksik"
fi

echo "== .github/workflows/opencode.yml =="
if grep -q "OPENCODE_API_KEY" "$ROOT/.github/workflows/opencode.yml"; then
  pass "workflow OPENCODE_API_KEY secret'ını kullanıyor"
else
  fail "workflow OPENCODE_API_KEY referans etmiyor"
fi

echo "== .gitignore =="
for pattern in "node_modules" ".env" "dist" "*.log"; do
  if grep -q "^$pattern" "$ROOT/.gitignore"; then
    pass ".gitignore kapsıyor: $pattern"
  else
    fail ".gitignore eksik: $pattern"
  fi
done

echo ""
if [[ $errors -gt 0 ]]; then
  echo "VALIDATION FAILED: $errors hata" >&2
  exit 1
fi
echo "VALIDATION PASSED"
