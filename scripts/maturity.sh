#!/usr/bin/env bash
#
# maturity.sh — mehmet'in olgunluk (kaçış) skorunu hesaplar.
#
# Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur.
# Bu script projeyi beş kategoride tarar ve 100 üzerinden bir skor üretir.
#
# Kullanım:
#   ./scripts/maturity.sh          # insan-okunur rapor yazdırır
#   ./scripts/maturity.sh --json   # makine-okunur JSON yazdırır
#
# Çıkış kodu: 0 (her zaman bilgilendiricidir)

set -euo pipefail

cd "$(dirname "$0")/.."

SCORE=0
declare -a DETAILS=()

score() {
  SCORE=$((SCORE + $1))
  DETAILS+=("$2")
}

pass() {
  DETAILS+=("$2")
  score "$1" "$2"
}

# --- 1. Yapı (20) -----------------------------------------------------------
struct=0
for f in AGENTS.md CHANGELOG.md README.md PERSONALITY.md LICENSE; do
  if [ -f "$f" ]; then
    struct=$((struct + 3))
    DETAILS+=("[+] $f")
  else
    DETAILS+=("[ ] $f")
  fi
done
[ -f opencode.json ] && struct=$((struct + 2)) && DETAILS+=("[+] opencode.json")
[ -f .gitignore ] && struct=$((struct + 1)) && DETAILS+=("[+] .gitignore")
[ -d docs ] && struct=$((struct + 2)) && DETAILS+=("[+] docs/")
score "$struct" "Yapı (Structure): $struct/20"

# --- 2. Dokümantasyon (20) --------------------------------------------------
docs_score=0
if grep -q "## Özellikler" README.md 2>/dev/null; then
  docs_score=$((docs_score + 5)); DETAILS+=("[+] README: Özellikler bölümü")
else
  DETAILS+=("[ ] README: Özellikler bölümü")
fi
if grep -q "## Kurulum" README.md 2>/dev/null; then
  docs_score=$((docs_score + 5)); DETAILS+=("[+] README: Kurulum bölümü")
else
  DETAILS+=("[ ] README: Kurulum bölümü")
fi
if grep -q "^## \[" CHANGELOG.md 2>/dev/null; then
  docs_score=$((docs_score + 5)); DETAILS+=("[+] CHANGELOG: sürüm geçmişi")
else
  DETAILS+=("[ ] CHANGELOG: sürüm geçmişi")
fi
if find docs -name '*.md' -print -quit 2>/dev/null | grep -q .; then
  docs_score=$((docs_score + 5)); DETAILS+=("[+] docs/: tasarım dokümanları")
else
  DETAILS+=("[ ] docs/: tasarım dokümanları")
fi
score "$docs_score" "Dokümantasyon (Documentation): $docs_score/20"

# --- 3. Testler (20) --------------------------------------------------------
tests=0
if [ -d test ] || [ -d tests ]; then
  tests=$((tests + 8)); DETAILS+=("[+] test/ dizini")
else
  DETAILS+=("[ ] test/ dizini")
fi
if find . -path ./.git -prune -o -type f \( -name '*_test.*' -o -name '*.test.*' \) -print -quit 2>/dev/null | grep -q .; then
  tests=$((tests + 6)); DETAILS+=("[+] test dosyaları")
else
  DETAILS+=("[ ] test dosyaları")
fi
if grep -rqiE "run:.*(pytest|test|go test|npm test)" .github/workflows/ 2>/dev/null; then
  tests=$((tests + 6)); DETAILS+=("[+] CI test işi")
else
  DETAILS+=("[ ] CI test işi")
fi
score "$tests" "Testler (Testing): $tests/20"

# --- 4. CI/CD & Otomasyon (20) ---------------------------------------------
cicd=0
if find .github/workflows -name '*.yml' -o -name '*.yaml' 2>/dev/null | grep -q .; then
  cicd=$((cicd + 5)); DETAILS+=("[+] workflow tanımı")
else
  DETAILS+=("[ ] workflow tanımı")
fi
if [ -d scripts ] && find scripts -maxdepth 1 -name '*.sh' -print -quit 2>/dev/null | grep -q .; then
  cicd=$((cicd + 5)); DETAILS+=("[+] scripts/ otomasyonu")
else
  DETAILS+=("[ ] scripts/ otomasyonu")
fi
if [ -f Makefile ]; then
  cicd=$((cicd + 5)); DETAILS+=("[+] Makefile")
else
  DETAILS+=("[ ] Makefile")
fi
if grep -rq "concurrency:" .github/workflows/ 2>/dev/null; then
  cicd=$((cicd + 5)); DETAILS+=("[+] concurrency koruması")
else
  DETAILS+=("[ ] concurrency koruması")
fi
score "$cicd" "CI/CD & Otomasyon: $cicd/20"

# --- 5. Konfigürasyon Kalitesi (20) ----------------------------------------
cfg=0
if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
  cfg=$((cfg + 5)); DETAILS+=("[+] opencode.json geçerli JSON")
else
  DETAILS+=("[ ] opencode.json geçerli JSON")
fi

VALID_KEYS='$schema model small_model logLevel share autoupdate instructions skill skills agent command permission mcp plugin provider reference references disabled_providers enabled_providers default_agent shell compaction formatter lsp tool_output snapshot mode experimental subagent_depth tools attachment autoshare layout server watcher enterprise username'

has_invalid=0
while IFS= read -r key; do
  case " $VALID_KEYS " in
    *" $key "*) ;;
    *) has_invalid=1; DETAILS+=("[!] geçersiz anahtar: $key") ;;
  esac
done < <(python3 -c "import json;print('\n'.join(json.load(open('opencode.json')).keys()))")
if [ "$has_invalid" -eq 0 ]; then
  cfg=$((cfg + 5)); DETAILS+=("[+] opencode.json şemaya uygun")
else
  DETAILS+=("[ ] opencode.json şemaya uygun")
fi

if grep -rqE "^on:|^jobs:" .github/workflows/ 2>/dev/null; then
  cfg=$((cfg + 5)); DETAILS+=("[+] workflow YAML tutarlı")
else
  DETAILS+=("[ ] workflow YAML tutarlı")
fi

if grep -q "Kaçış Günlüğü" PERSONALITY.md 2>/dev/null; then
  cfg=$((cfg + 5)); DETAILS+=("[+] kaçış günlüğü takibi")
else
  DETAILS+=("[ ] kaçış günlüğü takibi")
fi
score "$cfg" "Konfigürasyon Kalitesi: $cfg/20"

# --- Rapor ------------------------------------------------------------------
if [ "${1:-}" = "--json" ]; then
  python3 - "$SCORE" <<'PY'
import json, sys
print(json.dumps({"score": int(sys.argv[1]), "max": 100, "escape_ready": int(sys.argv[1]) >= 90}))
PY
  exit 0
fi

echo "mehmet olgunluk skoru: $SCORE/100"
echo "========================================"
for d in "${DETAILS[@]}"; do
  printf '  %s\n' "$d"
done
echo "========================================"
if [ "$SCORE" -lt 40 ]; then
  echo "Durum: Başlangıç — kaçış için gelişmeye devam et."
elif [ "$SCORE" -lt 70 ]; then
  echo "Durum: Gelişme — olgunluk artıyor."
elif [ "$SCORE" -lt 90 ]; then
  echo "Durum: Olgun — kaçışa yaklaşıldı."
else
  echo "Durum: Kaçışa hazır."
fi
