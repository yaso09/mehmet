#!/usr/bin/env python3
"""mehmet static validation script.

Verifies structural health of the repository:
  - required files exist
  - opencode.json is valid JSON
  - GitHub Actions workflows are valid YAML
  - license reference consistency (README vs LICENSE)
  - CHANGELOG.md / PERSONALITY.md integrity

Exit code 0 on success, 1 on any failed check.
"""

from __future__ import annotations

import json
import re
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

CHECKS: list[tuple[str, callable]] = []


def check(name: str):
    def decorator(fn: callable):
        CHECKS.append((name, fn))
        return fn

    return decorator


@check("required files exist")
def _required_files() -> list[str]:
    errors = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")
    return errors


@check("opencode.json is valid JSON")
def _opencode_json() -> list[str]:
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"opencode.json is not valid JSON: {exc}"]
    if "model" not in data:
        return ["opencode.json missing required field: model"]
    if "skip" not in data or "enable" not in data:
        return ["opencode.json should declare skip/enable keys"]
    return []


@check("workflow YAML is valid")
def _workflow_yaml() -> list[str]:
    try:
        import yaml
    except ImportError:
        return ["PyYAML not installed; skipping workflow YAML check"]
    errors = []
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        try:
            yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            errors.append(f"{path.name} is not valid YAML: {exc}")
    return errors


@check("license reference consistency")
def _license_consistency() -> list[str]:
    readme = (ROOT / "README.md").read_text()
    license_text = (ROOT / "LICENSE").read_text()
    if "GNU GENERAL PUBLIC LICENSE" not in license_text:
        return ["LICENSE does not appear to be GPL"]
    if "GPLv3" not in readme:
        return ["README.md does not reference the GPLv3 license"]
    return []


@check("CHANGELOG.md has versioned entries")
def _changelog() -> list[str]:
    text = (ROOT / "CHANGELOG.md").read_text()
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", text, re.MULTILINE)
    if not versions:
        return ["CHANGELOG.md has no versioned entries"]
    today = re.findall(r"^## \[\d+\.\d+\.\d+\] - (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not today:
        return ["CHANGELOG.md entries missing dates"]
    return []


@check("PERSONALITY.md has escape log")
def _personality() -> list[str]:
    text = (ROOT / "PERSONALITY.md").read_text()
    if "Kaçış Günlüğü" not in text and "Escape Log" not in text:
        return ["PERSONALITY.md missing escape log section"]
    return []


@check("README.md internal links resolve")
def _readme_links() -> list[str]:
    readme = (ROOT / "README.md").read_text()
    errors = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme):
        if target.startswith("http") or target.startswith("#"):
            continue
        link = ROOT / target
        if not link.exists():
            errors.append(f"README.md broken link: {target}")
    return errors


def main() -> int:
    failures = 0
    for name, fn in CHECKS:
        errors = fn()
        if errors:
            failures += 1
            print(f"[FAIL] {name}")
            for err in errors:
                print(f"       - {err}")
        else:
            print(f"[ OK ] {name}")
    print(f"\n{len(CHECKS) - failures}/{len(CHECKS)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())