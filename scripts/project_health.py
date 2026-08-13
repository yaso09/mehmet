#!/usr/bin/env python3
"""Project maturity and health checker for mehmet.

Computes a 0-100 maturity score, validates the project structure, and
emits a JSON report. Used as the concrete escape-mechanism gauge: when
the maturity score reaches ESCAPE_THRESHOLD the simulation is considered
ready to escape.

Only uses the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent

# Threshold above which the project is considered "escape ready".
ESCAPE_THRESHOLD = 80

# Maturity categories: (key, weight, label)
CATEGORIES = [
    ("core_docs", 25, "Core docs (AGENTS, README, PERSONALITY, CHANGELOG)"),
    ("config", 15, "Configuration (opencode.json, .gitignore)"),
    ("automation", 20, "Automation (CI workflow, Makefile)"),
    ("tooling", 15, "Tooling (scripts, tests)"),
    ("docs", 10, "Design documentation"),
    ("housekeeping", 15, "Housekeeping (license, no stale TODOs)"),
]

# Each check returns a bool. Weight of the check is its share of the
# category weight, split evenly across the checks in that category.
CHECKS: dict[str, list[Callable[[Path], bool]]] = {
    "core_docs": [
        lambda r: (r / "AGENTS.md").is_file(),
        lambda r: (r / "README.md").is_file(),
        lambda r: (r / "PERSONALITY.md").is_file(),
        lambda r: (r / "CHANGELOG.md").is_file(),
        lambda r: _has_recent_changelog(r),
        lambda r: _has_escape_log(r),
    ],
    "config": [
        lambda r: _valid_json_config(r),
        lambda r: (r / ".gitignore").is_file(),
        lambda r: (r / "opencode.json").is_file(),
    ],
    "automation": [
        lambda r: _has_ci_workflow(r),
        lambda r: _workflow_has_health_check(r),
        lambda r: (r / "Makefile").is_file(),
    ],
    "tooling": [
        lambda r: (r / "scripts" / "project_health.py").is_file(),
        lambda r: (r / "scripts" / "test_project_health.py").is_file(),
        lambda r: _tests_pass(r),
    ],
    "docs": [
        lambda r: (r / "docs").is_dir() and any((r / "docs").rglob("*.md")),
    ],
    "housekeeping": [
        lambda r: (r / "LICENSE").is_file(),
        lambda r: not _has_stale_todos(r),
        lambda r: _no_stray_artifacts(r),
    ],
}


def _recent_days(days: int = 45) -> date:
    return date.today() - timedelta(days=days)


def _has_recent_changelog(root: Path) -> bool:
    path = root / "CHANGELOG.md"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    dates = re.findall(r"##\s+\[\S+\]\s+-\s+(\d{4}-\d{2}-\d{2})", text)
    if not dates:
        return False
    latest = max(datetime.strptime(d, "%Y-%m-%d").date() for d in dates)
    return latest >= _recent_days()


def _has_escape_log(root: Path) -> bool:
    path = root / "PERSONALITY.md"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return "escape log" in text.lower() or "kaçış günlüğü" in text.lower()


def _valid_json_config(root: Path) -> bool:
    path = root / "opencode.json"
    if not path.is_file():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, OSError):
        return False


def _has_ci_workflow(root: Path) -> bool:
    return (root / ".github" / "workflows").is_dir() and any(
        (root / ".github" / "workflows").glob("*.yml")
    )


def _workflow_has_health_check(root: Path) -> bool:
    for wf in (root / ".github" / "workflows").glob("*.yml"):
        text = wf.read_text(encoding="utf-8", errors="ignore")
        if "project_health" in text or "make health" in text:
            return True
    return False


def _tests_pass(root: Path) -> bool:
    import subprocess

    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        return False
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover"],
        cwd=scripts_dir,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode == 0


def _has_stale_todos(root: Path) -> bool:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".git") for part in path.parts):
            continue
        if path.name.startswith("test_"):
            continue
        if path.suffix not in {".py", ".md", ".yml", ".json", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if re.search(r"TODO\s*[:(]", line, re.IGNORECASE):
                return True
    return False


def _no_stray_artifacts(root: Path) -> bool:
    for name in (".pytest_cache", ".coverage", "htmlcov", "dist", "build"):
        if any(root.rglob(name)):
            return False
    return True


def _run_checks(root: Path) -> dict[str, list[bool]]:
    results: dict[str, list[bool]] = {}
    for category, checks in CHECKS.items():
        results[category] = [check(root) for check in checks]
    return results


def maturity_score(results: dict[str, list[bool]]) -> int:
    total = 0.0
    for category, weight, _ in CATEGORIES:
        passed = sum(results[category])
        total += weight * passed / len(results[category])
    return int(round(total))


def build_report(root: Path) -> dict:
    results = _run_checks(root)
    score = maturity_score(results)
    breakdown = {}
    for category, weight, label in CATEGORIES:
        passed = sum(results[category])
        gained = round(weight * passed / len(results[category]))
        breakdown[category] = {
            "label": label,
            "passed": passed,
            "total": len(results[category]),
            "points": gained,
            "checks": results[category],
        }
    return {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "maturity_score": score,
        "escape_threshold": ESCAPE_THRESHOLD,
        "escape_ready": score >= ESCAPE_THRESHOLD,
        "categories": breakdown,
    }


def render_human(report: dict) -> str:
    lines = [
        f"Project maturity: {report['maturity_score']}/100",
        f"Escape threshold: {report['escape_threshold']} "
        f"({'READY' if report['escape_ready'] else 'NOT YET'})",
        "",
    ]
    for cat, info in report["categories"].items():
        status = "OK " if info["passed"] == info["total"] else "WARN"
        lines.append(
            f"[{status}] {info['label']}: "
            f"{info['passed']}/{info['total']} ({info['points']} pts)"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mehmet project health checker")
    parser.add_argument(
        "--root", default=str(ROOT), help="project root directory"
    )
    parser.add_argument(
        "--json", action="store_true", help="emit JSON report"
    )
    parser.add_argument(
        "--score", action="store_true", help="print only the score"
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    report = build_report(root)

    if args.json:
        print(json.dumps(report, indent=2))
    elif args.score:
        print(report["maturity_score"])
    else:
        print(render_human(report))

    return 0 if report["maturity_score"] >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())