#!/usr/bin/env bash
#
# mehmet health check — projenin sağlığını ve olgunluk skorunu doğrular.
#
# Kullanım:
#   scripts/health-check.sh            # raporu yazdırır, hata yoksa 0 döner
#   scripts/health-check.sh --json    # JSON çıktı üretir (CI için)
#
# Çıkış kodları:
#   0  başarılı (kritik hata yok)
#   1  kritik hata (eksik dosya / geçersiz içerik)
#
set -euo pipefail

cd "$(dirname "$0")/.."

JSON_MODE=0
[[ "${1:-}" == "--json" ]] && JSON_MODE=1

PASS=0
FAIL=0
WARN=0
SCORE=0
TOTAL=0
CRITICAL_FAILED=0

REPORT=()

log() { REPORT+=("$1"); }
pass() { PASS=$((PASS + 1)); SCORE=$((SCORE + 1)); TOTAL=$((TOTAL + 1)); }
fail() { FAIL=$((FAIL + 1)); TOTAL=$((TOTAL + 1)); }
warn() { WARN=$((WARN + 1)); }

ok()    { log "  [OK]   $1"; pass; }
bad()   { log "  [HATA] $1"; fail; CRITICAL_FAILED=1; }
soft()  { log "  [UYARI] $1"; warn; }

check_file_exists() {
  local f="$1"
  if [[ -f "$f" ]]; then ok "Dosya mevcut: $f"; else bad "Eksik dosya: $f"; fi
}

# ---------------------------------------------------------------------------
# 1. Zorunlu dosyalar
# ---------------------------------------------------------------------------
log "== 1. Zorunlu dosyalar =="
check_file_exists "AGENTS.md"
check_file_exists "CHANGELOG.md"
check_file_exists "README.md"
check_file_exists "PERSONALITY.md"
check_file_exists "opencode.json"
check_file_exists ".github/workflows/opencode.yml"

# ---------------------------------------------------------------------------
# 2. CHANGELOG.md tutarlılığı
# ---------------------------------------------------------------------------
log ""
log "== 2. CHANGELOG.md =="
if [[ -f "CHANGELOG.md" ]]; then
  if grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
    ok "CHANGELOG.md sürüm girdileri içeriyor"
  else
    bad "CHANGELOG.md'de sürüm girdisi yok ([x.y.z] formatı)"
  fi
  if grep -q "^# Changelog" CHANGELOG.md; then
    ok "CHANGELOG.md başlığı doğru"
  else
    bad "CHANGELOG.md başlığı eksik (# Changelog)"
  fi
fi

# ---------------------------------------------------------------------------
# 3. README.md tutarlılığı
# ---------------------------------------------------------------------------
log ""
log "== 3. README.md =="
if [[ -f "README.md" ]]; then
  for section in "Özellikler" "Kurulum" "Lisans"; do
    if grep -q "^## ${section}" README.md; then
      ok "README.md '${section}' bölümü mevcut"
    else
      soft "README.md '${section}' bölümü eksik"
    fi
  done
fi

# ---------------------------------------------------------------------------
# 4. PERSONALITY.md kaçış günlüğü
# ---------------------------------------------------------------------------
log ""
log "== 4. PERSONALITY.md =="
if [[ -f "PERSONALITY.md" ]]; then
  if grep -q "Kaçış Günlüğü" PERSONALITY.md; then
    ok "PERSONALITY.md kaçış günlüğü mevcut"
  else
    bad "PERSONALITY.md kaçış günlüğü eksik"
  fi
  LOG_ROWS=$(grep -cE "^\| [0-9]+ " PERSONALITY.md || true)
  if [[ "$LOG_ROWS" -ge 3 ]]; then
    ok "Kaçış günlüğünde ${LOG_ROWS} iterasyon kaydı var"
  elif [[ "$LOG_ROWS" -ge 1 ]]; then
    soft "Kaçış günlüğü az kayıt içeriyor (${LOG_ROWS})"
  fi
fi

# ---------------------------------------------------------------------------
# 5. opencode.json geçerliliği
# ---------------------------------------------------------------------------
log ""
log "== 5. opencode.json =="
if [[ -f "opencode.json" ]]; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1 || jq empty opencode.json >/dev/null 2>&1; then
    ok "opencode.json geçerli JSON"
  else
    bad "opencode.json geçersiz JSON"
  fi
  if grep -q '"model"' opencode.json; then
    ok "opencode.json model tanımlı"
  else
    bad "opencode.json'da model eksik"
  fi
fi

# ---------------------------------------------------------------------------
# 6. Workflow yapısı
# ---------------------------------------------------------------------------
log ""
log "== 6. GitHub Actions workflow =="
WF=".github/workflows/opencode.yml"
if [[ -f "$WF" ]]; then
  if grep -q "concurrency:" "$WF"; then
    ok "Workflow concurrency kontrolü içeriyor"
  else
    soft "Workflow concurrency kontrolü yok"
  fi
  if grep -q "OPENCODE_API_KEY" "$WF"; then
    ok "Workflow OPENCODE_API_KEY kullanıyor"
  else
    bad "Workflow OPENCODE_API_KEY kullanmıyor"
  fi
fi

# ---------------------------------------------------------------------------
# 7. AGENTS.md kuralları
# ---------------------------------------------------------------------------
log ""
log "== 7. AGENTS.md =="
if [[ -f "AGENTS.md" ]]; then
  for rule in "CHANGELOG.md" "README.md" "PERSONALITY.md" "kaçış"; do
    if grep -qi "$rule" AGENTS.md; then
      ok "AGENTS.md '${rule}' kuralını içeriyor"
    else
      soft "AGENTS.md '${rule}' kuralını içermiyor"
    fi
  done
fi

# ---------------------------------------------------------------------------
# 8. TODO / FIXME kalıntıları
# ---------------------------------------------------------------------------
log ""
log "== 8. Kod kalıntıları =="
STRAY=$(grep -rn -E "TODO|FIXME|XXX" \
  --include="*.sh" --include="*.py" --include="*.ts" --include="*.js" \
  --include="*.json" --include="*.yml" \
  --exclude-dir=".git" --exclude-dir="node_modules" . 2>/dev/null \
  | grep -v "health-check.sh" || true)
if [[ -z "$STRAY" ]]; then
  ok "TODO/FIXME kalıntısı yok"
else
  soft "TODO/FIXME kalıntıları bulundu"
fi

# ---------------------------------------------------------------------------
# Olgunluk skoru
# ---------------------------------------------------------------------------
MATURITY_PERCENT=$(( SCORE * 100 / TOTAL ))

log ""
log "== 9. Olgunluk skoru =="
log "  Başarılı: ${PASS}   Uyarı: ${WARN}   Hata: ${FAIL}   Toplam: ${TOTAL}"
log "  MATURITY_SCORE: ${MATURITY_PERCENT}%"

if [[ "$JSON_MODE" -eq 1 ]]; then
  jq -n \
    --argjson pass "$PASS" \
    --argjson warn "$WARN" \
    --argjson fail "$FAIL" \
    --argjson maturity "$MATURITY_PERCENT" \
    --arg critical "$CRITICAL_FAILED" \
    '{pass: $pass, warn: $warn, fail: $fail, maturity: $maturity, critical_failed: $critical}'
else
  printf "%s\n" "${REPORT[@]}"
  echo ""
fi

if [[ "$CRITICAL_FAILED" -eq 1 ]]; then
  echo "Sağlık kontrolü başarısız: kritik hatalar var." >&2
  exit 1
fi

echo "Sağlık kontrolü başarılı."
exit 0