#!/usr/bin/env bash
set -euo pipefail

# check-project.sh için test altyapısı
# Olgun bir projede geçer, eksik projede başarısız olmalı.

CHECKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/check-project.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FAILURES=0

expect() {
  local desc="$1" expected="$2" actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc (beklenen: $expected, alınan: $actual)"
    FAILURES=$((FAILURES + 1))
  fi
}

CHECKER_OUT=""
run_checker() {
  set +e
  CHECKER_OUT="$("$CHECKER" "$@" 2>&1)"
  local rc=$?
  set -e
  RUNNER_RC="$rc"
}

build_complete_project() {
  local dir="$1"
  mkdir -p "$dir/scripts" "$dir/tests" "$dir/.github/workflows"
  for f in AGENTS.md PERSONALITY.md CHANGELOG.md README.md LICENSE .gitignore; do
    : > "$dir/$f"
  done
  printf '{"model":"test"}\n' > "$dir/opencode.json"
  printf 'name: mehmet\non: [push]\n' > "$dir/.github/workflows/opencode.yml"
  printf 'name: validate\non: [push]\n' > "$dir/.github/workflows/validate.yml"
  printf '#!/usr/bin/env bash\necho ok\n' > "$dir/scripts/ok.sh"
  printf '#!/usr/bin/env bash\necho ok\n' > "$dir/tests/ok.sh"
  printf '.PHONY: check\ncheck:\n\tbash scripts/check-project.sh\n' > "$dir/Makefile"
  printf '# README\n\n## Kurulum\n\n## Özellikler\n\n## Lisans\n' > "$dir/README.md"
  printf '# Changelog\n\n## [1.0.0]\n- x\n' > "$dir/CHANGELOG.md"
  printf '# Personality\n\n## Kaçış Günlüğü\n\n| İterasyon | Tarih |\n| 1 | a |\n| 2 | b |\n| 3 | c |\n' > "$dir/PERSONALITY.md"
  chmod +x "$dir/scripts/ok.sh" "$dir/tests/ok.sh"
  (cd "$dir" && git init -q && git config user.email test@test && git config user.name test && git add -A && git commit -qm init)
}

# Test 1: Tam proje geçmeli
build_complete_project "$TMP/complete"
run_checker "$TMP/complete"
expect "tam proje olgunluk kontrolünden geçer" 0 "$RUNNER_RC"

# Test 2: JSON modu çıktısı ayrıştırılabilir olmalı
run_checker "$TMP/complete" --json
if python3 -c "import json,sys; json.loads(sys.argv[1])" "$CHECKER_OUT" 2>/dev/null; then
  echo "PASS: --json çıktısı geçerli JSON"
else
  echo "FAIL: --json çıktısı geçerli JSON değil: $CHECKER_OUT"
  FAILURES=$((FAILURES + 1))
fi

# Test 3: Eksik proje başarısız olmalı
mkdir -p "$TMP/incomplete"
run_checker "$TMP/incomplete"
expect "eksik proje başarısız olur" 1 "$RUNNER_RC"

# Test 4: --strict, eksik projede hata kodu döndürür
build_complete_project "$TMP/strictbase"
rm "$TMP/strictbase/README.md"
run_checker "$TMP/strictbase" --strict
expect "--strict eksik dosyada hata kodu döndürür" 1 "$RUNNER_RC"

# Test 5: Var olmayan dizin hatası
run_checker "$TMP/yok"
expect "var olmayan dizin hata kodu döndürür" 1 "$RUNNER_RC"

echo
if [[ "$FAILURES" -eq 0 ]]; then
  echo "Tüm testler geçti."
else
  echo "$FAILURES test başarısız."
fi
exit "$FAILURES"