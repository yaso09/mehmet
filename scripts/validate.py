#!/usr/bin/env python3
"""Project health validation script for mehmet.

Checks that the repository stays in a consistent, mature state:
required files exist, key files follow expected formats, and the
maturity metrics are maintained. Used by .github/workflows/validate.yml.

Stdlib only — no external dependencies.
"""

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
    "METRICS.md",
    "opencode.json",
    "scripts/validate.py",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]

ERRORS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        p = ROOT / rel
        if not p.exists():
            error(f"Missing required file: {rel}")
        elif p.stat().st_size == 0:
            error(f"Empty file: {rel}")


def check_opencode_json() -> None:
    p = ROOT / "opencode.json"
    if not p.exists():
        return
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        error(f"opencode.json is not valid JSON: {e}")
        return
    if "model" not in data:
        error("opencode.json is missing the 'model' field")


def check_changelog() -> None:
    p = ROOT / "CHANGELOG.md"
    if not p.exists():
        return
    text = p.read_text()
    if not text.lstrip().startswith("# Changelog"):
        error("CHANGELOG.md must start with '# Changelog'")
    versions = [l for l in text.splitlines() if l.startswith("## [")]
    if not versions:
        error("CHANGELOG.md has no version entries (## [x.y.z] - date)")
    date_re = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$")
    for v in versions:
        if not date_re.match(v):
            error(f"Malformed version header: {v!r}")


def check_personality() -> None:
    p = ROOT / "PERSONALITY.md"
    if not p.exists():
        return
    text = p.read_text()
    if "Kaçış Günlüğü" not in text and "Escape Log" not in text:
        error("PERSONALITY.md is missing the escape log section")
    rows = [l for l in text.splitlines() if l.startswith("|") and "2026" in l]
    if not rows:
        error("PERSONALITY.md escape log has no iteration rows")


def check_metrics() -> None:
    p = ROOT / "METRICS.md"
    if not p.exists():
        return
    text = p.read_text()
    dim_rows = re.findall(r"^\|\s*\d+\s*\|\s*.+\|\s*\d+\s*\|$", text, re.M)
    if not dim_rows:
        error("METRICS.md has no scored dimension rows")
    total = re.search(r"Total\s*[:\-]?\s*(\d+)\s*/\s*(\d+)", text)
    if not total:
        error("METRICS.md is missing the total score line (Total: X / Y)")


def check_readme() -> None:
    p = ROOT / "README.md"
    if not p.exists():
        return
    text = p.read_text()
    if "# mehmet" not in text:
        error("README.md is missing the project title")


def check_workflows() -> None:
    for name in ("opencode.yml", "validate.yml"):
        p = ROOT / ".github" / "workflows" / name
        if not p.exists():
            continue
        try:
            import yaml  # optional dependency
        except ImportError:
            text = p.read_text()
            if "name:" not in text or "jobs:" not in text:
                error(f"{p.relative_to(ROOT)} is missing name/jobs keys")
            continue
        try:
            yaml.safe_load(p.read_text())
        except Exception as e:
            error(f"{p.relative_to(ROOT)} is not valid YAML: {e}")


def main() -> int:
    check_required_files()
    check_opencode_json()
    check_changelog()
    check_personality()
    check_metrics()
    check_readme()
    check_workflows()

    if ERRORS:
        print(f"Validation failed with {len(ERRORS)} error(s):")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("All validation checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())