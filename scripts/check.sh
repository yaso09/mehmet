#!/usr/bin/env bash
#
# mehmet sağlık kontrolü (health check)
#
# Projenin MATURITY.md'de tanımlanan L2 kriterlerini doğrular.
# Başarısız kontrol için exit code 1 döner.
#
# Kullanım:
#   ./scripts/check.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0
PASS=0

ok() { printf '  [OK]   %s\n' "$1"; PASS=$((PASS + 1)); }
bad() { printf '  [FAIL] %s\n' "$1" >&2; FAILURES=$((FAILURES + 1)); }

printf 'mehmet health check\n'

printf '  Temel dosyalar:\n'
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  MATURITY.md \
  opencode.json \
  LICENSE \
  .github/workflows/opencode.yml \
  .github/workflows/quality.yml; do
  if [[ -f "$ROOT/$f" ]]; then
    ok "$f mevcut"
  else
    bad "$f eksik"
  fi
done

printf '  Yapılandırma:\n'
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$ROOT/opencode.json" 2>/dev/null; then
    ok "opencode.json geçerli JSON"
  else
    bad "opencode.json geçerli JSON değil"
  fi
else
  printf '  [SKIP] python3 bulunamadı, JSON doğrulanmadı\n'
fi

printf '  Changelog:\n'
if grep -qE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT/CHANGELOG.md"; then
  ok "CHANGELOG.md sürüm başlıkları içeriyor"
else
  bad "CHANGELOG.md sürüm başlığı yok (## [x.y.z] beklenir)"
fi

printf '  Escape günlüğü:\n'
if grep -qE '^\| [0-9]+ +\|' "$ROOT/PERSONALITY.md"; then
  ok "PERSONALITY.md kaçış günlüğü satırları içeriyor"
else
  bad "PERSONALITY.md kaçış günlüğü boş"
fi

printf '  Maturity:\n'
if grep -q '^### L2' "$ROOT/MATURITY.md"; then
  ok "MATURITY.md L2 seviyesini tanımlıyor"
else
  bad "MATURITY.md L2 bölümü yok"
fi

printf '  Erişilebilirlik (README -> dosyalar):\n'
while read -r link; do
  link="${link##*(}"
  link="${link%%#*}"
  if [[ -n "$link" && -f "$ROOT/$link" ]]; then
    ok "$link"
  elif [[ -n "$link" ]]; then
    bad "README.md bağlantısı kırık: $link"
  fi
done < <(
  grep -Eo '\([A-Za-z0-9_./-]+\.(md|json|yml|sh)\)' "$ROOT/README.md" |
    sed -E 's/^\(//; s/\)$//'
)

printf '  Workflowlar:\n'
for wf in "$ROOT"/.github/workflows/*.yml; do
  if [[ -s "$wf" ]]; then
    ok "$(basename "$wf") boş değil"
  else
    bad "$(basename "$wf") boş"
  fi
done

printf '\nSonuç: %d geçti, %d hata\n' "$PASS" "$FAILURES"
if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi
printf 'Sağlık kontrolü başarılı.\n'