#!/usr/bin/env bash
# mehmet proje sağlık kontrolü
# Her iterasyonda projenin temel bütünlüğünü doğrular.
# Kullanım: bash scripts/health-check.sh

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILURES=0
WARNINGS=0

pass()  { printf "  PASS  %s\n" "$1"; }
warn()  { printf "  WARN  %s\n" "$1"; WARNINGS=$((WARNINGS + 1)); }
fail()  { printf "  FAIL  %s\n" "$1"; FAILURES=$((FAILURES + 1)); }

check_file() {
  if [ -f "$1" ]; then pass "$1 mevcut"; else fail "$1 eksik"; fi
}

check_contains() {
  if grep -q "$2" "$1" 2>/dev/null; then pass "$1 '$2' içeriyor"; else fail "$1 '$2' içermiyor"; fi
}

echo "== Zorunlu dosyalar =="
check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "LICENSE"
check_file "opencode.json"
check_file "METRICS.md"
check_file "VERSION"
check_file ".github/workflows/opencode.yml"
check_file ".github/workflows/validate.yml"

echo "== Temel bütünlük =="
check_contains "opencode.json" "deepseek-v4-flash-free"
check_contains "LICENSE" "GNU GENERAL PUBLIC LICENSE"
check_contains "README.md" "GPLv3"

echo "== Versiyon tutarlılığı =="
VERSION_FILE="VERSION"
if [ -f "$VERSION_FILE" ]; then
  VERSION_VALUE="$(head -n1 "$VERSION_FILE" | tr -d '[:space:]')"
  if grep -q "\[$VERSION_VALUE\]" "CHANGELOG.md"; then
    pass "CHANGELOG.md VERSION ($VERSION_VALUE) ile uyumlu"
  else
    warn "CHANGELOG.md VERSION ($VERSION_VALUE) için kayıt içermiyor"
  fi
fi

echo "== Kaçış günlüğü =="
if [ -f "PERSONALITY.md" ]; then
  LOG_ROWS="$(grep -c '^| [0-9]' PERSONALITY.md || true)"
  if [ "$LOG_ROWS" -ge 3 ]; then
    pass "Kaçış günlüğünde $LOG_ROWS iterasyon kaydı var"
  else
    warn "Kaçış günlüğü az ($LOG_ROWS kayıt)"
  fi
fi

echo ""
echo "Sonuç: $FAILURES hata, $WARNINGS uyarı"

if [ "$FAILURES" -gt 0 ]; then
  echo "Sağlık kontrolü BAŞARISIZ."
  exit 1
fi

echo "Sağlık kontrolü başarılı."
exit 0