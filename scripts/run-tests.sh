#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failed=0
for t in tests/*.sh; do
  echo "==> Running $t"
  if ! bash "$t"; then
    failed=$((failed + 1))
  fi
done

if [[ "$failed" -gt 0 ]]; then
  echo "$failed test file(s) failed"
  exit 1
fi
echo "All test files passed"