#!/usr/bin/env python3
"""mehmet repo health & maturity validator.

Checks required files exist, configs parse, and the changelog is sane.
Exits non-zero on failure so CI can gate the escape progress.

Usage:
    python3 scripts/validate.py
    python3 scripts/validate.py --repo <path>
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

JSON_FILES = ["opencode.json"]

WORKFLOW_DIR = ".github/workflows"

CHANGELOG_SECTIONS = ["### Added", "### Fixed", "### Changed"]


class CheckResult:
    def __init__(self):
        self.failures = []
        self.passes = 0

    def ok(self, name):
        self.passes += 1
        print(f"  [PASS] {name}")

    def fail(self, name, detail=""):
        full = f"{name} — {detail}" if detail else name
        self.failures.append(full)
        print(f"  [FAIL] {full}")


def _load_json(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_yaml(path):
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyYAML required for YAML validation (pip install pyyaml)") from exc
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validate(repo: Path) -> CheckResult:
    result = CheckResult()

    for rel in REQUIRED_FILES:
        path = repo / rel
        if path.is_file():
            result.ok(f"exists {rel}")
        else:
            result.fail("missing file", rel)

    for rel in JSON_FILES:
        path = repo / rel
        if path.is_file():
            try:
                data = _load_json(path)
                if isinstance(data, dict) and data.get("model"):
                    result.ok(f"json {rel} (model={data['model']})")
                else:
                    result.fail(f"json {rel}", "missing 'model' key")
            except (json.JSONDecodeError, OSError) as exc:
                result.fail(f"json {rel}", str(exc))

    workflows = repo / WORKFLOW_DIR
    if workflows.is_dir():
        for wf in sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml")):
            rel = f"{WORKFLOW_DIR}/{wf.name}"
            try:
                data = _load_yaml(wf)
                if isinstance(data, dict) and data.get("jobs"):
                    result.ok(f"yaml {rel}")
                else:
                    result.fail(f"yaml {rel}", "missing 'jobs' key")
            except Exception as exc:
                result.fail(f"yaml {rel}", str(exc))

    changelog = repo / "CHANGELOG.md"
    if changelog.is_file():
        text = changelog.read_text(encoding="utf-8")
        if "## [" in text:
            result.ok("changelog has versioned entries")
        else:
            result.fail("changelog", "no '## [x.y.z]' entries")
        for section in CHANGELOG_SECTIONS:
            if section in text:
                result.ok(f"changelog section {section}")
                break
        else:
            result.fail("changelog", f"none of {CHANGELOG_SECTIONS} sections present")

    readme = repo / "README.md"
    if readme.is_file() and "mehmet" in readme.read_text(encoding="utf-8").lower():
        result.ok("readme mentions project")
    else:
        result.fail("readme", "does not mention project")

    personality = repo / "PERSONALITY.md"
    if personality.is_file() and "Kaçış Günlüğü" in personality.read_text(encoding="utf-8"):
        result.ok("personality has escape log")
    else:
        result.fail("personality", "missing escape log section")

    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root (default: current dir)")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    print(f"Validating repository: {repo}")
    result = validate(repo)

    print(f"\n{result.passes} checks passed, {len(result.failures)} failed")
    if result.failures:
        print("Failures:")
        for failure in result.failures:
            print(f"  - {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())