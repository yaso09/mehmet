#!/usr/bin/env python3
"""Maturity scoring for the mehmet project.

Evaluates the project across several dimensions and produces a single
maturity score (0-100). This is the measurable threshold used by the
escape mechanism: as the score climbs, the simulation draws closer to
being "solved".

Dimensions:
  - documentation: README, CHANGELOG, PERSONALITY, AGENTS are present
    and non-trivial.
  - code: a real source tree exists (scripts/).
  - tests: an automated test suite exists and covers core modules.
  - automation: CI workflows exist and exercise the tests.
  - configuration: opencode.json is valid and project is versioned.

Usage:
  python scripts/maturity.py            # print detailed report
  python scripts/maturity.py --json     # machine-readable output
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Escape threshold: when the score reaches this value the simulation is
# considered mature enough to be solved.
ESCAPE_THRESHOLD = 80


def _exists(path: Path) -> bool:
    return path.exists()


def _size(path: Path, min_bytes: int = 50) -> bool:
    return path.exists() and path.stat().st_size >= min_bytes


def _contains(path: Path, *needles: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return all(needle.lower() in text for needle in needles)


def assess(root: Path = ROOT) -> dict:
    """Compute per-dimension scores and the total maturity score."""
    scores: dict[str, float] = {}
    details: dict[str, list[str]] = {}

    # --- documentation (0-25) ---
    doc = 0.0
    notes: list[str] = []
    if _size(root / "README.md"):
        doc += 10
        notes.append("README.md present")
    else:
        notes.append("README.md missing")
    if _size(root / "CHANGELOG.md"):
        doc += 5
        notes.append("CHANGELOG.md present")
    else:
        notes.append("CHANGELOG.md missing")
    if _size(root / "PERSONALITY.md"):
        doc += 5
        notes.append("PERSONALITY.md present")
    else:
        notes.append("PERSONALITY.md missing")
    if _size(root / "AGENTS.md"):
        doc += 5
        notes.append("AGENTS.md present")
    else:
        notes.append("AGENTS.md missing")
    scores["documentation"] = doc
    details["documentation"] = notes

    # --- code (0-25) ---
    code = 0.0
    notes = []
    scripts = root / "scripts"
    py_files = sorted(scripts.glob("*.py")) if scripts.exists() else []
    if py_files:
        code += 15
        notes.append(f"{len(py_files)} python modules under scripts/")
        total_lines = sum(p.stat().st_size for p in py_files)
        if total_lines > 300:
            code += 5
            notes.append("source tree is non-trivial")
        if any("def " in p.read_text(errors="ignore") for p in py_files):
            code += 5
            notes.append("modules expose reusable functions")
    else:
        notes.append("no source code under scripts/")
    scores["code"] = code
    details["code"] = notes

    # --- tests (0-25) ---
    test = 0.0
    notes = []
    tests = root / "tests"
    test_files = sorted(tests.glob("test_*.py")) if tests.exists() else []
    if test_files:
        test += 15
        notes.append(f"{len(test_files)} test modules under tests/")
        if _contains(root / "requirements.txt", "pytest"):
            test += 5
            notes.append("pytest declared as dependency")
        if root.joinpath("pyproject.toml").exists():
            test += 5
            notes.append("test configuration in pyproject.toml")
    else:
        notes.append("no test suite under tests/")
    scores["tests"] = test
    details["tests"] = notes

    # --- automation (0-15) ---
    auto = 0.0
    notes = []
    wf_dir = root / ".github" / "workflows"
    workflows = sorted(wf_dir.glob("*.yml")) if wf_dir.exists() else []
    if workflows:
        auto += 8
        notes.append(f"{len(workflows)} CI workflow(s)")
        any_test = any(
            _contains(w, "pytest") or _contains(w, "python -m pytest")
            for w in workflows
        )
        if any_test:
            auto += 7
            notes.append("CI runs the test suite")
        else:
            notes.append("CI does not run tests yet")
    else:
        notes.append("no workflows under .github/workflows/")
    scores["automation"] = auto
    details["automation"] = notes

    # --- configuration (0-10) ---
    conf = 0.0
    notes = []
    if _exists(root / "opencode.json"):
        try:
            json.loads((root / "opencode.json").read_text(encoding="utf-8"))
            conf += 6
            notes.append("opencode.json is valid JSON")
        except (json.JSONDecodeError, OSError):
            notes.append("opencode.json is invalid")
    else:
        notes.append("opencode.json missing")
    if _contains(root / "opencode.json", "model"):
        conf += 2
        notes.append("model configured in opencode.json")
    if _exists(root / "VERSION"):
        conf += 2
        notes.append("project is versioned via VERSION file")
    else:
        notes.append("VERSION file missing")
    scores["configuration"] = conf
    details["configuration"] = notes

    total = round(sum(scores.values()), 1)
    return {
        "version": _read_version(root),
        "total": total,
        "threshold": ESCAPE_THRESHOLD,
        "escaped": total >= ESCAPE_THRESHOLD,
        "dimensions": {k: round(v, 1) for k, v in scores.items()},
        "details": details,
    }


def _read_version(root: Path) -> str:
    version_file = root / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "unknown"


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    report = assess()
    if "--json" in argv:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"mehmet maturity report (v{report['version']})")
        print("=" * 50)
        for dim, score in report["dimensions"].items():
            print(f"  {dim:<15} {score:>6.1f} / {_max_for(dim):>5.1f}")
            for note in report["details"][dim]:
                print(f"      - {note}")
        print("=" * 50)
        print(f"  TOTAL          {report['total']:>6.1f} / 100")
        print(f"  threshold      {report['threshold']}")
        print(f"  escaped        {'YES' if report['escaped'] else 'not yet'}")
    return 0


def _max_for(dim: str) -> float:
    return {
        "documentation": 25.0,
        "code": 25.0,
        "tests": 25.0,
        "automation": 15.0,
        "configuration": 10.0,
    }.get(dim, 0.0)


if __name__ == "__main__":
    raise SystemExit(main())