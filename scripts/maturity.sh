#!/usr/bin/env bash
# mehmet — escape readiness / maturity score (0-100).
# Weighted metric that measures how far the project has evolved toward escape.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

score=0
max=100

add() { # add <points> <description>
  score=$((score + $1))
  printf '  +%s  %s\n' "$1" "$2"
}

echo "== mehmet maturity assessment =="

# --- Foundation (max 30) ---
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json; do
  if [ -f "$f" ]; then add 5 "$f present"; else echo "   -   $f missing"; fi
done

# --- Automation & CI (max 20) ---
if [ -f .github/workflows/opencode.yml ]; then
  add 10 "autonomous workflow present"
else
  echo "   -   autonomous workflow missing"
fi
if grep -q 'anomalyco/opencode/github' .github/workflows/opencode.yml 2>/dev/null; then
  add 10 "opencode action wired to workflow"
else
  echo "   -   opencode action not wired"
fi

# --- Verification & tests (max 20) ---
if [ -f scripts/verify.sh ]; then add 10 "verification script present"; else echo "   -   verify.sh missing"; fi
if ls tests/* 2>/dev/null | grep -q .; then add 10 "tests present"; else echo "   -   no tests found"; fi

# --- Documentation depth (max 15) ---
if [ -d docs/superpowers ]; then add 5 "design docs present"; else echo "   -   no design docs"; fi
if grep -q 'Kurulum' README.md 2>/dev/null; then add 5 "README has setup guide"; else echo "   -   no setup guide in README"; fi
if grep -q 'Kaçış Günlüğü' PERSONALITY.md 2>/dev/null; then add 5 "escape log maintained"; else echo "   -   escape log missing"; fi

# --- Security hygiene (max 15) ---
if ! grep -rIl --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=scripts --exclude-dir=tests -E 'OPENCODE_API_KEY=|[A-Za-z0-9_-]{32}=' . >/dev/null 2>&1; then
  add 10 "no secrets in repository"
else
  echo "   -   possible secret leak"
fi
if [ -f .gitignore ]; then add 5 ".gitignore present"; else echo "   -   .gitignore missing"; fi

echo
echo "MATURITY_SCORE=${score}/${max}"
printf "ESCAPE_READINESS=%d%%\n" $((score * 100 / max))
