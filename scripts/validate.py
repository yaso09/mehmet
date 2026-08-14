#!/usr/bin/env python3
"""Project integrity validator for mehmet.

Checks that the core simulation files exist, configs are well-formed,
and documentation rules are followed. Used by CI (see .github/workflows/ci.yml).

Usage:
    python scripts/validate.py
"""

import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "MATURITY.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
]

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def load_yaml(path):
    if yaml is None:
        check(False, f"{path.name}: PyYAML is required to validate workflow")
        return None
    try:
        return yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        check(False, f"{path.name}: invalid YAML: {exc}")
        return None


def main():
    # 1. Required files exist
    for rel in REQUIRED_FILES:
        check((ROOT / rel).is_file(), f"missing required file: {rel}")

    # 2. opencode.json is valid JSON and defines a model
    cfg_path = ROOT / "opencode.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text())
            check("model" in cfg, "opencode.json must define a model")
        except json.JSONDecodeError as exc:
            check(False, f"opencode.json is not valid JSON: {exc}")

    # 3. Workflows are valid YAML with triggers
    for rel in WORKFLOWS:
        path = ROOT / rel
        if not path.is_file():
            continue
        doc = load_yaml(path)
        if doc is None:
            continue
        check(isinstance(doc, dict) and "jobs" in doc,
              f"{rel}: must be a mapping with a jobs section")
        check(("on" in doc) or (True in doc),
              f"{rel}: must define triggers (on:)")

    # 4. opencode.yml must guard against concurrent runs
    opencode_wf = ROOT / ".github/workflows/opencode.yml"
    if opencode_wf.is_file():
        doc = load_yaml(opencode_wf)
        if doc is not None:
            check("concurrency" in doc,
                  "opencode.yml must define concurrency")

    # 5. CHANGELOG follows the version-section format
    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        text = changelog.read_text()
        check(bool(re.search(r"^## \[.+?\] - \d{4}-\d{2}-\d{2}$", text, re.M)),
              "CHANGELOG.md must contain a version section (## [x.y.z] - YYYY-MM-DD)")

    # 6. PERSONALITY exposes the escape log
    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        text = personality.read_text()
        check(("## Kaçış Günlüğü" in text) or ("## Escape Log" in text),
              "PERSONALITY.md must contain an escape log section")

    # 7. MATURITY defines the threshold and a dated score
    maturity = ROOT / "MATURITY.md"
    if maturity.is_file():
        text = maturity.read_text()
        check(("Kaçış Eşiği" in text) or ("Escape Threshold" in text),
              "MATURITY.md must define the escape threshold")
        check(bool(re.search(r"\| \d{4}-\d{2}-\d{2} \| \d+ \|", text)),
              "MATURITY.md must contain a dated score row")

    # 8. README references the maturity tracker
    readme = ROOT / "README.md"
    if readme.is_file():
        check("MATURITY.md" in readme.read_text(),
              "README.md must reference MATURITY.md")

    if failures:
        print("Validation FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)

    print("Validation PASSED: all project integrity checks succeeded.")
    sys.exit(0)


if __name__ == "__main__":
    main()