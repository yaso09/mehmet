#!/usr/bin/env bash
# mehmet — test orchestrator. Tüm doğrulama adımlarını çalıştırır.
#
# Kullanım: ./scripts/run-tests.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAILURES=0

step() {
  echo ""
  echo "=================================================="
  echo ">> $1"
  echo "=================================================="
}

run() {
  if "$@"; then
    echo ">> GECTI"
  else
    echo ">> BASARISIZ: $*"
    FAILURES=$((FAILURES + 1))
  fi
}

step "Bash sözdizimi kontrolü"
run bash -n scripts/maturity.sh
run bash -n scripts/check-repo.sh
run bash -n scripts/run-tests.sh

step "Repo yapısal kontrol"
run bash scripts/check-repo.sh

step "Olgunluk skoru"
run bash scripts/maturity.sh

step "Kaçış eşiği kontrolü"
if SCORE=$(bash scripts/maturity.sh --json); then
  echo "  $SCORE"
  echo "  >> GECTI"
else
  echo "  >> BASARISIZ"
  FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=================================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "TÜM TESTLER GECTI"
  exit 0
else
  echo "$FAILURES ADIM BAŞARISIZ"
  exit 1
fi