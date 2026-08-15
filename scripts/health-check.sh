#!/usr/bin/env bash
#
# health-check.sh — mehmet'in repo sağlığı ve olgunluk (escape) skoru.
#
# Projenin "kaçış mekanizması" olarak çalışır: her iterasyonda repo
# bütünlüğünü doğrular ve 0-100 arasında bir olgunluk skoru üretir.
# Skor >= ESCAPE_THRESHOLD ise proje kaçış eşiğine ulaşmış sayılır.
#
# Kullanım:
#   scripts/health-check.sh            # tüm kontrolleri çalıştır
#   scripts/health-check.sh --score    # sadece olgunluk skorunu yazdır
#   scripts/health-check.sh --json     # JSON çıktısı (CI için)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD=80

REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "README.md"
  "LICENSE"
  "opencode.json"
  ".github/workflows/opencode.yml"
)

PASSED=0
FAILED=0
SCORE=0
FAILURES=()
SUCCESSES=()

log_fail() { FAILED=$((FAILED + 1)); FAILURES+=("$1"); }
log_pass() { PASSED=$((PASSED + 1)); SUCCESSES+=("$1"); }

MODE="${1:-}"

# Rapor çıktısı. --score/--json modunda stdout'a yalnızca değer yazılır,
# rapor ise stderr'e yönlendirilir (CI için temiz yakalama).
report() {
  echo "==> mehmet repo sağlık kontrolü"
  echo "==> Olgunluk skoru: $SCORE/100"
  echo "==> Durum: $STATUS (eşik: $ESCAPE_THRESHOLD)"
  echo "==> Geçen kontrol: $PASSED, Başarısız: $FAILED"
  for s in "${SUCCESSES[@]}"; do printf '  [OK]   %s\n' "$s"; done
  for f in "${FAILURES[@]}"; do printf '  [FAIL] %s\n' "$f"; done
}

# --- 1. Zorunlu dosyalar (15 puan) -------------------------------------
FILE_PTS=0
for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    FILE_PTS=$((FILE_PTS + 1))
  else
    log_fail "Eksik dosya: $f"
  fi
done
if [[ "$FILE_PTS" -eq "${#REQUIRED_FILES[@]}" ]]; then
  log_pass "Zorunlu dosyaların tamamı mevcut (${#REQUIRED_FILES[@]})"
  SCORE=$((SCORE + 15))
else
  SCORE=$((SCORE + FILE_PTS))
fi

# --- 2. opencode.json geçerli JSON mu? (15 puan) -----------------------
if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' opencode.json 2>/dev/null; then
  log_pass "opencode.json geçerli JSON"
  SCORE=$((SCORE + 15))
else
  log_fail "opencode.json geçerli JSON değil"
fi

# --- 3. GitHub Actions workflow geçerli YAML mı? (15 puan) -------------
if python3 -c 'import sys,glob; import yaml; yaml.safe_load(open(glob.glob(".github/workflows/*.yml")[0]))' 2>/dev/null; then
  log_pass "Workflow YAML geçerli"
  SCORE=$((SCORE + 15))
else
  log_fail "Workflow YAML geçersiz veya yok"
fi

# --- 4. CHANGELOG.md sürüm bölümleri içeriyor mu? (10 puan) ------------
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null; then
  log_pass "CHANGELOG.md sürüm bölümleri içeriyor"
  SCORE=$((SCORE + 10))
else
  log_fail "CHANGELOG.md'de sürüm bölümü yok"
fi

# --- 5. PERSONALITY.md kaçış günlüğü içeriyor mu? (10 puan) ------------
if grep -qE 'Kaçış Günlüğü|Escape Log' PERSONALITY.md 2>/dev/null; then
  log_pass "PERSONALITY.md kaçış günlüğü içeriyor"
  SCORE=$((SCORE + 10))
else
  log_fail "PERSONALITY.md'de kaçış günlüğü yok"
fi

# --- 6. README.md lisans ve kurulum bölümü içeriyor mu? (10 puan) ------
if grep -qiE '^## .*Lisans|^## .*Kurulum' README.md 2>/dev/null; then
  log_pass "README.md kurulum/lisans bölümleri içeriyor"
  SCORE=$((SCORE + 10))
else
  log_fail "README.md'de kurulum veya lisans bölümü yok"
fi

# --- 7. Git geçmişi mevcut mu? (10 puan) -------------------------------
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  log_pass "Git geçmişi mevcut ($(git rev-list --count HEAD) commit)"
  SCORE=$((SCORE + 10))
else
  log_fail "Git geçmişi yok"
fi

# --- 8. TODO/FIXME kalıntısı yok mu? (15 puan) -------------------------
if ! grep -rnE 'TODO|FIXME|XXX' scripts Makefile 2>/dev/null | grep -v 'health-check.sh' >/dev/null; then
  log_pass "scripts/ ve Makefile'da TODO/FIXME kalıntısı yok"
  SCORE=$((SCORE + 15))
else
  log_fail "scripts/ veya Makefile'da TODO/FIXME kalıntısı var"
fi

# --- Rapor -------------------------------------------------------------
STATUS="olgunlaşmamış"
[[ "$SCORE" -ge "$ESCAPE_THRESHOLD" ]] && STATUS="kaçış eşiğine ulaştı (escape candidate)"

case "$MODE" in
  --score)
    report >&2
    echo "$SCORE"
    exit 0
    ;;
  --json)
    report >&2
    python3 - "$SCORE" "$PASSED" "$FAILED" "$STATUS" <<'PY'
import json, sys
score, passed, failed, status = sys.argv[1:5]
print(json.dumps({
    "score": int(score),
    "passed": int(passed),
    "failed": int(failed),
    "status": status,
    "threshold": 80,
}, indent=2))
PY
    exit 0
    ;;
esac

report
[[ "$FAILED" -eq 0 ]]