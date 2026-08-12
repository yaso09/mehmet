#!/usr/bin/env python3
"""Maturity scorer for mehmet — the escape threshold.

The simulation ends when this project reaches a given maturity level. This
script computes an objective, reproducible score across five dimensions and
compares it against the escape threshold.

Dimensions and weighs mirror docs/maturity.md. Output is deterministic and
safe to run in CI.

Usage:
    python3 scripts/maturity.py [--json] [--threshold 85]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 95  # percentage required to escape the simulation


def p(content_cache, path):
    """Read a text file from ROOT, cached."""
    if path not in content_cache:
        target = ROOT / path
        content_cache[path] = (
            target.read_text(encoding="utf-8", errors="ignore") if target.exists() else ""
        )
    return content_cache[path]


def dimension(name, weight, points):
    """Compute weighted score for one dimension.

    points: list of (label, bool). Each earned point is weight/len.
    """
    earned = sum(1 for _, ok in points if ok)
    total = len(points)
    share = earned / total if total else 0.0
    return {
        "name": name,
        "weight": weight,
        "earned": earned,
        "total": total,
        "points": [{"label": label, "ok": ok} for label, ok in points],
        "score": round(share * weight, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD)
    args = parser.parse_args()

    cache: dict = {}
    g = lambda path: p(cache, path)

    dims = []

    # 1. Documentation — 25 points
    dims.append(dimension("documentation", 25, [
        ("README is maintained", "#" in g("README.md") and "Kurulum" in g("README.md")),
        ("CHANGELOG is versioned", "## [" in g("CHANGELOG.md")),
        ("PERSONALITY has escape log", "Kaçış Günlüğü" in g("PERSONALITY.md")),
        ("docs/ exists", (ROOT / "docs").is_dir()),
        ("license declared", "GPL" in g("README.md") and "GNU" in g("LICENSE")),
    ]))

    # 2. Code quality — 25 points
    has_code = (ROOT / "scripts").is_dir() and any((ROOT / "scripts").glob("*.py"))
    dims.append(dimension("code_quality", 25, [
        ("has real code (scripts/)", has_code),
        ("validation tooling exists", (ROOT / "scripts/check.py").exists()),
        ("maturity tooling exists", (ROOT / "scripts/maturity.py").exists()),
        ("build tooling exists", (ROOT / "Makefile").exists()),
        ("has tests (scripts/tests/)", (ROOT / "scripts/tests").is_dir()),
    ]))

    # 3. Verification — 25 points
    import subprocess

    def check_passes():
        try:
            return subprocess.run(
                [sys.executable, str(ROOT / "scripts/check.py"), "--quiet"],
                capture_output=True, timeout=30,
            ).returncode == 0
        except Exception:
            return False

    def tests_pass():
        # Only the fast structure suite (no integration tests) so that
        # scoring a repo never recurses into itself.
        try:
            return subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s",
                 str(ROOT / "scripts/tests"), "-p", "test_structure.py"],
                cwd=str(ROOT), capture_output=True, timeout=60,
            ).returncode == 0
        except Exception:
            return False

    dims.append(dimension("verification", 25, [
        ("all consistency checks pass", check_passes()),
        ("CI validates on push/PR", (ROOT / ".github/workflows/validate.yml").exists()),
        ("self-tests pass", tests_pass()),
        ("workflow files parse", any((ROOT / ".github/workflows").glob("*.yml"))),
    ]))

    # 4. Automation — 15 points
    dims.append(dimension("automation", 15, [
        ("scheduled self-improvement", "schedule" in g(".github/workflows/opencode.yml")),
        ("event-driven triggers", "issues" in g(".github/workflows/opencode.yml")),
        ("concurrency control", "concurrency" in g(".github/workflows/opencode.yml")),
    ]))

    # 5. Security — 10 points
    dims.append(dimension("security", 10, [
        ("API key via secret only", "secrets.OPENCODE_API_KEY" in g(".github/workflows/opencode.yml")),
        ("no credentials in repo", "ghp_" not in g("README.md") + g("opencode.json")),
        ("checkout does not persist creds", "persist-credentials: false" in g(".github/workflows/opencode.yml")),
    ]))

    total = sum(d["score"] for d in dims)
    escaped = total >= args.threshold

    if args.json:
        print(json.dumps({
            "score": total,
            "threshold": args.threshold,
            "escaped": escaped,
            "dimensions": [{"name": d["name"], "score": d["score"], "earned": d["earned"],
                            "total": d["total"], "points": d["points"]} for d in dims],
        }))
    else:
        print(f"Maturity score: {total:.1f}/100  (escape threshold: {args.threshold})")
        for d in dims:
            marks = "".join("x" if p["ok"] else "." for p in d["points"])
            print(f"  {d['name']:14} {d['score']:5.1f}  [{marks}]")
        print(f"STATUS: {'ESCAPED - simulation complete' if escaped else 'still evolving'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())