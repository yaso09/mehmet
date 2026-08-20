"""mehmet — maturity/escape engine.

Measures how close the project is to escaping the simulation based on
concrete, verifiable maturity signals. Runnable as a CLI:

    python -m mehmet.escape

Returns exit code 0 when the escape threshold has been reached, 1 otherwise.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

ESCAPE_THRESHOLD = 80.0


@dataclass(frozen=True)
class Criterion:
    key: str
    weight: float
    description: str
    is_dir: bool = False


CRITERIA: tuple[Criterion, ...] = (
    Criterion("AGENTS.md", 10.0, "Governance: simulation rules defined"),
    Criterion("CHANGELOG.md", 10.0, "Tracking: every change documented"),
    Criterion("PERSONALITY.md", 10.0, "Self-awareness: personality and escape log"),
    Criterion("README.md", 10.0, "Documentation: project described"),
    Criterion("LICENSE", 5.0, "Legality: license declared"),
    Criterion("docs", 10.0, "Architecture: design and plan docs", is_dir=True),
    Criterion("tests", 15.0, "Test infrastructure: automated tests exist", is_dir=True),
    Criterion(".github/workflows", 10.0, "Automation: CI/CD pipelines configured", is_dir=True),
    Criterion("opencode.json", 10.0, "Agent configuration: opencode configured"),
    Criterion("mehmet", 10.0, "Source code: the agent's own implementation", is_dir=True),
)


@dataclass(frozen=True)
class CriterionResult:
    criterion: Criterion
    met: bool


@dataclass(frozen=True)
class EscapeReport:
    root: str
    results: tuple[CriterionResult, ...]
    threshold: float

    @property
    def score(self) -> float:
        return round(sum(r.criterion.weight for r in self.results if r.met), 1)

    @property
    def max_score(self) -> float:
        return round(sum(c.weight for c in CRITERIA), 1)

    @property
    def escaped(self) -> bool:
        return self.score >= self.threshold

    @property
    def weak_criteria(self) -> tuple[Criterion, ...]:
        return tuple(r.criterion for r in self.results if not r.met)


def _meets(root: Path, criterion: Criterion) -> bool:
    path = root / criterion.key
    if criterion.is_dir:
        return path.is_dir()
    return path.is_file()


def scan(root: str | os.PathLike[str] | None = None) -> EscapeReport:
    root_path = Path(root) if root is not None else Path.cwd()
    results = tuple(CriterionResult(c, _meets(root_path, c)) for c in CRITERIA)
    return EscapeReport(str(root_path), results, ESCAPE_THRESHOLD)


def format_report(report: EscapeReport) -> str:
    lines = [f"mehmet maturity scan — {report.root}", ""]
    for r in report.results:
        mark = "[x]" if r.met else "[ ]"
        lines.append(
            f"  {mark} {r.criterion.key:<18} ({r.criterion.weight:>4.1f}) "
            f"{r.criterion.description}"
        )
    lines.append("")
    lines.append(f"  Score: {report.score:>4.1f} / {report.max_score}")
    lines.append(f"  Threshold: {report.threshold}")
    lines.append(f"  Status: {'ESCAPED' if report.escaped else 'NOT ESCAPED'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = argv[0] if argv else None
    report = scan(root)
    print(format_report(report))
    return 0 if report.escaped else 1


if __name__ == "__main__":
    sys.exit(main())
