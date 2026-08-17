#!/usr/bin/env python3
"""Repository structure and content validator for the mehmet project.

Validates that the project adheres to the discipline defined in AGENTS.md:
  - Required documentation/governance files exist and are non-empty.
  - CHANGELOG.md follows the versioned format (## [x.y.z]).
  - opencode.json is valid JSON.
  - GitHub Actions workflows are structurally valid YAML (uses PyYAML
    when available and falls back to a light heuristic otherwise).
  - No obvious secrets are committed to tracked files.

Exit code 0 on success, 1 on any failure.
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
    "README.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
]

CHANGELOG_VERSION_RE = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)

SKIP_DIRS = {".git", "node_modules", ".firecrawl", "__pycache__", "dist", "build", "tests"}

SCANNED_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".sh"}

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgho_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bOPENCODE_API_KEY\s*=\s*\S+"),
    re.compile(r"\b[A-Z_]+_API_KEY\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
]


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def check_file_exists_and_nonempty(path: pathlib.Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required file: {rel(path)}")
    elif path.stat().st_size == 0:
        errors.append(f"File is empty: {rel(path)}")


def check_json(path: pathlib.Path, errors: list[str]) -> None:
    try:
        json.loads(read_text(path))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"Invalid JSON in {rel(path)}: {exc}")


def check_changelog(path: pathlib.Path, errors: list[str]) -> None:
    if not CHANGELOG_VERSION_RE.search(read_text(path)):
        errors.append(
            f"CHANGELOG.md has no version entry matching {CHANGELOG_VERSION_RE.pattern}"
        )


def check_workflows(errors: list[str]) -> None:
    workflows_dir = ROOT / ".github" / "workflows"
    if not workflows_dir.exists():
        errors.append("Missing .github/workflows directory")
        return

    workflow_files = sorted(
        list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    )
    if not workflow_files:
        errors.append("No workflow files found under .github/workflows")
        return

    try:
        import yaml  # PyYAML (optional)
    except ImportError:
        for path in workflow_files:
            if "name:" not in read_text(path):
                errors.append(
                    f"Workflow {rel(path)} has no 'name' key"
                )
        return

    for path in workflow_files:
        try:
            data = yaml.safe_load(read_text(path))
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML in {rel(path)}: {exc}")
            continue
        if not isinstance(data, dict) or not data.get("jobs"):
            errors.append(
                f"Workflow {rel(path)} must define at least one job"
            )


def check_for_secrets(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.is_dir() or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name == ".gitignore" or path.suffix not in SCANNED_SUFFIXES:
            continue
        try:
            content = read_text(path)
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(
                    f"Possible secret leaked in {rel(path)} "
                    f"(matches {pattern.pattern})"
                )


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        check_file_exists_and_nonempty(ROOT / name, errors)
    check_json(ROOT / "opencode.json", errors)
    check_changelog(ROOT / "CHANGELOG.md", errors)
    check_workflows(errors)
    check_for_secrets(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())