#!/usr/bin/env python3
"""Project health verification.

Checks the structural integrity of the mehmet project. Exits with a
non-zero code if any check fails so it can be used as a CI gate.

Usage:
    python3 scripts/healthcheck.py [--json]
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "VERSION",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def _read(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    with open(full, encoding="utf-8") as fh:
        return fh.read()


def _version():
    content = _read("VERSION")
    if content is None:
        return None
    match = re.search(r"\d+\.\d+\.\d+", content)
    return match.group(0) if match else None


def check_files():
    missing = [f for f in REQUIRED_FILES if _read(f) is None]
    return (
        "required files exist",
        not missing,
        "missing: " + ", ".join(missing) if missing else "all present",
    )


def check_license():
    content = _read("LICENSE")
    if content is None:
        return ("license is GPLv3", False, "LICENSE missing")
    return (
        "license is GPLv3",
        "GNU GENERAL PUBLIC LICENSE" in content and "Version 3" in content,
        "GPLv3 header present" if "GPLv3" in content else "not GPLv3",
    )


def check_opencode_json():
    content = _read("opencode.json")
    if content is None:
        return ("opencode.json valid JSON", False, "missing")
    try:
        data = json.loads(content)
    except ValueError as exc:
        return ("opencode.json valid JSON", False, str(exc))
    return (
        "opencode.json valid JSON",
        isinstance(data, dict) and data.get("model"),
        "model = " + str(data.get("model")),
    )


def check_workflow_yaml():
    content = _read(".github/workflows/opencode.yml")
    if content is None:
        return ("workflow YAML valid", False, "missing")
    if yaml is None:
        return ("workflow YAML valid", True, "pyyaml unavailable, skipped")
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return ("workflow YAML valid", False, str(exc))
    jobs = data.get("jobs", {}) if isinstance(data, dict) else {}
    return (
        "workflow YAML valid",
        bool(jobs),
        "jobs: " + ", ".join(jobs),
    )


def check_version_consistency():
    version = _version()
    changelog = _read("CHANGELOG.md") or ""
    readme = _read("README.md") or ""
    if version is None:
        return ("VERSION consistent with CHANGELOG", False, "VERSION missing")
    ok = f"[{version}]" in changelog and version in readme
    return (
        "VERSION consistent with CHANGELOG/README",
        ok,
        f"version {version}",
    )


def check_changelog():
    changelog = _read("CHANGELOG.md") or ""
    releases = re.findall(r"## \[\d+\.\d+\.\d+\]", changelog)
    return (
            "CHANGELOG has versioned entries",
            bool(releases),
            f"{len(releases)} releases",
        )


def check_personality():
    content = _read("PERSONALITY.md") or ""
    return (
        "PERSONALITY has escape log",
        "Kaçış Günlüğü" in content and "| Iterasyon |" in content,
        "escape log table present" if "| Iterasyon |" in content else "missing",
    )


def check_readme():
    readme = _read("README.md") or ""
    return (
        "README documents license",
        "GPLv3" in readme and "Lisans" in readme,
        "license section present" if "Lisans" in readme else "missing",
    )


def check_gitignore():
    content = _read(".gitignore") or ""
    return (
        ".gitignore excludes secrets",
        ".env" in content,
        "secrets excluded" if ".env" in content else ".env not ignored",
    )


def all_checks():
    return [
        check_files(),
        check_license(),
        check_opencode_json(),
        check_workflow_yaml(),
        check_version_consistency(),
        check_changelog(),
        check_personality(),
        check_readme(),
        check_gitignore(),
    ]


def run():
    checks = all_checks()
    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    if "--json" in sys.argv:
        print(json.dumps({"passed": passed, "total": total, "checks": checks}))
    else:
        for name, ok, detail in checks:
            print(f"[{'OK' if ok else 'FAIL'}] {name}: {detail}")
        print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run())