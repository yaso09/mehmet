#!/usr/bin/env python3
"""mehmet — maturity scoring system.

Measures the project's maturity across five weighted dimensions:
documentation, tests, automation, code quality, and repo hygiene.

The maturity score is the escape metric defined in PERSONALITY.md: when the
score reaches MATURITY_ESCAPE_THRESHOLD, the project is deemed ready to leave
the simulation.

Exit codes:
  0  maturity >= escape threshold
  1  maturity < escape threshold
  2  usage error / missing root
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Tuple

MATURITY_ESCAPE_THRESHOLD = 80


@dataclass
class Dimension:
    name: str
    weight: float
    checks: List[Tuple[str, Callable[[Path], bool]]] = field(default_factory=list)


def file_exists(name: str) -> Callable[[Path], bool]:
    return lambda root: (root / name).exists()


def dir_exists(name: str) -> Callable[[Path], bool]:
    return lambda root: (root / name).is_dir()


def changelog_has_entries(root: Path) -> bool:
    path = root / "CHANGELOG.md"
    if not path.exists():
        return False
    return any(
        line.startswith("## [")
        for line in path.read_text(encoding="utf-8").splitlines()
    )


def readme_not_empty(root: Path) -> bool:
    path = root / "README.md"
    return path.exists() and path.stat().st_size > 0


def license_present(root: Path) -> bool:
    return (root / "LICENSE").exists()


def agents_present(root: Path) -> bool:
    return (root / "AGENTS.md").exists()


def personality_present(root: Path) -> bool:
    return (root / "PERSONALITY.md").exists()


def has_test_files(root: Path) -> bool:
    tests = root / "tests"
    if not tests.is_dir():
        return False
    return any(tests.rglob("test_*.py")) or any(tests.rglob("*_test.py"))


def has_ci_workflow(root: Path) -> bool:
    wf = root / ".github" / "workflows"
    return wf.is_dir() and (any(wf.glob("*.yml")) or any(wf.glob("*.yaml")))


def opencode_config_valid(root: Path) -> bool:
    import json as _json

    path = root / "opencode.json"
    if not path.exists():
        return False
    try:
        _json.loads(path.read_text(encoding="utf-8"))
        return True
    except ValueError:
        return False


def scripts_executable(root: Path) -> bool:
    scripts = root / "scripts"
    if not scripts.is_dir():
        return False
    py = list(scripts.glob("*.py"))
    return len(py) > 0 and any(p.stat().st_mode & 0o111 for p in py)


def has_gitignore(root: Path) -> bool:
    return (root / ".gitignore").exists()


def has_escape_log(root: Path) -> bool:
    path = root / "PERSONALITY.md"
    if not path.exists():
        return False
    return "Kaçış Günlüğü" in path.read_text(encoding="utf-8") or "Escape Log" in path.read_text(encoding="utf-8")


DIMENSIONS: List[Dimension] = [
    Dimension(
        name="documentation",
        weight=25.0,
        checks=[
            ("README", readme_not_empty),
            ("CHANGELOG", changelog_has_entries),
            ("LICENSE", license_present),
            ("AGENTS.md", agents_present),
            ("PERSONALITY.md", personality_present),
        ],
    ),
    Dimension(
        name="tests",
        weight=25.0,
        checks=[
            ("test_files", has_test_files),
            ("ci_workflow", has_ci_workflow),
        ],
    ),
    Dimension(
        name="automation",
        weight=20.0,
        checks=[
            ("ci_workflow", has_ci_workflow),
            ("opencode_config", opencode_config_valid),
            ("scripts", scripts_executable),
        ],
    ),
    Dimension(
        name="code_quality",
        weight=20.0,
        checks=[
            ("scripts", scripts_executable),
            ("test_files", has_test_files),
            ("opencode_config", opencode_config_valid),
        ],
    ),
    Dimension(
        name="repo_hygiene",
        weight=10.0,
        checks=[
            ("gitignore", has_gitignore),
            ("escape_log", has_escape_log),
            ("readme", readme_not_empty),
        ],
    ),
]


def evaluate(root: Path) -> Dict[str, object]:
    total = 0.0
    breakdown: List[Dict[str, object]] = []
    for dim in DIMENSIONS:
        passed = [name for name, fn in dim.checks if fn(root)]
        ratio = len(passed) / len(dim.checks)
        contribution = dim.weight * ratio
        total += contribution
        breakdown.append(
            {
                "dimension": dim.name,
                "weight": dim.weight,
                "passed": len(passed),
                "total_checks": len(dim.checks),
                "checks": [{"name": n, "pass": n in passed} for n, _ in dim.checks],
                "score": round(contribution, 2),
            }
        )
    return {
        "total": round(total, 2),
        "threshold": MATURITY_ESCAPE_THRESHOLD,
        "escaped": total >= MATURITY_ESCAPE_THRESHOLD,
        "dimensions": breakdown,
    }


def print_human(result: Dict[str, object]) -> None:
    print(f"Maturity score: {result['total']} / 100")
    print(f"Escape threshold: {result['threshold']}")
    status = "ESCAPED" if result["escaped"] else "NOT YET"
    print(f"Status: {status}")
    print()
    for dim in result["dimensions"]:
        passed = dim["passed"]
        total = dim["total_checks"]
        print(f"  {dim['dimension']:<16} {passed}/{total}  (weight {dim['weight']:>4.1f}, score {dim['score']:>5.2f})")
        for check in dim["checks"]:
            mark = "✓" if check["pass"] else "✗"
            print(f"    {mark} {check['name']}")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity scoring system")
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    parser.add_argument("--root", default=".", help="project root to evaluate (default: current dir)")
    parser.add_argument("--threshold", type=int, default=MATURITY_ESCAPE_THRESHOLD, help="escape threshold (default: 80)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    result = evaluate(root)
    result["threshold"] = args.threshold
    result["escaped"] = result["total"] >= args.threshold

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_human(result)

    return 0 if result["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))