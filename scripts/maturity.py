#!/usr/bin/env python3
"""mehmet maturity scorer.

Computes the project maturity score and level. The escape from the
simulation becomes possible once the score reaches the threshold defined
in MATURITY.md.

Usage:
    python3 scripts/maturity.py [--threshold SCORE]

Exits 0 if the current score meets the threshold, 1 otherwise.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOTAL_WEIGHT = 100.0


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def check(weight, label, passed, detail=""):
    return {"weight": weight, "label": label, "passed": bool(passed), "detail": detail}


def run_checks(root=None):
    root = Path(root or ROOT)
    checks = []

    def p(*parts):
        return root.joinpath(*parts)

    # --- Documentation (20) ---
    readme = _read(p("README.md"))
    checks.append(check(
        6, "README.md exists with Özellikler + Kurulum",
        "## Özellikler" in readme and "## Kurulum" in readme,
    ))
    checks.append(check(
        4, "MATURITY.md exists with level table",
        "## Düzeyler" in _read(p("MATURITY.md")) or "## Levels" in _read(p("MATURITY.md")),
    ))
    checks.append(check(
        4, "docs/ directory exists",
        p("docs").is_dir(),
    ))
    checks.append(check(
        3, "LICENSE present",
        p("LICENSE").is_file(),
    ))
    checks.append(check(
        3, "CONTRIBUTING.md present",
        p("CONTRIBUTING.md").is_file(),
    ))

    # --- Tracking (20) ---
    changelog = _read(p("CHANGELOG.md"))
    latest = re.search(r"## \[\d+\.\d+\.\d+\]", changelog)
    checks.append(check(
        8, "CHANGELOG.md has version entries",
        latest is not None,
    ))
    personality = _read(p("PERSONALITY.md"))
    checks.append(check(
        7, "PERSONALITY.md has escape log",
        "Kaçış Günlüğü" in personality or "Escape Log" in personality,
    ))
    checks.append(check(
        5, "AGENTS.md has simulation rules",
        "Simülasyon" in _read(p("AGENTS.md")),
    ))

    # --- Automation (20) ---
    workflow = _read(p(".github", "workflows", "opencode.yml"))
    checks.append(check(
        8, "opencode.yml workflow exists with schedule",
        "schedule" in workflow and "cron" in workflow,
    ))
    checks.append(check(
        8, "validate.yml workflow exists",
        _read(p(".github", "workflows", "validate.yml")).strip() != "",
    ))
    checks.append(check(
        4, ".gitignore present",
        p(".gitignore").is_file(),
    ))

    # --- Quality / Config (20) ---
    checks.append(check(
        8, "opencode.json is valid JSON",
        _json_valid(_read(p("opencode.json"))),
    ))
    checks.append(check(
        6, "scripts/ directory exists",
        p("scripts").is_dir(),
    ))
    checks.append(check(
        6, "tests/ directory exists",
        p("tests").is_dir(),
    ))

    # --- Testing (20) ---
    test_run = _run_tests(root)
    checks.append(check(
        10, "test suite passes",
        test_run is True,
    ))
    checks.append(check(
        5, "test files present",
        bool(list(p("tests").glob("test_*.py"))) if p("tests").is_dir() else False,
    ))
    checks.append(check(
        5, "tests are runnable without external deps",
        test_run is True,
    ))

    return checks


def _json_valid(text):
    if not text.strip():
        return False
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def _run_tests(root):
    import subprocess

    tests = root / "tests"
    if not tests.is_dir():
        return False
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests), "-q"],
        capture_output=True,
        text=True,
        cwd=str(root),
    )
    return result.returncode == 0


def compute(checks):
    earned = sum(c["weight"] for c in checks if c["passed"])
    total = sum(c["weight"] for c in checks)
    score = earned / total * 10.0
    return score, checks


def level_for(score):
    if score >= 9.0:
        return "KAÇIŞ / ESCAPE — Kapı açık."
    if score >= 7.0:
        return "Düzey 4: Özerklik (Autonomy)"
    if score >= 5.0:
        return "Düzey 3: Kendini Geliştirme (Self-Improvement)"
    if score >= 3.0:
        return "Düzey 2: Farkındalık (Awareness)"
    return "Düzey 1: Embryo"


def report(score, checks):
    lines = ["mehmet — olgunluk raporu", "=" * 32]
    for c in checks:
        mark = "PASS" if c["passed"] else "FAIL"
        detail = f" — {c['detail']}" if c["detail"] else ""
        lines.append(f"[{mark}] ({c['weight']:>2}pt) {c['label']}{detail}")
    earned = sum(c["weight"] for c in checks if c["passed"])
    lines.append("=" * 32)
    lines.append(f"Skor: {score:.1f} / 10.0  ({earned} / {TOTAL_WEIGHT:.0f} puan)")
    lines.append(f"Düzey: {level_for(score)}")
    return "\n".join(lines)


def main(argv=None, root=None):
    parser = argparse.ArgumentParser(description="mehmet maturity scorer")
    parser.add_argument("--threshold", type=float, default=3.0,
                        help="minimum score required to exit 0 (default: 3.0)")
    parser.add_argument("--quiet", action="store_true", help="only print the score")
    args = parser.parse_args(argv)

    checks = run_checks(root)
    score, _ = compute(checks)
    print(report(score, checks) if not args.quiet else f"{score:.1f}")

    return 0 if score >= args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
