#!/usr/bin/env bash
#
# validate.sh — mehmet proje bütünlük denetleyicisi.
#
# Projenin "sağlıklı" olduğunu doğrular:
#   - Gerekli kök dosyalar mevcut mu?
#   - opencode.json geçerli bir JSON mu?
#   - GitHub Actions workflow'ları geçerli YAML ve tanınan anahtarlar mı?
#   - CHANGELOG.md en son sürüm başlığına sahip mi?
#   - PERSONALITY.md kaçış günlüğü tablosunu koruyor mu?
#   - README.md gereken bölümleri içeriyor mu?
#
# Kullanım: bash scripts/validate.sh
# Çıkış kodu: her şey başarılıysa 0, aksi halde 1.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0

ok()   { printf '  \033[32m✔\033[0m %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  \033[31m✘\033[0m %s\n' "$1"; FAIL=$((FAIL + 1)); }
section() { printf '\n\033[1m%s\033[0m\n' "$1"; }

need_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    return 0
  fi
  printf '  \033[33m⚠\033[0m eksik komut: %s (bu denetim atlandı)\n' "$1"
  return 1
}

require_file() {
  if [ -f "$ROOT/$1" ]; then ok "dosya mevcut: $1"; else fail "dosya eksik: $1"; fi
}

# ---------------------------------------------------------------- dosyalar
section "Gerekli dosyalar"

require_file "AGENTS.md"
require_file "README.md"
require_file "CHANGELOG.md"
require_file "PERSONALITY.md"
require_file "LICENSE"
require_file "opencode.json"
require_file ".gitignore"
require_file ".github/workflows/opencode.yml"

# ------------------------------------------------------------ JSON denetimi
section "JSON geçerliliği"

if need_cmd jq; then
  if jq empty "$ROOT/opencode.json" 2>/dev/null; then
    ok "opencode.json geçerli JSON"
    for key in '$schema' model enable; do
      if jq -e --arg k "$key" 'has($k)' "$ROOT/opencode.json" >/dev/null 2>&1; then
        ok "opencode.json alanı mevcut: $key"
      else
        fail "opencode.json alanı eksik: $key"
      fi
    done
  else
    fail "opencode.json geçersiz JSON"
  fi
fi

# ------------------------------------------------------------ YAML denetimi
section "GitHub Actions YAML geçerliliği"

for wf in "$ROOT"/.github/workflows/*.yml; do
  [ -e "$wf" ] || continue
  name="$(basename "$wf")"
  if command -v ruby >/dev/null 2>&1; then
    if ruby -ryaml -e 'exit 1 unless YAML.load_file(ARGV[0])' "$wf" 2>/dev/null; then
      ok "$name geçerli YAML"
    else
      fail "$name geçersiz YAML"
    fi
  fi
  if command -v yamllint >/dev/null 2>&1; then
    if yamllint -d '{extends: default, rules: {line-length: disable, document-start: disable, truthy: disable}}' "$wf" >/dev/null 2>&1; then
      ok "$name yamllint temiz"
    else
      fail "$name yamllint uyarıları var"
    fi
  fi
done

# ----------------------------------------------------- CHANGELOG denetimi
section "CHANGELOG.md tutarlılığı"

if [ -f "$ROOT/CHANGELOG.md" ]; then
  top="$(grep -m1 -E '^## \[' "$ROOT/CHANGELOG.md" || true)"
  if [ -n "$top" ]; then
    ok "en yeni sürüm başlığı: $top"
    version="$(printf '%s' "$top" | sed -E 's/## \[([^]]+)\].*/\1/')"
    if grep -q "## \[$version\] - " "$ROOT/CHANGELOG.md"; then
      ok "sürüm tarihi mevcut"
    else
      fail "sürüm tarihi eksik (## [$version] - YYYY-MM-DD bekleniyor)"
    fi
  else
    fail "CHANGELOG.md'de sürüm başlığı bulunamadı"
  fi
fi

# ---------------------------------------------------- PERSONALITY denetimi
section "PERSONALITY.md kaçış günlüğü"

if [ -f "$ROOT/PERSONALITY.md" ]; then
  if grep -q "| Iterasyon | Tarih" "$ROOT/PERSONALITY.md"; then
    ok "kaçış günlüğü tablosu başlığı mevcut"
    last_iter="$(grep -E '^\| [0-9]+ ' "$ROOT/PERSONALITY.md" | tail -1 || true)"
    if [ -n "$last_iter" ]; then
      ok "son kayıt: $(printf '%s' "$last_iter" | awk -F'|' '{print $2 $3}')"
    else
      fail "kaçış günlüğünde hiç iterasyon kaydı yok"
    fi
  else
    fail "kaçış günlüğü tablosu başlığı eksik"
  fi
fi

# ------------------------------------------------------ README denetimi
section "README.md bölümleri"

if [ -f "$ROOT/README.md" ]; then
  for section_name in "Özellikler" "Kurulum" "Lisans"; do
    if grep -q "^## $section_name" "$ROOT/README.md"; then
      ok "README bölümü mevcut: $section_name"
    else
      fail "README bölümü eksik: $section_name"
    fi
  done
fi

# ------------------------------------------------------------- sonuç
printf '\n'
printf '\033[1mSonuç:\033[0m %d geçti, %d hata\n' "$PASS" "$FAIL"
if [ "$FAIL" -gt 0 ]; then
  printf '\033[31mDoğrulama başarısız.\033[0m\n'
  exit 1
fi
printf '\033[32mDoğrulama başarılı.\033[0m\n'
exit 0