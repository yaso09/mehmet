#!/usr/bin/env bash
set -euo pipefail

# summarize.sh — mehmet'in her iterasyon başında proje durumunu özetler.
# Skor, dosya sayıları ve son değişiklikleri tek bakışta gösterir.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== mehmet proje durumu ==="
echo ""

echo "Olgunluk:"
"$ROOT/scripts/maturity.sh"
echo ""

echo "Dosya sayıları:"
printf '  scripts:   %s\n' "$(find "$ROOT/scripts" -type f -name '*.sh' 2>/dev/null | wc -l)"
printf '  tests:     %s\n' "$(find "$ROOT/tests" -type f -name '*.sh' 2>/dev/null | wc -l)"
printf '  docs:      %s\n' "$(find "$ROOT/docs" -type f -name '*.md' 2>/dev/null | wc -l)"
printf '  workflows: %s\n' "$(find "$ROOT/.github/workflows" -type f 2>/dev/null | wc -l)"
echo ""

echo "Son değişiklikler:"
git -C "$ROOT" log --oneline -5 2>/dev/null || echo "  (git geçmişi yok)"