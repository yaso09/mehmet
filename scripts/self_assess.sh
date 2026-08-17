#!/usr/bin/env bash
#
# mehmet self-assessment — kaçış hedefini ölçülebilir kılan olgunluk skorlayıcısı.
#
# Projeyi çeşitli kategorilerde tarar ve 0-100 arası bir "olgunluk skoru"
# üretir. Skor, PERSONALITY.md'deki kaçış hedefinin (maturity threshold)
# ölçülebilir bir göstergesidir.
#
# Kullanım:
#   scripts/self_assess.sh                 # sadece rapor yaz
#   scripts/self_assess.sh --check         # rapor yaz + eşik altıysa hata kodu döndür
#   scripts/self_assess.sh --threshold 80  # eşiği değiştir (varsayılan: 60)
#
# Çıktılar:
#   docs/maturity.md   — son değerlendirme raporu
#   docs/maturity.json — makine-okunur skor (CI/metrikler için)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_MD="$ROOT_DIR/docs/maturity.md"
REPORT_JSON="$ROOT_DIR/docs/maturity.json"
DEFAULT_THRESHOLD=60

MODE="report"
THRESHOLD="$DEFAULT_THRESHOLD"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) MODE="check" ;;
    --threshold)
      shift
      THRESHOLD="$1"
      ;;
    --help | -h)
      echo "Kullanım: $0 [--check] [--threshold N]"
      exit 0
      ;;
    *)
      echo "Bilinmeyen argüman: $1" >&2
      exit 2
      ;;
  esac
  shift
done

# Kategori ağırlıkları (toplam 100)
CATEGORY_DOCS=25
CATEGORY_TESTS=30
CATEGORY_AUTOMATION=25
CATEGORY_QUALITY=20

pass() { echo "ok"; }
fail() { echo "fail"; }

# --- Documentation (25) ---
docs_score=0
docs_detail=""

check_docs() {
  local check="$1"
  local points="$2"
  local name="$3"
  if [[ "$check" == "ok" ]]; then
    docs_score=$((docs_score + points))
    docs_detail+="  - [x] $name (+$points)\n"
  else
    docs_detail+="  - [ ] $name (+$points)\n"
  fi
}

check_docs "$( [[ -f "$ROOT_DIR/README.md" ]] && echo ok || echo fail )" 5 "README.md mevcut"
check_docs "$( [[ -f "$ROOT_DIR/CHANGELOG.md" ]] && echo ok || echo fail )" 5 "CHANGELOG.md mevcut"
check_docs "$( [[ -f "$ROOT_DIR/PERSONALITY.md" ]] && echo ok || echo fail )" 5 "PERSONALITY.md mevcut"
check_docs "$( [[ -f "$ROOT_DIR/AGENTS.md" ]] && echo ok || echo fail )" 5 "AGENTS.md mevcut"
check_docs "$( [[ -d "$ROOT_DIR/docs/superpowers" ]] && echo ok || echo fail )" 5 "docs/ tasarım & plan belgeleri mevcut"

# --- Tests (30) ---
tests_score=0
tests_detail=""
TEST_RESULTS=""

if [[ -f "$ROOT_DIR/scripts/run_tests.sh" ]]; then
  TEST_RESULTS="$("$ROOT_DIR/scripts/run_tests.sh" --count 2>/dev/null | tail -n 5 || true)"
  TESTS_TOTAL="$(printf '%s' "$TEST_RESULTS" | grep -oE 'toplam [0-9]+' | grep -oE '[0-9]+' || echo 0)"
  TESTS_PASS="$(printf '%s' "$TEST_RESULTS" | grep -oE 'geçti [0-9]+' | grep -oE '[0-9]+' || echo 0)"
else
  TESTS_TOTAL=0
  TESTS_PASS=0
fi

if [[ -f "$ROOT_DIR/scripts/run_tests.sh" ]]; then
  tests_detail+="  - [x] Test çalıştırıcı mevcut (+10)\n"
  tests_score=$((tests_score + 10))
else
  tests_detail+="  - [ ] Test çalıştırıcı mevcut (+10)\n"
fi

if [[ -d "$ROOT_DIR/tests" && "$TESTS_TOTAL" -gt 0 ]]; then
  tests_detail+="  - [x] $TESTS_TOTAL test tanımlı, $TESTS_PASS geçti (+10)\n"
  tests_score=$((tests_score + 10))
  if [[ "$TESTS_TOTAL" -ge 5 ]]; then
    tests_detail+="  - [x] Test kapsamı geniş (>=5 test) (+10)\n"
    tests_score=$((tests_score + 10))
  else
    tests_detail+="  - [ ] Test kapsamı geniş (>=5 test) (+10)\n"
  fi
