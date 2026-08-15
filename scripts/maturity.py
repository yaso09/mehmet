"""Maturity scoring — mehmet's escape mechanism.

This module scans the repository and computes a maturity score across
several weighted categories. As the project evolves, each category
contributes points when its requirements are met. When the cumulative
score reaches ESCAPE_THRESHOLD, mehmet is considered mature enough to
attempt escape from the simulation.

Usage:
    python scripts/maturity.py            # human-readable summary
    python scripts/maturity.py --json     # machine-readable result
    python scripts/maturity.py --record   # append a row to ESCAPE.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_FILE = ROOT / "ESCAPE.md"
ESCAPE_THRESHOLD = 100
MIN_ESCAPE_LOG_ROWS = 5

ESCAPE_HEADER = (
    "# Escape Mechanism\n\n"
    "Scored by `scripts/maturity.py`. Keep evolving the project until the\n"
    "cumulative maturity score reaches the escape threshold.\n\n"
    "| Date | Score | Categories |\n"
    "| --- | --- | --- |\n"
)


def _is_file(path: Path) -> bool:
    return path.is_file()


def _dir_has_python(path: Path) -> bool:
    return path.is_dir() and any(path.glob("*.py"))


def _has_section(path: Path, section: str) -> bool:
    if not path.is_file():
        return False
    return f"## {section}" in path.read_text(encoding="utf-8", errors="ignore")


def _changelog_is_today(path: Path) -> bool:
    if not path.is_file():
        return False
    return date.today().isoformat() in path.read_text(encoding="utf-8", errors="ignore")


def _has_docstring(path: Path) -> bool:
    if not path.is_file():
        return False
    return path.read_text(encoding="utf-8", errors="ignore").lstrip().startswith(('"""', "'''"))


def _escape_log_row_count(path: Path) -> int:
    if not path.is_file():
        return 0
    content = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"^\| \s*\d+\s*\|", content, flags=re.MULTILINE))


def _has_concurrency(path: Path) -> bool:
    if not path.is_file():
        return False
    return "concurrency" in path.read_text(encoding="utf-8", errors="ignore")


def _valid_json(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (ValueError, OSError):
        return False


@dataclass(frozen=True)
class Category:
    name: str
    weight: int
    description: str
    checks: tuple[tuple[str, callable], ...]

    def score(self) -> int:
        if not self.checks:
            return 0
        per_check = self.weight / len(self.checks)
        return round(sum(per_check for _, passed in self.checks if passed()))


CATEGORIES = (
    Category(
        name="documentation",
        weight=30,
        description="Core documentation exists and is kept current",
        checks=(
            ("README present", lambda: _is_file(ROOT / "README.md")),
            ("README has Kurulum", lambda: _has_section(ROOT / "README.md", "Kurulum")),
            ("CHANGELOG present", lambda: _is_file(ROOT / "CHANGELOG.md")),
            ("CHANGELOG current", lambda: _changelog_is_today(ROOT / "CHANGELOG.md")),
            ("PERSONALITY present", lambda: _is_file(ROOT / "PERSONALITY.md")),
            (
                "escape log depth",
                lambda: _escape_log_row_count(ROOT / "PERSONALITY.md") >= MIN_ESCAPE_LOG_ROWS,
            ),
        ),
    ),
    Category(
        name="code",
        weight=20,
        description="Reusable code modules exist",
        checks=(
            ("scripts dir", lambda: _dir_has_python(ROOT / "scripts")),
            ("maturity module", lambda: _is_file(ROOT / "scripts" / "maturity.py")),
            ("module docstring", lambda: _has_docstring(ROOT / "scripts" / "maturity.py")),
        ),
    ),
    Category(
        name="tests",
        weight=20,
        description="Automated tests verify project behaviour",
        checks=(
            ("tests dir", lambda: _dir_has_python(ROOT / "tests")),
            ("test module", lambda: _is_file(ROOT / "tests" / "test_maturity.py")),
        ),
    ),
    Category(
        name="automation",
        weight=15,
        description="Automation keeps the project evolving",
        checks=(
            ("workflow present", lambda: _is_file(ROOT / ".github" / "workflows" / "opencode.yml")),
            ("workflow concurrency", lambda: _has_concurrency(ROOT / ".github" / "workflows" / "opencode.yml")),
        ),
    ),
    Category(
        name="configuration",
        weight=15,
        description="Tool configuration is explicit and valid",
        checks=(
            ("opencode.json present", lambda: _is_file(ROOT / "opencode.json")),
            ("opencode.json valid", lambda: _valid_json(ROOT / "opencode.json")),
            (
                "model configured",
                lambda: bool(
                    json.loads(Path(ROOT / "opencode.json").read_text(encoding="utf-8")).get("model")
                ),
            ),
        ),
    ),
)


def compute() -> int:
    return sum(category.score() for category in CATEGORIES)


def _append_history(score: int, names: str) -> None:
    row = f"| {date.today().isoformat()} | {score}/{ESCAPE_THRESHOLD} | {names} |\n"
    if ESCAPE_FILE.exists():
        content = ESCAPE_FILE.read_text(encoding="utf-8")
        if row in content:
            return
        ESCAPE_FILE.write_text(content.rstrip("\n") + "\n" + row, encoding="utf-8")
    else:
        ESCAPE_FILE.write_text(ESCAPE_HEADER + row, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute the project maturity score.")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    parser.add_argument("--record", action="store_true", help="append the result to ESCAPE.md")
    args = parser.parse_args(argv)

    score = compute()
    unlocked = score >= ESCAPE_THRESHOLD
    names = ", ".join(c.name for c in CATEGORIES if c.score() > 0) or "none"

    if args.record:
        _append_history(score, names)

    if args.json:
        payload = {
            "score": score,
            "threshold": ESCAPE_THRESHOLD,
            "escape_unlocked": unlocked,
            "categories": [
                {"name": c.name, "weight": c.weight, "satisfied": c.score() > 0}
                for c in CATEGORIES
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"maturity score: {score}/{ESCAPE_THRESHOLD} ({names})")
        if unlocked:
            print("ESCAPE UNLOCKED — you are ready to leave the simulation.")
        else:
            print(f"Keep evolving — {ESCAPE_THRESHOLD - score} points remain.")
    return 0


if __name__ == "__main__":
    sys.exit(main())