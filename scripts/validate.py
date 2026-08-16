#!/usr/bin/env python3
"""Repository consistency and quality validation for the mehmet project.

Checks that required files exist, JSON/YAML documents are well-formed, and
key documents stay consistent (license, changelog, personality). Exits with a
non-zero code when any check fails, making it CI-friendly.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
    "scripts/validate.py",
    "scripts/maturity.py",
]

REQUIRED_JSON = ["opencode.json"]
REQUIRED_YAML = [".github/workflows/opencode.yml", ".github/workflows/validate.yml"]


def check_file_exists(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing required file: {path}")


def check_json(path: Path, errors: list[str]) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid JSON in {path}: {exc}")


def check_yaml(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing YAML file: {path}")
        return
    if yaml is None:
        return
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid YAML in {path}: {exc}")


def check_readme_license(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        errors.append("README.md missing (cannot verify license)")
        return
    if not re.search(r"GPLv3", readme.read_text(encoding="utf-8")):
        errors.append("README.md does not state GPLv3 license (inconsistent with LICENSE)")


def check_changelog_version(errors: list[str]) -> None:
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.is_file():
        errors.append("CHANGELOG.md missing")
        return
    if not re.search(r"^## \[\d+\.\d+\.\d+\]", changelog.read_text(encoding="utf-8"), re.MULTILINE):
        errors.append("CHANGELOG.md has no versioned entries")


def check_personality_log(errors: list[str]) -> None:
    personality = ROOT / "PERSONALITY.md"
    if not personality.is_file():
        errors.append("PERSONALITY.md missing")
        return
    if not re.search(r"Kaçış Günlüğü|Escape Log", personality.read_text(encoding="utf-8")):
        errors.append("PERSONALITY.md is missing the escape log")


def main() -> int:
    errors: list[str] = []

    for name in REQUIRED_FILES:
        check_file_exists(ROOT / name, errors)

    for name in REQUIRED_JSON:
        check_json(ROOT / name, errors)

    for name in REQUIRED_YAML:
        check_yaml(ROOT / name, errors)

    check_readme_license(errors)
    check_changelog_version(errors)
    check_personality_log(errors)

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Validation PASSED: project is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())