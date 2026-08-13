#!/usr/bin/env python3
"""Project integrity validator for mehmet.

Checks the repository is in a healthy, well-documented, consistent state.
Exits non-zero if any check fails. Intended to run in CI (validate workflow)
and locally.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".gitignore",
]

REQUIRED_AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
]

CONFIG_SCHEMA = "https://opencode.ai/config.json"
EXPECTED_MODEL = "opencode/deepseek-v4-flash-free"


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"  [PASS] {message}")
    else:
        print(f"  [FAIL] {message}")
        failures.append(message)


def check_files(failures: list[str]) -> None:
    print("> Required files")
    for name in REQUIRED_FILES:
        check((ROOT / name).exists(), f"{name} exists", failures)


def check_agents_rules(failures: list[str]) -> None:
    print("> AGENTS.md rules")
    path = ROOT / "AGENTS.md"
    if not path.exists():
        check(False, "AGENTS.md exists", failures)
        return
    content = path.read_text(encoding="utf-8")
    for keyword in REQUIRED_AGENTS_RULES:
        check(keyword in content, f"AGENTS.md references {keyword}", failures)


def check_opencode_config(failures: list[str]) -> None:
    print("> opencode.json config")
    path = ROOT / "opencode.json"
    if not path.exists():
        check(False, "opencode.json exists", failures)
        return
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
        check(True, "opencode.json is valid JSON", failures)
    except json.JSONDecodeError as exc:
        check(False, f"opencode.json is valid JSON ({exc})", failures)
        return

    check(config.get("$schema") == CONFIG_SCHEMA, "opencode.json has $schema", failures)
    check(config.get("model") == EXPECTED_MODEL, "opencode.json model is expected", failures)


def check_readme(failures: list[str]) -> None:
    print("> README.md content")
    path = ROOT / "README.md"
    if not path.exists():
        check(False, "README.md exists", failures)
        return
    content = path.read_text(encoding="utf-8")
    for keyword in ["mehmet", "Kurulum", "Lisans", "Özellikler"]:
        check(keyword in content, f"README.md mentions {keyword}", failures)


def check_changelog(failures: list[str]) -> None:
    print("> CHANGELOG.md format")
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        check(False, "CHANGELOG.md exists", failures)
        return
    content = path.read_text(encoding="utf-8")
    version_header = re.search(r"^## \[(\d+\.\d+\.\d+)\]", content, re.MULTILINE)
    check(version_header is not None, "CHANGELOG.md has a version header", failures)
    if version_header:
        latest = version_header.group(1)
        version_file = ROOT / "VERSION"
        if version_file.exists():
            file_version = version_file.read_text(encoding="utf-8").strip()
            check(latest == file_version, f"CHANGELOG latest ({latest}) matches VERSION ({file_version})", failures)


def main() -> int:
    failures: list[str] = []
    print(f"Validating project at {ROOT}\n")

    check_files(failures)
    check_agents_rules(failures)
    check_opencode_config(failures)
    check_readme(failures)
    check_changelog(failures)

    print(f"\n{'=' * 40}")
    if failures:
        print(f"Validation FAILED: {len(failures)} issue(s)")
        return 1
    print("Validation PASSED: all checks OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())