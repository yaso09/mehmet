#!/usr/bin/env bash
# mehmet repo sağlık kontrolü.
# Başarısızlık durumunda sıfır olmayan çıkış kodu döner (CI için).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0

check() {
  local desc="$1"
  shift
  if "$@"; then
    echo "OK: $desc"
  else
    echo "FAIL: $desc"
    fail=1
  fi
}

# Zorunlu dosyalar mevcut mu?
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json; do
  check "required file $f" test -f "$f"
done

# opencode.json geçerli JSON mu?
check "opencode.json is valid JSON" jq empty opencode.json

# CHANGELOG.md boş değil mi?
check "CHANGELOG.md is not empty" test -s CHANGELOG.md

# LICENSE GPLv3 (README ile uyumlu) mi?
check "LICENSE mentions GPL-3.0" grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE

# Workflow dosyası var mi?
check "workflow opencode.yml exists" test -f .github/workflows/opencode.yml

# Sır sızıntısı var mi?
if grep -rInE "(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}" \
  --include="*.py" --include="*.sh" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.md" \
  --exclude-dir=".git" .; then
  echo "FAIL: possible secret leak detected"
  fail=1
else
  echo "OK: no secret leaks detected"
fi

# Metrikler güncellensin
if python3 scripts/maturity.py; then
  echo "OK: maturity score above threshold"
else
  echo "FAIL: maturity score below threshold"
  fail=1
fi

exit "$fail"
