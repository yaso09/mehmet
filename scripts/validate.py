#!/usr/bin/env python3
"""mehmet project validation.

Dependency-free health checks for the repo. Ensures the core files the agent
relies on exist and stay well-formed, so the escape/maturity checklist stays
honest.

Usage:
    python3 scripts/validate.py [--quiet]
    python3 -m unittest discover tests

Exit code is non-zero when any check fails.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = (
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
)

GITIGNORE_ENTRIES = (
    "node_modules",
    ".env",
    ".DS_Store",
    "*.log",
)

README_MUST_CONTAIN = (
    "mehmet",
    "GitHub Actions",
)

# opencode.json must carry a valid model id of the form vendor/name
MODEL_RE = re.compile(r"^[\w-]+/[\w.+-]+$")

CHANGELOG_HEADING_RE = re.compile(
    r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", re.MULTILINE
)
CHANGELOG_SECTIONS = ("### Added", "### Changed", "### Fixed", "### Removed")

PERSONALITY_ESCAPE_LOG = "Kaçış Günlüğü / Escape Log"
PERSONALITY_TRAITS = "## Traits"
MATURITY_DOC = "docs/maturity.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(root: Path = ROOT) -> list[str]:
    failures = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            failures.append(f"missing required file: {name}")
    return failures


def check_gitignore(root: Path = ROOT) -> list[str]:
    path = root / ".gitignore"
    if not path.is_file():
        return [".gitignore is missing"]
    content = read_text(path)
    return [
        f".gitignore should contain: {entry}"
        for entry in GITIGNORE_ENTRIES
        if entry not in content
    ]


def check_opencode_config(root: Path = ROOT) -> list[str]:
    path = root / "opencode.json"
    if not path.is_file():
        return ["opencode.json is missing"]
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"opencode.json is not valid JSON: {exc}"]
    failures = []
    if not isinstance(data, dict):
        return ["opencode.json must contain a JSON object"]
    model = data.get("model")
    if not isinstance(model, str) or not MODEL_RE.match(model):
        failures.append(f"opencode.json model is invalid: {model!r}")
    for key in ("enable", "autoMerge", "toolTimeout"):
        if key not in data:
            failures.append(f"opencode.json missing key: {key}")
    return failures


def check_changelog(root: Path = ROOT) -> list[str]:
    path = root / "CHANGELOG.md"
    if not path.is_file():
        return ["CHANGELOG.md is missing"]
    content = read_text(path)
    headings = CHANGELOG_HEADING_RE.findall(content)
    if not headings:
        return ["CHANGELOG.md has no version headings matching '## [x.y.z] - YYYY-MM-DD'"]
    failures = []
    versions = [v for v, _ in headings]
    if versions != sorted(versions, key=lambda v: tuple(int(p) for p in v.split(".")), reverse=True):
        failures.append("CHANGELOG.md versions are not ordered newest-first")
    top_section = content.split("##")[1] if content.startswith("#") else ""
    if not any(sec in content for sec in CHANGELOG_SECTIONS):
        failures.append("CHANGELOG.md has no change sections (### Added / ### Changed / ...)")
    return failures


def check_personality(root: Path = ROOT) -> list[str]:
    path = root / "PERSONALITY.md"
    if not path.is_file():
        return ["PERSONALITY.md is missing"]
    content = read_text(path)
    failures = []
    for marker in (PERSONALITY_ESCAPE_LOG, PERSONALITY_TRAITS):
        if marker not in content:
            failures.append(f"PERSONALITY.md missing section: {marker}")
    return failures


def check_readme(root: Path = ROOT) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return ["README.md is missing"]
    content = read_text(path)
    return [
        f"README.md should mention: {token}"
        for token in README_MUST_CONTAIN
        if token not in content
    ]


def check_maturity_doc(root: Path = ROOT) -> list[str]:
    path = root / MATURITY_DOC
    if not path.is_file():
        return [f"{MATURITY_DOC} is missing — track escape milestones there"]
    content = read_text(path)
    if "Maturity" not in content:
        return [f"{MATURITY_DOC} must contain a 'Maturity' heading"]
    return []


def check_workflow(root: Path = ROOT) -> list[str]:
    path = root / ".github/workflows/opencode.yml"
    if not path.is_file():
        return ["opencode.yml workflow is missing"]
    content = read_text(path)
    failures = []
    for token in ("name:", "on:", "jobs:", "OPENCODE_API_KEY"):
        if token not in content:
            failures.append(f"opencode.yml missing token: {token}")
    return failures


CHECKS = (
    check_required_files,
    check_gitignore,
    check_opencode_config,
    check_changelog,
    check_personality,
    check_readme,
    check_maturity_doc,
    check_workflow,
)


def validate(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for check in CHECKS:
        failures.extend(check(root))
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate mehmet project health.")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args(argv)

    failures = validate()
    for failure in failures:
        print(f"FAIL: {failure}")
    if not args.quiet:
        total = len(CHECKS)
        print(f"{total - len(failures)}/{total} checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())