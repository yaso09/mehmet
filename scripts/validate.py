#!/usr/bin/env python3
"""Project integrity validator for mehmet.

Verifies the core invariants of the self-improving agent project:
existence and consistency of required files, valid configuration,
and up-to-date documentation. Runs in CI on every push and PR.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

PERSONALITY_ESCAPE_HEADER = "## Kaçış Günlüğü / Escape Log"

errors = []
warnings = []


def error(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_required_files():
    for f in REQUIRED_FILES:
        if not (ROOT / f).is_file():
            error(f"missing required file: {f}")


def check_json(file):
    path = ROOT / file
    try:
        json.loads(path.read_text())
    except FileNotFoundError:
        return
    except json.JSONDecodeError as exc:
        error(f"{file} is not valid JSON: {exc}")


def check_changelog():
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        return
    content = path.read_text()
    if not re.search(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}$", content, re.M):
        error("CHANGELOG.md has no version entry matching '## [x.y.z] - YYYY-MM-DD'")


def check_personality():
    path = ROOT / "PERSONALITY.md"
    if not path.is_file():
        return
    content = path.read_text()
    if PERSONALITY_ESCAPE_HEADER not in content:
        error(f"PERSONALITY.md is missing the '{PERSONALITY_ESCAPE_HEADER}' section")


def check_readme_license():
    readme = ROOT / "README.md"
    license_file = ROOT / "LICENSE"
    if not readme.is_file() or not license_file.is_file():
        return
    readme_text = readme.read_text()
    header = license_file.read_text().splitlines()[0]
    license_name = re.sub(r"\s+", " ", header).strip()
    if license_name not in readme_text:
        warn(f"README.md does not mention the LICENSE header '{license_name}'")


def check_workflow():
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.is_file():
        return
    content = path.read_text()
    if "secrets.OPENCODE_API_KEY" not in content:
        error("opencode.yml is missing the OPENCODE_API_KEY secret reference")


def check_changelog_tracked():
    """New file additions should be recorded in CHANGELOG.md (best effort)."""
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.is_file():
        return
    content = changelog.read_text()
    for script in (ROOT / "scripts").glob("*.py") if (ROOT / "scripts").is_dir() else []:
        if script.name not in content:
            warn(f"CHANGELOG.md does not mention {script.name}")


def main():
    check_required_files()
    check_json("opencode.json")
    check_changelog()
    check_personality()
    check_readme_license()
    check_workflow()
    check_changelog_tracked()

    for w in warnings:
        print(f"[warn] {w}")
    for e in errors:
        print(f"[error] {e}")

    if errors:
        print(f"\nValidation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if warnings:
        print(f"\nValidation passed with {len(warnings)} warning(s)")
        return 0
    print("\nValidation passed: all checks OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())