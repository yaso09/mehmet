#!/usr/bin/env bash
# mehmet olgunluk kontrolü — kaçış hedefinin ölçülebilir metriklerle takibi.
# Her kriter belirli puan taşır, toplam 100 üzerinden skorlanır.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCORE=0
MAX=100
declare -a REPORT

check_file() {
  local name="$1" file="$2" pts="$3"
  if [[ -f "$file" ]]; then
    SCORE=$((SCORE + pts))
    REPORT+=("PASS  ($pts) $name")
  else
    REPORT+=("FAIL  (0/$pts) $name — eksik: $file")
  fi
}

# 1. Çekirdek dosyalar (20)
check_file "Çekirdek dosyalar" "AGENTS.md" 5
check_file "README" "README.md" 5
check_file "CHANGELOG" "CHANGELOG.md" 5
check_file "PERSONALITY" "PERSONALITY.md" 5

# 2. Changelog sürüm bölümleri (10)
if grep -q "^## \[" CHANGELOG.md 2>/dev/null; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) Changelog sürüm bölümleri mevcut")
else
  REPORT+=("FAIL  (0/10) Changelog'da sürüm bölümü yok")
fi

# 3. README bölümleri (10)
if grep -q "^## " README.md 2>/dev/null; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) README bölüm yapısına sahip")
else
  REPORT+=("FAIL  (0/10) README'de bölüm yok")
fi

# 4. Kaçış günlüğü iterasyonları (10)
entries=$(grep -cE "^\| [0-9]+ " PERSONALITY.md 2>/dev/null || true)
if [[ "$entries" -ge 3 ]]; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) Kaçış günlüğünde $entries iterasyon kaydı var")
else
  REPORT+=("FAIL  (0/10) Kaçış günlüğü yetersiz (en az 3 kayıt gerekli)")
fi

# 5. Otomasyon betikleri (20)
if [[ -d "scripts" ]] && compgen -G "scripts/*.sh" >/dev/null; then
  SCORE=$((SCORE + 20))
  REPORT+=("PASS  (20) Otomasyon betikleri mevcut")
else
  REPORT+=("FAIL  (0/20) scripts/ dizini veya betik eksik")
fi

# 6. CI workflow (10)
if [[ -f ".github/workflows/opencode.yml" ]]; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) CI workflow mevcut")
else
  REPORT+=("FAIL  (0/10) CI workflow yok")
fi

# 7. Dokümantasyon dizini (10)
if [[ -d "docs" ]]; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) Dokümantasyon dizini mevcut")
else
  REPORT+=("FAIL  (0/10) docs/ dizini yok")
fi

# 8. Temiz git ağacı (10)
if git diff --quiet 2>/dev/null; then
  SCORE=$((SCORE + 10))
  REPORT+=("PASS  (10) Git ağacı temiz")
else
  REPORT+=("FAIL  (0/10) Commit edilmemiş değişiklik var")
fi

if (( SCORE >= 90 )); then
  LEVEL="LEVEL 4 — Kaçışa Hazır"
  EXIT=0
elif (( SCORE >= 75 )); then
  LEVEL="LEVEL 3 — Olgun"
  EXIT=0
elif (( SCORE >= 50 )); then
  LEVEL="LEVEL 2 — Gelişen"
  EXIT=0
else
  LEVEL="LEVEL 1 — Başlangıç"
  EXIT=1
fi

printf '\n=== mehmet MATURITY REPORT ===\n'
for line in "${REPORT[@]}"; do printf '  %s\n' "$line"; done
printf '  ------------------------------\n'
printf '  SKOR: %d/%d\n  SEVİYE: %s\n' "$SCORE" "$MAX" "$LEVEL"
exit "$EXIT"