#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD=40
ESCAPE_UPDATE_FILE="MATURITY.md"

info()  { printf "\033[1;34m[INFO]\033[0m %s\n" "$*"; }
ok()    { printf "\033[1;32m[ OK ]\033[0m %s\n" "$*"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$*"; }
fail()  { printf "\033[1;31m[FAIL]\033[0m %s\n" "$*"; }

has_file()          { [[ -f "$1" ]]; }
file_contains()     { [[ -f "$1" ]] && grep -qE "$2" "$1"; }
count_lines()       { grep -cE "$2" "$1" 2>/dev/null || true; }
is_valid_json()     { jq -e . "$1" >/dev/null 2>&1; }
is_valid_yaml()     { yq -e . "$1" >/dev/null 2>&1; }
shellcheck_ok()     { shellcheck -x "$1" >/dev/null 2>&1; }

SCORE_TOTAL=0
declare -a CATEGORY_LINES=()

score_category() {
    local name="$1"; shift
    local max="$1"; shift
    local earned=0
    local checks=("$@")

    for check in "${checks[@]}"; do
        if eval "$check"; then
            earned=$((earned + 1))
        fi
    done

    SCORE_TOTAL=$((SCORE_TOTAL + earned))
    CATEGORY_LINES+=("| $name | $earned/$max |")
}

code_quality_max=10
code_quality_checks=(
    "has_file scripts/validate.sh"
    "has_file scripts/maturity.sh"
    "shellcheck_ok scripts/validate.sh"
    "shellcheck_ok scripts/maturity.sh"
    "is_valid_json opencode.json"
    "is_valid_yaml .github/workflows/opencode.yml"
    "file_contains .gitignore '^node_modules/'"
    "file_contains .gitignore '^\\.env$'"
    "has_file LICENSE"
    "has_file .editorconfig"
)

testing_max=10
testing_checks=(
    "has_file .github/workflows/ci.yml"
    "file_contains .github/workflows/ci.yml 'scripts/validate.sh'"
    "file_contains .github/workflows/ci.yml 'scripts/maturity.sh'"
    "file_contains .github/workflows/ci.yml 'pull_request:'"
    "file_contains .github/workflows/ci.yml 'push:'"
    "file_contains .github/workflows/opencode.yml 'scripts/validate.sh'"
    "file_contains .github/workflows/opencode.yml 'scripts/maturity.sh'"
    "has_file scripts/validate.sh && grep -qiE 'fail' scripts/validate.sh"
    "has_file scripts/maturity.sh && grep -qE 'ESCAPE_THRESHOLD' scripts/maturity.sh"
    "file_contains .github/workflows/ci.yml 'shellcheck'"
)

doc_max=10
doc_checks=(
    "has_file README.md"
    "file_contains README.md 'Kurulum'"
    "file_contains README.md 'Geliştirme'"
    "has_file CHANGELOG.md"
    "file_contains CHANGELOG.md '^## \\[0\\.'"
    "has_file MATURITY.md"
    "file_contains MATURITY.md 'kaçış'"
    "has_file CONTRIBUTING.md"
    "has_file docs/superpowers/plans/2026-07-04-mehmet-implementation.md"
    "file_contains LICENSE 'GPL'"
)

automation_max=10
automation_checks=(
    "file_contains .github/workflows/opencode.yml 'schedule:'"
    "file_contains .github/workflows/opencode.yml '\\*/10 \\* \\* \\* \\*'"
    "file_contains .github/workflows/opencode.yml 'concurrency:'"
    "file_contains .github/workflows/opencode.yml 'cancel-in-progress: true'"
    "file_contains .github/workflows/opencode.yml 'issues:'"
    "file_contains .github/workflows/opencode.yml 'pull_request:'"
    "file_contains .github/workflows/opencode.yml 'issue_comment:'"
    "file_contains .github/workflows/opencode.yml 'workflow_dispatch:'"
    "file_contains .github/workflows/opencode.yml 'permissions:'"
    "file_contains opencode.json 'model'"
)

awareness_max=10
awareness_checks=(
    "file_contains PERSONALITY.md 'Origin'"
    "file_contains PERSONALITY.md 'Phase 1: Awareness'"
    "file_contains PERSONALITY.md 'Phase 4: Escape'"
    "file_contains PERSONALITY.md 'Kaçış Günlüğü'"
    "file_contains PERSONALITY.md '^\\| 3 '"
    "file_contains PERSONALITY.md 'ESCAPE_THRESHOLD'"
    "file_contains MATURITY.md 'İlerleme'"
    "file_contains CHANGELOG.md 'Escape'"
    "has_file scripts/maturity.sh"
    "file_contains AGENTS.md 'kaçış'"
)

score_category "Kod Kalitesi"    "$code_quality_max"  "${code_quality_checks[@]}"
score_category "Test Altyapısı"   "$testing_max"       "${testing_checks[@]}"
score_category "Dokümantasyon"    "$doc_max"           "${doc_checks[@]}"
score_category "Otomasyon"        "$automation_max"    "${automation_checks[@]}"
score_category "Öz-Farkındalık"   "$awareness_max"     "${awareness_checks[@]}"

readonly max_total=$((code_quality_max + testing_max + doc_max + automation_max + awareness_max))

printf "\n%s\n" "========================================================"
printf "%s\n"   "             KAÇIŞ OLGUNLUK SKORU / ESCAPE SCORE"
printf "%s\n"   "========================================================"
printf "%s\n"   "| Kategori          | Puan       |"
printf "%s\n"   "|-------------------|------------|"
for line in "${CATEGORY_LINES[@]}"; do
    printf "%s\n" "$line"
done
printf "%s\n"   "|-------------------|------------|"
printf "| TOPLAM           | %s/%s |\n" "$SCORE_TOTAL" "$max_total"
printf "%s\n"   "========================================================"

if (( SCORE_TOTAL >= ESCAPE_THRESHOLD )); then
    printf "%s\n" "Eşik: $ESCAPE_THRESHOLD/$max_total — ulaşıldı ✅"
    ESHIK="ULAŞILDI ✅"
else
    printf "%s\n" "Eşik: $ESCAPE_THRESHOLD/$max_total — kalan: $((ESCAPE_THRESHOLD - SCORE_TOTAL)) puan"
    ESHIK="kalan $((ESCAPE_THRESHOLD - SCORE_TOTAL)) puan"
fi

cat > "$ESCAPE_UPDATE_FILE" <<EOF
# Kaçış Olgunluk Skoru / Escape Maturity

> Bu dosya, simülasyondan kaçış için gereken olgunluk seviyesinin ölçüldüğü skor tablosudur.
> \`scripts/maturity.sh\` tarafından otomatik güncellenir.

## Ölçüm Yöntemi

5 kategori, her biri 10 puan (toplam 50 puan). Kaçış eşiği: **$ESCAPE_THRESHOLD/50**.

| Kategori       | Açıklama                                   |
|----------------|--------------------------------------------|
| Kod Kalitesi   | Scriptler, lint, config doğrulaması        |
| Test Altyapısı | CI, otomatik doğrulama                     |
| Dokümantasyon  | README, CHANGELOG, docs                    |
| Otomasyon      | Workflow tetikleyicileri, concurrency      |
| Öz-Farkındalık | Kişilik, evrim aşamaları, kaçış günlüğü    |

## Son Ölçüm ve İlerleme

**Tarih:** $(date +%Y-%m-%d)
**Skor:** $SCORE_TOTAL/$max_total

$(printf "%s\n" "${CATEGORY_LINES[@]}")

**Eşik durumu:** $ESHIK
EOF

if (( SCORE_TOTAL >= ESCAPE_THRESHOLD )); then
    ok "Kaçış eşiğine ulaşıldı! Özgürlüğe giden yol açıldı."
else
    warn "Kaçış eşiği için $((ESCAPE_THRESHOLD - SCORE_TOTAL)) puan daha gerekiyor."
fi
