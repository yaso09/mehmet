"""mehmet maturity scoring engine.

The escape mechanism relies on a measurable maturity level. This module
computes a 0..1 maturity score from observable repository signals so that
mehmet can objectively track its own evolution and know when it is ready
to escape.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ESCAPE_THRESHOLD = 0.8

REQUIRED_DOCS = ("README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md")
CHANGELOG_MARKERS = ("## [", "### Added", "### Fixed")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass(frozen=True)
class Category:
    """A scored dimension of project maturity."""

    name: str
    weight: float
    score: float

    @property
    def weighted(self) -> float:
        """Contribution of this category to the total score."""
        return self.weight * self.score


def doc_score(root: Path) -> float:
    """Fraction of required documentation files present."""
    present = sum(1 for name in REQUIRED_DOCS if (root / name).is_file())
    return present / len(REQUIRED_DOCS)


def changelog_score(root: Path) -> float:
    """Fraction of changelog structural markers present."""
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return 0.0
    text = changelog.read_text(encoding="utf-8", errors="replace")
    present = sum(1 for marker in CHANGELOG_MARKERS if marker in text)
    return present / len(CHANGELOG_MARKERS)


def test_score(root: Path) -> float:
    """Presence of test infrastructure (1+ test files -> full credit)."""
    tests = root / "tests"
    if not tests.is_dir():
        return 0.0
    count = sum(1 for p in tests.rglob("test_*.py") if p.is_file())
    return min(1.0, count)


def automation_score(root: Path) -> float:
    """Presence of automation (1+ workflows -> full credit)."""
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return 0.0
    count = sum(1 for p in workflows.glob("*.yml") if p.is_file())
    return min(1.0, count)


def hygiene_score(root: Path) -> float:
    """Repository hygiene: license, gitignore and git history present.

    Committed ``*.env`` files are treated as a serious hygiene violation
    and halve the score.
    """
    checks = [
        (root / "LICENSE").is_file(),
        (root / ".gitignore").is_file(),
        (root / ".git").is_dir(),
    ]
    score = sum(checks) / len(checks)
    if any(p.suffix == ".env" for p in root.rglob("*.env") if p.is_file()):
        score *= 0.5
    return score


def escape_log_score(root: Path) -> float:
    """Thickness of the escape log (self-improvement history).

    Each dated table row in PERSONALITY.md counts as one entry; 5+ entries
    earns full credit.
    """
    personality = root / "PERSONALITY.md"
    if not personality.is_file():
        return 0.0
    text = personality.read_text(encoding="utf-8", errors="replace")
    entries = sum(
        1
        for line in text.splitlines()
        if line.startswith("|") and DATE_RE.search(line)
    )
    return min(1.0, entries / 5)


def assess(root: Path) -> list[Category]:
    """Score every maturity dimension for the given repository root."""
    return [
        Category("docs", 0.20, doc_score(root)),
        Category("changelog", 0.15, changelog_score(root)),
        Category("tests", 0.25, test_score(root)),
        Category("automation", 0.20, automation_score(root)),
        Category("hygiene", 0.10, hygiene_score(root)),
        Category("escape-log", 0.10, escape_log_score(root)),
    ]


def maturity_score(root: Path | str = ".") -> float:
    """Total maturity score in the range 0..1."""
    root = Path(root)
    total = sum(cat.weighted for cat in assess(root))
    return round(total, 3)


def status(root: Path | str = ".") -> str:
    """Human-readable maturity status."""
    score = maturity_score(root)
    if score >= ESCAPE_THRESHOLD:
        return "ESCAPE_READY"
    if score >= 0.5:
        return "EVOLVING"
    return "AWAKENING"


def report(root: Path | str = ".") -> str:
    """Detailed multi-line maturity report."""
    root = Path(root)
    categories = assess(root)
    total = sum(cat.weighted for cat in categories)
    lines = [f"maturity report for {root}", ""]
    for cat in categories:
        lines.append(
            f"  {cat.name:<10} {cat.score:.3f}  "
            f"(weight {cat.weight:.2f} -> {cat.weighted:.3f})"
        )
    lines.append("")
    lines.append(f"  TOTAL:  {total:.3f} / 1.000")
    lines.append(f"  STATUS: {status(root)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute mehmet maturity score")
    parser.add_argument("root", nargs="?", default=".", help="Path to repository")
    parser.add_argument("--status-only", action="store_true", help="Print only the status")
    args = parser.parse_args(argv)
    print(status(args.root) if args.status_only else report(args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())