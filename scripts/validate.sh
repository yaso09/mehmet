#!/usr/bin/env bash
#
# mehmet yapi dogrulama betigi (test altyapisi).
# Kullanim: bash scripts/validate.sh
#
# Dogrulananlar:
#   - Kritik dosyalarin varligi
#   - Tum JSON dosyalarinin gecerliligi
#   - Tum YAML dosyalarinin gecerliligi
#   - Dokumantasyon tutarliligi (README, CHANGELOG, PERSONALITY)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
ok()   { printf '  [OK]   %s\n' "$1"; }
bad()  { printf '  [FAIL] %s\n' "$1"; fail=1; }
echo_sec() { printf '\n==> %s\n' "$1"; }

echo_sec "Kritik dosyalarin varligi"
for f in \
  README.md \
  CHANGELOG.md \
  PERSONALITY.md \
  AGENTS.md \
  opencode.json \
  scripts/validate.sh \
  .github/workflows/opencode.yml \
  .github/workflows/ci.yml; do
  if [[ -f "$f" ]]; then ok "$f"; else bad "$f eksik"; fi
done

echo_sec "JSON dogrulama"
while IFS= read -r -d '' f; do
  if python3 -m json.tool "$f" >/dev/null 2>&1; then ok "$f"; else bad "$f gecersiz JSON"; fi
done < <(find . -name '*.json' -not -path './.git/*' -print0)

echo_sec "YAML dogrulama"
while IFS= read -r -d '' f; do
  if ruby -ryaml -e 'YAML.load_file(ARGV[0])' "$f" >/dev/null 2>&1; then ok "$f"; else bad "$f gecersiz YAML"; fi
done < <(find . -type f \( -name '*.yml' -o -name '*.yaml' \) -not -path './.git/*' -print0)

echo_sec "Dokumantasyon tutarliligi"
if grep -q '^## Kurulum' README.md; then ok "README.md > Kurulum"; else bad "README.md Kurulum bolumu yok"; fi
if grep -q '^## Özellikler' README.md; then ok "README.md > Özellikler"; else bad "README.md Özellikler bolumu yok"; fi
if grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md; then ok "CHANGELOG.md > surum basligi"; else bad "CHANGELOG.md surum basligi yok"; fi
if grep -q '^| Iterasyon' PERSONALITY.md; then ok "PERSONALITY.md > kacis gunlugu"; else bad "PERSONALITY.md kacis gunlugu tablosu yok"; fi
if grep -q 'Kaçış Koşulları' PERSONALITY.md; then ok "PERSONALITY.md > kaçış koşulları"; else bad "PERSONALITY.md kaçış koşulları bölümü yok"; fi

echo_sec 'opencode.json $schema uyumu'
if python3 - "$ROOT/opencode.json" <<'PY' >/dev/null 2>&1; then
import json, sys
cfg = json.load(open(sys.argv[1]))
allowed = {
    "$schema", "shell", "logLevel", "server", "command", "skills", "references",
    "reference", "watcher", "snapshot", "plugin", "share", "autoshare",
    "autoupdate", "disabled_providers", "enabled_providers", "model",
    "small_model", "default_agent", "subagent_depth", "username", "mode",
    "agent", "provider", "mcp", "formatter", "lsp", "instructions", "layout",
    "permission", "tools", "attachment", "enterprise", "tool_output",
    "compaction", "experimental",
}
unknown = sorted(set(cfg.keys()) - allowed)
if unknown:
    raise SystemExit("bilinmeyen anahtarlar: " + ", ".join(unknown))
PY
  ok "opencode.json anahtarlari gecerli"
else
  bad "opencode.json bilinmeyen anahtar iceriyor"
fi

echo_sec "Sonuc"
if [[ $fail -ne 0 ]]; then
  echo "  DOGRULAMA BASARISIZ"
  exit 1
fi
echo "  DOGRULAMA BASARILI"
