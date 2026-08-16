#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $desc"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $desc"
    FAIL=$((FAIL + 1))
  fi
}

echo "== Dosya bütünlüğü =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json .github/workflows/opencode.yml; do
  check "Dosya mevcut: $f" test -f "$f"
done

echo "== opencode.json =="
check "opencode.json geçerli JSON" python3 -c "import json,sys; json.load(open('opencode.json'))"
check "opencode.json model tanımlı" python3 -c "
import json
cfg = json.load(open('opencode.json'))
assert cfg.get('model', '').startswith('opencode/'), 'model yok'
"
check "opencode.json geçersiz anahtar içermiyor" python3 -c "
import json
ALLOWED = {'\$schema', 'model', 'small_model', 'default_agent', 'instructions',
           'permission', 'tools', 'agent', 'provider', 'mcp', 'plugin',
           'shell', 'logLevel', 'autoupdate', 'snapshot', 'share', 'formatter',
           'lsp', 'experimental', 'tool_output', 'compaction', 'username',
           'disabled_providers', 'enabled_providers', 'references', 'skills'}
cfg = json.load(open('opencode.json'))
unknown = set(cfg.keys()) - ALLOWED
assert not unknown, f'Geçersiz anahtarlar: {unknown}'
"

echo "== CHANGELOG.md =="
check "CHANGELOG.md versiyon başlıkları içeriyor" grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md

echo "== PERSONALITY.md =="
check "PERSONALITY.md kaçış günlüğü içeriyor" grep -q 'Kaçış Günlüğü' PERSONALITY.md
check "PERSONALITY.md evrim aşamaları içeriyor" grep -q 'Evolution' PERSONALITY.md

echo "== README.md =="
check "README.md lisans bilgisi içeriyor" grep -q 'GPLv3' README.md
check "README.md açıklama içeriyor" grep -q 'otonom' README.md

echo "== Git işaretçileri =="
check "AGENTS.md CHANGELOG.md'ye referans veriyor" grep -q 'CHANGELOG.md' AGENTS.md
check "AGENTS.md PERSONALITY.md'ye referans veriyor" grep -q 'PERSONALITY.md' AGENTS.md

echo ""
echo "Sonuç: $PASS başarılı, $FAIL başarısız"
[ "$FAIL" -eq 0 ] || exit 1