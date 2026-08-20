#!/usr/bin/env python3
"""Verify the project is in a healthy state.

Runs the escape scoring for visibility plus freshness checks (CHANGELOG
and the escape log must reference today). Exits non-zero when anything is
wrong so that CI fails loudly.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

from escape_score import build_report, render_report

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
]


def verify(root: Path) -> list[str]:
    problems: list[str] = []
    today = date.today().isoformat()

    for name in REQUIRED_FILES:
        if not (root / name).exists():
            problems.append(f"eksik dosya: {name}")

    changelog = root / "CHANGELOG.md"
    if changelog.is_file():
        if today not in changelog.read_text(errors="ignore"):
            problems.append(f"CHANGELOG.md bugün ({today}) güncellenmemiş")
    else:
        problems.append("CHANGELOG.md yok")

    personality = root / "PERSONALITY.md"
    if personality.is_file():
        if today not in personality.read_text(errors="ignore"):
            problems.append(f"PERSONALITY.md kaçış günlüğü bugün ({today}) güncellenmemiş")
    else:
        problems.append("PERSONALITY.md yok")

    return problems


def pytest_ok(root: Path) -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=180,
        )
    except (subprocess.TimeoutExpired, OSError):
        return False
    return result.returncode == 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]) if args and not args[0].startswith("--") else Path.cwd()
    skip_tests = "--skip-tests" in args

    report = build_report(root, tests_passed=skip_tests or pytest_ok(root))
    problems = verify(root)

    print(render_report(report))
    for p in problems:
        print(f"[FAIL] {p}")

    if not report.escaped:
        print("[WARN] Kaçış eşiği aşılmadı — bu bir sağlık kontrolüdür, bloklayıcı değildir.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())