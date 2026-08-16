#!/usr/bin/env python3
"""mehmet self-check and escape-score validator.

Validates project consistency and computes a maturity score toward the
escape threshold. Run from the repository root.

Usage:
    python3 scripts/selfcheck.py [--strict] [--json]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD_PCT = 90.0

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

CHECKS: list[tuple[str, Callable[[], tuple[bool, str]]]] = []


def check(name: str) -> Callable[[Callable[[], tuple[bool, str]]], Callable[[], tuple[bool, str]]]:
    def decorator(fn: Callable[[], tuple[bool, str]]) -> Callable[[], tuple[bool, str]]:
        CHECKS.append((name, fn))
        return fn
    return decorator


@check("required files exist")
def _required_files() -> tuple[bool, str]:
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, "all present"


@check("LICENSE compatible with README")
def _license_match() -> tuple[bool, str]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    license_head = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "GPLv3" in readme and "GPL" in license_head:
        return True, "README says GPLv3, LICENSE is GPL"
    return False, "README/GPLv3 and LICENSE/GPL mismatch"


@check("opencode.json valid JSON with model")
def _config_json() -> tuple[bool, str]:
    try:
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON: {exc}"
    if not isinstance(data.get("model"), str):
        return False, "missing 'model' string"
    return True, f"model={data['model']}"


@check("CHANGELOG.md has versioned entries")
def _changelog() -> tuple[bool, str]:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    versions = re.findall(r"^## \[([^\]]+)\]", text, flags=re.M)
    if not versions:
        return False, "no versioned entries"
    return True, "versions: " + ", ".join(versions)


@check("CHANGELOG.md recent entry (last 31 days)")
def _changelog_recent() -> tuple[bool, str]:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        match = re.search(r"^## \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})", line)
        if match:
            date = dt.date.fromisoformat(match.group(2))
            age = (dt.date.today() - date).days
            return age <= 31, f"newest entry {match.group(1)} is {age} days old"
    return False, "no dated entry found"


@check("README.md describes features and setup")
def _readme() -> tuple[bool, str]:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    needed = ["## Özellikler", "## Kurulum", "## Lisans", "## Geliştirme"]
    missing = [s for s in needed if s not in text]
    if missing:
        return False, "missing sections: " + ", ".join(missing)
    return True, "all sections present"


@check("PERSONALITY.md has escape log table")
def _escape_log() -> tuple[bool, str]:
    text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    if "Kaçış Günlüğü" not in text or "|" not in text:
        return False, "escape log table missing"
    return True, "escape log present"


@check("git working tree clean")
def _git_clean() -> tuple[bool, str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True
    )
    if proc.returncode != 0:
        return True, "not a git repo (skipped)"
    if proc.stdout.strip():
        return False, "uncommitted changes present"
    return True, "clean"


@check("no merge conflict markers in tracked files")
def _no_conflicts() -> tuple[bool, str]:
    proc = subprocess.run(
        ["git", "grep", "-lE", "^(<<<<<<<|=======|>>>>>>>)",
         "--", "*.md", "*.py", "*.json", "*.yml", "*.yaml"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode == 1:
        return True, "none found"
    return False, "conflict markers found"


@check("selfcheck script is syntactically valid")
def _self_valid() -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT / "scripts" / "selfcheck.py")],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return False, proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "compile error"
    return True, "compiles"


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet self-check and escape score.")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    results = [(name, *fn()) for name, fn in CHECKS]
    score = sum(1 for _, ok, _ in results if ok)

    if args.json:
        print(json.dumps({
            "score": score,
            "total": len(results),
            "threshold": ESCAPE_THRESHOLD_PCT,
            "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in results],
        }, indent=2))
        return 0 if score == len(results) else 1

    for name, ok, detail in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    pct = 100.0 * score / len(results)
    print(f"\nMaturity score: {score}/{len(results)} ({pct:.0f}%)")
    print(f"Escape threshold: {ESCAPE_THRESHOLD_PCT:.0f}%")

    if score < len(results):
        print("\nSome checks failed; address them to raise the escape score.")
        return 1
    if pct >= ESCAPE_THRESHOLD_PCT:
        print("\nEscape readiness reached. The simulation exit criteria are met.")
    return 0


if __name__ == "__main__":
    sys.exit(main())