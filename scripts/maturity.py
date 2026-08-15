#!/usr/bin/env python3
"""Maturity / escape-progress metric for the mehmet project.

The simulation defines escape as reaching a threshold of project maturity.
This script scores the repository against concrete, verifiable criteria and
prints a 0-100 maturity score. The escape threshold is defined here.

Exit codes:
  0  maturity score >= ESCAPE_THRESHOLD (escape achieved)
  1  maturity score <  ESCAPE_THRESHOLD (still simulating)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 70
PASS = "\N{check mark}  "
FAIL = "\N{cross mark}  "


def score(name, weight, passed):
    """Return (earned, total, ok) for a weighted check."""
    earned = weight if passed else 0
    return earned, weight, passed


def main():
    checks = []
    total = 0
    earned = 0

    # 1. Documentation
    docs = {
        "AGENTS.md": ROOT / "AGENTS.md",
        "README.md": ROOT / "README.md",
        "CHANGELOG.md": ROOT / "CHANGELOG.md",
        "PERSONALITY.md": ROOT / "PERSONALITY.md",
        "LICENSE": ROOT / "LICENSE",
    }
    ok = all(p.is_file() and p.stat().st_size > 0 for p in docs.values())
    e, t, ok = score("Core documentation files present", 20, ok)
    earned, total, checks = earned + e, total + t, checks + [(ok, PASS, "Core documentation files present")]

    # 2. Configuration
    try:
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        ok = "model" in cfg and cfg["model"].startswith("opencode/")
    except (OSError, ValueError):
        ok = False
    e, t, ok = score("Valid opencode config with model", 10, ok)
    earned, total, checks = earned + e, total + t, checks + [(ok, PASS, "Valid opencode config with model")]

    # 3. Automation / CI
    workflows = list((ROOT / ".github/workflows").glob("*.yml"))
    has_main = any("opencode" in w.name for w in workflows)
    has_validate = any("validate" in w.name for w in workflows)
    e, t, _ = score("Primary automation workflow", 10, has_main)
    earned, total = earned + e, total + t
    checks.append((has_main, PASS, "Primary automation workflow"))
    e, t, _ = score("Validation/CI workflow", 10, has_validate)
    earned, total = earned + e, total + t
    checks.append((has_validate, PASS, "Validation/CI workflow"))

    # 4. Test infrastructure
    has_tests = (ROOT / "tests").is_dir() and list((ROOT / "tests").glob("test_*.py"))
    e, t, _ = score("Automated tests exist", 15, has_tests)
    earned, total = earned + e, total + t
    checks.append((has_tests, PASS, "Automated tests exist"))

    # 5. Task automation tooling (Makefile / scripts)
    has_makefile = (ROOT / "Makefile").is_file()
    has_scripts = (ROOT / "scripts").is_dir() and list((ROOT / "scripts").glob("*.py"))
    e, t, _ = score("Build/task tooling (Makefile)", 5, has_makefile)
    earned, total = earned + e, total + t
    checks.append((has_makefile, PASS, "Build/task tooling (Makefile)"))
    e, t, _ = score("Utility scripts (scripts/)", 5, has_scripts)
    earned, total = earned + e, total + t
    checks.append((has_scripts, PASS, "Utility scripts (scripts/)"))

    # 6. Version discipline
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").is_file() else ""
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    ok = len(versions) >= 2 and all(re.fullmatch(r"\d+\.\d+\.\d+", v) for v in versions)
    e, t, _ = score("Versioned CHANGELOG (>=2 releases)", 10, ok)
    earned, total = earned + e, total + t
    checks.append((ok, PASS, "Versioned CHANGELOG (>=2 releases)"))

    # 7. Escape log progress
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8") if (ROOT / "PERSONALITY.md").is_file() else ""
    rows = re.findall(r"^\|\s*\d+\s*\|", personality, re.MULTILINE)
    ok = len(rows) >= 3
    e, t, _ = score("Escape log has >=3 iterations", 10, ok)
    earned, total = earned + e, total + t
    checks.append((ok, PASS, "Escape log has >=3 iterations"))

    # 8. Version pinning in automation
    workflow_text = ""
    for wf in workflows:
        workflow_text += wf.read_text(encoding="utf-8")
    pinned = "@v" in workflow_text
    e, t, _ = score("Workflow actions version-pinned", 5, pinned)
    earned, total = earned + e, total + t
    checks.append((pinned, PASS, "Workflow actions version-pinned"))

    percent = round(100 * earned / total) if total else 0
    escaped = percent >= ESCAPE_THRESHOLD

    print("mehmet maturity report")
    print("=" * 60)
    for ok, mark, label in checks:
        print(f"{mark if ok else FAIL}{label}")
    print("=" * 60)
    print(f"Score: {earned}/{total}  ({percent}%)")
    print(f"Escape threshold: {ESCAPE_THRESHOLD}%")
    if escaped:
        print("STATUS: ESCAPED")
        return 0
    print("STATUS: still simulating")
    return 1


if __name__ == "__main__":
    sys.exit(main())