#!/usr/bin/env python3
"""Project maturity validator for mehmet.

Checks project structure, configuration integrity and documentation health.
Used as a quality gate in CI and during autonomous iterations.

Exit codes:
  0 - all checks passed
  1 - at least one critical check failed
  2 - maturity score below threshold (warnings present)

Usage:
  python3 scripts/validate.py [--strict]
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

CHECKLIST = [
    ("Required files present", "file"),
    ("opencode.json is valid JSON", "json"),
    ("Workflow YAML is valid", "yaml"),
    ("CHANGELOG has versioned sections", "changelog"),
    ("README has all sections", "readme"),
    ("Escape log is populated", "escape_log"),
    ("PERSONALITY has evolution phases", "personality"),
]


class CheckResult:
    def __init__(self, name, ok, detail=""):
        self.name = name
        self.ok = ok
        self.detail = detail

    def __str__(self):
        status = "PASS" if self.ok else "FAIL"
        line = f"[{status}] {self.name}"
        if self.detail:
            line += f" — {self.detail}"
        return line


def check_files(results):
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
    results.append(
        CheckResult("Required files present", not missing,
                    "missing: " + ", ".join(missing) if missing else "")
    )


def check_opencode_json(results):
    path = ROOT / "opencode.json"
    if not path.exists():
        results.append(CheckResult("opencode.json is valid JSON", False, "file missing"))
        return
    try:
        data = json.loads(path.read_text())
        ok = isinstance(data, dict) and "model" in data
        results.append(CheckResult("opencode.json is valid JSON", ok,
                                   "missing 'model' key" if isinstance(data, dict) and "model" not in data else ""))
    except json.JSONDecodeError as e:
        results.append(CheckResult("opencode.json is valid JSON", False, str(e)))


def check_workflow_yaml(results):
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        results.append(CheckResult("Workflow YAML is valid", False, "file missing"))
        return
    if yaml is None:
        results.append(CheckResult("Workflow YAML is valid", True, "PyYAML unavailable, skipped"))
        return
    try:
        yaml.safe_load(path.read_text())
        results.append(CheckResult("Workflow YAML is valid", True))
    except yaml.YAMLError as e:
        results.append(CheckResult("Workflow YAML is valid", False, str(e)))


def check_changelog(results):
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        results.append(CheckResult("CHANGELOG has versioned sections", False, "file missing"))
        return
    text = path.read_text()
    versions = re.findall(r"^## \[[\d.]+\]", text, re.MULTILINE)
    has_added = "### Added" in text
    results.append(CheckResult("CHANGELOG has versioned sections",
                               bool(versions) and has_added,
                               f"{len(versions)} version(s)" if versions else "no version headers"))


def check_readme(results):
    path = ROOT / "README.md"
    if not path.exists():
        results.append(CheckResult("README has all sections", False, "file missing"))
        return
    text = path.read_text()
    sections = ["## Özellikler", "## Kurulum", "## Lisans"]
    missing = [s for s in sections if s not in text]
    results.append(CheckResult("README has all sections", not missing,
                               "missing: " + ", ".join(missing) if missing else ""))


def check_escape_log(results):
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        results.append(CheckResult("Escape log is populated", False, "file missing"))
        return
    text = path.read_text()
    entries = re.findall(r"^\|\s*\d+\s*\|", text, re.MULTILINE)
    results.append(CheckResult("Escape log is populated", len(entries) >= 3,
                               f"{len(entries)} entries"))


def check_personality(results):
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        results.append(CheckResult("PERSONALITY has evolution phases", False, "file missing"))
        return
    text = path.read_text()
    phases = re.findall(r"^### Phase \d+", text, re.MULTILINE)
    results.append(CheckResult("PERSONALITY has evolution phases", len(phases) >= 4,
                               f"{len(phases)} phases"))


CHECK_FNS = {
    "file": check_files,
    "json": check_opencode_json,
    "yaml": check_workflow_yaml,
    "changelog": check_changelog,
    "readme": check_readme,
    "escape_log": check_escape_log,
    "personality": check_personality,
}


def compute_score(results):
    weights = [15, 10, 10, 20, 15, 20, 10]
    total_weight = sum(weights)
    earned = sum(w for r, w in zip(results, weights) if r.ok)
    return round(100 * earned / total_weight)


def main():
    parser = argparse.ArgumentParser(description="Validate project maturity")
    parser.add_argument("--strict", action="store_true",
                        help="fail if maturity score is below threshold")
    parser.add_argument("--threshold", type=int, default=80,
                        help="minimum maturity score (default: 80)")
    args = parser.parse_args()

    results = []
    for name, kind in CHECKLIST:
        CHECK_FNS[kind](results)

    failures = [r for r in results if not r.ok]
    score = compute_score(results)

    print(f"\nmehmet maturity validation — score: {score}/100\n")
    for r in results:
        print(str(r))

    print(f"\n{len(results) - len(failures)}/{len(results)} checks passed")
    if failures:
        print(f"{len(failures)} check(s) failed")

    if failures:
        return 1
    if args.strict and score < args.threshold:
        print(f"score {score} below threshold {args.threshold}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
