#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0

log_ok()   { printf "  \033[32mPASS\033[0m  %s\n" "$1"; }
log_fail() { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; FAILED=1; }

required_files=(
  "AGENTS.md"
  "CHANGELOG.md"
  "LICENSE"
  "PERSONALITY.md"
  "README.md"
  "opencode.json"
  ".github/workflows/opencode.yml"
)

echo "== Dosya bütünlüğü =="
for f in "${required_files[@]}"; do
  if [ -f "$f" ]; then
    log_ok "$f mevcut"
  else
    log_fail "$f eksik"
  fi
done

echo "== JSON doğrulama =="
while IFS= read -r -d '' file; do
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$file" 2>/dev/null; then
    log_ok "$file geçerli JSON"
  else
    log_fail "$file geçersiz JSON"
  fi
done < <(find . -name "*.json" -not -path "./node_modules/*" -print0)

echo "== YAML doğrulama =="
while IFS= read -r -d '' file; do
  if python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$file" 2>/dev/null; then
    log_ok "$file geçerli YAML"
  else
    log_fail "$file geçersiz YAML"
  fi
done < <(find .github -name "*.yml" -o -name "*.yaml" | while read -r f; do printf '%s\0' "$f"; done)

echo "== İçerik kontrolü =="
check_non_empty() {
  local f="$1"
  if [ -s "$f" ]; then
    log_ok "$f boş değil"
  else
    log_fail "$f boş"
  fi
}
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md; do
  check_non_empty "$f"
done

echo "== CHANGELOG uygunluğu =="
if grep -q "## \[" CHANGELOG.md; then
  log_ok "CHANGELOG.md sürüm başlıkları içeriyor"
else
  log_fail "CHANGELOG.md'de sürüm başlığı bulunamadı"
fi

echo "== Lisans uygunluğu =="
if grep -qi "GPL" LICENSE; then
  log_ok "LICENSE GPL içeriyor"
else
  log_fail "LICENSE GPL içermiyor"
fi
if grep -qi "GPL" README.md; then
  log_ok "README.md lisansı LICENSE ile uyumlu (GPL)"
else
  log_fail "README.md lisans bilgisi uyumsuz"
fi

echo "== Git temizliği =="
if [ -z "$(git status --porcelain)" ]; then
  log_ok "çalışma dizini temiz"
else
  log_fail "işlenmemiş değişiklikler var"
fi

echo ""
if [ "$FAILED" -eq 0 ]; then
  printf "\033[32mTüm kontroller geçti.\033[0m\n"
  exit 0
else
  printf "\033[31mBazı kontroller başarısız.\033[0m\n"
  exit 1
fi