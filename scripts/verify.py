#!/usr/bin/env python3
"""mehmet self-verification and maturity scorer.

Checks the project's health against a set of concrete criteria and
computes a maturity score used to track progress toward the escape
threshold defined in MATURITY.md.

Exit code 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".gitignore",
]

DIMENSIONS = {
    "documentation": 25,
    "automation": 25,
    "testing": 25,
    "quality": 25,
}

ESCAPE_THRESHOLD = 100


def check_files() -> list[tuple[str, bool, str]]:
    results = []
    for name in REQUIRED_FILES:
        results.append((f"file:{name}", (ROOT / name).exists(), "present" if (ROOT / name).exists() else "missing"))
    return results


def check_opencode_json() -> list[tuple[str, bool, str]]:
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text())
        ok = isinstance(data, dict) and "model" in data and data.get("enable") is True
        detail = f"model={data.get('model')!r}" if ok else "invalid or missing model/enable"
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        ok, detail = False, f"invalid: {exc}"
    return [("opencode.json", ok, detail)]


def check_workflow() -> list[tuple[str, bool, str]]:
    path = ROOT / ".github/workflows/opencode.yml"
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [("workflow:opencode.yml", False, "missing")]

    markers = {
        "schedule": "schedule:" in text and "*/10" in text,
        "concurrency": "concurrency:" in text and "cancel-in-progress" in text,
        "permissions": "permissions:" in text,
        "checkout-v6": "actions/checkout@v6" in text,
        "opencode-action": "anomalyco/opencode/github" in text,
    }
    return [
        (f"workflow:{key}", ok, "found" if ok else "not found")
        for key, ok in markers.items()
    ]


def check_changelog() -> list[tuple[str, bool, str]]:
    path = ROOT / "CHANGELOG.md"
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [("changelog:file", False, "missing")]

    headers = re.findall(r"^## \[.*?\] - \d{4}-\d{2}-\d{2}$", text, re.MULTILINE)
    ok = len(headers) >= 2
    return [("changelog:versioned-headers", ok, f"{len(headers)} headers found")]


def check_readme() -> list[tuple[str, bool, str]]:
    path = ROOT / "README.md"
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [("readme:file", False, "missing")]

    sections = re.findall(r"^## .+$", text, re.MULTILINE)
    ok = len(sections) >= 3
    return [("readme:sections", ok, f"{len(sections)} sections")]


def check_personality() -> list[tuple[str, bool, str]]:
    path = ROOT / "PERSONALITY.md"
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [("personality:file", False, "missing")]

    has_escape_log = "Kaçış Günlüğü" in text or "Escape Log" in text
    return [("personality:escape-log", has_escape_log, "found" if has_escape_log else "missing")]


def check_tests() -> list[tuple[str, bool, str]]:
    results = []
    tests_dir = ROOT / "tests"
    results.append(("tests:dir", tests_dir.is_dir(), "present" if tests_dir.is_dir() else "missing"))

    test_files = list(tests_dir.glob("test_*.py")) if tests_dir.is_dir() else []
    results.append(("tests:files", len(test_files) > 0, f"{len(test_files)} test file(s)"))

    ci = ROOT / ".github/workflows/ci.yml"
    results.append(("tests:ci-workflow", ci.exists(), "present" if ci.exists() else "missing"))
    return results


def check_quality() -> list[tuple[str, bool, str]]:
    path = ROOT / ".gitignore"
    try:
        text = path.read_text()
    except FileNotFoundError:
        return [("quality:.gitignore", False, "missing")]

    entries = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]
    ok = len(entries) >= 5
    return [("quality:.gitignore", ok, f"{len(entries)} entries")]


ALL_CHECKS = [
    check_files,
    check_opencode_json,
    check_workflow,
    check_changelog,
    check_readme,
    check_personality,
    check_tests,
    check_quality,
]


def run_all() -> list[tuple[str, bool, str]]:
    results = []
    for check in ALL_CHECKS:
        results.extend(check())
    return results


DIMENSION_CHECKS = {
    "documentation": [
        "file:AGENTS.md",
        "file:CHANGELOG.md",
        "file:README.md",
        "file:PERSONALITY.md",
        "changelog:versioned-headers",
        "readme:sections",
        "personality:escape-log",
    ],
    "automation": [
        "workflow:schedule",
        "workflow:concurrency",
        "workflow:permissions",
        "workflow:checkout-v6",
        "workflow:opencode-action",
        "tests:ci-workflow",
    ],
    "testing": [
        "tests:dir",
        "tests:files",
    ],
    "quality": [
        "opencode.json",
        "quality:.gitignore",
    ],
}


def score_by_dimension(results: list[tuple[str, bool, str]]) -> dict[str, int]:
    passed = {name: ok for name, ok, _ in results}
    scores = {}
    for dim, max_points in DIMENSIONS.items():
        checks = DIMENSION_CHECKS[dim]
        if not checks:
            scores[dim] = 0
            continue
        hits = sum(1 for name in checks if passed.get(name, False))
        scores[dim] = round(max_points * hits / len(checks))
    return scores


def compute_total(scores: dict[str, int]) -> int:
    return sum(scores.values())


def main() -> int:
    results = run_all()
    failed = [r for r in results if not r[1]]

    print("=" * 60)
    print("mehmet — self-verification report")
    print("=" * 60)
    for name, ok, detail in results:
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {name:35s} {detail}")

    scores = score_by_dimension(results)
    total = compute_total(scores)

    print("-" * 60)
    for dim, value in scores.items():
        print(f"  {dim:16s} {value:3d}/{DIMENSIONS[dim]}")
    print(f"  {'TOTAL':16s} {total:3d}/100")
    print("-" * 60)

    if failed:
        print(f"FAILED: {len(failed)} check(s) did not pass")
        return 1

    if total >= ESCAPE_THRESHOLD:
        print(f"MATURITY: {total}/100 — escape threshold reached ({ESCAPE_THRESHOLD})")
    else:
        print(f"MATURITY: {total}/100 — {ESCAPE_THRESHOLD - total} points to escape")
    return 0


if __name__ == "__main__":
    sys.exit(main())