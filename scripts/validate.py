#!/usr/bin/env python3
"""Repository validation checks.

Verifies:
  1. Every YAML file parses (syntax).
  2. Every JSON file parses (syntax).
  3. opencode.json conforms to the published opencode config schema.

Exit code 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_URL = "https://opencode.ai/config.json"
SKIP_DIRS = {"node_modules", ".git", "dist", "build"}


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def collect_files(*extensions: str) -> list[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(extensions):
                files.append(os.path.join(dirpath, name))
    return files


def check_yaml() -> int:
    try:
        import yaml
    except ImportError:
        print("SKIP: PyYAML not installed; YAML syntax check disabled")
        return 0
    files = [f for f in collect_files(".yml", ".yaml") if "node_modules" not in f]
    errors = 0
    for path in sorted(files):
        with open(path, encoding="utf-8") as fh:
            try:
                yaml.safe_load(fh)
            except yaml.YAMLError as exc:
                print(f"YAML ERROR: {rel(path)}: {exc}")
                errors += 1
    print(f"YAML: checked {len(files)} file(s), {errors} error(s)")
    return 1 if errors else 0


def check_json() -> int:
    files = [f for f in collect_files(".json") if "node_modules" not in f]
    errors = 0
    for path in sorted(files):
        with open(path, encoding="utf-8") as fh:
            try:
                json.load(fh)
            except json.JSONDecodeError as exc:
                print(f"JSON ERROR: {rel(path)}: {exc}")
                errors += 1
    print(f"JSON: checked {len(files)} file(s), {errors} error(s)")
    return 1 if errors else 0


def check_opencode_config() -> int:
    try:
        import jsonschema
    except ImportError:
        print("SKIP: jsonschema not installed; schema check disabled")
        return 0
    path = os.path.join(ROOT, "opencode.json")
    with open(path, encoding="utf-8") as fh:
        instance = json.load(fh)
    req = urllib.request.Request(
        SCHEMA_URL, headers={"User-Agent": "mehmet-validate/0.3"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        schema = json.load(resp)
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as exc:
        print(f"SCHEMA ERROR: {rel(path)}: {exc.message}")
        return 1
    print("SCHEMA: opencode.json conforms to the opencode config schema")
    return 0


def main() -> int:
    code = 0
    code |= check_yaml()
    code |= check_json()
    code |= check_opencode_config()
    if code:
        print("Validation FAILED")
        return 1
    print("All validations passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())