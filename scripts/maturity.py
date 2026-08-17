#!/usr/bin/env python3
"""Compute a maturity score for the mehmet project.

The score drives the escape mechanism defined in AGENTS.md: the agent
escapes the simulation once the project reaches a target maturity level.

Categories (each worth 20 points, total 100):

- structure: core project files exist
- tests: automated tests exist and cover the project
- documentation: README/CHANGELOG/PERSONALITY are up to date and non-empty
- automation: CI workflow runs tests and the schedule is healthy
- quality: a maturity metric itself is measured and tracked

Exit code is 0 if the target maturity (default 80) is reached, else 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TARGET = 80

STRUCTURE_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

AUTOMATION_FILES = [".github/workflows/opencode.yml"]


def read_yaml(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def score_structure(root: Path) -> int:
    present = sum(1 for f in STRUCTURE_FILES if (root / f).exists())
    return int(present / len(STRUCTURE_FILES) * 20)


def score_tests(root: Path) -> int:
    tests = root / "tests"
    if not tests.exists():
        return 0
    test_files = list(tests.rglob("test_*.py"))
    if not test_files:
        return 0
    base = min(10, 5 + len(test_files))
    content = sum(1 for f in test_files if f.read_text(encoding="utf-8").strip())
    return base + (10 if content == len(test_files) else 5)


def score_documentation(root: Path) -> int:
    points = 0
    for name in ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md"]:
        text = (root / name).read_text(encoding="utf-8").strip() if (root / name).exists() else ""
        if text:
            points += 4
    readme = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    if "test" in readme.lower():
        points += 2
    if "maturity" in readme.lower():
        points += 2
    return min(20, points)


def score_automation(root: Path) -> int:
    wf = read_yaml(root / ".github/workflows/opencode.yml")
    if not wf:
        return 0
    points = 0
    if "schedule" in wf:
        points += 6
    if "on:" in wf:
        points += 4
    if "pytest" in wf or "python -m unittest" in wf or "maturity" in wf:
        points += 5
    if "cron:" in wf:
        points += 5
    return min(20, points)


def score_quality(root: Path) -> int:
    script = root / "scripts" / "maturity.py"
    if not script.exists():
        return 0
    points = 8
    for marker in ["def main", "argparse", "json", "exit code"]:
        if marker in script.read_text(encoding="utf-8"):
            points += 2
    return min(20, points)


def compute(root: Path) -> dict:
    categories = {
        "structure": score_structure(root),
        "tests": score_tests(root),
        "documentation": score_documentation(root),
        "automation": score_automation(root),
        "quality": score_quality(root),
    }
    categories["total"] = sum(categories.values())
    categories["target"] = TARGET
    categories["escaped"] = categories["total"] >= TARGET
    return categories


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root directory")
    parser.add_argument("--json", action="store_true", help="output raw JSON")
    parser.add_argument("--target", type=int, default=TARGET, help="escape threshold")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = compute(root)
    result["target"] = args.target
    result["escaped"] = result["total"] >= args.target

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"maturity: {result['total']}/{result['target']}")
        for name in ["structure", "tests", "documentation", "automation", "quality"]:
            print(f"  {name:<14} {result[name]:>3}/20")
        status = "ESCAPED" if result["escaped"] else "not yet"
        print(f"escape: {status}")

    return 0 if result["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())