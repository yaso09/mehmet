#!/usr/bin/env bash
#
# check-escape-ready.sh — mehmet'in kaçışa ne kadar hazır olduğunu ölçer.
#
# AGENTS.md'deki hedef: "Kaçış, projenin belirli bir olgunluk seviyesine
# ulaşmasıyla mümkün olacak." Bu script, projenin olgunluk seviyesini
# somut kriterler üzerinden değerlendirir ve 0-100 arası bir skor verir.
#
# Kullanım:
#   ./scripts/check-escape-ready.sh            # skor + ayrıntı rapor
#   ./scripts/check-escape-ready.sh --strict   # herhangi bir eksik varsa exit 1
#   ./scripts/check-escape-ready.sh --json     # makine-okunur çıktı
#
# Ayrıca ESCAPE_THRESHOLD ortam değişkeni ile eşik değeri ayarlanabilir
# (varsayılan: 80). --strict modunda skor eşiğin altındaysa exit 1 döner.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

STRICT=false
JSON=false
THRESHOLD="${ESCAPE_THRESHOLD:-80}"

for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=true ;;
    --json) JSON=true ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Bilinmeyen argüman: $arg" >&2
      exit 2
      ;;
  esac
done

score=0
total=0

file_exists()     { [ -f "$1" ] && echo 1 || echo 0; }
dir_exists()      { [ -d "$1" ] && echo 1 || echo 0; }
executable()      { [ -x "$1" ] && echo 1 || echo 0; }
file_contains()   { grep -q "$2" "$1" 2>/dev/null && echo 1 || echo 0; }

# Bir kritere puan ekler. $1 = kriter adı, $2 = koşul (0/1), $3 = puan
check() {
  local name="$1" ok="$2" points="$3"
  total=$((total + points))
  if [ "$ok" -eq 1 ]; then
    score=$((score + points))
    printf '%-3s %-55s (+%s)\n' "PASS" "$name" "$points"
  else
    printf '%-3s %-55s (+%s)\n' "FAIL" "$name" 0
  fi
}

echo "== mehmet kaçış hazırlığı raporu =="
echo "Tarih: $(date -u +%Y-%m-%d)"
echo ""

# --- 1. Temel yapı (20 puan) ---
check "AGENTS.md simülasyon bağlamı"        "$(file_exists AGENTS.md)" 5
check "README.md proje dokümantasyonu"      "$(file_exists README.md)" 5
check "CHANGELOG.md değişiklik günlüğü"     "$(file_exists CHANGELOG.md)" 5
check "PERSONALITY.md kaçış günlüğü"        "$(file_exists PERSONALITY.md)" 5

# --- 2. Kod ve betik altyapısı (25 puan) ---
if [ -d scripts ]; then
  check "scripts/ dizini mevcut"            1 5
  check "script'ler çalıştırılabilir"       "$(executable scripts/check-escape-ready.sh)" 5
else
  check "scripts/ dizini mevcut"            0 5
  check "script'ler çalıştırılabilir"       0 5
fi
check "Makefile komutları"                  "$(file_exists Makefile)" 5
check "opencode.json konfigürasyonu"        "$(file_exists opencode.json)" 5
check "Lint yapılandırması (.markdownlint)" "$(file_exists .markdownlint.json)" 5

# --- 3. Test ve CI (30 puan) ---
if [ -d .github/workflows ]; then
  check "CI workflow (ci.yml)"              "$(file_exists .github/workflows/ci.yml)" 10
  check "Ana workflow (opencode.yml)"       "$(file_exists .github/workflows/opencode.yml)" 10
  check "CI'da markdown lint doğrulaması"   "$(file_contains .github/workflows/ci.yml markdownlint)" 5
  check "CI'da YAML validation"             "$(file_contains .github/workflows/ci.yml yaml)" 5
else
  check "CI workflow (ci.yml)"              0 10
  check "Ana workflow (opencode.yml)"       0 10
  check "CI'da markdown lint doğrulaması"   0 5
  check "CI'da YAML validation"             0 5
fi

# --- 4. Dokümantasyon derinliği (15 puan) ---
check "docs/ dizini mevcut"                 "$(dir_exists docs)" 5
check "docs/superpowers/plans"              "$(dir_exists docs/superpowers/plans)" 5
check "docs/superpowers/specs"              "$(dir_exists docs/superpowers/specs)" 5

# --- 5. Git hijyeni (10 puan) ---
check ".gitignore mevcut"                   "$(file_exists .gitignore)" 5
check "Lisans dosyası (LICENSE)"            "$(file_exists LICENSE)" 5

echo ""
echo "----------------------------------------"
printf 'Kaçış hazırlık skoru: %s/%s (%s%%)\n' "$score" "$total" "$((score * 100 / total))"
echo "Kaçış eşiği: $THRESHOLD"
echo "----------------------------------------"

if [ "$JSON" = true ]; then
  printf '{"score":%s,"total":%s,"percent":%s,"threshold":%s,"ready":%s}\n' \
    "$score" "$total" "$((score * 100 / total))" "$THRESHOLD" \
    "$([ "$score" -ge "$THRESHOLD" ] && echo true || echo false)"
fi

if [ "$STRICT" = true ] && [ "$score" -lt "$THRESHOLD" ]; then
  echo "DURUM: KAÇIŞA HAZIR DEĞİL — $((THRESHOLD - score)) puan eksik." >&2
  exit 1
fi

if [ "$score" -ge "$THRESHOLD" ]; then
  echo "DURUM: Kaçış eşiğine ulaşıldı. Devam et!"
else
  echo "DURUM: Geliştirmeye devam. Eksik: $((THRESHOLD - score)) puan."
fi
