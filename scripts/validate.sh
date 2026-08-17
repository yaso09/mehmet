#!/usr/bin/env bash
#
# mehmet — Proje sağlık doğrulama scripti
#
# Kaçış hedefinin somut adımlarından biri olan test altyapısının parçasıdır.
# Projenin temel dosya yapısının ve AGENTS.md kurallarının ihlal edilmediğini
# otomatik olarak doğrular. CI'da (validate.yml) ve yerel olarak çalıştırılabilir.
#
# Kullanım:
#   ./scripts/validate.sh        # tüm kontrolleri çalıştırır
#   ./scripts/validate.sh -v     # ayrıntılı çıktı

set -u

FAILED=0
PASSED=0
VERBOSE=0

if [ "${1:-}" = "-v" ]; then
  VERBOSE=1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() {
  printf '[FAIL] %s\n' "$1"
  FAILED=$((FAILED + 1))
}

ok() {
  PASSED=$((PASSED + 1))
  if [ "$VERBOSE" -eq 1 ]; then
    printf '[ OK ] %s\n' "$1"
  fi
}

check_file_exists() {
  if [ -f "$ROOT/$1" ]; then
    ok "dosya mevcut: $1"
  else
    log "dosya eksik: $1"
  fi
}

check_contains() {
  local file="$1" pattern="$2" label="$3"
  if grep -q -- "$pattern" "$ROOT/$file"; then
    ok "$label"
  else
    log "$label ($file içinde \"$pattern\" bulunamadı)"
  fi
}

# --- 1. Zorunlu dosyalar -------------------------------------------------
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  MATURITY.md \
  LICENSE \
  opencode.json \
  .gitignore \
  .github/workflows/opencode.yml \
  .github/workflows/validate.yml; do
  check_file_exists "$f"
done

# --- 2. AGENTS.md kuralları ----------------------------------------------
check_contains AGENTS.md "CHANGELOG.md" "AGENTS.md: CHANGELOG kuralı mevcut"
check_contains AGENTS.md "README.md" "AGENTS.md: README kuralı mevcut"
check_contains AGENTS.md "PERSONALITY.md" "AGENTS.md: PERSONALITY kuralı mevcut"

# --- 3. opencode.json geçerli JSON ve model tanımlı ----------------------
if jq -e '.model' "$ROOT/opencode.json" >/dev/null 2>&1; then
  ok "opencode.json geçerli JSON ve model tanımlı"
else
  log "opencode.json geçerli JSON değil veya model eksik"
fi

# --- 4. CHANGELOG.md en son sürümün başlığı ------------------------------
if grep -q '^## \[' "$ROOT/CHANGELOG.md"; then
  ok "CHANGELOG.md sürüm başlıkları mevcut"
else
  log "CHANGELOG.md sürüm başlığı bulunamadı"
fi

# --- 5. PERSONALITY.md kaçış günlüğü -------------------------------------
if grep -q "Kaçış Günlüğü\|Escape Log" "$ROOT/PERSONALITY.md"; then
  ok "PERSONALITY.md kaçış günlüğü mevcut"
else
  log "PERSONALITY.md kaçış günlüğü eksik"
fi

# --- 6. MATURITY.md tutarlılığı ------------------------------------------
if grep -q '^|' "$ROOT/MATURITY.md"; then
  ok "MATURITY.md ilerleme tablosu mevcut"
else
  log "MATURITY.md ilerleme tablosu eksik"
fi

# --- 7. Workflow dosyaları temel event'leri içeriyor ---------------------
check_contains .github/workflows/opencode.yml "schedule" "opencode.yml: schedule tetikleyici mevcut"
check_contains .github/workflows/validate.yml "on:" "validate.yml: tetikleyici tanımlı"

# --- 8. README.md proje tanımı -------------------------------------------
check_contains README.md "mehmet" "README.md: proje adı mevcut"

echo
echo "Sonuç: $PASSED geçti, $FAILED başarısız"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi

exit 0