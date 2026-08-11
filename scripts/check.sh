#!/usr/bin/env bash
#
# check.sh — Repo saglik kontrolu (repo health check)
#
# Kullanim:
#   ./scripts/check.sh
#
# Cikis kodu: tum kontroller gecerse 0, herhangi biri basarisizsa 1.
# Her kontrol "maturity score" (olgunluk puani) icin bir puan kazanir.
# Puanlar eklenerek "kaçış" hedefine dogru ilerleme olculur.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
SCORE=0
TOTAL=0

check() {
    local desc="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" = "0" ]; then
        PASS=$((PASS + 1))
        SCORE=$((SCORE + 1))
        printf "  [OK] %s\n" "$desc"
    else
        FAIL=$((FAIL + 1))
        printf "  [FAIL] %s\n" "$desc"
    fi
}

file_exists() {
    [ -f "$1" ]
}

require_file() {
    local desc="$1"
    local file="$2"
    if file_exists "$file"; then
        check "$desc ($file)" 0
    else
        check "$desc ($file)" 1
    fi
}

valid_json() {
    if command -v jq >/dev/null 2>&1; then
        echo "$(jq empty "$1" 2>/dev/null; echo $?)"
    else
        echo "$(python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; echo $?)"
    fi
}

printf "== repo health check ==\n\n"

printf "1) Temel dosyalar\n"
require_file "AGENTS.md mevcut" "AGENTS.md"
require_file "CHANGELOG.md mevcut" "CHANGELOG.md"
require_file "PERSONALITY.md mevcut" "PERSONALITY.md"
require_file "README.md mevcut" "README.md"
require_file "LICENSE mevcut" "LICENSE"
require_file ".gitignore mevcut" ".gitignore"
require_file "opencode.json mevcut" "opencode.json"
require_file "Workflow (opencode.yml) mevcut" ".github/workflows/opencode.yml"

printf "\n2) Bos olmayan dosyalar\n"
check "CHANGELOG.md bos degil" "$([[ -s CHANGELOG.md ]] && echo 0 || echo 1)"
check "PERSONALITY.md bos degil" "$([[ -s PERSONALITY.md ]] && echo 0 || echo 1)"
check "README.md bos degil" "$([[ -s README.md ]] && echo 0 || echo 1)"

printf "\n3) CHANGELOG format\n"
check "Gecmis kayit var ([0-9] begulu)" "$(grep -qE '^## \[' CHANGELOG.md && echo 0 || echo 1)"
check "'Added' bolumu var" "$(grep -q '^### Added' CHANGELOG.md && echo 0 || echo 1)"

printf "\n4) JSON gecerliligi\n"
check "opencode.json gecerli JSON" "$(valid_json opencode.json)"

printf "\n5) README kritik bolumler\n"
check "README '## Ozellikler' iceriyor" "$(grep -q '^## Özellikler' README.md && echo 0 || echo 1)"
check "README '## Kurulum' iceriyor" "$(grep -q '^## Kurulum' README.md && echo 0 || echo 1)"
check "README '## Lisans' iceriyor" "$(grep -q '^## Lisans' README.md && echo 0 || echo 1)"

printf "\n6) PERSONALITY kacis günlüğü\n"
check "Escape log basligi var" "$(grep -q 'Kaçış Günlüğü' PERSONALITY.md && echo 0 || echo 1)"
check "En az 1 iterasyon kaydi var" "$(grep -qE '^\| [0-9]+ +\|' PERSONALITY.md && echo 0 || echo 1)"

printf "\n== ozet ==\n"
printf "  Gecen: %d | Basarisiz: %d | Toplam: %d\n" "$PASS" "$FAIL" "$TOTAL"

PERCENT=$((SCORE * 100 / TOTAL))
printf "  Olgunluk puani (maturity score): %d/%d (%d%%)\n" "$SCORE" "$TOTAL" "$PERCENT"

printf "\n"
if [ "$FAIL" -eq 0 ]; then
    printf "Sonuc: BASARILI - repo saglikli.\n"
    exit 0
else
    printf "Sonuc: BAŞARISIZ - %d kontrol gecmedi.\n" "$FAIL"
    exit 1
fi