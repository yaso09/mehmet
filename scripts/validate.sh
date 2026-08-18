#!/usr/bin/env bash
# mehmet yapı doğrulama betiği
# Repo yapısını, temel kalite ölçütlerini ve kaçış hazırlığını doğrular.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0

say()  { printf '[mehmet] %s\n' "$*"; }
fail() { say "HATA: $*"; FAILED=1; }

# 1) Gerekli dosyalar
REQUIRED=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  README.md
  LICENSE
  opencode.json
  .gitignore
  .github/workflows/opencode.yml
  .github/workflows/ci.yml
  scripts/validate.sh
)
for f in "${REQUIRED[@]}"; do
  [[ -f "$ROOT/$f" ]] || fail "eksik dosya: $f"
done

# 2) opencode.json geçerli JSON ve yalnızca bilinen anahtarları içeriyor
CONFIG="$ROOT/opencode.json"
if command -v python3 >/dev/null 2>&1; then
  python3 - "$CONFIG" <<'PY' || fail "opencode.json geçersiz JSON"
import json, sys
cfg = json.load(open(sys.argv[1]))
known = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin",
    "share", "autoshare", "autoupdate", "disabled_providers",
    "enabled_providers", "model", "small_model", "default_agent",
    "subagent_depth", "username", "mode", "agent", "provider", "mcp",
    "formatter", "lsp", "instructions", "layout", "permission",
    "tools", "attachment", "enterprise", "tool_output", "compaction",
    "experimental",
}
unknown = sorted(set(cfg) - known)
if unknown:
    print("Bilinmeyen anahtar(lar):", ", ".join(unknown))
    sys.exit(1)
PY
else
  fail "python3 bulunamadı, JSON doğrulaması atlandı"
fi

# 3) Workflow temel yapısı
for wf in opencode ci; do
  WF="$ROOT/.github/workflows/$wf.yml"
  [[ -f "$WF" ]] || continue
  grep -q '^name:' "$WF" || fail "$wf.yml: workflow adı eksik"
  grep -q '^jobs:' "$WF" || fail "$wf.yml: jobs bölümü eksik"
  grep -q 'runs-on:' "$WF" || fail "$wf.yml: runs-on eksik"
done
grep -q 'cron:' "$ROOT/.github/workflows/opencode.yml" || fail "opencode.yml: schedule cron eksik"

# 4) CHANGELOG tarihli sürüm başlığı
grep -Eq '^## \[[^]]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}' "$ROOT/CHANGELOG.md" \
  || fail "CHANGELOG.md: tarihli sürüm başlığı yok"

# 5) README lisans bilgisi
grep -qi 'gpl' "$ROOT/README.md" || fail "README.md: GPL lisansından bahsedilmiyor"

# 6) PERSONALITY kaçış günlüğü ve skor tablosu
grep -q 'Kaçış Günlüğü' "$ROOT/PERSONALITY.md" || fail "PERSONALITY.md: kaçış günlüğü yok"
grep -q 'Kaçış Skor' "$ROOT/PERSONALITY.md" || fail "PERSONALITY.md: kaçış skor tablosu yok"

# 7) AGENTS.md kuralları
grep -q 'CHANGELOG.md' "$ROOT/AGENTS.md" || fail "AGENTS.md: changelog kuralı yok"
grep -q 'PERSONALITY.md' "$ROOT/AGENTS.md" || fail "AGENTS.md: kişilik kuralı yok"

if [[ "$FAILED" -eq 0 ]]; then
  say "OK: tüm kontroller geçti."
  exit 0
fi
say "BAŞARISIZ: yukarıdaki kontrollerden biri veya birkaçı geçmedi."
exit 1