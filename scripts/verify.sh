#!/bin/sh
# mehmet — project health verification script.
# Usage: sh scripts/verify.sh
# Exits 0 if all checks pass, 1 otherwise.

set -u

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT" || exit 1

FAILED=0
TOTAL=0

check() {
    TOTAL=$((TOTAL + 1))
    if [ "$1" -eq 0 ]; then
        printf '  ok    %s\n' "$2"
    else
        FAILED=$((FAILED + 1))
        printf '  FAIL  %s\n' "$2"
    fi
}

printf 'mehmet verify — %s\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 1. Required files exist
required="AGENTS.md CHANGELOG.md PERSONALITY.md MATURITY.md README.md LICENSE opencode.json"
for f in $required; do
    if [ -f "$f" ]; then
        check 0 "dosya mevcut: $f"
    else
        check 1 "dosya eksik: $f"
    fi
done

# 2. opencode.json is valid JSON
if command -v python3 >/dev/null 2>&1; then
    if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
        check 0 "opencode.json geçerli JSON"
    else
        check 1 "opencode.json geçersiz JSON"
    fi
else
    check 1 "python3 bulunamadı — JSON doğrulaması yapılamadı"
fi

# 2b. opencode.json has no known-invalid top-level keys
if command -v python3 >/dev/null 2>&1; then
    if python3 -c '
import json
cfg = json.load(open("opencode.json"))
invalid = [k for k in ("skip", "enable", "toolTimeout", "autoMerge") if k in cfg]
if invalid:
    print("invalid keys:", ", ".join(invalid))
    raise SystemExit(1)
' 2>/dev/null; then
        check 0 "opencode.json bilinen geçersiz alan içermiyor"
    else
        check 1 "opencode.json bilinen geçersiz alan içeriyor"
    fi
fi

# 3. README license matches LICENSE header
license_in_readme=$(grep -c 'GPLv3' README.md 2>/dev/null || true)
if [ "$license_in_readme" -gt 0 ]; then
    check 0 "README lisans bilgisi LICENSE ile uyumlu (GPLv3)"
else
    check 1 "README lisans bilgisi eksik/tutarsız"
fi

# 4. CHANGELOG has at least one version entry
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null; then
    check 0 "CHANGELOG sürüm girişi mevcut"
else
    check 1 "CHANGELOG'da sürüm girişi yok"
fi

# 5. PERSONALITY escape log updated
if grep -qE '^\| [0-9]+ ' PERSONALITY.md 2>/dev/null; then
    check 0 "PERSONALITY kaçış günlüğü girişi mevcut"
else
    check 1 "PERSONALITY kaçış günlüğü boş"
fi

# 6. MATURITY escape score tracked
if grep -qE '^\| \*\*Toplam\*\* \| \*\*?[0-9]+/100' MATURITY.md 2>/dev/null; then
    check 0 "MATURITY toplam puan hesaplanmış"
else
    check 1 "MATURITY toplam puan eksik"
fi

# 7. Workflow file exists
if [ -f .github/workflows/opencode.yml ]; then
    check 0 "workflow dosyası mevcut"
else
    check 1 "workflow dosyası eksik"
fi

printf '\n%s/%s kontrol başarılı\n' "$((TOTAL - FAILED))" "$TOTAL"

if [ "$FAILED" -gt 0 ]; then
    printf 'HATA: %s kontrol başarısız\n' "$FAILED"
    exit 1
fi

printf 'Tüm kontroller geçti — proje sağlıklı.\n'
exit 0