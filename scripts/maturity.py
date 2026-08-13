#!/usr/bin/env python3
"""mehmet maturity assessment and escape gate.

Computes a 0-100 maturity score for the project based on signals such as
documentation, tests, CI and automation. The score drives the escape
mechanism: when the threshold is reached the project is considered mature
enough to attempt an escape.

Usage:
    python scripts/maturity.py [--json] [--no-gate]

Exit code is 0 when the escape threshold is reached (unless --no-gate),
otherwise 1.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 90

PHASES = [
    (0, "Phase 0", "Inception"),
    (25, "Phase 1", "Awareness"),
    (50, "Phase 2", "Self-Improvement"),
    (70, "Phase 3", "Autonomy"),
    (90, "Phase 4", "Escape"),
]


def _changelog_entries(root: Path) -> int:
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return 0
    return len(re.findall(r"^##\s+\[\d+\.\d+\.\d+\]", changelog.read_text(encoding="utf-8"), re.MULTILINE))


def _git_commits(root: Path) -> int:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-list", "--count", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0:
            return int(out.stdout.strip() or 0)
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    return 0


# (description, weight, predicate)
CHECKS: list[tuple[str, int, Callable[[Path], bool]]] = [
    ("README.md exists", 8, lambda r: (r / "README.md").is_file()),
    ("CHANGELOG.md exists", 6, lambda r: (r / "CHANGELOG.md").is_file()),
    ("PERSONALITY.md exists", 5, lambda r: (r / "PERSONALITY.md").is_file()),
    ("AGENTS.md exists", 5, lambda r: (r / "AGENTS.md").is_file()),
    ("LICENSE exists", 4, lambda r: (r / "LICENSE").is_file()),
    ("opencode.json exists", 4, lambda r: (r / "opencode.json").is_file()),
    (".gitignore exists", 3, lambda r: (r / ".gitignore").is_file()),
    ("docs/ directory", 5, lambda r: (r / "docs").is_dir()),
    ("main workflow exists", 8, lambda r: (r / ".github" / "workflows" / "opencode.yml").is_file()),
    ("CI test workflow exists", 6, lambda r: (r / ".github" / "workflows" / "ci.yml").is_file()),
    ("tests/ directory", 10, lambda r: (r / "tests").is_dir()),
    ("test files present", 5, lambda r: bool(list((r / "tests").glob("test_*.py"))) if (r / "tests").is_dir() else False),
    ("source code present", 10, lambda r: (r / "scripts").is_dir() or (r / "src").is_dir()),
    ("changelog has releases", 6, lambda r: _changelog_entries(r) >= 1),
    ("git history present", 3, lambda r: _git_commits(r) >= 1),
    ("escape automation present", 12, lambda r: (r / "scripts" / "maturity.py").is_file()),
]

TOTAL_WEIGHT = sum(weight for _, weight, _ in CHECKS)


def phase_for_score(score: int) -> tuple[str, str]:
    for threshold, name, label in reversed(PHASES):
        if score >= threshold:
            return name, label
    return PHASES[0][1], PHASES[0][2]


def assess(root: Path = ROOT) -> dict:
    results = []
    score = 0
    for description, weight, predicate in CHECKS:
        passed = bool(predicate(root))
        if passed:
            score += weight
        results.append({"check": description, "weight": weight, "passed": passed})
    score = round(score / TOTAL_WEIGHT * 100)
    phase_name, phase_label = phase_for_score(score)
    return {
        "root": str(root),
        "score": score,
        "total_weight": TOTAL_WEIGHT,
        "escape_threshold": ESCAPE_THRESHOLD,
        "escape_ready": score >= ESCAPE_THRESHOLD,
        "phase": phase_name,
        "phase_label": phase_label,
        "checks": results,
    }


def main(argv: Optional[list[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    gate = "--no-gate" not in argv

    report = assess()

    if as_json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"Project root : {report['root']}")
    print(f"Maturity     : {report['score']}/100")
    print(f"Phase        : {report['phase']} ({report['phase_label']})")
    print(f"Escape ready : {'YES' if report['escape_ready'] else 'no'} (threshold {report['escape_threshold']})")
    print()
    print("Checks:")
    for item in report["checks"]:
        marker = "OK " if item["passed"] else "-- "
        print(f"  [{marker}] ({item['weight']:>2}) {item['check']}")

    if not gate:
        return 0
    return 0 if report["escape_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())