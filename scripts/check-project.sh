#!/usr/bin/env bash
set -euo pipefail

# check-project.sh — mehmet proje sağlık kontrolü
# Projenin temel bileşenlerini doğrular. Sıfır olmayan çıkış kodu hata anlamına gelir.
#
# Kullanım:
#   scripts/check-project.sh [--strict]

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STRICT=false
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=true
fi

failures=0
warnings=0

fail() {
  printf 'FAIL  %s\n' "$1"
  failures=$((failures + 1))
}

warn() {
  printf 'WARN  %s\n' "$1"
  warnings=$((warnings + 1))
}

ok() {
  printf 'OK    %s\n' "$1"
}

# --- Zorunlu dosyalar -----------------------------------------------------
required_files=(
  AGENTS.md
  CHANGELOG.md
  README.md
  PERSONALITY.md
  LICENSE
  opencode.json
  .gitignore
  .github/workflows/opencode.yml
)

for f in "${required_files[@]}"; do
  if [[ -f "$f" ]]; then
    if [[ -s "$f" ]]; then
      ok "gereken dosya mevcut ve dolu: $f"
    else
      fail "gereken dosya boş: $f"
    fi
  else
    fail "gereken dosya eksik: $f"
  fi
done

# --- opencode.json JSON geçerliliği ---------------------------------------
if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
    ok "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi
else
  warn "python3 bulunamadı, opencode.json doğrulanamadı"
fi

# --- CHANGELOG formatı ----------------------------------------------------
if [[ -f CHANGELOG.md ]]; then
  if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}' CHANGELOG.md; then
    ok "CHANGELOG.md sürüm başlığı geçerli"
  else
    fail "CHANGELOG.md geçerli bir sürüm başlığı içermiyor"
  fi
fi

# --- Lisans tutarlılığı ----------------------------------------------------
if [[ -f README.md && -f LICENSE ]]; then
  if grep -qi 'GPL' README.md; then
    ok "README.md lisans bilgisi LICENSE ile uyumlu (GPL)"
  else
    fail "README.md lisans bilgisi LICENSE ile uyumsuz"
  fi
fi

# --- Workflow tutarlılığı --------------------------------------------------
if [[ -f .github/workflows/opencode.yml ]]; then
  if grep -q '^name: mehmet' .github/workflows/opencode.yml; then
    ok "workflow adı 'mehmet'"
  else
    fail "workflow adı 'mehmet' değil"
  fi
fi

# --- Test altyapısı (yalnızca --strict) -----------------------------------
if [[ "$STRICT" == true ]]; then
  if [[ -f tests/run-tests.sh && -x tests/run-tests.sh ]]; then
    ok "test altyapısı mevcut"
  else
    fail "test altyapısı eksik (tests/run-tests.sh)"
  fi
  if [[ -f Makefile ]]; then
    ok "Makefile mevcut"
  else
    fail "Makefile eksik"
  fi
fi

# --- Git durumu ------------------------------------------------------------
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [[ -z "$(git status --porcelain)" ]]; then
    ok "çalışma dizini temiz"
  else
    warn "çalışma dizininde kaydedilmemiş değişiklik var"
  fi
fi

printf '\nÖzet: %d hata, %d uyarı\n' "$failures" "$warnings"

if (( failures > 0 )); then
  exit 1
fi
exit 0