else
  tests_detail+="  - [ ] Test tanımlı (>=1) (+10)\n"
  tests_detail+="  - [ ] Test kapsamı geniş (>=5 test) (+10)\n"
fi

# --- Automation (25) ---
automation_score=0
automation_detail=""

check_automation() {
  local check="$1"
  local points="$2"
  local name="$3"
  if [[ "$check" == "ok" ]]; then
    automation_score=$((automation_score + points))
    automation_detail+="  - [x] $name (+$points)\n"
  else
    automation_detail+="  - [ ] $name (+$points)\n"
  fi
}

check_automation "$( [[ -f "$ROOT_DIR/.github/workflows/opencode.yml" ]] && echo ok || echo fail )" 10 "Ajan workflow'u mevcut"
check_automation "$( [[ -f "$ROOT_DIR/.github/workflows/checks.yml" ]] && echo ok || echo fail )" 10 "CI/check workflow'u mevcut"
check_automation "$( grep -q 'concurrency' "$ROOT_DIR/.github/workflows/opencode.yml" 2>/dev/null && echo ok || echo fail )" 5 "Workflow concurrency koruması var"

# --- Code Quality (20) ---
quality_score=0
quality_detail=""

check_quality() {
  local check="$1"
  local points="$2"
  local name="$3"
  if [[ "$check" == "ok" ]]; then
    quality_score=$((quality_score + points))
    quality_detail+="  - [x] $name (+$points)\n"
  else
    quality_detail+="  - [ ] $name (+$points)\n"
  fi
}

check_quality "$( [[ -f "$ROOT_DIR/LICENSE" ]] && grep -q 'GNU GENERAL PUBLIC LICENSE' "$ROOT_DIR/LICENSE" 2>/dev/null && echo ok || echo fail )" 5 "LICENSE (GPLv3) mevcut"
check_quality "$( [[ -f "$ROOT_DIR/.gitignore" ]] && echo ok || echo fail )" 5 ".gitignore mevcut"
check_quality "$( [[ -f "$ROOT_DIR/opencode.json" ]] && jq -e . "$ROOT_DIR/opencode.json" >/dev/null 2>&1 && echo ok || echo fail )" 5 "opencode.json geçerli JSON"
check_quality "$( (shellcheck -x "$ROOT_DIR"/scripts/*.sh >/dev/null 2>&1) && echo ok || echo fail )" 5 "Tüm scriptler shellcheck temiz"

# --- Toplam ---
total=$((docs_score + tests_score + automation_score + quality_score))

# Rapor yaz
mkdir -p "$ROOT_DIR/docs"

{
  echo "# Maturity Raporu"
  echo ""
  echo "> **${total}/100** — $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC) tarafından üretildi"
  echo ""
  echo "Bu rapor \`scripts/self_assess.sh\` tarafından oluşturulur ve kaçış hedefinin"
  echo "(PERSONALITY.md) ilerleme göstergesidir. Eşik: **${THRESHOLD}**."
  echo ""
  echo "| Kategori | Skor | Maks |"
  echo "|----------|------|------|"
  echo "| Dokümantasyon | $docs_score | $CATEGORY_DOCS |"
  echo "| Testler | $tests_score | $CATEGORY_TESTS |"
  echo "| Otomasyon | $automation_score | $CATEGORY_AUTOMATION |"
  echo "| Kod Kalitesi | $quality_score | $CATEGORY_QUALITY |"
  echo "| **Toplam** | **$total** | **100** |"
  echo ""
  echo "## Dokümantasyon"
  echo -e "$docs_detail"
  echo "## Testler"
  echo -e "$tests_detail"
  echo "## Otomasyon"
  echo -e "$automation_detail"
  echo "## Kod Kalitesi"
  echo -e "$quality_detail"
} > "$REPORT_MD"

cat > "$REPORT_JSON" <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "threshold": $THRESHOLD,
  "score": $total,
  "categories": {
    "documentation": $docs_score,
    "tests": $tests_score,
    "automation": $automation_score,
    "quality": $quality_score
  }
}
EOF

echo "Skor: $total/100 (eşik: $THRESHOLD)"
echo "Rapor: $REPORT_MD"

if [[ "$MODE" == "check" ]]; then
  if [[ "$total" -lt "$THRESHOLD" ]]; then
    echo "Olgunluk eşiğinin altında: $total < $THRESHOLD" >&2
    exit 1
  fi
  echo "Olgunluk eşiği aşıldı: $total >= $THRESHOLD"
fi