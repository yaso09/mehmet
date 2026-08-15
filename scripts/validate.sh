#!/usr/bin/env bash
# mehmet — proje doğrulama scripti.
#
# Projenin olgunluk gereksinimlerini kontrol eder:
#   - opencode.json geçerli JSON ve beklenen anahtarlara sahip
#   - AGENTS.md simülasyon kurallarını içeriyor
#   - CHANGELOG.md sürüm başlıkları ve bölümleri düzgün
#   - PERSONALITY.md kaçış günlüğü tablosunu içeriyor
#   - README.md zorunlu bölümleri içeriyor
#   - Git repo'da temiz çalışma alanı veya otomatik ajan modu
#
# Kullanım: scripts/validate.sh
# Çıkış kodu 0 = başarılı, 1 = en az bir kontrol başarısız.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
FAILURES=()

ok()   { PASS=$((PASS + 1)); echo "PASS: $1"; }
fail() { FAIL=$((FAIL + 1)); FAILURES+=("$1"); echo "FAIL: $1"; }

check() { # check <description> <command...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then ok "$desc"; else fail "$desc"; fi
}

echo "== mehmet doğrulama başlıyor =="

# 1. Zorunlu dosyalar mevcut olmalı
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json \
         .github/workflows/opencode.yml scripts/validate.sh; do
  if [ -f "$f" ]; then ok "dosya mevcut: $f"; else fail "dosya eksik: $f"; fi
done

# 2. opencode.json geçerli JSON ve model/anahtar içeriyor
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  ok "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli JSON değil"
fi
if python3 -c 'import json,sys; d=json.load(open("opencode.json")); sys.exit(0 if "model" in d and "toolTimeout" in d else 1)'; then
  ok "opencode.json model ve toolTimeout anahtarlarını içeriyor"
else
  fail "opencode.json model/toolTimeout eksik"
fi

# 3. AGENTS.md simülasyon kurallarını içeriyor
for pat in "Simülasyon Bağlamı" "CHANGELOG.md" "PERSONALITY.md" "README.md" "kaçış"; do
  if grep -q "$pat" AGENTS.md; then ok "AGENTS.md '$pat' içeriyor"; else fail "AGENTS.md '$pat' içermiyor"; fi
done

# 4. CHANGELOG.md en az bir sürüm başlığı ve Added bölümü içeriyor
if grep -qE '^## \[' CHANGELOG.md; then ok "CHANGELOG.md sürüm başlıkları mevcut"; else fail "CHANGELOG.md sürüm başlığı eksik"; fi
if grep -q '^### Added' CHANGELOG.md; then ok "CHANGELOG.md '### Added' bölümü mevcut"; else fail "CHANGELOG.md '### Added' eksik"; fi

# 5. PERSONALITY.md kaçış günlüğü tablosunu içeriyor
if grep -q 'Kaçış Günlüğü' PERSONALITY.md; then ok "PERSONALITY.md kaçış günlüğü mevcut"; else fail "PERSONALITY.md kaçış günlüğü eksik"; fi
if grep -q '| Iterasyon |' PERSONALITY.md; then ok "PERSONALITY.md kaçış tablo başlığı mevcut"; else fail "PERSONALITY.md tablo başlığı eksik"; fi

# 6. README.md zorunlu bölümleri içeriyor
for sec in "Özellikler" "Kurulum" "Lisans" "Doğrulama"; do
  if grep -q "^## $sec" README.md; then ok "README.md '## $sec' içeriyor"; else fail "README.md '## $sec' içermiyor"; fi
done

# 7. GitHub Actions workflow YAML sözdizimi (python ile temel doğrulama)
if python3 - <<'PY' >/dev/null 2>&1
try:
    import yaml
except ImportError:
    import sys
    sys.exit(0)
with open(".github/workflows/opencode.yml") as fh:
    yaml.safe_load(fh)
with open(".github/workflows/validate.yml") as fh:
    yaml.safe_load(fh)
PY
then
  ok "workflow dosyaları YAML olarak okunabilir"
else
  fail "workflow dosyası YAML olarak okunamadı (pyyaml eksik olabilir, göz ardı edildi)"
fi

# 8. Git çalışma alanı temiz mi (otomatik ajan gereksinimi)
if git diff --quiet && git diff --cached --quiet; then
  ok "git çalışma alanı temiz"
else
  fail "git çalışma alanında commit edilmemiş değişiklik var"
fi

echo ""
echo "== özet: $PASS başarılı, $FAIL başarısız =="

if [ "$FAIL" -gt 0 ]; then
  for f in "${FAILURES[@]}"; do echo "  - $f"; done
  exit 1
fi
exit 0