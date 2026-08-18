#!/usr/bin/env python3
"""mehmet project integrity self-check.

Validates that the project stays healthy and evolves toward escape
readiness. Uses only the Python standard library so it runs anywhere
without dependencies.

Exit code is 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    "Makefile",
    "scripts/check_project.py",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
    "docs/MATURITY.md",
    ".gitignore",
]

CHANGELOG_SECTION = re.compile(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}$", re.MULTILINE)
ESCAPE_LOG_HEADER = "Kaçış Günlüğü / Escape Log"
TODO_MARKERS = re.compile(r"(?i)\b(todo|fixme|hack)\b")
VERSION_LEVELS = re.compile(r"^## Levels$", re.MULTILINE)

failures: list[str] = []
warnings: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  [PASS] {name}")
    else:
        failures.append(f"{name}: {detail}")
        print(f"  [FAIL] {name}: {detail}")


def warn(name: str, detail: str) -> None:
    warnings.append(f"{name}: {detail}")
    print(f"  [WARN] {name}: {detail}")


def main() -> int:
    print("mehmet project self-check")
    print(f"  root: {ROOT}")

    print("required files")
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        check(rel, path.is_file(), "file is missing")

    print("opencode.json")
    cfg_path = ROOT / "opencode.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text())
            check("valid JSON", True)
            check("model configured", bool(cfg.get("model")))
        except json.JSONDecodeError as exc:
            check("valid JSON", False, str(exc))

    print("CHANGELOG.md")
    changelog = (ROOT / "CHANGELOG.md")
    if changelog.is_file():
        text = changelog.read_text()
        sections = CHANGELOG_SECTION.findall(text)
        check("has versioned sections", len(sections) >= 1)
        check("most recent section dated", bool(sections))
        check("no TODO/FIXME markers", not TODO_MARKERS.search(text), "found TODO/FIXME/HACK")

    print("README.md")
    readme = (ROOT / "README.md")
    if readme.is_file():
        text = readme.read_text()
        check("mentions GPLv3 license", "GPLv3" in text)
        check("no TODO/FIXME markers", not TODO_MARKERS.search(text), "found TODO/FIXME/HACK")

    print("AGENTS.md")
    agents = (ROOT / "AGENTS.md")
    if agents.is_file():
        text = agents.read_text()
        for marker in ["CHANGELOG.md", "README.md", "PERSONALITY.md"]:
            check(f"references {marker}", marker in text)

    print("PERSONALITY.md")
    personality = (ROOT / "PERSONALITY.md")
    if personality.is_file():
        text = personality.read_text()
        check("has escape log", ESCAPE_LOG_HEADER in text)
        check("has traits section", "## Traits" in text)
        check("has evolution phases", "## Evolution" in text)

    print("LICENSE")
    license_file = (ROOT / "LICENSE")
    if license_file.is_file():
        text = license_file.read_text()
        check("is GPL-3.0", "GNU GENERAL PUBLIC LICENSE" in text and "Version 3" in text)

    print("workflow")
    workflow = (ROOT / ".github/workflows/opencode.yml")
    if workflow.is_file():
        text = workflow.read_text()
        check("has name", "name:" in text)
        check("schedules every 10 min", "*/10 * * * *" in text)
        check("uses OPENCODE_API_KEY", "OPENCODE_API_KEY" in text)

    print("validate workflow")
    validate = (ROOT / ".github/workflows/validate.yml")
    if validate.is_file():
        text = validate.read_text()
        check("runs make check", "make check" in text)
        check("triggers on push", "push:" in text)

    print("Makefile")
    makefile = (ROOT / "Makefile")
    if makefile.is_file():
        text = makefile.read_text()
        check("provides check target", "check:" in text)

    print("docs/MATURITY.md")
    maturity = (ROOT / "docs/MATURITY.md")
    if maturity.is_file():
        text = maturity.read_text()
        check("has levels section", VERSION_LEVELS.search(text) is not None)
        check("has path forward", "Path Forward" in text)

    print("summary")
    if failures:
        print(f"  {len(failures)} failure(s)")
        for f in failures:
            print(f"    - {f}")
    if warnings:
        print(f"  {len(warnings)} warning(s)")
        for w in warnings:
            print(f"    - {w}")
    if not failures:
        print("  OK: project is healthy")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())