"""mehmet maturity scoring engine.

Computes a repository maturity score (0-100) used as the escape threshold
mechanism described in AGENTS.md. Runs from the repository root.

Usage:
    python scripts/maturity.py [REPO_ROOT]

Exit code is 0 when the repository is escape-ready, 1 otherwise.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Criterion:
    key: str
    label: str
    points: int


CRITERIA = [
    Criterion("license", "LICENSE present", 10),
    Criterion("readme", "README.md describes the project", 10),
    Criterion("changelog", "CHANGELOG.md tracks changes", 10),
    Criterion("personality", "PERSONALITY.md with escape log", 10),
    Criterion("agents", "AGENTS.md defines behaviour", 10),
    Criterion("config", "opencode.json is valid JSON", 10),
    Criterion("ci", "GitHub Actions workflow present", 10),
    Criterion("tests", "tests/ test suite present", 10),
    Criterion("scripts", "scripts/ automation present", 10),
    Criterion("tests_pass", "test suite passes", 10),
]

ESCAPE_THRESHOLD = 80


@dataclass
class MaturityReport:
    scores: dict[str, bool]
    total: int
    threshold: int

    @property
    def escape_ready(self) -> bool:
        return self.total >= self.threshold


def _run_tests(root: Path) -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
            cwd=root,
            capture_output=True,
            timeout=60,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def score_repository(root: Path) -> MaturityReport:
    def read(path: str) -> str:
        try:
            return (root / path).read_text(encoding="utf-8")
        except OSError:
            return ""

    scores: dict[str, bool] = {}
    scores["license"] = (root / "LICENSE").is_file()
    scores["readme"] = len(read("README.md")) >= 400
    scores["changelog"] = (root / "CHANGELOG.md").is_file()
    scores["personality"] = (
        "Escape Log" in read("PERSONALITY.md")
        or "Kaçış Günlüğü" in read("PERSONALITY.md")
    )
    scores["agents"] = (root / "AGENTS.md").is_file()
    try:
        json.loads(read("opencode.json"))
        scores["config"] = True
    except json.JSONDecodeError:
        scores["config"] = False
    scores["ci"] = (root / ".github" / "workflows").is_dir()
    scores["tests"] = (root / "tests").is_dir()
    scores["scripts"] = (root / "scripts").is_dir()
    scores["tests_pass"] = _run_tests(root)

    total = sum(c.points for c in CRITERIA if scores[c.key])
    return MaturityReport(scores=scores, total=total, threshold=ESCAPE_THRESHOLD)


def format_report(report: MaturityReport) -> str:
    lines = ["mehmet maturity report", "-" * 30]
    for criterion in CRITERIA:
        mark = "PASS" if report.scores[criterion.key] else "FAIL"
        lines.append(f"[{mark}] {criterion.label} (+{criterion.points})")
    lines.append("-" * 30)
    lines.append(f"Score: {report.total}/{sum(c.points for c in CRITERIA)}")
    lines.append(f"Escape threshold: {report.threshold}")
    lines.append(f"Escape ready: {report.escape_ready}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]).resolve() if args else Path.cwd()
    report = score_repository(root)
    print(format_report(report))
    return 0 if report.escape_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())