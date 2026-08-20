#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

json_failed=0
yaml_failed=0

echo "==> JSON doğrulama"
while IFS= read -r -d '' f; do
  if python3 -m json.tool "$f" >/dev/null 2>&1; then
    echo "OK: $f"
  else
    echo "HATA: geçersiz JSON -> $f"
    json_failed=1
  fi
done < <(find . -type f -name "*.json" \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -print0)

echo "==> YAML doğrulama"
if python3 -c "import yaml" >/dev/null 2>&1; then
  while IFS= read -r -d '' f; do
    if python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$f" >/dev/null 2>&1; then
      echo "OK: $f"
    else
      echo "HATA: geçersiz YAML -> $f"
      yaml_failed=1
    fi
  done < <(find . -type f \( -name "*.yml" -o -name "*.yaml" \) \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" \
    -print0)
else
  echo "UYARI: PyYAML bulunamadı, YAML doğrulaması atlandı"
fi

echo "==> opencode.json anahtar kontrolü"
python3 - <<'PY'
import json, sys

KNOWN_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

cfg = json.load(open("opencode.json"))
unknown = sorted(set(cfg) - KNOWN_KEYS)
if unknown:
    print("HATA: bilinmeyen config anahtarlari:", unknown)
    sys.exit(1)
print("OK: opencode.json anahtarlari sema uyumlu")
PY

if [ "$json_failed" -ne 0 ] || [ "$yaml_failed" -ne 0 ]; then
  echo "Doğrulama BAŞARISIZ."
  exit 1
fi

echo "Tüm doğrulamalar geçti."