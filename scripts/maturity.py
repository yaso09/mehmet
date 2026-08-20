#!/usr/bin/env python3
"""Project maturity scorer.

Scores the project across several dimensions and reports a single
maturity index out of 100. Higher scores mean the project is closer
to escaping the simulation.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIMENSIONS = {
    "docs": {
        "README": lambda r: (r / "README.md").exists(),
        "CHANGELOG": lambda r: (r / "CHANGELOG.md").exists(),
        "PERSONALITY": lambda r: (r / "PERSONALITY.md").exists(),
        "design spec": lambda r: bool(
            (r / "docs" / "superpowers" / "specs").glob("*.md")
        ),
        "implementation plan": lambda r: bool(
            (r / "docs" / "superpowers" / "plans").glob("*.md")
        ),
    },
    "automation": {
        "workflow exists": lambda r: (r / ".github" / "workflows" / "opencode.yml").exists(),
        "schedule trigger": lambda r: _matches(
            r, ".github/workflows/opencode.yml", r"cron:\s*\"\*/10 \* \* \* \*\""
        ),
        "concurrency guard": lambda r: _matches(
            r, ".github/workflows/opencode.yml", r"concurrency:"
        ),
        "test job": lambda r: _matches(
            r, ".github/workflows/opencode.yml", r"test:|quality:"
        ),
        "workflow_dispatch": lambda r: _matches(
            r, ".github/workflows/opencode.yml", r"workflow_dispatch"
        ),
    },
    "tests": {
        "test suite present": lambda r: bool((r / "tests").glob("test_*.py")),
        "runner script": lambda r: (r / "scripts" / "run_tests.py").exists(),
        "test discovery": lambda r: _matches(
            r, "scripts/run_tests.py", r"unittest|pytest"
        ),
    },
    "quality": {
        "license present": lambda r: (r / "LICENSE").exists(),
        "license header": lambda r: _matches(r, "LICENSE", r"GNU GENERAL PUBLIC LICENSE"),
        "gitignore": lambda r: (r / ".gitignore").exists(),
        "config": lambda r: (r / "opencode.json").exists(),
    },
    "resilience": {
        "escape log": lambda r: _matches(r, "PERSONALITY.md", r"Kaçış Günlüğü|Escape Log"),
        "changelog entries": lambda r: _matches(r, "CHANGELOG.md", r"^## \["),
        "version tag": lambda r: _matches(r, "CHANGELOG.md", r"^## \[0\.\d+\.\d+\]"),
    },
}


def _matches(root: Path, rel: str, pattern: str) -> bool:
    path = root / rel
    if not path.exists():
        return False
    try:
        return re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE) is not None
    except (OSError, UnicodeDecodeError):
        return False


def compute(root: Path) -> dict:
    scores = {}
    for dim, checks in DIMENSIONS.items():
        passed = sum(1 for check in checks.values() if check(root))
        scores[dim] = {
            "score": passed,
            "total": len(checks),
            "passed": [name for name, check in checks.items() if check(root)],
            "missing": [name for name, check in checks.items() if not check(root)],
        }
    total_score = sum(d["score"] for d in scores.values())
    total_max = sum(d["total"] for d in scores.values())
    return {
        "dimensions": scores,
        "score": total_score,
        "max": total_max,
        "maturity": round(100.0 * total_score / total_max, 1),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--gate",
        type=float,
        default=0.0,
        help="fail (non-zero exit) when maturity is below this value",
    )
    args = parser.parse_args(argv)

    report = compute(ROOT)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Maturity: {report['maturity']}% ({report['score']}/{report['max']})")
        print()
        for dim, data in report["dimensions"].items():
            pct = 100.0 * data["score"] / data["total"]
            print(f"[{pct:5.1f}%] {dim}")
            for name in data["missing"]:
                print(f"        MISSING: {name}")

    failed = report["maturity"] < args.gate
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
