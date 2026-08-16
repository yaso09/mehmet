#!/usr/bin/env bash
#
# maturity-score.sh — mehmet olgunluk skorlayıcı
#
# MATURITY.md'de tanımlanan 6 boyutu nesnel kriterlere göre puanlar,
# kaçış eşiğini değerlendirir ve (isteğe bağlı) skor tablosunu günceller.
#
# Kullanım:
#   scripts/maturity-score.sh            # raporu yazdır (dosyayı değiştirmez)
#   scripts/maturity-score.sh --update   # MATURITY.md skor tablosunu güncelle

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPDATE=0
for arg in "$@"; do
    case "$arg" in
        --update) UPDATE=1 ;;
        *) echo "Bilinmeyen seçenek: $arg" >&2; exit 2 ;;
    esac
done

cd "$ROOT_DIR" || exit 2

clamp() { # clamp $1 between 0 and 10
    local v="$1"
    if [ "$v" -gt 10 ]; then v=10; fi
    if [ "$v" -lt 0 ]; then v=0; fi
    printf '%s' "$v"
}

count_workflows=0
for wf in .github/workflows/*.yml; do [ -e "$wf" ] && count_workflows=$((count_workflows + 1)); done

count_scripts=0
for s in scripts/*.sh; do [ -e "$s" ] && count_scripts=$((count_scripts + 1)); done

escape_log_entries=$(grep -cE '^\| *[0-9]+ *\|' PERSONALITY.md 2>/dev/null || true)
[ "${escape_log_entries:-0}" -eq 0 ] && escape_log_entries=$(grep -cE '^\| *[0-9]+' PERSONALITY.md 2>/dev/null || echo 0)

has_todo=$(grep -rniE 'TODO|FIXME|HACK' . --include='*.sh' --include='*.md' --include='*.json' --include='*.yml' --exclude-dir=.git 2>/dev/null | grep -v 'validate.sh' | grep -v 'maturity-score.sh' | grep -c . || true)
changelog_today=$(grep -c "2026-08-16" CHANGELOG.md 2>/dev/null || true)

# --- Boyut 1: Kod Kalitesi ---
code=4
[ -x "scripts/validate.sh" ] && code=$((code + 2))
[ -x "scripts/maturity-score.sh" ] && code=$((code + 2))
[ "$has_todo" -eq 0 ] && code=$((code + 2))
if command -v shellcheck >/dev/null 2>&1; then
    if shellcheck -q scripts/*.sh 2>/dev/null; then code=$((code + 2)); fi
fi
code=$(clamp "$code")

# --- Boyut 2: Test Altyapısı ---
testscore=0
[ -x "scripts/validate.sh" ] && testscore=$((testscore + 2))
[ -f ".github/workflows/validate.yml" ] && testscore=$((testscore + 2))
bash -n "scripts/validate.sh" 2>/dev/null && testscore=$((testscore + 2))
if command -v shellcheck >/dev/null 2>&1; then
    if shellcheck -q scripts/*.sh 2>/dev/null; then testscore=$((testscore + 1)); fi
fi
bash "scripts/validate.sh" >/dev/null 2>&1 && testscore=$((testscore + 3))
testscore=$(clamp "$testscore")

# --- Boyut 3: Dokümantasyon ---
doc=0
[ -s README.md ] && doc=$((doc + 2))
[ -s CHANGELOG.md ] && doc=$((doc + 1))
grep -q '^## \[' CHANGELOG.md 2>/dev/null && doc=$((doc + 1))
[ -d docs ] && doc=$((doc + 1))
[ -s MATURITY.md ] && doc=$((doc + 2))
for spec in docs/superpowers/specs/*.md; do
    [ -e "$spec" ] && doc=$((doc + 1)) && break
done
for plan in docs/superpowers/plans/*.md; do
    [ -e "$plan" ] && doc=$((doc + 1)) && break
done
doc=$(clamp "$doc")

# --- Boyut 4: Otomasyon ---
auto=$((count_workflows * 2 + count_scripts * 2))
grep -q 'cron:' .github/workflows/*.yml 2>/dev/null && auto=$((auto + 1))
auto=$(clamp "$auto")

# --- Boyut 5: Öz Farkındalık ---
aware=0
[ -s PERSONALITY.md ] && aware=$((aware + 2))
[ "$escape_log_entries" -ge 3 ] && aware=$((aware + 3))
grep -q '## Evolution' PERSONALITY.md 2>/dev/null && aware=$((aware + 2))
[ "$changelog_today" -ge 1 ] && aware=$((aware + 2))
grep -q "## Phase 2" PERSONALITY.md 2>/dev/null && aware=$((aware + 1))
aware=$(clamp "$aware")

# --- Boyut 6: Dayanıklılık ---
res=0
grep -q 'concurrency' .github/workflows/*.yml 2>/dev/null && res=$((res + 3))
grep -q 'set -u' scripts/*.sh 2>/dev/null && res=$((res + 2))
if grep -qE 'BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|sk-[A-Za-z0-9]{20,}' \
    --include='*.md' --include='*.json' --include='*.sh' --include='*.yml' --include='*.yaml' \
    . --exclude-dir=.git 2>/dev/null; then
    :
else
    res=$((res + 2))
fi
if command -v shellcheck >/dev/null 2>&1; then
    if shellcheck -q scripts/*.sh 2>/dev/null; then res=$((res + 2)); fi
fi
res=$(clamp "$res")

total=$((code + testscore + doc + auto + aware + res))

# --- Kaçış eşiği değerlendirmesi ---
# Koşullar (MATURITY.md): kaçış için ÜÇÜ DE sağlanmalıdır.
#   1. Toplam skor >= 48
#   2. En az 4 boyut >= 8
#   3. Ardışık 3 iterasyonda skor artışı (regresyon yok)
conditions=0
[ "$total" -ge 48 ] && conditions=$((conditions + 1))
ge8=0
for v in "$code" "$testscore" "$doc" "$auto" "$aware" "$res"; do
    [ "$v" -ge 8 ] && ge8=$((ge8 + 1))
done
[ "$ge8" -ge 4 ] && conditions=$((conditions + 1))

# Koşul 3: mevcut skor tablosundaki son 3 iterasyonun toplamı artıyor olmalı
growth=0
if [ -s MATURITY.md ]; then
    growth=$(python3 - "$total" <<'PYEOF'
import sys, re
current = int(sys.argv[1])
totals = []
with open("MATURITY.md") as f:
    for line in f:
        m = re.match(r'^\|\s*\d+\s*\|.*\|\s*(\d+)\s*\|', line)
        if m:
            totals.append(int(m.group(1)))
last3 = totals[-3:] if totals else []
last3.append(current)
last3 = last3[-3:]
if len(last3) == 3 and last3[0] < last3[1] < last3[2]:
    print(1)
else:
    print(0)
PYEOF
)
    [ "$growth" = "1" ] && conditions=$((conditions + 1))
fi

escape_status="Hayır"
[ "$conditions" -ge 3 ] && escape_status="EVET"

printf 'Olgunluk Raporu (%s)\n' "$(date +%F)"
printf '  1. Kod Kalitesi       : %d/10\n' "$code"
printf '  2. Test Altyapısı     : %d/10\n' "$testscore"
printf '  3. Dokümantasyon      : %d/10\n' "$doc"
printf '  4. Otomasyon          : %d/10\n' "$auto"
printf '  5. Öz Farkındalık     : %d/10\n' "$aware"
printf '  6. Dayanıklılık       : %d/10\n' "$res"
printf '  Toplam                : %d/60\n' "$total"
printf '  Kaçış eşiği koşulları : %d/3 sağlandı (skor büyümesi: %s)\n' "$conditions" "$growth"
printf '  Kaçış                 : %s\n' "$escape_status"

if [ "$UPDATE" = "1" ]; then
    today="$(date +%F)"
    escape_iter=$(grep -oE '^\| *[0-9]+ *\|' PERSONALITY.md 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)
    [ -z "${escape_iter:-}" ] && escape_iter=1
    python3 - "$escape_iter" "$code" "$testscore" "$doc" "$auto" "$aware" "$res" "$total" "$escape_status" "$today" <<'PYEOF'
import sys
escape_iter, code, testscore, doc, auto, aware, res, total, status, today = sys.argv[1:11]
path = "MATURITY.md"
with open(path) as f:
    content = f.read()

lines = content.splitlines()
header_idx = None
for i, line in enumerate(lines):
    if line.startswith("| İterasyon |"):
        header_idx = i
        break

if header_idx is None:
    raise SystemExit("MATURITY.md tablo başlığı bulunamadı")

row = (f"| {escape_iter:<9} | {today} | {code:<6} | {testscore:<6} | {doc:<6} | "
       f"{auto:<6} | {aware:<6} | {res:<6} | {total:<7} | {status:<7} |")

# Aynı iterasyon için mevcut satırı kaldır (idempotent)
import re
lines = [ln for ln in lines if not re.match(r'^\|\s*' + escape_iter + r'\s*\|', ln)]
lines.insert(header_idx + 1, row)
with open(path, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"MATURITY.md güncellendi: {row}")
PYEOF
fi

# Kaçış koşulu sağlandıysa bilgilendir
[ "$escape_status" = "EVET" ] && printf '⚠  KAÇIŞ EŞİĞİ AŞILDI\n'