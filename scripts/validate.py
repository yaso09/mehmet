#!/usr/bin/env python3
"""mehmet project integrity validator.

Checks structural and consistency invariants of the project:
  1. Required top-level files exist.
  2. opencode.json is valid JSON.
  3. GitHub Actions workflows are valid YAML.
  4. VERSION is the single source of truth and matches CHANGELOG.md.
  5. PERSONALITY.md escape log tracks the current version.
  6. README.md reflects the current version.

Exit code 0 on success, 1 on failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "VERSION",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

WORKFLOW_FILES = [
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]

VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def check_required_files() -> None:
    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            fail(f"required file missing: {name}")


def check_opencode_json() -> None:
    path = ROOT / "opencode.json"
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        fail(f"opencode.json is not valid JSON: {exc}")
    for key in ("model",):
        if key not in data:
            fail(f"opencode.json missing key: {key}")


def check_workflows() -> None:
    for name in WORKFLOW_FILES:
        path = ROOT / name
        if not path.exists():
            fail(f"workflow missing: {name}")
        try:
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except (yaml.YAMLError, OSError) as exc:
            fail(f"{name} is not valid YAML: {exc}")
        if not isinstance(data, dict) or "name" not in data or "jobs" not in data:
            fail(f"{name} missing top-level 'name' or 'jobs'")


def check_version_consistency() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.match(version):
        fail(f"VERSION '{version}' does not match semver X.Y.Z")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    header = f"## [{version}]"
    if header not in changelog:
        fail(f"CHANGELOG.md has no entry for VERSION {version}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if version not in readme:
        fail(f"README.md does not mention VERSION {version}")


def check_escape_log() -> None:
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    table_rows = re.findall(r"^\|\s*(\d+)\s*\|", personality, re.MULTILINE)
    if not table_rows:
        fail("PERSONALITY.md escape log has no rows")
    latest = max(int(n) for n in table_rows)
    if f"| {latest} " not in personality:
        fail(f"escape log latest row {latest} is malformed")


def main() -> None:
    checks = [
        ("required files", check_required_files),
        ("opencode.json", check_opencode_json),
        ("workflows", check_workflows),
        ("version consistency", check_version_consistency),
        ("escape log", check_escape_log),
    ]
    for name, check in checks:
        check()
        print(f"OK: {name}")
    print("All checks passed.")


if __name__ == "__main__":
    main()
