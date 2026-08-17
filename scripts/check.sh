#!/usr/bin/env bash
set -euo pipefail

FAILURES=0

pass() { printf 'PASS  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; FAILURES=$((FAILURES + 1)); }

check_file_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    pass "Dosya mevcut: $file"
  else
    fail "Dosya yok: $file"
  fi
}

check_contains() {
  local file="$1"
  local needle="$2"
  local label="$3"
  if grep -q -- "$needle" "$file"; then
    pass "$label ($file)"
  else
    fail "$label ($file)"
  fi
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Zorunlu dosyalar =="
check_file_exists "$ROOT/AGENTS.md"
check_file_exists "$ROOT/README.md"
check_file_exists "$ROOT/CHANGELOG.md"
check_file_exists "$ROOT/PERSONALITY.md"
check_file_exists "$ROOT/opencode.json"
check_file_exists "$ROOT/.github/workflows/opencode.yml"

echo "== Yapısal doğrulama =="
if python3 -c "import json,sys; json.load(open('$ROOT/opencode.json'))" 2>/dev/null; then
  pass "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli JSON değil"
fi

if python3 - <<'PY' 2>/dev/null; then
import sys, glob
import yaml
for f in glob.glob('$ROOT/.github/workflows/*.yml') + glob.glob('$ROOT/.github/workflows/*.yaml'):
    yaml.safe_load(open(f))
PY
  pass "Workflow YAML'ları geçerli"
else
  fail "Workflow YAML'ları geçerli değil"
fi

echo "== İçerik kontrolü =="
check_contains "$ROOT/CHANGELOG.md" "^# Changelog" "CHANGELOG başlığı"
check_contains "$ROOT/CHANGELOG.md" "^- " "CHANGELOG madde satırları"
check_contains "$ROOT/PERSONALITY.md" "Kaçış Günlüğü" "PERSONALITY kaçış günlüğü"
check_contains "$ROOT/README.md" "^# " "README başlığı"
check_contains "$ROOT/README.md" "GPLv3" "README lisans bilgisi"
check_contains "$ROOT/AGENTS.md" "^## Kurallar" "AGENTS kurallar bölümü"

echo "== Kaçış hedefi kontrolü =="
check_file_exists "$ROOT/docs/maturity.md"
check_contains "$ROOT/docs/maturity.md" "Kaçış Eşiği" "Kaçış eşiği tanımlı"

echo ""
if [[ "$FAILURES" -eq 0 ]]; then
  echo "OK: tüm kontroller geçti."
  exit 0
else
  echo "HATA: $FAILURES kontrol başarısız."
  exit 1
fi
