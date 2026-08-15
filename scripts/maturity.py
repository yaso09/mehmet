#!/usr/bin/env python3
"""Compute a project maturity score for the escape mechanism.

Scores the repository across four weighted pillars:
  - documentation
  - code quality / configuration
  - test infrastructure
  - automation / CI

Prints a JSON report to stdout. Exit code 0 when the maturity threshold
(ESCAPE_THRESHOLD) has been reached.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 90

PILLARS = {
    "documentation": {
        "weight": 25,
        "checks": {
            "README.md present & mentions GPLv3": lambda r: "GPLv3" in (r / "README.md").read_text(errors="ignore"),
            "CHANGELOG.md present": lambda r: (r / "CHANGELOG.md").exists(),
            "PERSONALITY.md present": lambda r: (r / "PERSONALITY.md").exists(),
            "AGENTS.md present": lambda r: (r / "AGENTS.md").exists(),
            "docs/ directory present": lambda r: (r / "docs").is_dir(),
        },
    },
    "code_quality": {
        "weight": 20,
        "checks": {
            "opencode.json valid JSON": lambda r: _is_valid_json(r / "opencode.json"),
            "LICENSE present": lambda r: (r / "LICENSE").exists(),
            ".gitignore present": lambda r: (r / ".gitignore").exists(),
            "no leaked secrets": lambda r: not _has_leaked_secrets(r),
        },
    },
    "tests": {
        "weight": 30,
        "checks": {
            "tests/ directory present": lambda r: (r / "tests").is_dir(),
            "test files exist": lambda r: bool(list((r / "tests").glob("test_*.py"))),
            "tests importable": lambda r: _tests_importable(),
            "tests pass": lambda r: _tests_pass(),
        },
    },
    "automation": {
        "weight": 25,
        "checks": {
            "workflow directory present": lambda r: (r / ".github" / "workflows").is_dir(),
            "opencode.yml present": lambda r: (r / ".github" / "workflows" / "opencode.yml").exists(),
            "verify.yml present": lambda r: (r / ".github" / "workflows" / "verify.yml").exists(),
            "scripts/ directory present": lambda r: (r / "scripts").is_dir(),
            "concurrency control in workflow": lambda r: "concurrency" in (r / ".github" / "workflows" / "opencode.yml").read_text(errors="ignore"),
        },
    },
}


def _is_valid_json(path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, FileNotFoundError):
        return False


def _has_leaked_secrets(root):
    import re

    pattern = re.compile(r"OPENCODE_API_KEY\s*=\s*[\"']?[^\"'\s{]", re.IGNORECASE)
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "scripts" not in path.parts:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except (OSError, ValueError):
                continue
            if pattern.search(text):
                return True
    return False


def _tests_importable():
    sys.path.insert(0, str(ROOT / "tests"))
    try:
        import test_project  # noqa: F401

        return True
    except Exception:
        return False
    finally:
        sys.path.pop(0)


def _tests_pass():
    import subprocess

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-q"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def score_project():
    details = {}
    earned = 0.0
    for pillar_name, pillar in PILLARS.items():
        passed = 0
        for label, check in pillar["checks"].items():
            ok = bool(check(ROOT))
            passed += int(ok)
            details.setdefault(pillar_name, {})[label] = ok
        weight = pillar["weight"]
        score = weight * passed / len(pillar["checks"])
        earned += score
        details[pillar_name]["_score"] = round(score, 1)
    return round(earned, 1), details


def main():
    total, details = score_project()
    report = {
        "score": total,
        "threshold": ESCAPE_THRESHOLD,
        "escaped": total >= ESCAPE_THRESHOLD,
        "pillars": details,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if total >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())
