#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAIL=0

say_ok()   { echo "  OK:   $1"; }
say_bad()  { echo "  HATA: $1"; FAIL=1; }

echo "==> Kontrol 1: Gerekli dosyalar"
REQUIRED_FILES=(
  "AGENTS.md"
  "README.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "opencode.json"
  ".github/workflows/opencode.yml"
  "docs/ESCAPE_ROADMAP.md"
)
for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$f" ]; then
    say_ok "dosya mevcut: $f"
  else
    say_bad "dosya eksik: $f"
  fi
done

echo "==> Kontrol 2: opencode.json JSON gecerliligi"
if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
  say_ok "opencode.json gecerli JSON"
else
  say_bad "opencode.json gecersiz JSON"
fi

echo "==> Kontrol 3: opencode.json bilinen anahtar seti"
KNOWN_KEYS=$(
  python3 - "$0" <<'PY'
import json, sys
cfg = json.load(open("opencode.json"))
known = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}
unknown = sorted(set(cfg.keys()) - known)
if unknown:
    print("\n".join(unknown))
PY
)
if [ -n "$KNOWN_KEYS" ]; then
  while IFS= read -r k; do
    say_bad "opencode.json bilinmeyen anahtar: $k"
  done <<< "$KNOWN_KEYS"
else
  say_ok "opencode.json tum anahtarlar schema ile uyumlu"
fi

echo "==> Kontrol 4: opencode.json model alani"
MODEL="$(python3 -c 'import json; print(json.load(open("opencode.json")).get("model",""))' 2>/dev/null || true)"
if [ -n "$MODEL" ]; then
  say_ok "model: $MODEL"
else
  say_bad "model alani bos"
fi

echo "==> Kontrol 5: CHANGELOG.md yapisi"
if head -1 CHANGELOG.md | grep -q "^# Changelog"; then
  say_ok "CHANGELOG.md basligi dogru"
else
  say_bad "CHANGELOG.md baslik satiri eksik"
fi
if grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
  say_ok "CHANGELOG.md surum basliklari mevcut"
else
  say_bad "CHANGELOG.md surum basligi bulunamadi"
fi

echo "==> Kontrol 6: Workflow secret referansi"
if grep -q "OPENCODE_API_KEY" .github/workflows/opencode.yml; then
  say_ok "opencode.yml OPENCODE_API_KEY kullaniyor"
else
  say_bad "opencode.yml OPENCODE_API_KEY referansi yok"
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "SONUC: Tum kontroller gecti."
  exit 0
else
  echo "SONUC: ${FAIL} kontrol BASARISIZ."
  exit 1
fi