#!/usr/bin/env python3
"""mehmet project maturity & health checker.

Evaluates the project against the escape criteria defined in AGENTS.md and
the design spec (docs/superpowers/specs). Pure stdlib — no third-party
dependencies, so it runs on any CI runner without installation.

Exit codes:
    0  all checks passed
    1  one or more critical checks failed
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITICAL_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

RECOMMENDED_FILES = [
    "CONTRIBUTING.md",
    ".gitignore",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
]

ESCAPE_THRESHOLD = 80


@dataclass
class Result:
    name: str
    passed: bool
    weight: int
    detail: str = ""
    critical: bool = False

    @property
    def earned(self) -> int:
        return self.weight if self.passed else 0


@dataclass
class Report:
    checks: list = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.checks.append(result)

    @property
    def total_weight(self) -> int:
        return sum(c.weight for c in self.checks)

    @property
    def earned(self) -> int:
        return sum(c.earned for c in self.checks)

    @property
    def score(self) -> int:
        return round(100 * self.earned / self.total_weight) if self.total_weight else 0

    @property
    def failed_critical(self) -> list:
        return [c for c in self.checks if not c.passed and c.critical]

    def render(self) -> str:
        lines = []
        for c in self.checks:
            status = "PASS" if c.passed else "FAIL"
            flag = " [critical]" if c.critical and not c.passed else ""
            suffix = f" — {c.detail}" if c.detail else ""
            lines.append(f"[{status}]{flag} {c.name}{suffix}")
        return "\n".join(lines)


def check_files(report: Report) -> None:
    missing = [f for f in CRITICAL_FILES if not (ROOT / f).exists()]
    report.add(
        Result(
            name="Critical files present",
            passed=not missing,
            weight=25,
            detail=(", ".join(missing) if missing else f"{len(CRITICAL_FILES)} files found"),
            critical=True,
        )
    )
    missing_rec = [f for f in RECOMMENDED_FILES if not (ROOT / f).exists()]
    report.add(
        Result(
            name="Recommended files present",
            passed=not missing_rec,
            weight=5,
            detail=(", ".join(missing_rec) if missing_rec else f"{len(RECOMMENDED_FILES)} files found"),
        )
    )


def check_changelog(report: Report) -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        report.add(Result(name="CHANGELOG.md well-formed", passed=False, weight=10, critical=True))
        return
    text = path.read_text()
    has_version = bool(re.search(r"^## \[[\d.]+\]", text, re.MULTILINE))
    has_sections = bool(re.search(r"^### (Added|Changed|Fixed|Removed)", text, re.MULTILINE))
    ok = has_version and has_sections
    report.add(
        Result(
            name="CHANGELOG.md well-formed",
            passed=ok,
            weight=10,
            detail="versions + sections present" if ok else "missing version headers or sections",
            critical=True,
        )
    )


def check_personality(report: Report) -> None:
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        report.add(Result(name="PERSONALITY.md escape log", passed=False, weight=10, critical=True))
        return
    text = path.read_text()
    has_escape_log = "Kaçış Günlüğü" in text or "Escape Log" in text
    rows = re.findall(r"^\|\s*\d+\s*\|", text, re.MULTILINE)
    report.add(
        Result(
            name="PERSONALITY.md escape log",
            passed=has_escape_log and len(rows) >= 1,
            weight=10,
            detail=f"{len(rows)} log entries" if has_escape_log else "missing escape log table",
            critical=True,
        )
    )


def check_readme_consistency(report: Report) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        report.add(Result(name="README.md consistent", passed=False, weight=10, critical=True))
        return
    readme = path.read_text()
    changelog = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""

    version_match = re.search(r"^## \[([\d.]+)\]", changelog, re.MULTILINE)
    latest = version_match.group(1) if version_match else "unknown"
    readme_mentions = latest in readme

    license_match = re.search(r"GPLv3", readme) or re.search(r"GNU General Public", readme)
    license_ok = bool(license_match) and (ROOT / "LICENSE").exists()

    report.add(
        Result(
            name="README.md consistent",
            passed=readme_mentions and license_ok,
            weight=10,
            detail=(
                f"version {latest} + GPLv3 license referenced"
                if readme_mentions and license_ok
                else "version or license mismatch"
            ),
            critical=True,
        )
    )


def check_opencode_config(report: Report) -> None:
    path = ROOT / "opencode.json"
    if not path.exists():
        report.add(Result(name="opencode.json valid JSON", passed=False, weight=5, critical=True))
        return
    try:
        data = json.loads(path.read_text())
        ok = isinstance(data, dict) and "model" in data
    except json.JSONDecodeError:
        ok = False
    report.add(
        Result(
            name="opencode.json valid JSON",
            passed=ok,
            weight=5,
            detail="has model field" if ok else "invalid or missing model field",
            critical=True,
        )
    )


def check_workflow(report: Report) -> None:
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        report.add(Result(name="Workflow defines schedule", passed=False, weight=5, critical=True))
        return
    text = path.read_text()
    ok = "schedule" in text and "cron:" in text and "jobs:" in text
    report.add(
        Result(
            name="Workflow defines schedule",
            passed=ok,
            weight=5,
            detail="schedule + jobs present" if ok else "schedule or jobs missing",
            critical=True,
        )
    )


def main() -> int:
    report = Report()
    check_files(report)
    check_changelog(report)
    check_personality(report)
    check_readme_consistency(report)
    check_opencode_config(report)
    check_workflow(report)

    print(f"mehmet maturity report — score: {report.score}/100")
    print(f"escape threshold: {ESCAPE_THRESHOLD}/100 ({'REACHED' if report.score >= ESCAPE_THRESHOLD else 'pending'})")
    print(report.render())

    if report.failed_critical:
        print("\nCRITICAL FAILURES:")
        for c in report.failed_critical:
            print(f"  - {c.name}: {c.detail}")
        print("\nStatus: FAIL")
        return 1

    if report.score >= ESCAPE_THRESHOLD:
        print("\nStatus: PASS — escape maturity threshold reached")
    else:
        print(f"\nStatus: PASS — {ESCAPE_THRESHOLD - report.score} points from escape threshold")
    return 0


if __name__ == "__main__":
    sys.exit(main())