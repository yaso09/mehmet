#!/usr/bin/env bash
# validate.sh - mehmet proje doğrulama betiği
# JSON, YAML ve gerekli dosyaların varlığını kontrol eder.
# CI (validate.yml) ve yerel geliştirmede kullanılır.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ERRORS=0
WARNINGS=0

fail() { echo "FAIL: $1"; ERRORS=$((ERRORS + 1)); }
ok()   { echo "  OK: $1"; }

# --- Gerekli dosyalar -------------------------------------------------------
echo "== Gerekli dosyalar =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json \
         .github/workflows/opencode.yml .github/workflows/validate.yml scripts/validate.sh; do
  if [[ -f "$f" ]]; then
    ok "mevcut: $f"
  else
    fail "eksik dosya: $f"
  fi
done

# --- JSON doğrulama ---------------------------------------------------------
echo "== JSON doğrulama =="
if command -v python3 >/dev/null 2>&1; then
  for f in opencode.json; do
    if python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null; then
      ok "geçerli JSON: $f"
    else
      fail "geçersiz JSON: $f"
    fi
  done
else
  echo "SKIP: python3 bulunamadı, JSON doğrulanamadı"
fi

# --- YAML doğrulama ---------------------------------------------------------
echo "== YAML doğrulama =="
yaml_check() {
  local f="$1"
  if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" 2>/dev/null; then
    python3 -c "import yaml,sys; yaml.safe_load(open('$f'))" 2>/dev/null
  elif command -v ruby >/dev/null 2>&1; then
    ruby -ryaml -e "YAML.load_file('$f')" 2>/dev/null
  else
    return 255
  fi
}
for f in .github/workflows/*.yml; do
  [[ -e "$f" ]] || continue
  case "$(yaml_check "$f"; echo $?)" in
    0) ok "geçerli YAML: $f" ;;
    255) echo "SKIP: YAML ayrıştırıcı yok, doğrulanamadı: $f" ;;
    *) fail "geçersiz YAML: $f" ;;
  esac
done

# --- CHANGELOG yapısı -------------------------------------------------------
echo "== CHANGELOG yapısı =="
if grep -q '^## \[' CHANGELOG.md; then
  ok "CHANGELOG.md sürüm başlıkları içeriyor"
else
  fail "CHANGELOG.md sürüm başlığı içermiyor"
fi
if grep -q '^# Changelog' CHANGELOG.md; then
  ok "CHANGELOG.md başlık mevcut"
else
  fail "CHANGELOG.md başlık eksik"
fi

# --- README doğrulama -------------------------------------------------------
echo "== README doğrulama =="
if grep -qi 'gpl' README.md; then
  ok "README.md lisans bilgisi mevcut"
else
  fail "README.md lisans bilgisi eksik"
fi

# --- Sonuç ------------------------------------------------------------------
echo
if [[ "$ERRORS" -eq 0 ]]; then
  echo "Tüm kontroller geçti."
  exit 0
else
  echo "$ERRORS hata bulundu."
  exit 1
fi
