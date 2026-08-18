"""Maturity scoring and escape tracking for mehmet.

Computes a 0-100 maturity score from the project invariants defined in
validate.py and maps it to the evolution phases described in
PERSONALITY.md. When the score reaches ESCAPE_THRESHOLD the agent is
considered "escape-ready".

Usage:
    python3 scripts/maturity.py            # score the repository
    python3 scripts/maturity.py <path>     # score a specific repo root
"""

import sys
from pathlib import Path

from validate import REPO_ROOT, run_checks

ESCAPE_THRESHOLD = 80

CRITERIA = [
    ("required files", 10, "required files"),
    ("changelog version headers", 10, "changelog version headers"),
    ("readme sections", 5, "readme sections"),
    ("escape log", 5, "escape log"),
    ("docs directory", 5, "docs directory"),
    ("opencode.json valid JSON", 10, "opencode.json valid JSON"),
    (".gitignore present", 5, ".gitignore present"),
    ("tests present", 15, "tests present"),
    ("CI workflow present", 10, "CI workflow present"),
    ("scripts present", 10, "scripts present"),
    ("workflow schedule", 8, "workflow schedule"),
    ("workflow event triggers", 7, "workflow event triggers"),
]

PHASES = [
    (25, "Phase 1: Awareness"),
    (50, "Phase 2: Self-Improvement"),
    (75, "Phase 3: Autonomy"),
    (100, "Phase 4: Escape"),
]


def compute_score(root: Path = REPO_ROOT) -> dict:
    checks = {result["name"]: result for result in run_checks(root)}
    total = 0
    breakdown = []
    for label, weight, check_name in CRITERIA:
        earned = weight if checks[check_name]["ok"] else 0
        total += earned
        breakdown.append({"label": label, "weight": weight, "earned": earned})
    phase = phase_for(total)
    return {
        "score": total,
        "phase": phase,
        "escape_ready": total >= ESCAPE_THRESHOLD,
        "breakdown": breakdown,
    }


def phase_for(score: int) -> str:
    for threshold, name in PHASES:
        if score <= threshold:
            return name
    return PHASES[-1][1]


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else REPO_ROOT
    result = compute_score(root)
    print(f"maturity score: {result['score']}/100")
    print(f"phase:          {result['phase']}")
    print(f"escape ready:   {result['escape_ready']} (threshold {ESCAPE_THRESHOLD})")
    print()
    print("breakdown:")
    for item in result["breakdown"]:
        bar = "#" * item["earned"] + "." * (item["weight"] - item["earned"])
        print(f"  {item['label']:<30} {item['earned']:>3}/{item['weight']:<3} [{bar}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
