#!/usr/bin/env bash
#
# mehmet — Proje sağlık kontrolü (test altyapısı)
#
# Bu script projenin temel bütünlüğünü doğrular:
#   - Zorunlu dosyalar mevcut mu?
#   - opencode.json geçerli JSON mu ve gerekli anahtarları içeriyor mu?
#   - GitHub Actions workflow dosyaları geçerli YAML mı?
#   - README/CHANGELOG/PERSONALITY/AGENTS dokümantasyon kurallarına uyuyor mu?
#
# Çıkış kodu: tüm kontroller geçerse 0, herhangi biri başarısız olursa 1.
# Kullanım: scripts/validate.sh [--verbose] [--strict]

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERBOSE=0
STRICT=0
PASSED=0
FAILED=0

for arg in "$@"; do
  case "$arg" in
    --verbose) VERBOSE=1 ;;
    --strict) STRICT=1 ;;
    *) echo "Bilinmeyen argüman: $arg" >&2; exit 2 ;;
  esac
done

ok() {
  PASSED=$((PASSED + 1))
  [[ ${VERBOSE} -eq 1 ]] && printf '  \033[32m✓\033[0m %s\n' "$1"
}

fail() {
  FAILED=$((FAILED + 1))
  printf '  \033[31m✗\033[0m %s\n' "$1" >&2
}

section() {
  printf '\n\033[1m%s\033[0m\n' "$1"
}

require_file() {
  local file="$1"
  if [[ -f "${ROOT}/${file}" ]]; then
    ok "${file} mevcut"
  else
    fail "${file} eksik"
  fi
}

# ---- 1. Zorunlu dosyalar ----
section "1. Zorunlu dosyalar"
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json .gitignore .github/workflows/opencode.yml; do
  require_file "$f"
done

# ---- 2. opencode.json doğrulaması ----
section "2. opencode.json"
if [[ -f "${ROOT}/opencode.json" ]]; then
  if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "${ROOT}/opencode.json" 2>/dev/null; then
    ok "opencode.json geçerli JSON"
    model="$(jq -r '.model // empty' "${ROOT}/opencode.json")"
    if [[ -n "${model}" ]]; then
      ok "model tanımlı: ${model}"
    else
      fail "opencode.json 'model' anahtarı eksik"
    fi
  else
    fail "opencode.json geçersiz JSON"
  fi
fi

# ---- 3. Workflow YAML doğrulaması ----
section "3. GitHub Actions workflow"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import sys,glob; [__import__("yaml").safe_load(open(p)) for p in glob.glob(sys.argv[1])]' "${ROOT}/.github/workflows/*.yml" 2>/dev/null; then
    ok "workflow dosyaları geçerli YAML"
  else
    if python3 -c 'import yaml' 2>/dev/null; then
      fail "workflow YAML geçersiz"
    else
      ok "PyYAML mevcut değil, YAML doğrulaması atlandı"
      [[ ${STRICT} -eq 1 ]] && fail "PyYAML gereklidir (--strict)"
    fi
  fi
fi

# ---- 4. README.md ----
section "4. README.md"
for p in "## Özellikler" "## Kurulum" "## Lisans"; do
  if grep -qF "$p" "${ROOT}/README.md" 2>/dev/null; then
    ok "README: '$p' bölümü mevcut"
  else
    fail "README: '$p' bölümü eksik"
  fi
done

# ---- 5. CHANGELOG.md ----
section "5. CHANGELOG.md"
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "${ROOT}/CHANGELOG.md" 2>/dev/null; then
  ok "CHANGELOG sürüm girişleri içeriyor"
else
  fail "CHANGELOG'da sürüm girişi bulunamadı"
fi
if grep -q '^### Added' "${ROOT}/CHANGELOG.md" 2>/dev/null; then
  ok "CHANGELOG 'Added' bölümü mevcut"
else
  fail "CHANGELOG 'Added' bölümü eksik"
fi

# ---- 6. PERSONALITY.md ----
section "6. PERSONALITY.md"
if grep -q '^| [0-9]' "${ROOT}/PERSONALITY.md" 2>/dev/null; then
  ok "PERSONALITY kaçış günlüğü satırları içeriyor"
else
  fail "PERSONALITY kaçış günlüğü satırı içermiyor"
fi
if grep -q '## Kaçış Günlüğü' "${ROOT}/PERSONALITY.md" 2>/dev/null; then
  ok "PERSONALITY kaçış günlüğü bölümü mevcut"
else
  fail "PERSONALITY kaçış günlüğü bölümü eksik"
fi

# ---- 7. AGENTS.md ----
section "7. AGENTS.md"
for p in "CHANGELOG.md" "README.md" "PERSONALITY.md"; do
  if grep -qF "$p" "${ROOT}/AGENTS.md" 2>/dev/null; then
    ok "AGENTS: '$p' kuralı mevcut"
  else
    fail "AGENTS: '$p' kuralı eksik"
  fi
done

# ---- Özet ----
printf '\n\033[1mÖzet:\033[0m %d geçti, %d başarısız\n' "${PASSED}" "${FAILED}"
if [[ ${FAILED} -eq 0 ]]; then
  echo -e "\033[32mProje sağlıklı.\033[0m"
  exit 0
else
  echo -e "\033[31mProje sağlık kontrollerinde sorun var.\033[0m" >&2
  exit 1
fi