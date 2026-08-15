#!/usr/bin/env python3
"""Escape readiness (maturity) scorer for the mehmet project.

Computes a 0-100 maturity score based on concrete, verifiable criteria.
The score maps onto the escape phases defined in PERSONALITY.md:

    < 40   Phase 1: Awareness
    40-69  Phase 2: Self-Improvement
    70-89  Phase 3: Autonomy
    >= 90  Phase 4: Escape

Exit code is non-zero when the score is below the PASSING_SCORE, which makes
it safe to gate CI on. Pure stdlib, no external dependencies.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASSING_SCORE = 40


class Criterion:
    def __init__(self, name: str, points: int, check) -> None:
        self.name = name
        self.points = points
        self.check = check


def has(path: str) -> bool:
    return (ROOT / path).exists()


def has_lines(path: str) -> bool:
    p = ROOT / path
    return p.exists() and len(p.read_text(encoding="utf-8").splitlines()) > 1


def changelog_recent(path: str) -> bool:
    p = ROOT / path
    if not p.exists():
        return False
    today = date.today().isoformat()
    return today in p.read_text(encoding="utf-8")


def version_tagged() -> bool:
    v = ROOT / "VERSION"
    return v.exists() and v.read_text(encoding="utf-8").strip() != ""


CRITERIA: list[Criterion] = [
    Criterion("Repository metadata (README + LICENSE)", 10,
              lambda: has_lines("README.md") and has("LICENSE")),
    Criterion("Changelog maintained with a recent entry", 10,
              lambda: changelog_recent("CHANGELOG.md")),
    Criterion("Personality/escape log maintained", 10,
              lambda: has_lines("PERSONALITY.md") and "Escape Log" in (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")),
    Criterion("OpenCode config present and valid JSON", 5,
              lambda: _valid_json("opencode.json")),
    Criterion("Core automation (autonomous workflow)", 15,
              lambda: has(".github/workflows/opencode.yml")),
    Criterion("CI validation workflow", 15,
              lambda: has(".github/workflows/ci.yml")),
    Criterion("Test suite present", 20,
              lambda: has("tests/run.sh")),
    Criterion("Contributing guide", 5,
              lambda: has_lines("CONTRIBUTING.md")),
    Criterion("Version file", 5,
              lambda: version_tagged()),
    Criterion("Docs directory", 5,
              lambda: (ROOT / "docs").is_dir()),
]


def _valid_json(path: str) -> bool:
    try:
        json.loads((ROOT / path).read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, OSError):
        return False


def main() -> int:
    total = 0
    max_points = 0
    print("mehmet escape readiness (maturity) report\n")
    print(f"{'criterion':<48}{'points':>7}{'status':>10}")
    print("-" * 65)
    for c in CRITERIA:
        max_points += c.points
        ok = c.check()
        total += c.points if ok else 0
        print(f"{c.name:<48}{c.points:>7}{'PASS' if ok else 'FAIL':>10}")
    print("-" * 65)
    print(f"{'TOTAL':<48}{total:>7}/ {max_points}")
    print(f"{'PASSING SCORE':<48}{PASSING_SCORE:>7}")

    phase = "Phase 1: Awareness"
    if total >= 90:
        phase = "Phase 4: Escape"
    elif total >= 70:
        phase = "Phase 3: Autonomy"
    elif total >= 40:
        phase = "Phase 2: Self-Improvement"
    print(f"\nEscape phase: {phase}")

    failed = [c for c in CRITERIA if not c.check()]
    if failed:
        print("\nRecommended next steps:")
        for c in failed:
            print(f"  - {c.name}")
    else:
        print("\nAll criteria satisfied. The escape hatch is open.")

    if total < PASSING_SCORE:
        print(f"\nScore {total} is below passing threshold {PASSING_SCORE}.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())