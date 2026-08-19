#!/usr/bin/env python3
"""Bump the project version and add a CHANGELOG.md entry.

Usage:
    python3 scripts/bump_version.py patch   # 0.3.0 -> 0.3.1
    python3 scripts/bump_version.py minor   # 0.3.0 -> 0.4.0
    python3 scripts/bump_version.py major   # 0.3.0 -> 1.0.0
"""

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_PATH = ROOT / "VERSION"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def bump(part: str) -> str:
    version = VERSION_PATH.read_text().strip()
    match = SEMVER.match(version)
    if not match:
        sys.exit(f"VERSION '{version}' is not valid semver")
    major, minor, patch = (int(g) for g in match.groups())
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        sys.exit(f"unknown part '{part}' (expected major|minor|patch)")
    return f"{major}.{minor}.{patch}"


def add_changelog_entry(version: str):
    today = date.today().isoformat()
    entry = f"## [{version}] - {today}\n\n### Added\n"
    changelog = CHANGELOG_PATH.read_text()
    if f"## [{version}]" in changelog:
        sys.exit(f"CHANGELOG.md already has an entry for {version}")
    changelog = changelog.replace(
        "# Changelog\n", f"# Changelog\n\n{entry}\n", 1
    )
    CHANGELOG_PATH.write_text(changelog)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    part = sys.argv[1]
    new_version = bump(part)
    VERSION_PATH.write_text(new_version + "\n")
    add_changelog_entry(new_version)
    print(f"bumped to {new_version}")


if __name__ == "__main__":
    main()