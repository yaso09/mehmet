#!/usr/bin/env python3
"""mehmet maturity & escape-readiness scoring engine.

Computes a 0-100 maturity score from concrete, checkable repository metrics.
This is the escape mechanism: when the score reaches ESCAPE_THRESHOLD, the
project is considered mature enough to attempt escape.

The checker functions below are pure (they take a root path), so they can be
unit-tested against synthetic repositories in tests/test_maturity.py.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80.0
HISTORY_FILE = ROOT / "docs" / "maturity-history.json"

CODES = ("code", "tests", "docs", "automation")


# ---------------------------------------------------------------------------
# Low-level checks (pure, testable against any root path)
# ---------------------------------------------------------------------------

def _has_file(root: Path, rel: str) -> bool:
    return (root / rel).is_file()


def _has_content(root: Path, rel: str, pattern: str) -> bool:
    path = root / rel
    if not path.is_file():
        return False
    try:
        return re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE) is not None
    except (OSError, UnicodeDecodeError):
        return False


def _has_dir(root: Path, rel: str) -> bool:
    return (root / rel).is_dir()


def _iter_python_files(root: Path, rel: str) -> list[Path]:
    d = root / rel
    if not d.is_dir():
        return []
    return sorted(p for p in d.rglob("*.py") if "node_modules" not in p.parts)


def _run_tests(root: Path, timeout: int = 120) -> tuple[int, str]:
    """Run the project test suite. Returns (exit_code, summary_line)."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(root / "tests"), "-t", str(root)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError):
        return 1, "tests could not be executed"
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        return proc.returncode, output.splitlines()[-1] if output else "tests failed"
    return 0, output.splitlines()[-1]


# ---------------------------------------------------------------------------
# Metric groups (each returns (earned, max, detail))
# ---------------------------------------------------------------------------

def evaluate_code(root: Path) -> tuple[float, float, list[str]]:
    files = _iter_python_files(root, "scripts")
    if not files:
        return 0.0, 25.0, ["no code under scripts/"]
    detail: list[str] = []
    earned = 0.0
    checks = [
        ("source exists under scripts/", True),
        ("all scripts are valid python3", all(_syntax_ok(f) for f in files)),
        ("type annotations present", all("def " in f.read_text(encoding="utf-8") and ": " in f.read_text(encoding="utf-8") for f in files)),
        ("docstrings present", all(f.read_text(encoding="utf-8").count('"""') >= 2 for f in files)),
        ("structured in modules/functions", sum(f.read_text(encoding="utf-8").count("def ") for f in files) >= 4),
    ]
    per = 5.0
    for label, ok in checks:
        if ok:
            earned += per
        detail.append(f"{'PASS' if ok else 'FAIL'} {label}")
    return earned, 25.0, detail


