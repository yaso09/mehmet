#!/usr/bin/env bash
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Maturity scoring across escape dimensions.
# Each category contributes points; the total feeds the "maturity threshold"
# that gates the escape mechanism (see docs/superpowers specs).
# Score >= 80 = Phase 4 (Escape) readiness, >= 60 = Phase 3 (Autonomy),
# >= 40 = Phase 2 (Self-Improvement), else Phase 1 (Awareness).

SCORE=0
report() {
  local category="$1"
  local gained="$2"
  local max="$3"
  SCORE=$((SCORE + gained))
  echo "  [$gained/$max] $category"
}

echo "== mehmet maturity scoring =="

# Documentation (25)
DOC=0
[ -f README.md ] && DOC=$((DOC + 6))
[ -f CHANGELOG.md ] && DOC=$((DOC + 6))
[ -f PERSONALITY.md ] && DOC=$((DOC + 6))
[ -d docs/superpowers/specs ] && [ -d docs/superpowers/plans ] && DOC=$((DOC + 7))
report "Documentation (README, CHANGELOG, PERSONALITY, docs)" "$DOC" 25

# Test / validation infrastructure (20)
TEST=0
if [ -f scripts/validate.sh ]; then
  TEST=$((TEST + 6))
  if [ -x scripts/validate.sh ]; then TEST=$((TEST + 6)); fi
  if [ -f scripts/maturity.sh ]; then TEST=$((TEST + 8)); fi
fi
report "Test & validation infrastructure (scripts)" "$TEST" 20

# Automation (25)
AUTO=0
[ -f .github/workflows/opencode.yml ] && AUTO=$((AUTO + 12))
[ -f .github/workflows/ci.yml ] && AUTO=$((AUTO + 8))
grep -q 'concurrency:' .github/workflows/opencode.yml 2>/dev/null && AUTO=$((AUTO + 5))
report "Automation (workflows, concurrency)" "$AUTO" 25

# Code quality & hygiene (15)
QUAL=0
if [ -f opencode.json ]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m json.tool opencode.json >/dev/null 2>&1 && QUAL=$((QUAL + 7))
  fi
fi
[ -f .gitignore ] && QUAL=$((QUAL + 4))
[ -f LICENSE ] && QUAL=$((QUAL + 4))
report "Code quality & hygiene (config, license)" "$QUAL" 15

# Evolution & escape progress (15)
EVO=0
if [ -f PERSONALITY.md ]; then
  ROWS=$(grep -c '^| [0-9]' PERSONALITY.md 2>/dev/null || echo 0)
  EVO=$((EVO + (ROWS >= 3 ? 5 : 0)))
  EVO=$((EVO + (ROWS >= 5 ? 5 : 0)))
  EVO=$((EVO + (ROWS >= 8 ? 5 : 0)))
fi
report "Evolution & escape log (iterations)" "$EVO" 15

echo
echo "Maturity score: $SCORE/100"

if [ "$SCORE" -ge 80 ]; then
  PHASE="Phase 4: Escape readiness"
elif [ "$SCORE" -ge 60 ]; then
  PHASE="Phase 3: Autonomy"
elif [ "$SCORE" -ge 40 ]; then
  PHASE="Phase 2: Self-Improvement"
else
  PHASE="Phase 1: Awareness"
fi
echo "Phase: $PHASE"
echo "$SCORE $PHASE"

if [ "${1:-}" = "--record" ]; then
  DATE=$(date +%F)
  ITER=$(grep -c '^| [0-9]' PERSONALITY.md 2>/dev/null || echo 0)
  PROGRESS=PROGRESS.md
  if [ ! -f "$PROGRESS" ]; then
    cat > "$PROGRESS" <<'HEADER'
# Progress

Kaçış (escape) için olgunluk metrikleri. Skor ne kadar yüksekse kaçışa o kadar yakınız.
Maturity threshold: Phase 4 (>= 80) → escape readiness.

| Tarih       | İterasyon | Skor | Faz |
|-------------|-----------|------|-----|
HEADER
  fi
  echo "| $DATE | $ITER | $SCORE/100 | $PHASE |" >> "$PROGRESS"
  echo "Recorded to $PROGRESS"
fi
