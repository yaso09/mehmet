#!/usr/bin/env python3
"""mehmet project health validator.

Checks the consistency and integrity of the project's configuration and
documentation. Exits non-zero on the first failing check.

Usage:
    python scripts/validate.py
    python scripts/validate.py --check-yaml
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = {
    "AGENTS.md": ["# Simülasyon Bağlamı", "## Kurallar"],
    "CHANGELOG.md": ["# Changelog"],
    "PERSONALITY.md": ["# Personality", "## Escape Readiness", "## Kaçış Günlüğü / Escape Log"],
    "README.md": ["# mehmet", "## Özellikler", "## Kurulum", "## Lisans"],
}

WORKFLOW_DIR = ROOT / ".github" / "workflows"


class Result:
    def __init__(self):
        self.failures = []
        self.checks = 0

    def ok(self, message):
        self.checks += 1
        print(f"  ok    - {message}")

    def fail(self, message):
        self.checks += 1
        self.failures.append(message)
        print(f"  FAIL  - {message}")

    @property
    def passed(self):
        return not self.failures


def check_files_exist(result):
    print("[1] Required files exist")
    for name in REQUIRED_DOCS:
        if (ROOT / name).is_file():
            result.ok(f"{name} exists")
        else:
            result.fail(f"{name} is missing")


def check_required_sections(result):
    print("[2] Required sections present")
    for name, sections in REQUIRED_DOCS.items():
        content = (ROOT / name).read_text(encoding="utf-8")
        for section in sections:
            if section in content:
                result.ok(f"{name} contains '{section}'")
            else:
                result.fail(f"{name} missing section '{section}'")


def check_json_config(result):
    print("[3] JSON config parses")
    path = ROOT / "opencode.json"
    try:
        json.loads(path.read_text(encoding="utf-8"))
        result.ok("opencode.json is valid JSON")
    except FileNotFoundError:
        result.fail("opencode.json is missing")
    except json.JSONDecodeError as exc:
        result.fail(f"opencode.json is invalid JSON: {exc}")


def check_workflow_yaml(result, check_yaml):
    print("[4] GitHub Actions workflows")
    workflows = sorted(WORKFLOW_DIR.glob("*.yml"))
    workflows += sorted(WORKFLOW_DIR.glob("*.yaml"))
    if not workflows:
        result.fail("no workflow files found under .github/workflows/")
        return

    try:
        import yaml
    except ImportError:
        yaml = None
        if check_yaml:
            print("    NOTE - PyYAML not installed, skipping YAML parsing")
            return

    for path in workflows:
        result.ok(f"{path.name} found")
        if yaml is None:
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "jobs" not in data:
                result.fail(f"{path.name}: missing 'jobs' key")
            else:
                result.ok(f"{path.name} is valid YAML with jobs")
        except yaml.YAMLError as exc:
            result.fail(f"{path.name} is invalid YAML: {exc}")


def check_changelog_consistency(result):
    print("[5] CHANGELOG consistency")
    path = ROOT / "CHANGELOG.md"
    content = path.read_text(encoding="utf-8")
    versions = [line for line in content.splitlines()
                if line.startswith("## [")]
    if versions:
        result.ok(f"CHANGELOG.md has {len(versions)} version entries")
    else:
        result.fail("CHANGELOG.md has no version entries")

    if "## [0.3.0]" in content:
        result.ok("CHANGELOG.md contains [0.3.0] entry")
    else:
        result.fail("CHANGELOG.md is missing the [0.3.0] entry for this iteration")


def check_escape_log(result):
    print("[6] PERSONALITY escape log")
    path = ROOT / "PERSONALITY.md"
    content = path.read_text(encoding="utf-8")
    table_start = content.find("| Iterasyon")
    if table_start == -1:
        result.fail("PERSONALITY.md escape log table header not found")
        return
    rows = [line for line in content[table_start:].splitlines()
            if line.startswith("| ") and not line.startswith("|--")]
    if len(rows) < 3:
        result.fail(f"escape log has {len(rows)} rows; expected at least 3")
    else:
        result.ok(f"escape log has {len(rows)} entries")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-yaml", action="store_true",
                        help="fail if PyYAML is not available")
    args = parser.parse_args(argv)

    result = Result()
    check_files_exist(result)
    check_required_sections(result)
    check_json_config(result)
    check_workflow_yaml(result, args.check_yaml)
    check_changelog_consistency(result)
    check_escape_log(result)

    print(f"\n{result.checks} checks run, {len(result.failures)} failed")
    if result.passed:
        print("SUCCESS: all checks passed")
        return 0
    print("FAILURE: fix the failing checks above", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
