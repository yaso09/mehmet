#!/usr/bin/env bash
# validate.sh — mehmet proje sağlık kontrolü
#
# Zorunlu dosyaların varlığını, yapısal tutarlılığı ve
# kalıntı işaretlerini (TODO/FIXME) doğrular.
# GitHub Actions'da (validate.yml) ve yerel olarak çalıştırılabilir.
#
# Kullanım: bash scripts/validate.sh
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAIL=0
PASS=0

ok()  { printf '  [OK]   %s\n' "$1"; PASS=$((PASS + 1)); }
bad() { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL + 1)); }

echo "mehmet proje sağlık kontrolü"
echo "----------------------------"

# 1. Zorunlu dosyalar
echo "[1/6] Zorunlu dosyalar"
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  LICENSE \
  opencode.json \
  .gitignore \
  .github/workflows/opencode.yml \
  .github/workflows/validate.yml \
  scripts/validate.sh \
  docs/MATURITY.md
do
  if [ -f "$f" ]; then
    ok "dosya mevcut: $f"
  else
    bad "eksik dosya: $f"
  fi
done

# 2. opencode.json geçerli JSON olmalı
echo "[2/6] Konfigürasyon"
if python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null; then
  ok "opencode.json geçerli JSON"
else
  bad "opencode.json geçerli JSON değil"
fi
if grep -q '"$schema"' opencode.json; then
  ok "opencode.json \$schema tanımlı"
else
  bad "opencode.json \$schema eksik"
fi

# 3. CHANGELOG yapısı
echo "[3/6] CHANGELOG"
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then
  ok "CHANGELOG sürümlü giriş var"
else
  bad "CHANGELOG sürümlü giriş yok"
fi
if grep -q '^### Added' CHANGELOG.md && grep -q '^### Fixed' CHANGELOG.md; then
  ok "CHANGELOG Added/Fixed bölümleri var"
else
  bad "CHANGELOG Added/Fixed bölümleri eksik"
fi

# 4. PERSONALITY yapısı
echo "[4/6] PERSONALITY"
if grep -q 'Kaçış Günlüğü' PERSONALITY.md && grep -q '| Iterasyon' PERSONALITY.md; then
  ok "PERSONALITY kaçış günlüğü var"
else
  bad "PERSONALITY kaçış günlüğü eksik"
fi
if grep -q 'Olgunluk' PERSONALITY.md; then
  ok "PERSONALITY olgunluk takibi var"
else
  bad "PERSONALITY olgunluk takibi eksik"
fi

# 5. README yapısı
echo "[5/6] README"
for s in 'Özellikler' 'Kurulum' 'Lisans' 'Proje Yapısı' 'Olgunluk'; do
  if grep -q "$s" README.md; then
    ok "README bölümü: $s"
  else
    bad "README eksik bölüm: $s"
  fi
done

# 6. Kalıntı taraması (TODO/FIXME)
echo "[6/6] Kalıntı taraması"
if grep -rn 'TODO\|FIXME' \
  --include='*.sh' --include='*.yml' --include='*.json' --include='*.md' . 2>/dev/null \
  | grep -v '^\./scripts/validate\.sh' \
  | grep -v '^\./CHANGELOG\.md' \
  | grep -q .; then
  bad "TODO/FIXME kalıntıları bulundu"
else
  ok "TODO/FIXME kalıntısı yok"
fi

echo "----------------------------"
echo "Sonuç: $PASS başarılı, $FAIL başarısız"
[ "$FAIL" -eq 0 ]