#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0

assert() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf "PASS: %s\n" "$desc"
  else
    printf "FAIL: %s\n" "$desc"
    FAILURES=$((FAILURES + 1))
  fi
}

assert "README.md mevcut ve dolu" test -s "$ROOT/README.md"
assert "AGENTS.md mevcut ve dolu" test -s "$ROOT/AGENTS.md"
assert "CHANGELOG.md mevcut ve dolu" test -s "$ROOT/CHANGELOG.md"
assert "PERSONALITY.md mevcut ve dolu" test -s "$ROOT/PERSONALITY.md"
assert "LICENSE mevcut ve dolu" test -s "$ROOT/LICENSE"
assert ".gitignore mevcut ve dolu" test -s "$ROOT/.gitignore"
assert "opencode.json geçerli JSON" python3 -c "import json; json.load(open('$ROOT/opencode.json'))"
assert "Ana workflow mevcut" test -s "$ROOT/.github/workflows/opencode.yml"
assert "Ana workflow schedule içeriyor" grep -q "schedule" "$ROOT/.github/workflows/opencode.yml"
assert "Ana workflow concurrency içeriyor" grep -q "concurrency" "$ROOT/.github/workflows/opencode.yml"
assert "Doğrulama workflow'u mevcut" test -s "$ROOT/.github/workflows/validate.yml"
assert "CHANGELOG başlığı var" grep -q "^# Changelog" "$ROOT/CHANGELOG.md"
assert "CHANGELOG sürüm girişi var" grep -Eq "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" "$ROOT/CHANGELOG.md"
assert "README lisans bilgisi var" grep -qi "GPL" "$ROOT/README.md"
assert "PERSONALITY kaçış günlüğü var" grep -q "Kaçış Günlüğü" "$ROOT/PERSONALITY.md"
assert "PERSONALITY kaçış günlüğünde satır var" grep -Eq "\|[[:space:]]*[0-9]+" "$ROOT/PERSONALITY.md"
assert "Olgunluk scripti mevcut" test -s "$ROOT/scripts/maturity.sh"
assert "Makefile mevcut" test -s "$ROOT/Makefile"

SECRETS="$(grep -rInE "sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}" "$ROOT" 2>/dev/null | grep -v "^Binary" || true)"
assert "Sızıntı olabilecek secret yok" test -z "$SECRETS"

if [ "$FAILURES" -eq 0 ]; then
  printf "\nTüm testler geçti.\n"
  exit 0
else
  printf "\n%d test başarısız.\n" "$FAILURES"
  exit 1
fi