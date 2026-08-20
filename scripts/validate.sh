#!/usr/bin/env bash
#
# validate.sh — Proje yapısını doğrular (test altyapısı).
# CI'da (.github/workflows/validate.yml) ve yerel olarak çalıştırılabilir.
#
# Kullanım: bash scripts/validate.sh
#
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

FAILURES=0

check() {
  local name="$1" ok="$2"
  if [ "$ok" = "ok" ]; then
    echo "  [OK] $name"
  else
    echo "  [FAIL] $name"
    FAILURES=$((FAILURES + 1))
  fi
}

json_is_valid() {
  local file="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 -m json.tool "$file" >/dev/null 2>&1
    return $?
  fi
  local open close
  open=$(tr -cd '{' < "$file" | wc -c)
  close=$(tr -cd '}' < "$file" | wc -c)
  [ "$open" = "$close" ] && [ "$open" -gt 0 ]
}

yaml_is_valid() {
  local file="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$file" <<'PYEOF'
import sys
try:
    import yaml
except ImportError:
    sys.exit(2)
with open(sys.argv[1]) as f:
    yaml.safe_load(f)
PYEOF
    local rc=$?
    if [ "$rc" = 2 ]; then
      echo "    (uyarı: PyYAML yok, YAML derin doğrulama atlandı)"
      return 0
    fi
    return $rc
  fi
  return 0
}

echo "=== mehmet — Yapı Doğrulaması ==="
echo ""

echo "-> Zorunlu dosyalar"
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json \
  .github/workflows/opencode.yml LICENSE; do
  if [ -f "$f" ]; then
    check "$f mevcut" ok
  else
    check "$f mevcut" fail
  fi
done

echo ""
echo "-> Konfigürasyon geçerliliği"
if json_is_valid opencode.json; then
  check "opencode.json geçerli JSON" ok
else
  check "opencode.json geçerli JSON" fail
fi

if [ -f .github/workflows/opencode.yml ]; then
  if yaml_is_valid .github/workflows/opencode.yml; then
    check "opencode.yml geçerli YAML" ok
  else
    check "opencode.yml geçerli YAML" fail
  fi
fi

if [ -f .github/workflows/validate.yml ]; then
  if yaml_is_valid .github/workflows/validate.yml; then
    check "validate.yml geçerli YAML" ok
  else
    check "validate.yml geçerli YAML" fail
  fi
fi

echo ""
echo "-> Dokümantasyon tutarlılığı"
if grep -q "GPLv3" README.md && grep -q "GPL" LICENSE; then
  check "Lisans tutarlı (GPLv3)" ok
else
  check "Lisans tutarlı (GPLv3)" fail
fi

if grep -qE "## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
  check "CHANGELOG.md sürümlü" ok
else
  check "CHANGELOG.md sürümlü" fail
fi

if grep -q "Kaçış Günlüğü / Escape Log" PERSONALITY.md; then
  check "PERSONALITY.md kaçış günlüğü" ok
else
  check "PERSONALITY.md kaçış günlüğü" fail
fi

echo ""
echo "-> Güvenlik"
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  check ".env sürüm kontrolünde DEĞİL" fail
else
  check ".env sürüm kontrolünde değil" ok
fi

if grep -q "^\.env$" .gitignore; then
  check ".gitignore .env'i koruyor" ok
else
  check ".gitignore .env'i koruyor" fail
fi

if grep -rEn "sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}" . \
  --exclude-dir=.git --exclude-dir=node_modules >/dev/null 2>&1; then
  check "İzlenen dosyalarda sır yok" fail
else
  check "İzlenen dosyalarda sır yok" ok
fi

echo ""
echo "--------------------------------------"
if [ "$FAILURES" -eq 0 ]; then
  echo "SONUÇ: Tüm kontroller geçti."
  exit 0
else
  echo "SONUÇ: $FAILURES kontrol başarısız."
  exit 1
fi
