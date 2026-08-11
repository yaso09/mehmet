#!/usr/bin/env python3
"""Project structure validator for mehmet.

Runs from any directory; walks up to the repo root. Exits non-zero on failure.

Checks:
  1. Required markdown files exist and are non-empty
  2. opencode.json is valid JSON and pins a model
  3. Workflow YAML files parse (via yq if available)
  4. CHANGELOG.md uses the "## [x.y.z] - YYYY-MM-DD" format
  5. PERSONALITY.md contains an escape log table
  6. README.md references only existing local paths
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md"]
CHANGELOG_HEADING = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}")
LINK_REF = re.compile(r"\]\(([^)#][^)]*)\)")


def log(ok: bool, msg: str) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {msg}")


def check_markdown_files() -> int:
    failures = 0
    print("1. Required markdown files")
    for name in REQUIRED:
        f = ROOT / name
        ok = f.is_file() and f.stat().st_size > 0
        log(ok, f"{name} exists and non-empty")
        failures += 0 if ok else 1
    return failures


def check_opencode_json() -> int:
    print("2. opencode.json")
    f = ROOT / "opencode.json"
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        ok = bool(data.get("model"))
        log(ok, f"valid JSON with model={data.get('model')!r}")
        return 0 if ok else 1
    except (json.JSONDecodeError, FileNotFoundError) as e:
        log(False, f"could not parse: {e}")
        return 1


def check_workflows() -> int:
    print("3. Workflow YAML files")
    wf_dir = ROOT / ".github" / "workflows"
    if not wf_dir.is_dir():
        log(False, "no workflows directory")
        return 1
    failures = 0
    for f in sorted(wf_dir.glob("*.yml")):
        if shutil.which("yq"):
            proc = subprocess.run(["yq", "eval", "keys", str(f)], capture_output=True, text=True)
            ok = proc.returncode == 0
            log(ok, f"{f.name} parses")
        else:
            text = f.read_text(encoding="utf-8")
            ok = text.startswith("name:") and "jobs:" in text
            log(ok, f"{f.name} has name + jobs (yq not installed)")
        failures += 0 if ok else 1
    return failures


def check_changelog() -> int:
    print("4. CHANGELOG.md format")
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    headings = [line for line in text.splitlines() if line.startswith("## [")]
    ok = bool(headings) and all(CHANGELOG_HEADING.match(h) for h in headings)
    log(ok, f"{len(headings)} version heading(s), format valid")
    return 0 if ok else 1


def check_personality() -> int:
    print("5. PERSONALITY.md escape log")
    text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    ok = "Kaçış Günlüğü" in text and "| Iterasyon |" in text
    log(ok, "escape log table present")
    return 0 if ok else 1


def check_readme_links() -> int:
    print("6. README.md local links")
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    failures = 0
    for target in LINK_REF.findall(text):
        if target.startswith("http"):
            continue
        target = target.split("#")[0]
        if not target or not (ROOT / target).exists():
            log(False, f"broken link: {target}")
            failures += 1
    if failures == 0:
        log(True, "all local links resolve")
    return failures


def main() -> int:
    print(f"Validating project at {ROOT}")
    total = 0
    total += check_markdown_files()
    total += check_opencode_json()
    total += check_workflows()
    total += check_changelog()
    total += check_personality()
    total += check_readme_links()
    print(f"\n{total} failure(s) detected")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
