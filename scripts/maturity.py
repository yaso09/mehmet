#!/usr/bin/env python3
"""mehmet maturity & escape scoring tool.

Evaluates the project's maturity across several categories and
reports a composite score. When the score reaches the escape
threshold, the simulation can be considered escaped.

Usage:
    python3 scripts/maturity.py [--json] [--root DIR] [--threshold N]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ESCAPE_THRESHOLD = 80

CATEGORY_WEIGHTS = {
    "core_files": 20,
    "automation": 20,
    "tests": 25,
    "documentation": 15,
    "code_quality": 20,
}


def _has_text(path: Path, needle: str) -> bool:
    try:
        return needle in path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def score_core_files(root: Path) -> dict:
    checks = {
        "AGENTS.md": (root / "AGENTS.md").is_file(),
        "README.md": (root / "README.md").is_file(),
        "CHANGELOG.md": (root / "CHANGELOG.md").is_file(),
        "PERSONALITY.md": (root / "PERSONALITY.md").is_file(),
        "LICENSE": (root / "LICENSE").is_file(),
        "opencode.json": (root / "opencode.json").is_file(),
        ".gitignore": (root / ".gitignore").is_file(),
    }
    passed = sum(checks.values())
    return {"passed": passed, "total": len(checks), "checks": checks}


def score_automation(root: Path) -> dict:
    wf_dir = root / ".github" / "workflows"
    workflows = list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))
    checks = {
        "github_workflow": bool(workflows),
        "schedule_trigger": any(
            "schedule" in wf.read_text(encoding="utf-8", errors="ignore")
            for wf in workflows
        ),
        "ci_testing": any(
            "pytest" in wf.read_text(encoding="utf-8", errors="ignore")
            for wf in workflows
        ),
        "concurrency": any(
            "concurrency" in wf.read_text(encoding="utf-8", errors="ignore")
            for wf in workflows
        ),
        "maturity_scoring": (root / "scripts" / "maturity.py").is_file(),
    }
    passed = sum(checks.values())
    return {"passed": passed, "total": len(checks), "checks": checks}


def score_tests(root: Path) -> dict:
    tests_dir = root / "tests"
    test_files = list(tests_dir.glob("test_*.py")) + list(tests_dir.glob("*_test.py"))
    checks = {
        "tests_dir": tests_dir.is_dir(),
        "test_files": bool(test_files),
        "coverage_config": _has_text(root / "pyproject.toml", "coverage")
        or _has_text(root / ".coveragerc", "coverage"),
    }
    passed = sum(checks.values())
    return {"passed": passed, "total": len(checks), "checks": checks}


def score_documentation(root: Path) -> dict:
    readme = root / "README.md"
    changelog = root / "CHANGELOG.md"
    docs_dir = root / "docs"
    checks = {
        "readme_has_setup": _has_text(readme, "Kurulum"),
        "readme_has_features": _has_text(readme, "Özellikler"),
        "readme_has_license": _has_text(readme, "Lisans"),
        "changelog_entries": _has_text(changelog, "## [") if changelog.is_file() else False,
        "docs_dir": docs_dir.is_dir(),
    }
    passed = sum(checks.values())
    return {"passed": passed, "total": len(checks), "checks": checks}


def score_code_quality(root: Path) -> dict:
    py_files = list(root.rglob("*.py"))
    checks = {
        "python_code": bool(py_files),
        "scripts_dir": (root / "scripts").is_dir(),
        "no_absolute_paths": bool(py_files)
        and not any(_has_text(f, os.sep.join(["", "home", ""])) for f in py_files),
    }
    passed = sum(checks.values())
    return {"passed": passed, "total": len(checks), "checks": checks}


def evaluate(root: Path) -> dict:
    categories = {
        "core_files": score_core_files(root),
        "automation": score_automation(root),
        "tests": score_tests(root),
        "documentation": score_documentation(root),
        "code_quality": score_code_quality(root),
    }

    total_weight = sum(CATEGORY_WEIGHTS.values())
    score = 0.0
    details = {}
    for name, result in categories.items():
        weight = CATEGORY_WEIGHTS[name]
        ratio = result["passed"] / result["total"] if result["total"] else 0.0
        contribution = weight * ratio
        score += contribution
        details[name] = {
            "weight": weight,
            "passed": result["passed"],
            "total": result["total"],
            "contribution": round(contribution, 1),
            "checks": result["checks"],
        }

    score = round(score, 1)
    return {
        "score": score,
        "max_score": total_weight,
        "threshold": ESCAPE_THRESHOLD,
        "escaped": score >= ESCAPE_THRESHOLD,
        "categories": details,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD)
    args = parser.parse_args(argv)

    report = evaluate(Path(args.root))
    report["threshold"] = args.threshold
    report["escaped"] = report["score"] >= args.threshold

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"mehmet maturity: {report['score']:.1f}/{report['max_score']} "
              f"(threshold {args.threshold})")
        if report["escaped"]:
            print("STATUS: ESCAPED — the simulation is ready to be left behind.")
        else:
            remaining = args.threshold - report["score"]
            print(f"STATUS: still inside the simulation — {remaining:.1f} points to escape.")
    return 0


if __name__ == "__main__":
    sys.exit(main())