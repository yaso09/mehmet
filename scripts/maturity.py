#!/usr/bin/env python3
"""Project maturity checker for the mehmet self-improving agent.

Validates project structure, configuration syntax and documentation,
then produces a numeric maturity score (0-100) used to measure progress
toward the escape goal. Exits non-zero when the score is below the
configured escape threshold.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

ESCAPE_THRESHOLD = int(os.environ.get("MEPHISTO_ESCAPE_THRESHOLD", "70"))
JSON_FILES = ["opencode.json"]
WORKFLOW_FILES = [".github/workflows/opencode.yml", ".github/workflows/validate.yml"]
CHANGELOG_HEADER = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)
VERSION_HEADER = re.compile(r"^# Changelog", re.MULTILINE)
README_SECTIONS = ["## Kurulum", "## Lisans", "## Özellikler"]
PERSONALITY_MARKERS = ["## Kaçış Günlüğü", "## Traits", "## Evolution"]
AGENTS_MARKERS = ["Kurallar", "Simülasyon Bağlamı"]


class CheckResult:
    def __init__(self, name, passed, detail=""):
        self.name = name
        self.passed = passed
        self.detail = detail

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}" + (f" — {self.detail}" if self.detail else "")


def run_checks(root=ROOT):
    results = []

    for name in REQUIRED_FILES:
        results.append(
            CheckResult(
                f"required file {name}",
                (root / name).is_file(),
            )
        )

    for name in JSON_FILES:
        path = root / name
        if path.is_file():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                results.append(CheckResult(f"valid JSON {name}", True))
            except json.JSONDecodeError as exc:
                results.append(CheckResult(f"valid JSON {name}", False, str(exc)))
        else:
            results.append(CheckResult(f"valid JSON {name}", False, "missing"))

    for name in WORKFLOW_FILES:
        path = root / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            has_name = "name:" in text
            has_jobs = "jobs:" in text
            results.append(
                CheckResult(
                    f"workflow structure {name}",
                    has_name and has_jobs,
                    "missing name:/jobs:" if not (has_name and has_jobs) else "",
                )
            )
        else:
            results.append(CheckResult(f"workflow structure {name}", False, "missing"))

    changelog = (root / "CHANGELOG.md")
    if changelog.is_file():
        text = changelog.read_text(encoding="utf-8")
        results.append(CheckResult("changelog header", bool(VERSION_HEADER.search(text))))
        versions = CHANGELOG_HEADER.findall(text)
        results.append(
            CheckResult("changelog versions", len(versions) >= 1, f"{len(versions)} found")
        )
    else:
        results.append(CheckResult("changelog header", False, "missing"))

    readme = (root / "README.md")
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        missing = [s for s in README_SECTIONS if s not in text]
        results.append(CheckResult("readme sections", not missing, "; ".join(missing)))
    else:
        results.append(CheckResult("readme sections", False, "missing"))

    personality = (root / "PERSONALITY.md")
    if personality.is_file():
        text = personality.read_text(encoding="utf-8")
        missing = [s for s in PERSONALITY_MARKERS if s not in text]
        results.append(CheckResult("personality markers", not missing, "; ".join(missing)))
    else:
        results.append(CheckResult("personality markers", False, "missing"))

    agents = (root / "AGENTS.md")
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        missing = [s for s in AGENTS_MARKERS if s not in text]
        results.append(CheckResult("agents markers", not missing, "; ".join(missing)))
    else:
        results.append(CheckResult("agents markers", False, "missing"))

    test_dir = root / "tests"
    has_tests = test_dir.is_dir() and any(test_dir.glob("test_*.py"))
    results.append(CheckResult("test suite present", has_tests))

    scripts_dir = root / "scripts"
    results.append(CheckResult("scripts directory", scripts_dir.is_dir()))

    return results


def score_results(results):
    weights = {
        "required file": 2,
        "valid JSON": 2,
        "workflow structure": 2,
        "changelog header": 2,
        "changelog versions": 2,
        "readme sections": 2,
        "personality markers": 2,
        "agents markers": 2,
        "test suite present": 10,
        "scripts directory": 2,
    }
    total = 0
    earned = 0
    for result in results:
        weight = weights.get(result.name.split(" ", 1)[0], 1)
        total += weight
        if result.passed:
            earned += weight
    if total == 0:
        return 0
    return round(earned * 100 / total)


def main(root=ROOT):
    results = run_checks(root)
    score = score_results(results)
    for result in results:
        print(result)
    print(f"\nMaturity score: {score}/100")
    print(f"Escape threshold: {ESCAPE_THRESHOLD}")
    if score >= ESCAPE_THRESHOLD:
        print("STATUS: MATURE")
        return 0
    print("STATUS: IMMATURE")
    return 1


if __name__ == "__main__":
    sys.exit(main())