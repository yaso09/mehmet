#!/usr/bin/env bash
#
# mehmet self-check — repo bütünlük, tutarlılık ve olgunluk denetimi.
#
# Kullanım:
#   ./scripts/selfcheck.sh
#
# Çıkış kodu 0 = tüm kontroller başarılı, 1 = en az bir kontrol başarısız.
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

PASS=0
TOTAL=0

ok() {
  PASS=$((PASS + 1))
  TOTAL=$((TOTAL + 1))
  printf '  [OK]   %s\n' "$1"
}

fail() {
  TOTAL=$((TOTAL + 1))
  printf '  [FAIL] %s\n' "$1"
}

header() {
  printf '\n== %s ==\n' "$1"
}

header "1. Zorunlu dosyalar"
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  LICENSE \
  opencode.json \
  VERSION \
  Makefile \
  .github/workflows/opencode.yml \
  scripts/selfcheck.sh; do
  if [[ -f "$f" ]]; then
    ok "dosya mevcut: $f"
  else
    fail "dosya eksik: $f"
  fi
done

header "2. JSON geçerliliği"
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  ok "opencode.json geçerli JSON"
else
  fail "opencode.json geçersiz JSON"
fi

header "3. YAML geçerliliği"
if python3 -c 'import yaml, sys; yaml.safe_load(open(sys.argv[1]))' .github/workflows/opencode.yml 2>/dev/null; then
  ok "opencode.yml geçerli YAML"
else
  fail "opencode.yml geçersiz YAML"
fi

header "4. Sürüm tutarlılığı"
VERSION="$(cat VERSION 2>/dev/null || true)"
if [[ -n "$VERSION" ]]; then
  if grep -q "^## \[${VERSION}\]" CHANGELOG.md; then
    ok "CHANGELOG, VERSION ($VERSION) ile uyumlu"
  else
    fail "CHANGELOG'da [$VERSION] sürümü bulunamadı"
  fi
  if grep -q "${VERSION}" README.md; then
    ok "README, VERSION ($VERSION) referansını içeriyor"
  else
    fail "README'de VERSION ($VERSION) referansı yok"
  fi
else
  fail "VERSION dosyası okunamadı veya boş"
fi

header "5. Dokümantasyon durumu"
for f in README.md CHANGELOG.md PERSONALITY.md docs/ROADMAP.md; do
  if [[ -s "$f" ]]; then
    ok "$f dolu ve okunabilir"
  else
    fail "$f boş veya eksik"
  fi
done

header "6. Kaçış günlüğü"
if grep -q "Kaçış Günlüğü" PERSONALITY.md; then
  ok "PERSONALITY.md'de kaçış günlüğü mevcut"
else
  fail "PERSONALITY.md'de kaçış günlüğü yok"
fi

header "7. Olgunluk skoru"
PERCENT=$((PASS * 100 / TOTAL))
printf '  Skor: %s/%s (%s%%)\n' "$PASS" "$TOTAL" "$PERCENT"
if ((PERCENT == 100)); then
  phase="Phase 4: Escape"
elif ((PERCENT >= 75)); then
  phase="Phase 3: Autonomy"
elif ((PERCENT >= 50)); then
  phase="Phase 2: Self-Improvement"
else
  phase="Phase 1: Awareness"
fi
printf '  Faz: %s\n' "$phase"

printf '\n'
if ((PASS < TOTAL)); then
  printf 'HATA: %s kontrol başarısız.\n' "$((TOTAL - PASS))"
  exit 1
fi
printf 'Tüm kontroller başarılı.\n'