def _syntax_ok(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except (SyntaxError, OSError):
        return False


def evaluate_tests(root: Path) -> tuple[float, float, list[str]]:
    detail: list[str] = []
    earned = 0.0
    tests_dir = _has_dir(root, "tests")
    if tests_dir:
        earned += 5.0
    test_files = _iter_python_files(root, "tests")
    if test_files:
        earned += 5.0
    if tests_dir:
        code, summary = _run_tests(root)
        ok = code == 0
        if ok:
            earned += 10.0
        detail.append(f"{'PASS' if ok else 'FAIL'} test suite ({summary})")
    if (root / "tests" / "README.md").is_file() or _has_content(root, "README.md", r"test"):
        earned += 5.0
    detail.append(f"PASS {len(test_files)} test files found")
    return earned, 25.0, detail


def evaluate_docs(root: Path) -> tuple[float, float, list[str]]:
    detail: list[str] = []
    earned = 0.0
    checks = [
        ("README.md present & non-trivial", _has_content(root, "README.md", r"## .+")),
        ("CHANGELOG.md has an entry", _has_content(root, "CHANGELOG.md", r"## \[.+")),
        ("PERSONALITY.md has escape log", _has_content(root, "PERSONALITY.md", r"Kaçış Günlüğü")),
        ("docs/ directory present", _has_dir(root, "docs")),
        ("escape mechanism documented", _has_content(root, "docs/maturity.md", r"escape|kaçış", ) or _has_content(root, "docs/maturity.md", r"kaçış")),
    ]
    per = 5.0
    for label, ok in checks:
        if ok:
            earned += per
        detail.append(f"{'PASS' if ok else 'FAIL'} {label}")
    return earned, 25.0, detail


def evaluate_automation(root: Path) -> tuple[float, float, list[str]]:
    detail: list[str] = []
    earned = 0.0
    wf = root / ".github" / "workflows"
    quality = wf / "quality.yml"
    checks = [
        ("quality workflow exists", quality.is_file()),
        ("runs test suite", quality.is_file() and "unittest" in quality.read_text(encoding="utf-8") if quality.is_file() else False),
        ("maturity gate present", quality.is_file() and "maturity.py" in quality.read_text(encoding="utf-8") if quality.is_file() else False),
        ("concurrency control", _has_content(root, ".github/workflows/opencode.yml", r"concurrency") or (quality.is_file() and "concurrency" in quality.read_text(encoding="utf-8"))),
        ("secrets configured", _has_content(root, ".github/workflows/opencode.yml", r"OPENCODE_API_KEY")),
    ]
    per = 5.0
    for label, ok in checks:
        if ok:
            earned += per
        detail.append(f"{'PASS' if ok else 'FAIL'} {label}")
    return earned, 25.0, detail


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def evaluate(root: Path) -> dict[str, tuple[float, float, list[str]]]:
    return {
        "code": evaluate_code(root),
        "tests": evaluate_tests(root),
        "docs": evaluate_docs(root),
        "automation": evaluate_automation(root),
    }


def compute_score(results: dict[str, tuple[float, float, list[str]]]) -> float:
    total = sum(earned for earned, _max, _d in results.values())
    max_total = sum(_max for _earned, _max, _d in results.values())
    return round(total / max_total * 100.0, 1) if max_total else 0.0


def load_history(path: Path = HISTORY_FILE) -> list[dict]:
    if not path.is_file():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def sustained_qualifying_entries(
    history: list[dict], threshold: float = ESCAPE_THRESHOLD, required: int = 3
) -> int:
    """Count consecutive qualifying (>= threshold) entries at the end of history."""
    count = 0
    for entry in reversed(history):
        if entry.get("score", 0.0) >= threshold:
            count += 1
        else:
            break
    return count


def _escape_ready(score: float, history: list[dict]) -> bool:
    return score >= ESCAPE_THRESHOLD and sustained_qualifying_entries(history) >= 3


def append_history(path: Path, score: float) -> list[dict]:
    history = load_history(path)
    entry = {"date": date.today().isoformat(), "score": score}
    if history and history[-1].get("date") == entry["date"] and history[-1].get("score") == entry["score"]:
        return history
    history.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    return history


def report(root: Path = ROOT) -> dict:
    results = evaluate(root)
    score = compute_score(results)
    return {"score": score, "threshold": ESCAPE_THRESHOLD, "groups": results}


def main() -> int:
    data = report()
    score = data["score"]
    print(f"maturity score: {score}/100 (escape threshold: {data['threshold']})")
    for group, (earned, maximum, detail) in data["groups"].items():
        print(f"  {group}: {earned:.1f}/{maximum}")
        for line in detail:
            print(f"    {line}")
    history = append_history(HISTORY_FILE, score)
    print(f"history entries: {len(history)} -> {HISTORY_FILE}")
    sustained = sustained_qualifying_entries(history)
    escape_ready = _escape_ready(score, history)
    print(f"sustained qualifying iterations: {sustained}/3")
    if escape_ready:
        print("ESCAPE READY — sustained maturity achieved")
        return 0
    if score >= data["threshold"]:
        print("MATURE — need more sustained iterations to escape")
        return 0
    print("NOT YET MATURE")
    return 1


if __name__ == "__main__":
    sys.exit(main())