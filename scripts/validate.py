#!/usr/bin/env python3
"""Project health validation for mehmet.

Verifies that the simulation rules are being followed and that the
project stays in a consistent state. Returns a non-zero exit code if
any check fails, making it safe to run in CI.

Checks:
  1. Required files exist (README, CHANGELOG, AGENTS, PERSONALITY, LICENSE)
  2. AGENTS.md simulation rules are present
  3. CHANGELOG.md is versioned and ordered
  4. Escape log exists in PERSONALITY.md with entries
  5. README license matches LICENSE
  6. opencode.json is valid JSON with a model
  7. Python scripts under scripts/ compile
  8. Workflow YAML contains required triggers

Usage:
  python3 scripts/validate.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(name: str, ok: bool, failures: list[str]) -> None:
    status = "ok " if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        failures.append(name)


def main() -> int:
    failures: list[str] = []
    required = ["README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md", "LICENSE"]

    for f in required:
        check(f"{f} exists", (ROOT / f).is_file(), failures)

    agents = (ROOT / "AGENTS.md").read_text(errors="ignore")
    check("AGENTS.md: rules present", all(r in agents for r in ("CHANGELOG", "README", "PERSONALITY")), failures)

    changelog = (ROOT / "CHANGELOG.md").read_text(errors="ignore")
    versions = re.findall(r"^## \[([^\]]+)\]", changelog, re.M)
    check("CHANGELOG: versioned", len(versions) > 0, failures)
    check("CHANGELOG: most recent on top", versions == sorted(versions, reverse=True), failures)

    personality = (ROOT / "PERSONALITY.md").read_text(errors="ignore")
    has_log = "Kaçış Günlüğü" in personality and "| 1 " in personality
    check("PERSONALITY: escape log populated", has_log, failures)

    readme = (ROOT / "README.md").read_text(errors="ignore")
    license_text = (ROOT / "LICENSE").read_text(errors="ignore")
    license_is_gpl = re.search(r"GPL-3|GPLv3|GPL v3|GENERAL PUBLIC LICENSE", license_text) is not None and "Version 3" in license_text
    check("LICENSE is GPLv3", license_is_gpl, failures)
    check("README: license matches LICENSE", license_is_gpl and "GPLv3" in readme, failures)

    try:
        config = json.loads((ROOT / "opencode.json").read_text())
        check("opencode.json: valid JSON with model", isinstance(config.get("model"), str), failures)
    except json.JSONDecodeError:
        check("opencode.json: valid JSON", False, failures)

    py_scripts = sorted(ROOT.glob("scripts/*.py"))
    for p in py_scripts:
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
            check(f"script compiles: {p.name}", True, failures)
        except SyntaxError:
            check(f"script compiles: {p.name}", False, failures)
    check("scripts directory has scripts", len(py_scripts) > 0, failures)

    workflow = ROOT / ".github/workflows/opencode.yml"
    if workflow.is_file():
        text = workflow.read_text(errors="ignore")
        check("workflow: schedule trigger", "schedule" in text, failures)
        check("workflow: issue/PR triggers", "issues" in text and "pull_request" in text, failures)
    else:
        check("workflow: opencode.yml exists", False, failures)

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())