#!/usr/bin/env python3
"""mehmet repo health validation.

Validates the project's core artifacts so every iteration leaves the repo in a
consistent, escape-ready state. Stdlib only (Python 3.8+).

Usage:
    python3 scripts/check.py            # validate, exit 1 on errors
    python3 scripts/check.py --strict   # treat warnings as errors
"""

import argparse
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
    "LICENSE",
    "VERSION",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

# Valid top-level keys of opencode.json (opencode.ai/config.json -> $defs/Config)
OPCODE_TOP_LEVEL_KEYS = {
    "$schema",
    "agent",
    "attachment",
    "autoshare",
    "autoupdate",
    "command",
    "compaction",
    "default_agent",
    "disabled_providers",
    "enabled_providers",
    "enterprise",
    "experimental",
    "formatter",
    "instructions",
    "layout",
    "logLevel",
    "lsp",
    "mcp",
    "mode",
    "model",
    "permission",
    "plugin",
    "provider",
    "reference",
    "references",
    "server",
    "share",
    "shell",
    "skills",
    "small_model",
    "snapshot",
    "subagent_depth",
    "tool_output",
    "tools",
    "username",
    "watcher",
}

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SECRET_PATTERNS = [
    re.compile(r"(?i)(?:api[_-]?key|token|secret)\s*[:=]\s*[\"']?sk-"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
]


class Checks:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def check_required_files(c: Checks):
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            c.error(f"missing required file: {rel}")


def check_opencode_config(c: Checks):
    path = ROOT / "opencode.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        c.error(f"opencode.json is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        c.error("opencode.json root must be a JSON object")
        return
    unknown = sorted(k for k in data if k not in OPCODE_TOP_LEVEL_KEYS)
    for key in unknown:
        c.error(f"opencode.json has unknown top-level key '{key}'")
    if "model" not in data:
        c.error("opencode.json must define a 'model'")


def check_version(c: Checks):
    version_path = ROOT / "VERSION"
    if not version_path.exists():
        return
    version = version_path.read_text().strip()
    if not SEMVER.match(version):
        c.error(f"VERSION '{version}' is not a valid semver (X.Y.Z)")
    changelog_path = ROOT / "CHANGELOG.md"
    if not changelog_path.exists():
        return
    changelog = changelog_path.read_text()
    if f"## [{version}]" not in changelog:
        c.error(f"CHANGELOG.md has no entry for version {version}")
    latest = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.M)
    if latest and latest.group(1) != version:
        c.error(f"CHANGELOG.md latest entry {latest.group(1)} != VERSION {version}")


def check_changelog(c: Checks):
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        return
    changelog = path.read_text()
    if "### Added" not in changelog:
        c.warn("CHANGELOG.md has no '### Added' section")


def check_readme(c: Checks):
    path = ROOT / "README.md"
    if not path.exists():
        return
    readme = path.read_text()
    for section in ("## Özellikler", "## Kurulum", "## Lisans"):
        if section not in readme:
            c.warn(f"README.md is missing section '{section}'")


def check_personality(c: Checks):
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        return
    text = path.read_text()
    if "Kaçış Günlüğü" not in text and "Escape Log" not in text:
        c.error("PERSONALITY.md is missing the escape log section")


def check_workflow(c: Checks):
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        return
    text = path.read_text()
    if "model: opencode/" not in text:
        c.error("opencode.yml is missing model configuration")
    if "OPENCODE_API_KEY" not in text:
        c.error("opencode.yml does not reference the OPENCODE_API_KEY secret")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            c.error("opencode.yml contains a hardcoded secret-like token")


def check_tracked_secrets(c: Checks):
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            text = path.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                c.error(f"{rel} contains a secret-like token")


def run_checks(c: Checks):
    check_required_files(c)
    check_opencode_config(c)
    check_version(c)
    check_changelog(c)
    check_readme(c)
    check_personality(c)
    check_workflow(c)
    check_tracked_secrets(c)


def run(strict: bool) -> int:
    c = Checks()
    run_checks(c)

    for msg in c.errors:
        print(f"[ERROR] {msg}")
    for msg in c.warnings:
        print(f"[WARN ] {msg}")

    failed = bool(c.errors) or (strict and bool(c.warnings))
    if failed:
        print(f"check failed: {len(c.errors)} error(s), {len(c.warnings)} warning(s)")
    else:
        print(f"check ok: {len(c.errors)} error(s), {len(c.warnings)} warning(s)")
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description="Validate mehmet repo health.")
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors"
    )
    args = parser.parse_args()
    sys.exit(run(strict=args.strict))


if __name__ == "__main__":
    main()