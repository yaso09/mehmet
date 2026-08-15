#!/usr/bin/env bash
#
# run_tests.sh — mehmet projesinin yapısal bütünlüğünü doğrular.
#
# Kullanım: bash tests/run_tests.sh
# Çıkış:    tüm testler geçerse 0, aksi halde 1

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

pass=0
fail=0

check() {
  local desc="$1"
  local cond="$2"
  if eval "$cond"; then
    pass=$((pass + 1))
    echo "  PASS  $desc"
  else
    fail=$((fail + 1))
    echo "  FAIL  $desc"
  fi
}

echo "== mehmet test suite =="
echo ""

# --- Zorunlu dosyalar ---
check "AGENTS.md mevcut"            '[ -f AGENTS.md ]'
check "CHANGELOG.md mevcut"         '[ -f CHANGELOG.md ]'
check "PERSONALITY.md mevcut"       '[ -f PERSONALITY.md ]'
check "README.md mevcut"            '[ -f README.md ]'
check "LICENSE mevcut"              '[ -f LICENSE ]'
check "MATURITY.md mevcut"          '[ -f MATURITY.md ]'
check "opencode.json mevcut"        '[ -f opencode.json ]'
check "workflow mevcut"             '[ -f .github/workflows/opencode.yml ]'

# --- İçerik tutarlılığı ---
check "CHANGELOG başlık"            'head -1 CHANGELOG.md | grep -q "^# Changelog"'
check "CHANGELOG versiyon girdisi"  'grep -Eq "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md'
check "README lisans GPLv3"         'grep -q "GPLv3" README.md'
check "LICENSE GPLv3"               'grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE'
check "PERSONALITY kaçış günlüğü"   'grep -q "Kaçış Günlüğü" PERSONALITY.md'
check "AGENTS.md kaçış hedefi"      'grep -qi "kaçmak" AGENTS.md'
check "MATURITY skor tablosu"       'grep -Eq "^\| [0-9]{4}-[0-9]{2}-[0-9]{2} \|" MATURITY.md'

# --- opencode.json geçerli JSON ve geçerli anahtarlar ---
if command -v jq >/dev/null 2>&1; then
  check "opencode.json geçerli JSON"  'jq -e . opencode.json >/dev/null 2>&1'
  check "opencode.json geçerli schema" 'jq -e . opencode.json >/dev/null 2>&1 && python3 - <<'"'"'PY'"'"'
import json, os, urllib.request

schema_path = "/tmp/opencode/config.json"
if not os.path.exists(schema_path):
    try:
        urllib.request.urlretrieve("https://opencode.ai/config.json", schema_path)
    except Exception:
        print("SKIP: schema indirilemedi")
        raise SystemExit(0)

schema = json.load(open(schema_path))
valid = set(schema["$defs"]["Config"]["properties"].keys())
cfg = json.load(open("opencode.json"))
extra = set(cfg.keys()) - valid - {"$schema"}
if extra:
    print("Geçersiz anahtarlar:", extra)
raise SystemExit(1 if extra else 0)
PY'
else
  check "opencode.json geçerli JSON"  'python3 -c "import json; json.load(open('"'"'opencode.json'"'"'))"'
fi

# --- Betikler ---
check "scripts/maturity.sh mevcut"  '[ -f scripts/maturity.sh ]'
check "tests/run_tests.sh mevcut"   '[ -f tests/run_tests.sh ]'
check "Makefile mevcut"             '[ -f Makefile ]'

# --- Gizlilik taraması: takip edilen dosyalarda belirgin secret yok ---
check "belirgin secret yok" '! grep -rEi "(api[_-]?key|secret|token|password)[[:space:]]*=[[:space:]]*[\x27\x22][A-Za-z0-9_+/]{16,}" --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" . 2>/dev/null'

echo ""
echo "Sonuç: $pass geçti, $fail başarısız"
[[ "$fail" -eq 0 ]]