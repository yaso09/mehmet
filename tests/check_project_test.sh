#!/usr/bin/env bash
set -euo pipefail

# check_project_test.sh — scripts/check-project.sh için testler

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

assert() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf '  ok: %s\n' "$desc"
  else
    printf '  HATA: %s\n' "$desc"
    failures=$((failures + 1))
  fi
}

assert_refute() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf '  HATA: %s (beklenen başarısızlık)\n' "$desc"
    failures=$((failures + 1))
  else
    printf '  ok: %s\n' "$desc"
  fi
}

# Sağlıklı repoda kontrol başarılı olmalı
assert "sağlıklı repoda check başarılı" scripts/check-project.sh

# JSON geçerliliği: python3 gerektiren kontrolde bile sağlıklı repo geçer
if command -v python3 >/dev/null 2>&1; then
  assert "python3 ile JSON doğrulaması geçiyor" bash -c 'python3 -c "import json;json.load(open(\"opencode.json\"))"'
fi

# Bozuk repo tespiti: zorunlu dosya eksikse check başarısız olmalı
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/scripts" "$tmp/.github/workflows" "$tmp/tests"
cp scripts/*.sh "$tmp/scripts/"
printf 'fake\n' > "$tmp/CHANGELOG.md"
printf 'fake\n' > "$tmp/README.md"
printf 'fake\n' > "$tmp/PERSONALITY.md"
printf 'fake\n' > "$tmp/LICENSE"
printf 'fake\n' > "$tmp/.gitignore"
printf '{}\n' > "$tmp/opencode.json"
printf 'name: mehmet\n' > "$tmp/.github/workflows/opencode.yml"
# AGENTS.md bilinçli olarak oluşturulmuyor -> check başarısız olmalı
assert_refute "eksik AGENTS.md ile check başarısız olmalı" bash -c 'cd "$0" && scripts/check-project.sh' "$tmp"

if (( failures > 0 )); then
  printf 'check_project_test.sh: %d hata\n' "$failures"
  exit 1
fi

printf 'check_project_test.sh: tüm testler geçti\n'
exit 0