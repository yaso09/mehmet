#!/usr/bin/env python3
"""mehmet project integrity validator.

Validates the self-improving agent's repository state so every change is
verifiable. Exits non-zero if any check fails. Pure stdlib, no dependencies.

Checks:
  1. Required files exist.
  2. opencode.json is valid JSON and uses only schema-known keys.
  3. CHANGELOG.md has at least one semantic version entry.
  4. PERSONALITY.md contains a non-empty escape log table.
  5. METRICS.md scores are integers in the 0..10 range and match the table.
  6. GitHub Actions workflow contains the expected jobs.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "METRICS.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".yamllint",
    ".github/workflows/opencode.yml",
]

# Top-level keys accepted by https://opencode.ai/config.json (Config properties).
OPCODE_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills", "references",
    "reference", "watcher", "snapshot", "plugin", "share", "autoshare",
    "autoupdate", "disabled_providers", "enabled_providers", "model",
    "small_model", "default_agent", "subagent_depth", "username", "mode",
    "agent", "provider", "mcp", "formatter", "lsp", "instructions", "layout",
    "permission", "tools", "attachment", "enterprise", "tool_output",
    "compaction", "experimental",
}

VERSION_RE = re.compile(r"^## \[(\d+)\.(\d+)\.(\d+)\] - \d{4}-\d{2}-\d{2}$")
METRIC_RE = re.compile(r"^\d+$")

EXPECTED_JOBS = {"autonomous", "comment", "validate"}

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if ok:
        print(f"  ok: {message}")
    else:
        failures.append(message)
        print(f"FAIL: {message}")


def check_files() -> None:
    print("1. Required files")
    for name in REQUIRED_FILES:
        check((ROOT / name).is_file(), f"{name} exists")


def check_opencode() -> None:
    print("2. opencode.json")
    path = ROOT / "opencode.json"
    if not path.is_file():
        check(False, "opencode.json missing")
        return
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        check(False, f"opencode.json is not valid JSON: {exc}")
        return
    check(isinstance(data, dict), "opencode.json is a JSON object")
    if isinstance(data, dict):
        unknown = sorted(set(data) - OPCODE_KEYS)
        check(not unknown, f"opencode.json has no unknown keys (found: {unknown})")
        check("model" in data, "opencode.json declares a model")


def check_changelog() -> None:
    print("3. CHANGELOG.md")
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        check(False, "CHANGELOG.md missing")
        return
    versions = [ln for ln in path.read_text().splitlines() if VERSION_RE.match(ln)]
    check(len(versions) >= 1, f"CHANGELOG.md has >=1 version entry (found {len(versions)})")
    check("## [Unreleased]" in path.read_text(), "CHANGELOG.md tracks an Unreleased section")


def check_personality() -> None:
    print("4. PERSONALITY.md")
    path = ROOT / "PERSONALITY.md"
    if not path.is_file():
        check(False, "PERSONALITY.md missing")
        return
    text = path.read_text()
    check("Kaçış Günlüğü / Escape Log" in text, "escape log section present")
    rows = [ln for ln in text.splitlines() if ln.startswith("| ") and not ln.startswith("|---")]
    data_rows = [ln for ln in rows if "Iterasyon" not in ln and "İlerleme" not in ln]
    check(len(data_rows) >= 1, f"escape log has >=1 entry (found {len(data_rows)})")


def check_metrics() -> None:
    print("5. METRICS.md")
    path = ROOT / "METRICS.md"
    if not path.is_file():
        check(False, "METRICS.md missing")
        return
    text = path.read_text()
    check("Escape Threshold" in text or "Kaçış Eşiği" in text, "escape threshold documented")
    scores = []
    for ln in text.splitlines():
        if ln.startswith("|") and not ln.startswith("|---"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if len(cells) >= 3:
                m = METRIC_RE.match(cells[-2])
                if m:
                    scores.append(int(m.group(0)))
    check(len(scores) >= 5, f"at least 5 metric scores present (found {len(scores)})")
    in_range = all(0 <= s <= 10 for s in scores)
    check(in_range, f"all scores are integers in 0..10 (found: {scores})")


def check_workflow() -> None:
    print("6. Workflow")
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.is_file():
        check(False, "workflow missing")
        return
    text = path.read_text()
    for job in EXPECTED_JOBS:
        check(f"  {job}:" in text, f"job '{job}' declared")


def main() -> int:
    check_files()
    check_opencode()
    check_changelog()
    check_personality()
    check_metrics()
    check_workflow()
    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s) failed")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())