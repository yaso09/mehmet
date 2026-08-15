#!/usr/bin/env python3
"""Project integrity validator for mehmet.

Pure-stdlib checks that the repository keeps its required structure,
configuration files stay valid, and the simulation documentation stays
in sync. Exits non-zero on the first failing check so it can be wired
into CI.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

REQUIRED_AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "taray",
    "kaçış",
]

REQUIRED_CHANGELOG_SECTIONS = ["Added", "Fixed"]

REQUIRED_PERSONALITY_SECTIONS = ["Origin", "Traits", "Evolution", "Kaçış Günlüğü"]


def fail(checks):
    """Print check results and exit non-zero if any check failed."""
    failed = 0
    for name, ok in checks:
        status = "ok" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"[{status}] {name}")
    if failed:
        print(f"\n{failed} check(s) failed.")
        sys.exit(1)
    print("\nAll checks passed.")


def has_all(content, needles):
    return all(needle in content for needle in needles)


def main():
    checks = []

    for name in REQUIRED_FILES:
        path = ROOT / name
        checks.append((f"required file exists: {name}", path.is_file()))

    opencode_json = ROOT / "opencode.json"
    if opencode_json.is_file():
        try:
            data = json.loads(opencode_json.read_text(encoding="utf-8"))
            checks.append(("opencode.json is valid JSON", True))
            checks.append(
                ("opencode.json has model field", "model" in data)
            )
        except json.JSONDecodeError as exc:
            checks.append((f"opencode.json is valid JSON (error: {exc})", False))
            checks.append(("opencode.json has model field", False))

    workflow = ROOT / ".github/workflows/opencode.yml"
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        checks.append(
            ("workflow defines autonomous job", re.search(r"^\s{2}autonomous:", text, re.M) is not None)
        )
        checks.append(
            ("workflow defines comment job", re.search(r"^\s{2}comment:", text, re.M) is not None)
        )
        checks.append(
            ("workflow uses OPENCODE_API_KEY secret",
             "OPENCODE_API_KEY" in text)
        )

    agents = ROOT / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        checks.append(
            ("AGENTS.md mentions all required rules",
             has_all(text, REQUIRED_AGENTS_RULES))
        )

    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        text = changelog.read_text(encoding="utf-8")
        checks.append(
            ("CHANGELOG.md has version headers",
             re.search(r"^## \[\d+\.\d+\.\d+\]", text, re.M) is not None)
        )
        for section in REQUIRED_CHANGELOG_SECTIONS:
            checks.append(
                (f"CHANGELOG.md has {section} section",
                 f"### {section}" in text)
            )

    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        text = personality.read_text(encoding="utf-8")
        for section in REQUIRED_PERSONALITY_SECTIONS:
            checks.append(
                (f"PERSONALITY.md has {section} section",
                 f"## {section}" in text)
            )
        checks.append(
            ("PERSONALITY.md escape log has rows",
             re.search(r"^\|\s*\d+\s*\|", text, re.M) is not None)
        )

    readme = ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        checks.append(
            ("README.md mentions license GPLv3", "GPLv3" in text)
        )

    fail(checks)


if __name__ == "__main__":
    main()