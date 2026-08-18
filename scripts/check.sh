#!/usr/bin/env bash
# mehmet sağlık kontrolü — kaçış hedefine yönelik olgunluk metrikleri.
# CI'da (ci.yml) ve her commit öncesi çalıştırılmalıdır.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

passes=0
failures=0

ok()  { printf 'ok:   %s\n' "$1"; passes=$((passes + 1)); }
bad() { printf 'FAIL: %s\n' "$1"; failures=$((failures + 1)); }

echo "== 1. Gerekli dosyalar =="
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json VERSION \
         scripts/check.sh .github/workflows/opencode.yml .github/workflows/ci.yml; do
  if [[ -f "$ROOT/$f" ]]; then ok "dosya mevcut: $f"; else bad "dosya eksik: $f"; fi
done

echo "== 2. opencode.json geçerliliği (schema uyumu) =="
if [[ -f "$ROOT/opencode.json" ]]; then
  UNKNOWN="$(python3 - "$ROOT/opencode.json" <<'PY'
import json, sys
KNOWN = set("""$schema shell logLevel server command skills references reference watcher
snapshot plugin share autoshare autoupdate disabled_providers enabled_providers model
small_model default_agent subagent_depth username mode agent provider mcp formatter lsp
instructions layout permission tools attachment enterprise tool_output compaction
experimental""".split())
try:
    cfg = json.load(open(sys.argv[1]))
except Exception as e:
    print(f"INVALID_JSON: {e}")
    sys.exit(0)
unknown = sorted(set(cfg) - KNOWN)
if unknown:
    print("UNKNOWN_KEYS: " + " ".join(unknown))
PY
)"
  case "$UNKNOWN" in
    INVALID_JSON:*)
      bad "opencode.json geçerli JSON değil: ${UNKNOWN#INVALID_JSON: }"
      ;;
    UNKNOWN_KEYS:*)
      bad "opencode.json bilinmeyen anahtarlar içeriyor: ${UNKNOWN#UNKNOWN_KEYS: }"
      ;;
    "")
      ok "opencode.json geçerli JSON ve yalnızca bilinen anahtarlar içeriyor"
      ;;
  esac
fi

echo "== 3. Versiyon tutarlılığı =="
if [[ -f "$ROOT/VERSION" ]] && [[ -f "$ROOT/CHANGELOG.md" ]]; then
  VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
  if [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    ok "VERSION geçerli semver: $VERSION"
  else
    bad "VERSION geçerli semver değil: $VERSION"
  fi
  if grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$ROOT/CHANGELOG.md"; then
    ok "CHANGELOG.md en üst girişi tarihli ve sürümlü"
  else
    bad "CHANGELOG.md en üst girişi '## [X.Y.Z] - YYYY-MM-DD' formatında değil"
  fi
  TOP="$(grep -m1 -E '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT/CHANGELOG.md" | sed -E 's/^## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/')"
  if [[ "$VERSION" == "$TOP" ]]; then
    ok "VERSION ($VERSION) ile CHANGELOG en üst sürümü ($TOP) eşleşiyor"
  else
    bad "VERSION ($VERSION) ile CHANGELOG en üst sürümü ($TOP) uyuşmuyor"
  fi
fi

echo "== 4. Dokümantasyon =="
if grep -qi 'mehmet' "$ROOT/README.md"; then ok "README.md proje adını içeriyor"; else bad "README.md proje adını içermiyor"; fi
if grep -qi 'GPLv3' "$ROOT/README.md"; then ok "README.md lisans (GPLv3) içeriyor"; else bad "README.md lisans (GPLv3) içermiyor"; fi
if grep -Eq 'Özellikler|Kurulum' "$ROOT/README.md"; then ok "README.md Özellikler/Kurulum bölümleri içeriyor"; else bad "README.md Özellikler/Kurulum bölümleri eksik"; fi
if grep -q 'Kaçış Günlüğü' "$ROOT/PERSONALITY.md"; then ok "PERSONALITY.md kaçış günlüğü içeriyor"; else bad "PERSONALITY.md kaçış günlüğü içermiyor"; fi
if grep -q 'CHANGELOG.md' "$ROOT/AGENTS.md"; then ok "AGENTS.md CHANGELOG kuralını içeriyor"; else bad "AGENTS.md CHANGELOG kuralını içermiyor"; fi

echo "== 5. Workflow yapısı =="
for wf in opencode.yml ci.yml; do
  WF="$ROOT/.github/workflows/$wf"
  if [[ -f "$WF" ]]; then
    if grep -q '^on:' "$WF" || grep -q '^on$' "$WF"; then ok "$wf 'on:' tetikleyicisi içeriyor"; else bad "$wf 'on:' tetikleyicisi içermiyor"; fi
    if grep -q '^jobs:' "$WF"; then ok "$wf 'jobs:' içeriyor"; else bad "$wf 'jobs:' içermiyor"; fi
  fi
done

echo
echo "Sonuç: $passes geçti, $failures başarısız."
if [[ "$failures" -gt 0 ]]; then
  exit 1
fi