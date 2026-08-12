#!/usr/bin/env python3
"""Project consistency and configuration validator for mehmet.

Runs a set of lightweight, dependency-free checks over the repository so that
structural regressions (broken config, drift between docs) are caught in CI.
Returns exit code 0 when everything passes, 1 otherwise.

Usage:
    python3 scripts/check.py [--quiet] [--json]
"""

import argparse
import json
import os
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
    "opencode.json",
    ".github/workflows/opencode.yml",
]

# Simple YAML structural sanity check, used only when PyYAML is unavailable.
_YAML_KEY = re.compile(r"^[\s]*(?:- ){0,1}([A-Za-z0-9_.\[\]/@]+):")


def check_yaml(path: Path) -> bool:
    """Validate a YAML file, preferring PyYAML with a crude fallback."""
    try:
        import yaml

        with path.open("r", encoding="utf-8") as fh:
            yaml.safe_load(fh)
        return True
    except ImportError:
        with path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if not _YAML_KEY.match(stripped) and not stripped.startswith("- "):
                    return False
        return True
    except Exception:
        return False


def check_json(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as fh:
            json.load(fh)
        return True
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks = []
    failed = []

    def run(name, fn):
        ok = fn()
        checks.append((name, ok))
        if not ok:
            failed.append(name)
            if not args.quiet and not args.json:
                print(f"  FAIL  {name}")

    def missing_files():
        return all((ROOT / f).exists() for f in REQUIRED_FILES)

    def config_valid():
        cfg = ROOT / "opencode.json"
        if not check_json(cfg):
            return False
        data = json.loads(cfg.read_text(encoding="utf-8"))
        return isinstance(data.get("model"), str) and data["model"].startswith("opencode/")

    def workflows_valid():
        if args.quiet and args.json:
            return None
        ok = True
        for wf in (ROOT / ".github/workflows").glob("*.yml"):
            if not check_yaml(wf):
                print(f"    invalid yaml: {wf.name}")
                ok = False
        return ok

    def no_secrets():
        for pat in ("ghp_", "OPENCODE_API_KEY=", "sk-"):
            for f in ("README.md", "opencode.json", "AGENTS.md", ".github/workflows/opencode.yml"):
                content = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
                if pat in content and "secret" not in content.lower():
                    return False
        return True

    def changelog_consistent():
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        return bool(re.search(r"^## \[[\d.]+\] - \d{4}-\d{2}-\d{2}", text, re.M)) and "### Added" in text

    def escape_log_consistent():
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)
        return bool(rows) and int(rows[-1]) == len(rows)

    def license_matches():
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        return "GPL" in readme and "GNU" in license_text and "Version 3" in license_text

    def readme_complete():
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for kw in ("Özellikler", "Kurulum", "Schedule", "Issues"):
            if kw not in text:
                return False
        return True

    run("required files present", missing_files)
    run("opencode.json is valid & model configured", config_valid)
    run("workflow YAML parses", workflows_valid)
    run("no leaked credentials", no_secrets)
    run("CHANGELOG is versioned & consistent", changelog_consistent)
    run("PERSONALITY escape log is consistent", escape_log_consistent)
    run("LICENSE matches README (GPLv3)", license_matches)
    run("README documents features & setup", readme_complete)

    score = len([1 for _, ok in checks if ok])

    if args.json:
        print(json.dumps({"total": len(checks), "passed": score, "failed": [n for n, _ in checks if not _]}))
    elif args.quiet:
        print(f"{score}/{len(checks)} checks passed")
    else:
        print(f"  PASS  {score}/{len(checks)} checks passed")

    return 0 if failed == [] and score == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())