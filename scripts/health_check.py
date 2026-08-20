#!/usr/bin/env python3
"""mehmet health check.

Self-assessment tool that validates repository integrity and tracks
maturity toward the escape goal. Exits non-zero if any check fails.

Checks:
  1. Required files exist
  2. opencode.json is valid JSON and contains required keys
  3. Workflow YAML files parse and contain expected keys
  4. VERSION file exists and is semver-compatible
  5. CHANGELOG.md contains a section for the current VERSION
  6. README.md references the current VERSION
  7. PERSONALITY.md contains a well-formed escape log with no gaps
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES: List[str] = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "VERSION",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

REQUIRED_OPECODE_KEYS: List[str] = ["model"]

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

ESCAPE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(\S+)\s*\|\s*(.+?)\s*\|$")


def check_required_files(root: Path) -> List[str]:
    errors: List[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    return errors


def check_opencode_json(root: Path) -> List[str]:
    errors: List[str] = []
    path = root / "opencode.json"
    if not path.is_file():
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"opencode.json is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"opencode.json must contain a JSON object, got {type(data).__name__}"]
    for key in REQUIRED_OPECODE_KEYS:
        if key not in data:
            errors.append(f"opencode.json is missing required key: {key}")
    return errors


def _load_yaml(text: str) -> object:
    import yaml

    return yaml.safe_load(text)


def check_workflows(root: Path) -> List[str]:
    errors: List[str] = []
    workflows = sorted((root / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        return ["No workflow files found in .github/workflows"]
    try:
        import yaml
    except ImportError:
        return errors
    for path in workflows:
        try:
            data = _load_yaml(path.read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError) as exc:
            errors.append(f"{path.name} is not valid YAML: {exc}")
            continue
        if not isinstance(data, dict) or "jobs" not in data:
            errors.append(f"{path.name} must contain a 'jobs' key")
    return errors


def check_version(root: Path) -> List[str]:
    errors: List[str] = []
    path = root / "VERSION"
    if not path.is_file():
        return ["Missing required file: VERSION"]
    version = path.read_text(encoding="utf-8").strip()
    if not SEMVER_RE.match(version):
        errors.append(f"VERSION is not semver-compatible: {version!r}")
    return errors


def read_version(root: Path) -> str:
    path = root / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def check_changelog(root: Path) -> List[str]:
    errors: List[str] = []
    version = read_version(root)
    if not version:
        return ["Cannot validate CHANGELOG without a VERSION file"]
    path = root / "CHANGELOG.md"
    if not path.is_file():
        return ["Missing required file: CHANGELOG.md"]
    section = f"## [{version}]"
    if section not in path.read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG.md has no section for current version {version}")
    return errors


def check_readme(root: Path) -> List[str]:
    errors: List[str] = []
    version = read_version(root)
    if not version:
        return ["Cannot validate README without a VERSION file"]
    path = root / "README.md"
    if not path.is_file():
        return ["Missing required file: README.md"]
    if version not in path.read_text(encoding="utf-8"):
        errors.append(f"README.md does not reference current version {version}")
    return errors


def parse_escape_log(root: Path) -> List[str]:
    path = root / "PERSONALITY.md"
    if not path.is_file():
        return []
    rows: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ESCAPE_ROW_RE.match(line.strip())
        if match:
            rows.append(line.strip())
    return rows


def check_escape_log(root: Path) -> List[str]:
    errors: List[str] = []
    rows = parse_escape_log(root)
    if not rows:
        return ["PERSONALITY.md escape log is empty or missing"]
    numbers: List[int] = []
    for row in rows:
        match = ESCAPE_ROW_RE.match(row)
        if match is None:
            continue
        numbers.append(int(match.group(1)))
        if not match.group(3).strip():
            errors.append(f"Escape log row has no progress description: {row}")
    expected = list(range(1, len(rows) + 1))
    if numbers != expected:
        errors.append(
            f"Escape log iteration numbers have gaps: got {numbers}, expected {expected}"
        )
    return errors


def run_all(root: Path) -> List[str]:
    errors: List[str] = []
    checks: Iterable[List[str]] = (
        check_required_files(root),
        check_opencode_json(root),
        check_workflows(root),
        check_version(root),
        check_changelog(root),
        check_readme(root),
        check_escape_log(root),
    )
    for result in checks:
        errors.extend(result)
    return errors


def main(argv: List[str]) -> int:
    root = Path(argv[0]).resolve() if argv else ROOT
    errors = run_all(root)
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        print(f"\n{len(errors)} health check(s) failed.", file=sys.stderr)
        return 1
    print(f"OK: all health checks passed for {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))