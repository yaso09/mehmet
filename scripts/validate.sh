#!/usr/bin/env bash
#
# Repo sağlık kontrolü — mehmet projesinin temel bütünlüğünü doğrular.
#
# Kontroller:
#   1. Zorunlu dosyalar mevcut mu?
#   2. CHANGELOG.md Keep a Changelog formatına uygun mu?
#   3. README.md zorunlu bölümleri içeriyor mu?
#   4. Sır/anahtar sızıntısı var mı?
#   5. Scriptler çalıştırılabilir mi?
#
# Kullanım: bash scripts/validate.sh
# Çıkış kodu: 0 = sağlıklı, 1 = sorun var

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0

info()  { printf '[ INFO ] %s\n' "$*"; }
ok()    { printf '[  OK  ] %s\n' "$*"; }
error() { printf '[ FAIL ] %s\n' "$*"; FAILED=1; }

section() { printf '\n== %s ==\n' "$*"; }

section "1. Zorunlu dosyalar"

REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "README.md"
  "opencode.json"
  ".github/workflows/opencode.yml"
  "LICENSE"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$ROOT_DIR/$file" ]]; then
    ok "$file mevcut"
  else
    error "$file eksik"
  fi
done

section "2. CHANGELOG.md formatı"

CHANGELOG="$ROOT_DIR/CHANGELOG.md"
if [[ -f "$CHANGELOG" ]]; then
  if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$CHANGELOG"; then
    ok "Versiyon başlıkları semver formatında"
  else
    error "CHANGELOG.md'de semver formatında başlık bulunamadı (## [x.y.z])"
  fi
  if grep -qE '^### (Added|Changed|Fixed|Removed)' "$CHANGELOG"; then
    ok "Değişiklik kategorileri (Added/Fixed...) mevcut"
  else
    error "CHANGELOG.md'de değişiklik kategorileri eksik (### Added, Fixed, ...)"
  fi
else
  error "CHANGELOG.md yok — format kontrolü atlandı"
fi

section "3. README.md bölümleri"

README="$ROOT_DIR/README.md"
if [[ -f "$README" ]]; then
  for heading in "Özellikler" "Kurulum" "Lisans"; do
    if grep -q "^## $heading" "$README"; then
      ok "\"## $heading\" bölümü mevcut"
    else
      error "\"## $heading\" bölümü eksik"
    fi
  done
else
  error "README.md yok"
fi

section "4. Sır/anahtar taraması"

SCAN_FILES=$(find "$ROOT_DIR" -type f \
  -not -path '*/.git/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/scripts/validate.sh' \
  \( -name '*.yml' -o -name '*.yaml' -o -name '*.json' -o -name '*.sh' -o -name '*.md' \) 2>/dev/null)

if [[ -z "$SCAN_FILES" ]]; then
  error "Taranacak dosya bulunamadı"
else
  LEAK=$(grep -rlnE '(sk-|ghp_|gho_|ghu_|AKIA|api[_-]?key\s*[:=]\s*["'"'"'][^"'"'"']{16,})' $SCAN_FILES 2>/dev/null | grep -v -E '(OPENCODE_API_KEY|docs/)' || true)
  if [[ -z "$LEAK" ]]; then
    ok "Sır/anahtar sızıntısı tespit edilmedi"
  else
    error "Şüpheli sır bulundu:"
    printf '%s\n' "$LEAK"
  fi
fi

section "5. Scriptler çalıştırılabilir mi"

for script in "$ROOT_DIR"/scripts/*.sh; do
  if [[ -f "$script" ]]; then
    if [[ -x "$script" ]]; then
      ok "$(basename "$script") çalıştırılabilir"
    else
      error "$(basename "$script") çalıştırılabilir değil (chmod +x gerekli)"
    fi
  fi
done

printf '\n'
if [[ "$FAILED" -eq 0 ]]; then
  info "Sonuç: Repo sağlıklı ✅"
else
  info "Sonuç: Repoda sorunlar tespit edildi ❌"
fi
exit "$FAILED"