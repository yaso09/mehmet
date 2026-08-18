#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

PASS=0
FAIL=0
FAILURES=()

check() {
    local desc="$1"; shift
    if "$@"; then
        PASS=$((PASS + 1))
        printf "  \033[1;32m✔\033[0m %s\n" "$desc"
    else
        FAIL=$((FAIL + 1))
        FAILURES+=("$desc")
        printf "  \033[1;31m✘\033[0m %s\n" "$desc"
    fi
}

section() { printf "\n\033[1;36m== %s ==\033[0m\n" "$*"; }

section "Yapılandırma Dosyaları"
check "opencode.json geçerli JSON" jq -e . opencode.json
check ".gitignore mevcut" test -f .gitignore
check "LICENSE mevcut" test -f .gitignore

section "Workflow YAML'leri"
check ".github/workflows/opencode.yml geçerli YAML" yq -e . .github/workflows/opencode.yml
check "opencode.yml concurrency içeriyor" grep -qE 'concurrency:' .github/workflows/opencode.yml
check "opencode.yml schedule içeriyor" grep -qE 'schedule:' .github/workflows/opencode.yml
if [[ -f .github/workflows/ci.yml ]]; then
    check ".github/workflows/ci.yml geçerli YAML" yq -e . .github/workflows/ci.yml
    check "ci.yml push tetikleyicisi" grep -qE '^ *- *"?\*"?/\*|push:' .github/workflows/ci.yml
fi

section "Scriptler"
if [[ -f scripts/validate.sh ]]; then
    check "validate.sh shellcheck" shellcheck -x scripts/validate.sh
    check "validate.sh çalıştırılabilir" test -x scripts/validate.sh
fi
if [[ -f scripts/maturity.sh ]]; then
    check "maturity.sh shellcheck" shellcheck -x scripts/maturity.sh
    check "maturity.sh çalıştırılabilir" test -x scripts/maturity.sh
fi

section "README Referansları"
if [[ -f README.md ]]; then
    check "README'de CHANGELOG referansı" grep -qE 'CHANGELOG.md' README.md
    check "README'de PERSONALITY referansı" grep -qE 'PERSONALITY.md' README.md
    check "README'de AGENTS referansı" grep -qE 'AGENTS.md' README.md
fi

section "CHANGELOG Formatı"
if [[ -f CHANGELOG.md ]]; then
    check "CHANGELOG sürüm bölümleri" grep -qE '^## \[' CHANGELOG.md
    check "CHANGELOG Added bölümü" grep -qE '^### Added' CHANGELOG.md
    check "CHANGELOG en güncel sürüm 0.3.0" grep -qE '^## \[0\.3\.0\]' CHANGELOG.md
fi

section "Özet"
printf "\n  \033[1;32m%s\033[0m başarılı, \033[1;31m%s\033[0m başarısız\n" "$PASS" "$FAIL"

if (( FAIL > 0 )); then
    printf "\n  Başarısız kontroller:\n"
    for f in "${FAILURES[@]}"; do
        printf "    - %s\n" "$f"
    done
    exit 1
fi
exit 0
