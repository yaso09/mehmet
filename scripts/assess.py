#!/usr/bin/env python3
"""Escape readiness / maturity assessment for the mehmet project.

Evaluates the project against a defined set of maturity criteria and reports
a score. This gives the agent a measurable "escape threshold" to converge on.

Exit code is non-zero when the overall score is below --threshold (default 80).
"""

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_file(path: Path, name: str, weight: float, required_content: list[str] | None = None) -> dict:
    ok = path.is_file()
    detail = ""
    if ok and required_content:
        text = path.read_text(errors="ignore")
        missing = [kw for kw in required_content if kw not in text]
        if missing:
            ok = False
            detail = f"missing: {', '.join(missing)}"
    return {
        "id": name,
        "weight": weight,
        "passed": ok,
        "detail": detail,
    }


def assess() -> dict:
    checks = [
        check_file(REPO_ROOT / "README.md", "README", 10),
        check_file(REPO_ROOT / "CHANGELOG.md", "CHANGELOG", 10,
                   required_content=["# Changelog", "## [", "### Added"]),
        check_file(REPO_ROOT / "AGENTS.md", "AGENTS", 10),
        check_file(REPO_ROOT / "PERSONALITY.md", "PERSONALITY", 10),
        check_file(REPO_ROOT / "LICENSE", "LICENSE", 5),
        check_file(REPO_ROOT / "opencode.json", "opencode-config", 10,
                   required_content=["model"]),
        check_file(REPO_ROOT / ".gitignore", "gitignore", 5,
                   required_content=[".env", "node_modules"]),
    ]

    test_dir = REPO_ROOT / "tests"
    test_files = list(test_dir.glob("test_*.py")) if test_dir.is_dir() else []
    checks.append({
        "id": "tests",
        "weight": 15,
        "passed": len(test_files) > 0,
        "detail": f"{len(test_files)} test file(s)" if test_files else "no test files",
    })

    workflows = REPO_ROOT / ".github" / "workflows"
    workflow_files = list(workflows.glob("*.yml")) if workflows.is_dir() else []
    checks.append({
        "id": "automation",
        "weight": 10,
        "passed": len(workflow_files) > 0,
        "detail": f"{len(workflow_files)} workflow(s)" if workflow_files else "no workflows",
    })

    ci_dir = REPO_ROOT / ".github" / "workflows"
    ci_text = "\n".join(
        p.read_text(errors="ignore")
        for p in (ci_dir.glob("*.yml") if ci_dir.is_dir() else [])
        if p.is_file()
    )
    ci_has_tests = bool(ci_text) and any(
        kw in ci_text for kw in ("unittest", "pytest", "test ")
    )
    checks.append({
        "id": "ci-tests",
        "weight": 10,
        "passed": ci_has_tests,
        "detail": "workflow running tests found" if ci_has_tests else "no workflow runs tests",
    })

    has_changelog_entry = False
    changelog = REPO_ROOT / "CHANGELOG.md"
    if changelog.is_file():
        text = changelog.read_text(errors="ignore")
        has_changelog_entry = "## [0.3.0]" in text or len(text.splitlines()) > 25
    checks.append({
        "id": "changelog-fresh",
        "weight": 5,
        "passed": has_changelog_entry,
        "detail": "recent changelog activity" if has_changelog_entry else "changelog is stale",
    })

    score = 0.0
    for c in checks:
        if c["passed"]:
            score += c["weight"]

    return {
        "score": round(score, 1),
        "max_score": sum(c["weight"] for c in checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=80.0,
                        help="minimum acceptable score (default: 80)")
    parser.add_argument("--json", action="store_true",
                        help="emit machine-readable JSON")
    parser.add_argument("--summary", action="store_true",
                        help="print only the score line")
    args = parser.parse_args()

    result = assess()

    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["score"] >= args.threshold else 1

    if args.summary:
        print(f"score: {result['score']:.1f}/{result['max_score']} "
              f"threshold: {args.threshold:.0f}")
    else:
        print("=== mehmet escape readiness ===")
        for c in result["checks"]:
            mark = "PASS" if c["passed"] else "FAIL"
            detail = f" ({c['detail']})" if c["detail"] else ""
            print(f"  [{mark}] {c['id']:<16} weight={c['weight']}{detail}")
        print(f"\n  TOTAL: {result['score']:.1f}/{result['max_score']}")

    ok = result["score"] >= args.threshold
    if not ok:
        print(f"  WARNING: below maturity threshold {args.threshold:.0f}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())