#!/usr/bin/env bash
#
# check_project.sh — Proje bütünlüğü ve olgunluk doğrulama betiği.
#
# Kurallar:
#   1. Zorunlu dosyaların varlığını kontrol eder.
#   2. VERSION ile CHANGELOG tutarlılığını doğrular.
#   3. opencode.json geçerliliğini doğrular.
#   4. Workflow YAML dosyalarının varlığını kontrol eder.
#   5. Kaçış günlüğünün güncel olduğunu doğrular.
#
# Çıkış kodları:
#   0 — tüm kontroller geçti
#   1 — en az bir kontrol başarısız

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  FAILURES=$((FAILURES + 1))
}

ok() {
  printf 'ok:  %s\n' "$1"
}

check_file() {
  local path="$1"
  if [[ -f "$REPO_ROOT/$path" ]]; then
    ok "dosya mevcut: $path"
  else
    fail "eksik dosya: $path"
  fi
}

# 1. Zorunlu dosyalar
echo "== Zorunlu dosyalar =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md MATURITY.md VERSION LICENSE opencode.json; do
  check_file "$f"
done
check_file ".github/workflows/opencode.yml"
check_file ".github/workflows/ci.yml"
check_file "scripts/check_project.sh"

# 2. VERSION — CHANGELOG tutarlılığı
echo "== Sürüm tutarlılığı =="
if [[ -f "$REPO_ROOT/VERSION" ]]; then
  VERSION="$(tr -d '[:space:]' < "$REPO_ROOT/VERSION")"
  if [[ -z "$VERSION" ]]; then
    fail "VERSION boş olamaz"
  elif grep -q "## \[$VERSION\]" "$REPO_ROOT/CHANGELOG.md"; then
    ok "CHANGELOG'da v$VERSION girişi mevcut"
  else
    fail "CHANGELOG'da v$VERSION girişi bulunamadı"
  fi
else
  fail "VERSION dosyası yok"
fi

# 3. opencode.json geçerliliği
echo "== JSON geçerliliği =="
if command -v python3 >/dev/null 2>&1; then
  if python3 -m json.tool "$REPO_ROOT/opencode.json" >/dev/null 2>&1; then
    ok "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi
else
  ok "python3 yok, JSON kontrolü atlandı"
fi

# 4. Workflow dosyaları geçerli YAML anahtarları
echo "== Workflow yapısı =="
for wf in "$REPO_ROOT"/.github/workflows/*.yml; do
  if grep -q '^name:' "$wf" && grep -q '^jobs:' "$wf"; then
    ok "workflow yapısı geçerli: $(basename "$wf")"
  else
    fail "workflow yapısı eksik: $(basename "$wf")"
  fi
done

# 5. Kaçış günlüğü güncel mi?
echo "== Kaçış günlüğü =="
if [[ -f "$REPO_ROOT/PERSONALITY.md" ]] && grep -q '^| [0-9]' "$REPO_ROOT/PERSONALITY.md"; then
  LAST_ITER="$(grep '^| [0-9]' "$REPO_ROOT/PERSONALITY.md" | tail -n1 | cut -d'|' -f2 | tr -d ' ')"
  ok "kaçış günlüğü en son iterasyon: $LAST_ITER"
else
  fail "PERSONALITY.md kaçış günlüğünde iterasyon satırı yok"
fi

# 6. Olgunluk skoru eşiği
echo "== Olgunluk eşiği =="
if [[ -f "$REPO_ROOT/MATURITY.md" ]] && grep -q '\*\*80/100\*\*' "$REPO_ROOT/MATURITY.md"; then
  ok "olgunluk eşiği (80/100) tanımlı"
else
  fail "MATURITY.md eşiği tanımsız"
fi

echo
if [[ "$FAILURES" -eq 0 ]]; then
  echo "SONUÇ: Tüm kontroller geçti."
  exit 0
else
  echo "SONUÇ: $FAILURES kontrol başarısız."
  exit 1
fi