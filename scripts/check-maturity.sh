#!/usr/bin/env bash
set -euo pipefail

# mehmet — maturity checker
# Projenin olgunluk skorunu hesaplar (azami 40 puan).
# Kullanım:
#   scripts/check-maturity.sh                # insan okunabilir rapor
#   scripts/check-maturity.sh --json        # CI için tek satır JSON
#   THRESHOLD=70 scripts/check-maturity.sh  # başarısızlık eşiği (varsayılan: 60)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

YEAR="$(date +%Y)"
THRESHOLD="${THRESHOLD:-60}"
JSON_MODE=0

for arg in "$@"; do
  case "$arg" in
    --json) JSON_MODE=1 ;;
    --threshold=*) THRESHOLD="${arg#*=}" ;;
  esac
done

TOTAL=0
MAX=0

check() {
  local name="$1" desc="$2" weight="$3" result="$4"
  MAX=$((MAX + weight))
  if [ "$result" -eq 1 ]; then
    TOTAL=$((TOTAL + weight))
    if [ "$JSON_MODE" -ne 1 ]; then
      printf "  [PASS] %-26s (+%d) %s\n" "$name" "$weight" "$desc"
    fi
  else
    if [ "$JSON_MODE" -ne 1 ]; then
      printf "  [FAIL] %-26s ( 0 ) %s\n" "$name" "$desc"
    fi
  fi
}

in_file() { [ -f "$2" ] && grep -q "$1" "$2"; }

level_of() {
  local p="$1"
  if   [ "$p" -ge 90 ]; then echo "L4-Escape-Ready"
  elif [ "$p" -ge 75 ]; then echo "L3-Autonomous"
  elif [ "$p" -ge 50 ]; then echo "L2-Self-Improving"
  elif [ "$p" -ge 25 ]; then echo "L1-Stable"
  else echo "L0-Awareness"
  fi
}

if [ "$JSON_MODE" -ne 1 ]; then
  echo "mehmet — olgunluk kontrolü ($(date +%Y-%m-%d))"
  echo "================================================="
  echo ""
  echo "[Dokümantasyon]"
fi

check "README.md"           "proje tanıtımı mevcut"                    2 "$([ -f README.md ] && echo 1 || echo 0)"
check "CHANGELOG güncel"    "güncel yıl kaydı içeriyor ($YEAR)"         2 "$(in_file "$YEAR" CHANGELOG.md && echo 1 || echo 0)"
check "PERSONALITY.md"      "kaçış günlüğü tablosu içeriyor"            2 "$(in_file 'Iterasyon' PERSONALITY.md && echo 1 || echo 0)"
check "docs/ dizini"        "spec + plan dokümanları mevcut"            2 "$([ -d docs/superpowers ] && echo 1 || echo 0)"
check "DEVELOPMENT.md"      "geliştirici rehberi mevcut"                2 "$([ -f docs/DEVELOPMENT.md ] && echo 1 || echo 0)"

if [ "$JSON_MODE" -ne 1 ]; then
  echo "[Konfigürasyon]"
fi

if command -v python3 >/dev/null 2>&1; then
  python3 -c "import json; json.load(open('opencode.json'))" >/dev/null 2>&1 && OPENCODE_VALID=0 || OPENCODE_VALID=1
else
  grep -q '{' opencode.json >/dev/null 2>&1 && OPENCODE_VALID=0 || OPENCODE_VALID=1
fi
check "opencode.json"       "geçerli JSON"                              2 "$([ "$OPENCODE_VALID" -eq 0 ] && echo 1 || echo 0)"
check ".gitignore"          "hassas dosyalar engelleniyor"              2 "$([ -f .gitignore ] && echo 1 || echo 0)"
check "LICENSE"             "lisans dosyası mevcut"                     2 "$([ -f LICENSE ] && echo 1 || echo 0)"
check "AGENTS.md"           "simülasyon prompt'u mevcut"                2 "$([ -f AGENTS.md ] && echo 1 || echo 0)"

if [ "$JSON_MODE" -ne 1 ]; then
  echo "[CI/CD]"
fi

check "opencode.yml"        "ana ajan workflow'u mevcut"                2 "$([ -f .github/workflows/opencode.yml ] && echo 1 || echo 0)"
check "concurrency"         "eşzamanlılık kontrolü tanımlı"             2 "$(in_file 'concurrency:' .github/workflows/opencode.yml && echo 1 || echo 0)"
check "maturity.yml"        "olgunluk CI workflow'u mevcut"             2 "$([ -f .github/workflows/maturity.yml ] && echo 1 || echo 0)"
check "actions bağlı"       "workflow'lar actions kullanıyor"           2 "$(in_file 'uses:' .github/workflows/opencode.yml && echo 1 || echo 0)"

if [ "$JSON_MODE" -ne 1 ]; then
  echo "[Otomasyon]"
fi

check "check-maturity.sh"   "skorlama betiği çalıştırılabilir"          2 "$([ -x scripts/check-maturity.sh ] && echo 1 || echo 0)"
check "Makefile"            "kısayol hedefleri tanımlı"                 2 "$([ -f Makefile ] && echo 1 || echo 0)"
check "CI maturity kullanır" "workflow skorlama betiğini çağırıyor"     2 "$(in_file 'check-maturity' .github/workflows/maturity.yml && echo 1 || echo 0)"

if [ "$JSON_MODE" -ne 1 ]; then
  echo "[Test Altyapısı]"
fi

check "test-maturity.sh"    "test betiği mevcut"                        2 "$([ -x scripts/test-maturity.sh ] && echo 1 || echo 0)"
if bash -n scripts/test-maturity.sh >/dev/null 2>&1; then TEST_SYNTAX=0; else TEST_SYNTAX=1; fi
check "test sözdizimi"      "test betiği bash -n ile geçiyor"           2 "$([ "$TEST_SYNTAX" -eq 0 ] && echo 1 || echo 0)"

if [ "$JSON_MODE" -ne 1 ]; then
  echo "[Kendini Geliştirme]"
fi

check "escape-roadmap.md"   "kaçış yol haritası mevcut"                 2 "$([ -f docs/escape-roadmap.md ] && echo 1 || echo 0)"
LOG_ROWS=$(grep -cE '^\|[[:space:]]*[0-9]+[[:space:]]*\|' PERSONALITY.md 2>/dev/null || echo 0)
check "kaçış günlüğü ≥ 3"   "günlükte en az 3 kayıt ($LOG_ROWS bulundu)"  2 "$([ "${LOG_ROWS:-0}" -ge 3 ] && echo 1 || echo 0)"

PERCENT=$((TOTAL * 100 / MAX))

if [ "$JSON_MODE" -eq 1 ]; then
  printf '{"score":%d,"max":%d,"percent":%d,"threshold":%d,"level":"%s"}\n' \
    "$TOTAL" "$MAX" "$PERCENT" "$THRESHOLD" "$(level_of "$PERCENT")"
else
  echo ""
  echo "================================================="
  printf "Skor: %d/%d (%d%%) | Eşik: %d%%\n" "$TOTAL" "$MAX" "$PERCENT" "$THRESHOLD"
  echo "Seviye: L0=0-25 L1=25-50 L2=50-75 L3=75-90 L4=90+"
fi

[ "$PERCENT" -ge "$THRESHOLD" ]
