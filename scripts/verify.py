#!/usr/bin/env python3
"""mehmet project integrity verification.

Ensures every iteration starts from a known-good state and reports a
maturity score that tracks progress toward the escape threshold.
"""

import json
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

REQUIRED_README_SECTIONS = ["## Özellikler", "## Kurulum", "## Lisans"]

errors = []


def check(condition: bool, message: str) -> None:
    status = "OK" if condition else "FAIL"
    print(f"  [{status}] {message}")
    if not condition:
        errors.append(message)


def main() -> int:
    print("== mehmet project verification ==")

    print("\n[1] Required files")
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        check(path.is_file(), f"{rel} exists")
        if path.is_file():
            check(len(path.read_text(encoding="utf-8").strip()) > 0, f"{rel} is not empty")

    print("\n[2] README sections")
    readme = ROOT / "README.md"
    if readme.is_file():
        content = readme.read_text(encoding="utf-8")
        for section in REQUIRED_README_SECTIONS:
            check(section in content, f"README contains '{section}'")

    print("\n[3] Config")
    config = ROOT / "opencode.json"
    if config.is_file():
        try:
            json.loads(config.read_text(encoding="utf-8"))
            check(True, "opencode.json is valid JSON")
        except json.JSONDecodeError as exc:
            check(False, f"opencode.json is valid JSON (error: {exc})")

    print("\n[4] Escape log")
    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        content = personality.read_text(encoding="utf-8")
        check(
            "Escape Log" in content or "Kaçış Günlüğü" in content,
            "PERSONALITY contains escape log",
        )

    print("\n[5] Changelog")
    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        content = changelog.read_text(encoding="utf-8")
        check("## " in content, "CHANGELOG has versioned entries")

    print("\n[6] Maturity score")
    passed = len(REQUIRED_FILES) * 2 + len(REQUIRED_README_SECTIONS) + 2 + 1 + 1
    maturity = max(0, passed - len(errors))
    score = maturity / passed * 100
    print(f"  Passed {maturity}/{passed} checks ({score:.1f}%)")
    print(f"  Escaped: {'YES' if score == 100 else 'NOT YET'}")

    print()
    if errors:
        print(f"FAILED with {len(errors)} error(s)")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())