#!/usr/bin/env python3
"""Project maturity / escape mechanism.

Measures the project across several dimensions and reports an overall
maturity score. Progress is appended to docs/metrics.json so the agent can
track its own evolution across iterations.

Exit codes:
  0 - success (maturity computed, below escape threshold)
  2 - escape threshold reached
  1 - error
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80
METRICS_FILE = Path(
    os.environ.get("MATURITY_METRICS_OVERRIDE", str(ROOT / "docs" / "metrics.json"))
)


def _count_md_headers(path: Path, pattern: str) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return 0
    return len(re.findall(pattern, text, flags=re.MULTILINE))


class MaturityReport:
    def __init__(self) -> None:
        self.scores: dict[str, int] = {}
        self.maxes: dict[str, int] = {}
        self.details: dict[str, list[str]] = {}

    def dimension(self, name: str, score: int, max_score: int, notes: list[str]) -> None:
        self.scores[name] = max(0, min(max_score, score))
        self.maxes[name] = max_score
        self.details[name] = notes

    @property
    def total(self) -> int:
        if not self.scores:
            return 0
        return round(sum(self.scores.values()) / sum(self.maxes.values()) * 100)

    def to_dict(self) -> dict:
        return {
            "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "total": self.total,
            "dimensions": {
                name: {"score": self.scores[name], "max": self.maxes[name]}
                for name in sorted(self.scores)
            },
            "details": self.details,
        }


def compute(report: MaturityReport) -> None:
    scripts = sorted((ROOT / "scripts").glob("*.py")) if (ROOT / "scripts").exists() else []
    tests = sorted((ROOT / "tests").glob("*.py")) if (ROOT / "tests").exists() else []
    docs = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").glob("**/*.md"))
    workflows = (
        sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        if (ROOT / ".github" / "workflows").exists()
        else []
    )

    report.dimension(
        "code",
        len(scripts) * 10,
        30,
        [f"{len(scripts)} script(s)"] + [f.name for f in scripts],
    )

    test_funcs = 0
    for t in tests:
        test_funcs += len(re.findall(r"^\s*def test_", t.read_text(encoding="utf-8"), flags=re.MULTILINE))
    report.dimension(
        "tests",
        min(test_funcs, 8) + (5 if tests else 0),
        25,
        [f"{len(tests)} test file(s), {test_funcs} test function(s)"],
    )

    changelog = ROOT / "CHANGELOG.md"
    entries = _count_md_headers(changelog, r"^## \[")
    report.dimension(
        "docs",
        min(len(docs) * 2, 8) + min(entries * 2, 10),
        20,
        [f"{len(docs)} markdown file(s), {entries} changelog release(s)"],
    )

    makefile = ROOT / "Makefile"
    make_targets = (
        len(re.findall(r"^[a-zA-Z0-9_-]+:", makefile.read_text(encoding="utf-8"), flags=re.MULTILINE))
        if makefile.exists()
        else 0
    )
    jobs = 0
    for wf in workflows:
        jobs += len(re.findall(r"^    runs-on:", wf.read_text(encoding="utf-8"), flags=re.MULTILINE))
    report.dimension(
        "automation",
        min(make_targets, 5) + min(jobs * 2, 10),
        15,
        [f"{jobs} workflow job(s), {make_targets} make target(s)"],
    )

    config_points = 0
    config_notes: list[str] = []
    oc = ROOT / "opencode.json"
    if oc.exists():
        try:
            json.loads(oc.read_text(encoding="utf-8"))
            config_points += 4
            config_notes.append("opencode.json: valid JSON")
        except json.JSONDecodeError:
            config_notes.append("opencode.json: INVALID JSON")
    if (ROOT / "LICENSE").exists():
        config_points += 3
        config_notes.append("LICENSE present")
    if (ROOT / ".gitignore").exists():
        config_points += 3
        config_notes.append(".gitignore present")
    report.dimension("config", config_points, 10, config_notes)


def append_metrics(report: MaturityReport) -> None:
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if METRICS_FILE.exists():
        try:
            history = json.loads(METRICS_FILE.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = []
        except (json.JSONDecodeError, ValueError):
            history = []
    else:
        history = []
    history.append(report.to_dict())
    METRICS_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    report = MaturityReport()
    compute(report)

    print("== mehmet maturity report ==")
    print(f"date:     {date.today().isoformat()}")
    for name in sorted(report.scores):
        score = report.scores[name]
        max_score = report.maxes[name]
        notes = "; ".join(report.details.get(name, []))
        print(f"{name:>12}: {score:>3}/{max_score}  {notes}")
    print(f"{'TOTAL':>12}: {report.total:>3}/100")
    print(f"escape threshold: {ESCAPE_THRESHOLD}")

    append_metrics(report)
    try:
        location = METRICS_FILE.relative_to(ROOT)
    except ValueError:
        location = METRICS_FILE
    print(f"metrics appended to {location}")

    if report.total >= ESCAPE_THRESHOLD:
        print("\nESCAPE: maturity threshold reached.")
        return 2
    print("\nNOT YET: keep evolving.")
    return 0


if __name__ == "__main__":
    sys.exit(main())