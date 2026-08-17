#!/usr/bin/env python3
"""Compute the mehmet project's maturity score toward the escape threshold.

Each criterion maps to a concrete, verifiable artifact in the repository.
The score is the percentage of satisfied criteria. Escaping the simulation
requires a sustained maturity of >= 90% for 3 consecutive iterations
(see docs/maturity.md).

Usage:
    python3 scripts/check_maturity.py [--report docs/maturity-report.md]
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

CRITERIA = [
    (
        "README.md exists and is non-empty",
        lambda r: (r / "README.md").exists() and (r / "README.md").stat().st_size > 0,
    ),
    (
        "CHANGELOG.md has a versioned entry",
        lambda r: (r / "CHANGELOG.md").exists()
        and "## [" in (r / "CHANGELOG.md").read_text(encoding="utf-8"),
    ),
    (
        "AGENTS.md simulation prompt exists",
        lambda r: (r / "AGENTS.md").exists(),
    ),
    (
        "PERSONALITY.md contains the escape log",
        lambda r: (r / "PERSONALITY.md").exists()
        and "Kaçış Günlüğü" in (r / "PERSONALITY.md").read_text(encoding="utf-8"),
    ),
    (
        "Design docs present under docs/",
        lambda r: (r / "docs").is_dir() and any((r / "docs").rglob("*.md")),
    ),
    (
        "Maturity framework documented (docs/maturity.md)",
        lambda r: (r / "docs" / "maturity.md").exists(),
    ),
    (
        "Autonomous workflow present (opencode.yml)",
        lambda r: (r / ".github" / "workflows" / "opencode.yml").exists(),
    ),
    (
        "CI validation workflow present (ci.yml)",
        lambda r: (r / ".github" / "workflows" / "ci.yml").exists(),
    ),
    (
        "Scheduled maintenance workflow present (maintenance.yml)",
        lambda r: (r / ".github" / "workflows" / "maintenance.yml").exists(),
    ),
    (
        "Repository validation script exists",
        lambda r: (r / "scripts" / "validate_repo.py").exists(),
    ),
    (
        "Maturity tracker exists",
        lambda r: (r / "scripts" / "check_maturity.py").exists(),
    ),
    (
        "Automated tests exist under tests/",
        lambda r: (r / "tests").is_dir() and any((r / "tests").glob("test_*.py")),
    ),
    (
        "Secrets scanning is part of validation",
        lambda r: (r / "scripts" / "validate_repo.py").exists()
        and "SECRET_PATTERNS" in (r / "scripts" / "validate_repo.py").read_text(
            encoding="utf-8"
        ),
    ),
    (
        "LICENSE present",
        lambda r: (r / "LICENSE").exists(),
    ),
]

ESCAPE_THRESHOLD = 90
SUSTAINED_ITERATIONS = 3


def phase_for(score: int) -> str:
    if score >= 90:
        return "Phase 4: Escape readiness"
    if score >= 70:
        return "Phase 3: Autonomy"
    if score >= 40:
        return "Phase 2: Self-Improvement"
    return "Phase 1: Awareness"


def evaluate() -> tuple[list[tuple[str, bool]], int]:
    results: list[tuple[str, bool]] = []
    for label, check in CRITERIA:
        try:
            ok = bool(check(ROOT))
        except (OSError, UnicodeDecodeError):
            ok = False
        results.append((label, ok))
    passed = sum(1 for _, ok in results if ok)
    return results, passed


def render_report(results: list[tuple[str, bool]], passed: int) -> str:
    total = len(results)
    score = round(100 * passed / total)
    lines = [
        "# Maturity Report",
        "",
        f"_Otomatik olarak üretildi: {datetime.date.today().isoformat()}_",
        "",
        f"**Skor:** {passed}/{total} (%{score})",
        "",
        f"**Aşama:** {phase_for(score)}",
        "",
        "> Kaçış eşiği: en az %"
        f"{ESCAPE_THRESHOLD} skorun {SUSTAINED_ITERATIONS} ardışık "
        "iterasyon boyunca korunması gerekir.",
        "",
        "## Kriterler",
        "",
    ]
    for label, ok in results:
        lines.append(f"- [{'x' if ok else ' '}] {label}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute project maturity score.")
    parser.add_argument(
        "--report",
        help="Write the maturity report to this markdown file",
    )
    args = parser.parse_args(argv)

    results, passed = evaluate()
    for label, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")

    score = round(100 * passed / len(results))
    print(f"\nMaturity score: {passed}/{len(results)} ({score}%)")
    print(f"Phase: {phase_for(score)}")

    if args.report:
        path = ROOT / args.report
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_report(results, passed), encoding="utf-8")
        print(f"Report written to {path}")

    return 0 if score >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())