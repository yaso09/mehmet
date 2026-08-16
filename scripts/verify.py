#!/usr/bin/env python3
"""Project health verification for mehmet.

Checks that the repository structure is intact, configuration files are valid,
and the simulation documents (CHANGELOG, PERSONALITY escape log) are up to date.

Exit code 0 on success, 1 on failure.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "opencode.json",
    "LICENSE",
    ".github/workflows/opencode.yml",
]

FAILURES = []


def check(condition, message):
    if condition:
        print(f"  [OK]   {message}")
    else:
        print(f"  [FAIL] {message}")
        FAILURES.append(message)
    return condition


def main():
    print(f"mehmet verification (root: {ROOT})")

    print("\n1. Required files")
    for name in REQUIRED_FILES:
        check((ROOT / name).is_file(), f"{name} exists")

    print("\n2. opencode.json")
    cfg_path = ROOT / "opencode.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text())
            check(isinstance(cfg, dict) and "model" in cfg, "valid JSON with model field")
        except json.JSONDecodeError as exc:
            check(False, f"valid JSON (error: {exc})")
    else:
        check(False, "valid JSON")

    print("\n3. Workflow YAML")
    for wf in ["opencode.yml", "ci.yml"]:
        path = ROOT / ".github" / "workflows" / wf
        if path.is_file():
            try:
                data = yaml.safe_load(path.read_text())
                check(isinstance(data, dict) and "jobs" in data, f"{wf} valid YAML with jobs")
            except yaml.YAMLError as exc:
                check(False, f"{wf} valid YAML (error: {exc})")
        else:
            check(False, f"{wf} exists")

    print("\n4. CHANGELOG.md")
    changelog = (ROOT / "CHANGELOG.md")
    if changelog.is_file():
        content = changelog.read_text()
        check(re.search(r"^## \[\d+\.\d+\.\d+\]", content, re.M), "has at least one version entry")
        check("### Added" in content, "has 'Added' section")
    else:
        check(False, "exists")

    print("\n5. PERSONALITY.md escape log")
    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        content = personality.read_text()
        check("Kaçış Günlüğü" in content or "Escape Log" in content, "has escape log section")
        check("| Iterasyon" in content, "has log table header")
        check("| 1" in content, "has at least one log entry")
    else:
        check(False, "exists")

    print("\n6. README.md")
    readme = ROOT / "README.md"
    if readme.is_file():
        content = readme.read_text()
        check(len(content.strip()) > 100, "is not empty")
    else:
        check(False, "exists")

    print(f"\n{'=' * 40}")
    if FAILURES:
        print(f"FAILED ({len(FAILURES)} problem(s))")
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())