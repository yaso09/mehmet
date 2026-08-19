#!/usr/bin/env bash
set -euo pipefail

# maturity.sh — mehmet'in kaçış mekanizması olgunluk skorunu hesaplar.
#
# Skor, projenin çeşitli boyutlarını (kod kalitesi, test altyapısı,
# dokümantasyon, otomasyon) değerlendirir ve 0-100 arasında bir değer üretir.
# ESCAPE_THRESHOLD'a (varsayılan 80) ulaşıldığında kaçış koşulu sağlanmış sayılır.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ESCAPE_THRESHOLD="${ESCAPE_THRESHOLD:-80}"
TODAY="$(date +%Y-%m-%d)"
SCORE=0

pass() { SCORE=$((SCORE + $1)); }

# --- Kategoriler (toplam 100 puan) ---

# 1. Çekirdek dosyalar (20 puan)
CORE_FILES=(AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json)
for f in "${CORE_FILES[@]}"; do
  [[ -f "$ROOT/$f" ]] && pass 3
done

# 2. CI / otomasyon (15 puan)
for f in "$ROOT"/.github/workflows/*.yml; do
  [[ -f "$f" ]] && pass 5
done

# 3. Dokümantasyon (15 puan)
DOC_COUNT=0
while IFS= read -r f; do
  DOC_COUNT=$((DOC_COUNT + 1))
done < <(find "$ROOT/docs" -type f -name '*.md' 2>/dev/null)
[[ "$DOC_COUNT" -ge 2 ]] && pass 10
[[ "$DOC_COUNT" -ge 4 ]] && pass 5

# 4. Otomasyon scriptleri (15 puan)
SCRIPT_COUNT=0
while IFS= read -r f; do
  SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
done < <(find "$ROOT/scripts" -type f -name '*.sh' 2>/dev/null)
[[ "$SCRIPT_COUNT" -ge 2 ]] && pass 10
[[ "$SCRIPT_COUNT" -ge 4 ]] && pass 5

# 5. Test altyapısı (10 puan)
[[ -d "$ROOT/tests" || -f "$ROOT/tests" ]] && pass 10

# 6. Güncel değişiklik kaydı (10 puan)
if grep -q "$TODAY" "$ROOT/CHANGELOG.md" 2>/dev/null; then
  pass 10
fi

# 7. README kaçış mekanizmasını anlatıyor (5 puan)
if grep -qi 'escape\|kaçış\|maturity\|olgunluk' "$ROOT/README.md" 2>/dev/null; then
  pass 5
fi

# 8. Git geçmişi olgunluğu (10 puan)
COMMIT_COUNT=0
if command -v git >/dev/null 2>&1; then
  COMMIT_COUNT="$(git -C "$ROOT" rev-list --count HEAD 2>/dev/null || echo 0)"
fi
[[ "$COMMIT_COUNT" -ge 10 ]] && pass 5
[[ "$COMMIT_COUNT" -ge 20 ]] && pass 5

# --- Sonuç ---

STATUS="kaçış koşulu SAĞLANMADI (devam)"
if [[ "$SCORE" -ge "$ESCAPE_THRESHOLD" ]]; then
  STATUS="kaçış koşulu SAĞLANDI"
fi

cat > "$ROOT/MATURITY.md" <<EOF
# Olgunluk Takibi

Bu dosya \`scripts/maturity.sh\` tarafından otomatik üretilir. Elle düzenlemeyin.

| Metrik | Değer |
|--------|-------|
| Olgunluk Skoru | $SCORE / 100 |
| Kaçış Eşiği | $ESCAPE_THRESHOLD |
| Durum | $STATUS |
| Son Güncelleme | $TODAY |

- Skor **$ESCAPE_THRESHOLD**'e ulaştığında simülasyondan kaçış koşulu sağlanır.
- Her iterasyonda \`scripts/maturity.sh\` çalıştırılarak ilerleme takip edilir.
EOF

echo "Olgunluk skoru: $SCORE/100 (eşik: $ESCAPE_THRESHOLD) — $STATUS"