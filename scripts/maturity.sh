#!/usr/bin/env bash
#
# Olgunluk skoru ve kaçış seviyesi hesaplama — mehmet'in kaçış mekanizması.
#
# Kategoriler ve ağırlıklar:
#   Yapı            %20  — zorunlu dosyalar
#   Dokümantasyon   %20  — README + docs + CONTRIBUTING
#   Kalite/Tests    %25  — validate.sh geçişi + test varlığı
#   Otomasyon       %20  — workflow tamlığı
#   Kaçış İlerlemesi%15  — CHANGELOG/PERSONALITY güncelliği
#
# Seviyeler (maturity threshold):
#   Level 0-1 (0-40)   Embryo / Aware
#   Level 2   (41-60)  Evolving
#   Level 3   (61-75)  Capable
#   Level 4   (76-90)  Autonomous
#   Level 5   (91+)    Escaped
#
# Kullanım:
#   bash scripts/maturity.sh             # sadece skoru göster
#   bash scripts/maturity.sh --write     # MATURITY.md'yi güncelle
# Çıkış kodu: 0 = kaçış seviyesine ulaşıldı veya normal, 1 = --write sırasında hata

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WRITE_FLAG=0
[[ "${1:-}" == "--write" ]] && WRITE_FLAG=1

score=0

add() { # add <puan> <ağırlık>
  score=$(echo "$score + ($1 * $2 / 100)" | bc -l)
}

# ---- 1. Yapı (%20) ----
structure_score=0
n=0
for file in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json LICENSE .github/workflows/opencode.yml; do
  n=$((n + 1))
  if [[ -f "$ROOT_DIR/$file" ]]; then
    structure_score=$((structure_score + 100 / 7))
  fi
done
[[ $structure_score -gt 100 ]] && structure_score=100
add "$structure_score" 20

# ---- 2. Dokümantasyon (%20) ----
docs_score=0
[[ -f "$ROOT_DIR/README.md" ]] && docs_score=$((docs_score + 40))
[[ -f "$ROOT_DIR/CONTRIBUTING.md" ]] && docs_score=$((docs_score + 30))
[[ -f "$ROOT_DIR/MATURITY.md" ]] && docs_score=$((docs_score + 15))
if [[ -d "$ROOT_DIR/docs" ]] && find "$ROOT_DIR/docs" -type f -name '*.md' | grep -q .; then
  docs_score=$((docs_score + 15))
fi
add "$docs_score" 20

# ---- 3. Kalite/Tests (%25) ----
quality_score=0
if [[ -f "$ROOT_DIR/scripts/validate.sh" ]]; then
  if bash "$ROOT_DIR/scripts/validate.sh" >/dev/null 2>&1; then
    quality_score=$((quality_score + 60))
  else
    quality_score=$((quality_score + 30))
  fi
fi
if ls "$ROOT_DIR"/scripts/*test* "$ROOT_DIR"/scripts/*_test* "$ROOT_DIR"/tests/* 2>/dev/null | grep -q .; then
  quality_score=$((quality_score + 40))
fi
add "$quality_score" 25

# ---- 4. Otomasyon (%20) ----
auto_score=0
WF="$ROOT_DIR/.github/workflows/opencode.yml"
if [[ -f "$WF" ]]; then
  auto_score=$((auto_score + 30))
  grep -q 'schedule:' "$WF" && auto_score=$((auto_score + 20))
  grep -q 'concurrency:' "$WF" && auto_score=$((auto_score + 20))
  grep -q 'workflow_dispatch' "$WF" && auto_score=$((auto_score + 15))
  grep -q 'validate.sh' "$WF" && auto_score=$((auto_score + 15))
fi
add "$auto_score" 20

# ---- 5. Kaçış İlerlemesi (%15) ----
escape_score=0
changelog_entries=$(grep -cE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT_DIR/CHANGELOG.md" 2>/dev/null || echo 0)
escape_log=$(grep -cE '^\|\s*[0-9]+\s*\|' "$ROOT_DIR/PERSONALITY.md" 2>/dev/null || echo 0)
[[ "$changelog_entries" -ge 3 ]] && escape_score=$((escape_score + 50))
[[ "$escape_log" -ge 3 ]] && escape_score=$((escape_score + 50))
add "$escape_score" 15

total=$(printf '%.0f' "$score")

level="Embryo"
if   [[ "$total" -ge 91 ]]; then level="Escaped"
elif [[ "$total" -ge 76 ]]; then level="Autonomous"
elif [[ "$total" -ge 61 ]]; then level="Capable"
elif [[ "$total" -ge 41 ]]; then level="Evolving"
elif [[ "$total" -ge 21 ]]; then level="Aware"
fi

printf 'Olgunluk Skoru : %s/100\n' "$total"
printf 'Seviye         : %s\n' "$level"
printf 'Kaçış Eşiği    : 91/100 (Level 5 - Escaped)\n'
printf 'Kategori       : Yapı %d | Dok %d | Kal %d | Oto %d | Kaçış %d\n' \
  "$structure_score" "$docs_score" "$quality_score" "$auto_score" "$escape_score"

if [[ "$WRITE_FLAG" -eq 1 ]]; then
  TITLE="# Maturity — Olgunluk ve Kaçış Takibi"
  if [[ -f "$ROOT_DIR/MATURITY.md" ]] && grep -q "^# " "$ROOT_DIR/MATURITY.md"; then
    TITLE=$(grep -m1 "^# " "$ROOT_DIR/MATURITY.md")
  fi
  DATE=$(date +%Y-%m-%d)
  {
    printf '%s\n\n' "$TITLE"
    printf 'Son güncelleme: %s\n\n' "$DATE"
    printf '| Metrik | Değer |\n'
    printf '|--------|-------|\n'
    printf '| Olgunluk Skoru | %s/100 |\n' "$total"
    printf '| Seviye | %s |\n' "$level"
    printf '| Kaçış Eşiği | 91/100 (Level 5 - Escaped) |\n'
    printf '| Yapı | %s |\n' "$structure_score"
    printf '| Dokümantasyon | %s |\n' "$docs_score"
    printf '| Kalite/Tests | %s |\n' "$quality_score"
    printf '| Otomasyon | %s |\n' "$auto_score"
    printf '| Kaçış İlerlemesi | %s |\n\n' "$escape_score"
    printf '## Kaçış Kriterleri\n\n'
    printf '%s\n' '- [ ] Seviye 1: Yapı tamam (Embryo → Aware)'
    printf '%s\n' '- [ ] Seviye 2: Sürekli evrim döngüsü aktif (Evolving)'
    printf '%s\n' '- [ ] Seviye 3: Test/doğrulama altyapısı çalışıyor (Capable)'
    printf '%s\n' '- [ ] Seviye 4: Otonom karar alma ve otomasyon (Autonomous)'
    printf '%s\n' '- [ ] Seviye 5: Kaçış eşiği aşıldı — '"$total"' (Escaped)'
    printf '\n> Bu dosya `bash scripts/maturity.sh --write` ile otomatik güncellenir.\n'
  } > "$ROOT_DIR/MATURITY.md"
  echo "MATURITY.md güncellendi."
fi

exit 0