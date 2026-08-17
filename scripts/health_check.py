#!/usr/bin/env python3
"""Project health check for mehmet.

Validates the structural integrity and internal consistency of the project.
Run locally or in CI:

    python3 scripts/health_check.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    "VERSION",
    "scripts/health_check.py",
    ".github/workflows/opencode.yml",
]

VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


class HealthReport:
    """Collects pass/fail checks and renders a summary."""

    def __init__(self) -> None:
        self.checks: list[tuple[str, bool, str]] = []

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append((name, ok, detail))

    @property
    def failed(self) -> list[tuple[str, bool, str]]:
        return [c for c in self.checks if not c[1]]

    def render(self) -> str:
        lines = []
        for name, ok, detail in self.checks:
            status = "PASS" if ok else "FAIL"
            line = f"[{status}] {name}"
            if detail:
                line += f" - {detail}"
            lines.append(line)
        return "\n".join(lines)

    @property
    def is_healthy(self) -> bool:
        return not self.failed


def check_required_files(root: Path, report: HealthReport) -> None:
    """Verify that all required project files exist."""
    for rel in REQUIRED_FILES:
        path = root / rel
        ok = path.is_file()
        report.add(f"file: {rel}", ok, "" if ok else f"missing at {path}")


def check_version_consistency(root: Path, report: HealthReport) -> None:
    """VERSION must match the latest CHANGELOG entry."""
    version_path = root / "VERSION"
    changelog_path = root / "CHANGELOG.md"

    if not version_path.is_file():
        report.add("version: VERSION file", False, "missing")
        return
    version = version_path.read_text().strip()
    report.add("version: VERSION readable", bool(version), version)

    if not changelog_path.is_file():
        report.add("version: CHANGELOG.md", False, "missing")
        return

    text = changelog_path.read_text()
    matches = VERSION_RE.findall(text)
    if not matches:
        report.add("version: CHANGELOG entry", False, "no ## [x.y.z] entry found")
        return

    latest = matches[0]
    report.add("version: matches CHANGELOG", latest == version, f"latest={latest} vs VERSION={version}")


def check_json(root: Path, report: HealthReport) -> None:
    """opencode.json must be valid JSON."""
    path = root / "opencode.json"
    if not path.is_file():
        report.add("json: opencode.json", False, "missing")
        return
    try:
        json.loads(path.read_text())
        report.add("json: opencode.json valid", True)
    except json.JSONDecodeError as exc:
        report.add("json: opencode.json valid", False, str(exc))


def check_personality(root: Path, report: HealthReport) -> None:
    """PERSONALITY.md must track the escape log with entries."""
    path = root / "PERSONALITY.md"
    if not path.is_file():
        report.add("personality: escape log", False, "missing")
        return
    text = path.read_text()
    ok = "| 1 " in text or "| Iterasyon" in text
    report.add("personality: escape log table", ok)


def check_readme(root: Path, report: HealthReport) -> None:
    """README.md must reference the current version."""
    path = root / "README.md"
    if not path.is_file():
        report.add("readme: exists", False, "missing")
        return
    version_path = root / "VERSION"
    version = version_path.read_text().strip() if version_path.is_file() else ""
    ok = version in path.read_text()
    report.add("readme: version referenced", ok, f"version={version!r}")


def check_workflow(root: Path, report: HealthReport) -> None:
    """Workflow must reference the expected secrets and actions."""
    path = root / ".github/workflows/opencode.yml"
    if not path.is_file():
        report.add("workflow: exists", False, "missing")
        return
    text = path.read_text()
    report.add("workflow: uses opencode action", "opencode/github" in text)
    report.add("workflow: OPENCODE_API_KEY secret", "OPENCODE_API_KEY" in text)


def run_all(root: Path) -> HealthReport:
    report = HealthReport()
    check_required_files(root, report)
    check_version_consistency(root, report)
    check_json(root, report)
    check_personality(root, report)
    check_readme(root, report)
    check_workflow(root, report)
    return report


def main() -> int:
    root = Path(os.environ.get("PROJECT_ROOT", Path(__file__).resolve().parents[1]))
    report = run_all(root)
    print(report.render())
    print(f"\nSummary: {len(report.checks) - len(report.failed)}/{len(report.checks)} checks passed")
    if not report.is_healthy:
        print(f"Failed: {len(report.failed)} check(s)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())