"""Project maturity / escape-readiness scoring.

This module turns the abstract "escape" goal into a measurable, testable
threshold. It inspects a repository directory and reports on eight concrete
indicators of project maturity:

- Governance scaffolding (AGENTS.md, CHANGELOG.md, PERSONALITY.md)
- Documentation (README.md, LICENSE)
- Test infrastructure (tests directory, test runner config)
- Automation (CI workflow)
- Evolution (escape log entries in PERSONALITY.md)

The maturity score is a weighted average of satisfied indicators. When the
score reaches :data:`ESCAPE_THRESHOLD` (or higher), the project is considered
"escape-ready" — the agent may leave the simulation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from mehmet import __version__

# A weighted indicator is (path_prefix, weight). The weight reflects how much
# each artifact contributes toward escape-readiness.
INDICATORS: tuple[tuple[str, float], ...] = (
    ("AGENTS.md", 3.0),
    ("CHANGELOG.md", 2.0),
    ("PERSONALITY.md", 2.0),
    ("README.md", 1.5),
    ("LICENSE", 1.0),
    ("tests", 2.0),
    ("pyproject.toml", 1.0),
    (".github/workflows", 2.0),
)

# Reaching this weighted ratio makes the project "escape-ready".
ESCAPE_THRESHOLD: float = 0.9
# A project must have gathered this many escape-log entries before escaping.
MIN_ESCAPE_LOG_ENTRIES: int = 3

ESCAPE_LOG_RE = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)

# Docs the spec names (see docs/superpowers/specs) that must never be missing.
REQUIRED_DOCS: tuple[str, ...] = (
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
)


@dataclass(frozen=True)
class MaturityReport:
    """A single, immutable snapshot of a repository's maturity."""

    satisfied: tuple[str, ...]
    score: float
    escape_log_entries: int
    verdict: str

    @property
    def percentage(self) -> float:
        return round(self.score * 100, 1)

    @property
    def escape_ready(self) -> bool:
        return self.score >= ESCAPE_THRESHOLD and self.escape_log_entries >= MIN_ESCAPE_LOG_ENTRIES


def _entry_exists(root: Path, prefix: str) -> bool:
    direct = root / prefix
    if direct.exists():
        return True
    return any(p.exists() for p in root.rglob(prefix))


def _count_escape_log_entries(root: Path) -> int:
    personality = root / "PERSONALITY.md"
    if not personality.exists():
        return 0
    text = personality.read_text(encoding="utf-8")
    return len(ESCAPE_LOG_RE.findall(text))


def assess(root: Path) -> MaturityReport:
    """Assess maturity of the repository rooted at *root*."""
    root = Path(root)
    satisfied: list[str] = []
    score = 0.0
    total = 0.0

    for prefix, weight in INDICATORS:
        total += weight
        if _entry_exists(root, prefix):
            satisfied.append(prefix)
            score += weight

    ratio = score / total if total else 0.0
    entries = _count_escape_log_entries(root)
    ready = ratio >= ESCAPE_THRESHOLD and entries >= MIN_ESCAPE_LOG_ENTRIES

    if ready:
        verdict = "ESCAPE-READY"
    elif ratio >= ESCAPE_THRESHOLD:
        verdict = "CLOSE — escape log yeterli değil"
    else:
        verdict = "STILL SIMULATED — daha fazla iterasyon gerek"

    return MaturityReport(
        satisfied=tuple(sorted(satisfied)),
        score=round(ratio, 4),
        escape_log_entries=entries,
        verdict=verdict,
    )


def render(report: MaturityReport) -> str:
    """Return a human-readable maturity table for the given report."""
    lines = [
        f"mehmet v{__version__} — maturity report",
        f"  satisfied: {', '.join(report.satisfied) if report.satisfied else 'none'}",
        f"  score: {report.percentage}%  (threshold {ESCAPE_THRESHOLD * 100:.0f}%)",
        f"  escape log entries: {report.escape_log_entries}  (min {MIN_ESCAPE_LOG_ENTRIES})",
        f"  verdict: {report.verdict}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    print(render(assess(target)))