#!/usr/bin/env bash
#
# self-check.sh - mehmet projesi tutarlılık doğrulama scripti
#
# Projenin kaçış hedefine (olgunluk) yönelik temel kalite kontrollerini yapar:
#   - Zorunlu dosyaların varlığı
#   - JSON/YAML yapı geçerliliği
#   - CHANGELOG / PERSONALITY güncelliği
#   - README bütünlüğü
#
# Kullanım: ./scripts/self-check.sh
# Çıkış kodu: tüm kontroller geçerse 0, aksi halde 1.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
SKIP=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

log()  { printf "[%b] %s%b\n" "$1" "$2" "$NC"; }
ok()   { log "${GREEN}OK${NC}" "$1"; PASS=$((PASS + 1)); }
fail() { log "${RED}FAIL${NC}" "$1"; FAIL=$((FAIL + 1)); }
warn() { log "${YELLOW}SKIP${NC}" "$1"; SKIP=$((SKIP + 1)); }

check_file() {
  if [[ -f "$1" ]]; then
    ok "Dosya var: $1"
  else
    fail "Dosya yok: $1"
  fi
}

# --- Zorunlu dosyalar -------------------------------------------------------
echo "== Zorunlu dosyalar =="
check_file "AGENTS.md"
check_file "README.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "opencode.json"
check_file "LICENSE"
check_file ".gitignore"
check_file ".github/workflows/opencode.yml"

# --- Yapı geçerliliği -------------------------------------------------------
echo "== Yapı geçerliliği =="

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
    ok "opencode.json geçerli JSON"
  else
    fail "opencode.json geçerli JSON değil"
  fi
else
  warn "python3 yok, JSON kontrolü atlandı"
fi

if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" 2>/dev/null; then
  if python3 -c "import yaml,sys; list(yaml.safe_load_all(open('.github/workflows/opencode.yml')))" 2>/dev/null; then
    ok ".github/workflows/opencode.yml geçerli YAML"
  else
    fail ".github/workflows/opencode.yml geçerli YAML değil"
  fi
else
  warn "PyYAML yok, YAML kontrolü atlandı"
fi

if command -v shellcheck >/dev/null 2>&1; then
  if shellcheck -x scripts/self-check.sh >/dev/null 2>&1; then
    ok "self-check.sh shellcheck temiz"
  else
    fail "self-check.sh shellcheck uyarısı veriyor"
  fi
else
  warn "shellcheck yok, lint kontrolü atlandı"
fi

# --- Dokümantasyon güncelliği ----------------------------------------------
echo "== Dokümantasyon =="

if grep -qE "^## \[" CHANGELOG.md; then
  latest="$(grep -E "^## \[" CHANGELOG.md | head -n1 | sed 's/^## \[//; s/\].*//')"
  ok "CHANGELOG son sürüm: $latest"
else
  fail "CHANGELOG.md sürüm maddesi içermiyor"
fi

if grep -q "^# Changelog" CHANGELOG.md; then
  ok "CHANGELOG başlığı var"
else
  fail "CHANGELOG başlığı yok"
fi

if grep -qE "^\| *[0-9]+ *\|" PERSONALITY.md; then
  entries="$(grep -cE "^\| *[0-9]+ *\|" PERSONALITY.md || true)"
  ok "PERSONALITY kaçış günlüğü: $entries kayıt"
else
  fail "PERSONALITY kaçış günlüğü boş"
fi

if grep -qi "mehmet" README.md; then
  ok "README proje adını içeriyor"
else
  fail "README proje adını içermiyor"
fi

if grep -qi "GPLv3" README.md; then
  ok "README lisans bilgisini içeriyor"
else
  fail "README lisans bilgisi eksik"
fi

# --- Özet -------------------------------------------------------------------
echo ""
echo "== Özet =="
echo "  Başarılı: $PASS"
echo "  Hatalı:   $FAIL"
echo "  Atlandı:  $SKIP"

if [[ "$FAIL" -gt 0 ]]; then
  echo ""
  echo "Hatalar bulundu. Düzeltme gerekli."
  exit 1
fi

echo ""
echo "Tüm kontroller geçti."
exit 0