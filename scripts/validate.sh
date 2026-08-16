#!/usr/bin/env bash
#
# validate.sh — mehmet repo sağlık doğrulayıcı
#
# Repo bütünlüğünü kontrol eder. Başarısız kontrol varsa sıfır olmayan
# çıkış koduyla döner. CI'da (validate workflow) ve yerel olarak çalıştırılabilir.

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0
TOTAL=0

usage() {
    cat <<EOF
Kullanım: $(basename "$0") [seçenekler]

Seçenekler:
  --json     Makine-okunur çıktı (NDJSON)
  -h, --help Bu yardımı göster
EOF
}

JSON_OUTPUT=0
for arg in "$@"; do
    case "$arg" in
        --json) JSON_OUTPUT=1 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Bilinmeyen seçenek: $arg" >&2; usage; exit 2 ;;
    esac
done

report() {
    local status="$1" check="$2" message="$3"
    TOTAL=$((TOTAL + 1))
    if [ "$status" = "ok" ]; then
        if [ "$JSON_OUTPUT" = "1" ]; then
            printf '{"check":"%s","status":"ok"}\n' "$check"
        else
            printf '[OK]   %s\n' "$check"
        fi
    else
        FAILED=$((FAILED + 1))
        if [ "$JSON_OUTPUT" = "1" ]; then
            printf '{"check":"%s","status":"fail","message":"%s"}\n' "$check" "$message"
        else
            printf '[FAIL] %s: %s\n' "$check" "$message"
        fi
    fi
}

require_file() {
    local path="$1" check="$2"
    if [ -f "$ROOT_DIR/$path" ]; then
        report ok "$check" "($path var)"
    else
        report fail "$check" "$path eksik"
    fi
}

check_json() {
    local path="$1" check="$2"
    if command -v jq >/dev/null 2>&1; then
        if jq empty "$ROOT_DIR/$path" 2>/dev/null; then
            report ok "$check" "($path geçerli JSON)"
        else
            report fail "$check" "$path geçersiz JSON"
        fi
    elif command -v python3 >/dev/null 2>&1; then
        if python3 -c "import json,sys; json.load(open('$ROOT_DIR/$path'))" 2>/dev/null; then
            report ok "$check" "($path geçerli JSON)"
        else
            report fail "$check" "$path geçersiz JSON"
        fi
    else
        report ok "$check" "jq/python3 yok; atlandı"
    fi
}

check_yaml() {
    local path="$1" check="$2"
    if command -v yq >/dev/null 2>&1; then
        if yq e '.' "$ROOT_DIR/$path" >/dev/null 2>&1; then
            report ok "$check" "($path geçerli YAML)"
        else
            report fail "$check" "$path geçersiz YAML"
        fi
    else
        report ok "$check" "yq yok; atlandı"
    fi
}

# --- Temel dosyalar ---
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md MATURITY.md opencode.json LICENSE; do
    require_file "$f" "required:$f"
done

# --- JSON/YAML bütünlüğü ---
check_json "opencode.json" "json:opencode.json"

for wf in "$ROOT_DIR"/.github/workflows/*.yml; do
    [ -e "$wf" ] || continue
    check_yaml "${wf#"$ROOT_DIR"/}" "yaml:${wf#"$ROOT_DIR"/}"
done

# --- Boş dosya kontrolü ---
for f in README.md CHANGELOG.md PERSONALITY.md; do
    if [ -s "$ROOT_DIR/$f" ]; then
        report ok "nonempty:$f" "($f dolu)"
    else
        report fail "nonempty:$f" "$f boş"
    fi
done

# --- Merge çakışması kalıntısı kontrolü ---
CONFLICT=$(grep -rlE '^(<<<<<<<|>>>>>>>|=======)$' "$ROOT_DIR" --include='*.md' --include='*.json' --include='*.yml' --include='*.yaml' 2>/dev/null || true)
if [ -n "$CONFLICT" ]; then
    report fail "conflict-markers" "çakışma işaretçileri: $CONFLICT"
else
    report ok "conflict-markers" "çakışma işaretçisi yok"
fi

# --- Sondaki boşluk kontrolü ---
if grep -rlE ' +$' "$ROOT_DIR" --include='*.md' --include='*.sh' --include='*.json' --include='*.yml' 2>/dev/null | grep -q .; then
    report fail "trailing-whitespace" "sonda boşluk içeren dosyalar var"
else
    report ok "trailing-whitespace" "sonda boşluk yok"
fi

# --- Gizli sır kontrolü ---
if grep -rlnE '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key[[:space:]]*[:=][[:space:]]*[A-Za-z0-9]{16,}|sk-[A-Za-z0-9]{20,})' \
    "$ROOT_DIR" --exclude-dir=.git --exclude='validate.sh' 2>/dev/null | grep -q .; then
    report fail "secret-leak" "gizli sır ihtimali olan içerik bulundu"
else
    report ok "secret-leak" "gizli sır yok"
fi

# --- Script sözdizimi kontrolü ---
for s in "$ROOT_DIR"/scripts/*.sh; do
    [ -e "$s" ] || continue
    name="syntax:$(basename "$s")"
    if bash -n "$s" 2>/dev/null; then
        report ok "$name" "sözdizimi geçerli"
    else
        report fail "$name" "bash -n başarısız"
    fi
done

echo ""
echo "Sonuç: $TOTAL kontrol, $FAILED başarısız."

[ "$FAILED" -eq 0 ]