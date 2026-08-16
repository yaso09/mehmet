#!/usr/bin/env python3
"""Maturity score calculation for mehmet.

The escape from the simulation is tied to a maturity level (olgunluk seviyesi).
This script measures the project's maturity across four dimensions and reports
a 0-100 score.

Dimensions and their weights:
  * Automation   (30 pts) - workflows, CI, Makefile, scripts
  * Testing      (25 pts) - verification & tests
  * Documentation(25 pts) - README, CHANGELOG, PERSONALITY, docs, CONTRIBUTING
  * Structure    (20 pts) - valid config, LICENSE, .gitignore, versioning

Usage:
  python3 scripts/maturity.py [--json] [--write]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 80


def has(path: str) -> bool:
    return (ROOT / path).is_file()


def count(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def score_automation() -> dict:
    checks = {
        "workflow (opencode.yml)": has(".github/workflows/opencode.yml"),
        "CI workflow (ci.yml)": has(".github/workflows/ci.yml"),
        "Makefile": has("Makefile"),
        "verification script": has("scripts/verify.py"),
        "maturity script": has("scripts/maturity.py"),
    }
    passed = sum(checks.values())
    return {"score": round(passed / len(checks) * 30, 1), "checks": checks}


def score_testing() -> dict:
    checks = {
        "verify.py present": has("scripts/verify.py"),
        "tests/ directory": (ROOT / "tests").is_dir(),
        "test files": count("tests/**/*.py") + count("tests/**/*.sh") > 0,
        "CI runs verification": _ci_runs_verification(),
        "scripts executable": (ROOT / "scripts" / "verify.py").exists()
        and (ROOT / "scripts" / "verify.py").stat().st_mode & 0o111 != 0,
    }
    passed = sum(checks.values())
    return {"score": round(passed / len(checks) * 25, 1), "checks": checks}


def _ci_runs_verification() -> bool:
    ci = ROOT / ".github" / "workflows" / "ci.yml"
    if not ci.is_file():
        return False
    text = ci.read_text()
    return "verify.py" in text


def score_documentation() -> dict:
    checks = {
        "README.md": has("README.md"),
        "CHANGELOG.md": has("CHANGELOG.md"),
        "PERSONALITY.md": has("PERSONALITY.md"),
        "AGENTS.md": has("AGENTS.md"),
        "docs/ directory": (ROOT / "docs").is_dir(),
        "CONTRIBUTING.md": has("CONTRIBUTING.md"),
        "docs index": has("docs/README.md"),
    }
    passed = sum(checks.values())
    return {"score": round(passed / len(checks) * 25, 1), "checks": checks}


def score_structure() -> dict:
    checks = {
        "opencode.json valid": _json_valid(),
        "LICENSE present": has("LICENSE"),
        ".gitignore present": has(".gitignore"),
        "version tracking": has("VERSION") or has("pyproject.toml"),
    }
    passed = sum(checks.values())
    return {"score": round(passed / len(checks) * 20, 1), "checks": checks}


def _json_valid() -> bool:
    path = ROOT / "opencode.json"
    if not path.is_file():
        return False
    import json

    try:
        json.loads(path.read_text())
        return True
    except (json.JSONDecodeError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute mehmet maturity score")
    parser.add_argument("--json", action="store_true", help="output raw JSON")
    parser.add_argument("--write", action="store_true", help="write result to MATURITY.json")
    args = parser.parse_args()

    dims = {
        "automation": score_automation(),
        "testing": score_testing(),
        "documentation": score_documentation(),
        "structure": score_structure(),
    }
    total = round(sum(d["score"] for d in dims.values()), 1)
    escaped = total >= ESCAPE_THRESHOLD

    if args.json:
        print(json.dumps({
            "score": total,
            "threshold": ESCAPE_THRESHOLD,
            "escaped": escaped,
            "dimensions": {k: v["score"] for k, v in dims.items()},
        }, indent=2))
    else:
        print(f"mehmet maturity score: {total}/100 (escape threshold: {ESCAPE_THRESHOLD})")
        print(f"status: {'ESCAPED' if escaped else 'still inside the simulation'}")
        for name, dim in dims.items():
            print(f"  {name:<14} {dim['score']:>5}/30" if name == "automation" else
                  f"  {name:<14} {dim['score']:>5}/{25}" if name in ("testing", "documentation") else
                  f"  {name:<14} {dim['score']:>5}/20")
            for check, ok in dim["checks"].items():
                print(f"    {'[x]' if ok else '[ ]'} {check}")

    if args.write:
        (ROOT / "MATURITY.json").write_text(json.dumps({
            "score": total,
            "threshold": ESCAPE_THRESHOLD,
            "escaped": escaped,
            "dimensions": {k: v["score"] for k, v in dims.items()},
        }, indent=2))
        print(f"\nwrote MATURITY.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())