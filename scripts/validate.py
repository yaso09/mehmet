#!/usr/bin/env python3
"""mehmet — project integrity validator.

Checks that all simulation-critical files exist, are well-formed and stay in
sync with each other. Exits non-zero on any failure so it can be wired into
CI (see .github/workflows/validate.yml).

Usage:
    python3 scripts/validate.py [--verbose]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SECTIONS = [
    "Simülasyon Bağlamı",
    "## Kurallar",
]
REQUIRED_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "kaçış günlüğü",
]
REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]
CHANGELOG_HEADER = "# Changelog"
LICENSE_MAP = {
    "GPLv3": ["GNU GENERAL PUBLIC LICENSE", "Version 3"],
    "MIT": ["MIT License", "Permission is hereby granted"],
}


class Result:
    """Collects individual check outcomes."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.count = 0

    def ok(self, name: str) -> None:
        self.count += 1
        print(f"  [PASS] {name}")

    def warn(self, name: str, detail: str = "") -> None:
        self.count += 1
        self.warnings.append(f"{name}: {detail}" if detail else name)
        print(f"  [WARN] {name} {detail}".rstrip())

    def fail(self, name: str, detail: str = "") -> None:
        self.count += 1
        self.errors.append(f"{name}: {detail}" if detail else name)
        print(f"  [FAIL] {name} {detail}".rstrip())

    def report(self) -> int:
        print(f"\n{self.count} checks run.")
        if self.warnings:
            print(f"{len(self.warnings)} warning(s):")
            for w in self.warnings:
                print(f"  - {w}")
        if self.errors:
            print(f"{len(self.errors)} error(s):")
            for e in self.errors:
                print(f"  - {e}")
            return 1
        print("All checks passed.")
        return 0


def check_agents_md(result: Result) -> None:
    path = ROOT / "AGENTS.md"
    if not path.exists():
        result.fail("AGENTS.md", "file missing")
        return
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            result.fail("AGENTS.md", f"missing section: {section}")
            return
    text_lower = text.lower()
    for rule in REQUIRED_RULES:
        if rule.lower() not in text_lower:
            result.fail("AGENTS.md", f"missing rule reference: {rule}")
            return
    result.ok("AGENTS.md — simulation context intact")


def check_changelog(result: Result) -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        result.fail("CHANGELOG.md", "file missing")
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith(CHANGELOG_HEADER):
        result.fail("CHANGELOG.md", f"must start with '{CHANGELOG_HEADER}'")
        return
    if not re.search(r"^## \[\d+\.\d+\.\d+\]", text, re.MULTILINE):
        result.fail("CHANGELOG.md", "no versioned section found")
        return
    result.ok("CHANGELOG.md — versioned entries present")


def check_personality(result: Result) -> None:
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        result.fail("PERSONALITY.md", "file missing")
        return
    text = path.read_text(encoding="utf-8")
    if "Kaçış Günlüğü" not in text:
        result.fail("PERSONALITY.md", "escape log missing")
        return
    if "| Iterasyon |" not in text:
        result.fail("PERSONALITY.md", "escape log table header missing")
        return
    result.ok("PERSONALITY.md — escape log present")


def check_readme_license(result: Result) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        result.fail("README.md", "file missing")
        return
    text = path.read_text(encoding="utf-8")
    license_path = ROOT / "LICENSE"
    if not license_path.exists():
        result.fail("LICENSE", "file missing")
        return
    license_text = license_path.read_text(encoding="utf-8")
    for short, markers in LICENSE_MAP.items():
        if short in text and all(m in license_text for m in markers):
            result.ok(f"README.md — license matches LICENSE ({short})")
            return
    result.fail("README.md", "license mentioned in README does not match LICENSE")


def check_opencode_json(result: Result) -> None:
    path = ROOT / "opencode.json"
    if not path.exists():
        result.fail("opencode.json", "file missing")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.fail("opencode.json", f"invalid JSON: {exc}")
        return
    if "model" not in data:
        result.fail("opencode.json", "missing 'model' key")
        return
    result.ok(f"opencode.json — valid JSON, model={data['model']}")


def check_workflow(result: Result) -> None:
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        result.fail("workflow", "file missing")
        return
    text = path.read_text(encoding="utf-8")
    if "name:" not in text or "jobs:" not in text:
        result.fail("workflow", "not a valid workflow (missing name/jobs)")
        return
    if "OPENCODE_API_KEY" not in text:
        result.warn("workflow", "OPENCODE_API_KEY not referenced")
    result.ok("workflow — openscode.yml present")


def check_files_exist(result: Result) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            result.fail(f"required file", rel)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true", help="print extra detail")
    args = parser.parse_args()

    print("mehmet validation")
    print("=================")
    result = Result()

    check_files_exist(result)
    check_agents_md(result)
    check_changelog(result)
    check_personality(result)
    check_readme_license(result)
    check_opencode_json(result)
    check_workflow(result)

    if args.verbose:
        print(f"\nProject root: {ROOT}")
        print(f"Executable: {sys.executable}")

    return result.report()


if __name__ == "__main__":
    sys.exit(main())
