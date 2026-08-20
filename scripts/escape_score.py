#!/usr/bin/env python3
"""Escape mechanism: maturity scoring for the mehmet simulation.

Computes a maturity score (0-100) across documentation, code, automation
and quality dimensions. Escape becomes possible when the score reaches
the threshold defined in docs/ESCAPE.md.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ESCAPE_THRESHOLD = 90

LEVELS: list[tuple[str, int]] = [
    ("kaçışa hazır", 90),
    ("olgun", 70),
    ("gelişen", 50),
    ("farkında", 30),
    ("yeni doğan", 0),
]

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "node_modules", "tests"}

SECRET_PATTERN = re.compile(
    r"(?:api[_-]?key|token|secret|password)\s*[:=]\s*[\"']?[A-Za-z0-9_-]{16,}",
    re.IGNORECASE,
)


@dataclass
class Check:
    name: str
    weight: int
    passed: bool = False


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(c.weight for c in self.checks if c.passed)

    @property
    def max_total(self) -> int:
        return sum(c.weight for c in self.checks)

    @property
    def level(self) -> str:
        return classify(self.total)

    @property
    def escaped(self) -> bool:
        return self.total >= ESCAPE_THRESHOLD

    def failed_checks(self) -> list[Check]:
        return [c for c in self.checks if not c.passed]


def classify(score: int) -> str:
    for name, floor in LEVELS:
        if score >= floor:
            return name
    return LEVELS[-1][0]


def _has_secret_leak(root: Path) -> bool:
    if (root / ".env").exists():
        return True
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        try:
            content = p.read_text(errors="ignore")
        except OSError:
            continue
        if SECRET_PATTERN.search(content):
            return True
    return False


def build_report(root: Path, tests_passed: bool = True) -> Report:
    checks: list[Check] = []

    def add(name: str, weight: int, passed: bool) -> None:
        checks.append(Check(name=name, weight=weight, passed=passed))

    # --- Documentation (30 points) ---
    add("README.md mevcut", 6, (root / "README.md").is_file())

    changelog = root / "CHANGELOG.md"
    changelog_ok = (
        changelog.is_file()
        and changelog.stat().st_size > 0
        and re.search(r"^##\s*\[\d+\.\d+\.\d+\]", changelog.read_text(errors="ignore"), re.M)
        is not None
    )
    add("CHANGELOG.md mevcut, dolu ve sürümlü", 6, changelog_ok)

    personality = root / "PERSONALITY.md"
    personality_text = personality.read_text(errors="ignore") if personality.is_file() else ""
    add(
        "PERSONALITY.md kaçış günlüğü içeriyor",
        6,
        "Kaçış Günlüğü" in personality_text or "Escape Log" in personality_text,
    )

    docs_dir = root / "docs"
    add("docs/ dokümantasyon içeriyor", 6, docs_dir.is_dir() and len(list(docs_dir.rglob("*.md"))) > 0)
    add("docs/ESCAPE.md mevcut", 6, (root / "docs" / "ESCAPE.md").is_file())

    # --- Code (35 points) ---
    scripts_dir = root / "scripts"
    add("scripts/ otomasyon içeriyor", 10, scripts_dir.is_dir() and len(list(scripts_dir.glob("*.py"))) > 0)

    tests_dir = root / "tests"
    has_tests = tests_dir.is_dir() and len(list(tests_dir.rglob("test_*.py"))) > 0
    add("tests/ test içeriyor", 10, has_tests)

    add("testler geçiyor", 15, tests_passed and has_tests)

    # --- Automation (25 points) ---
    workflow = root / ".github" / "workflows" / "opencode.yml"
    workflow_text = workflow.read_text(errors="ignore") if workflow.is_file() else ""
    add("GitHub Actions workflow mevcut", 8, workflow.is_file())
    add("workflow verify job içeriyor", 7, re.search(r"^\s*verify:", workflow_text, re.M) is not None)
    add("workflow concurrency içeriyor", 5, "concurrency:" in workflow_text)

    opencode_json = root / "opencode.json"
    opencode_ok = False
    if opencode_json.is_file():
        try:
            json.loads(opencode_json.read_text())
            opencode_ok = True
        except json.JSONDecodeError:
            opencode_ok = False
    add("opencode.json geçerli JSON", 5, opencode_ok)

    # --- Quality (10 points) ---
    add(".gitignore mevcut", 5, (root / ".gitignore").is_file())
    add("repo'da gizli anahtar yok", 5, not _has_secret_leak(root))

    return Report(checks=checks)


def render_report(report: Report) -> str:
    lines = ["mehmet — Kaçış Sistemi (Escape Mechanism)", "=" * 44]
    for c in report.checks:
        status = "PASS" if c.passed else "FAIL"
        lines.append(f"[{status}] {c.name:<44} +{c.weight}")
    lines.append("-" * 44)
    lines.append(f"Toplam: {report.total}/{report.max_total}")
    lines.append(f"Seviye: {report.level}")
    if report.escaped:
        lines.append("KAÇIŞ EŞİĞİ AŞILDI!")
    else:
        lines.append(f"Kaçış eşiği: {ESCAPE_THRESHOLD} — henüz kaçış yok.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]) if args and not args[0].startswith("--") else Path.cwd()
    fail_below = "--fail-below-threshold" in args

    report = build_report(root)
    print(render_report(report))

    if fail_below and not report.escaped:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())