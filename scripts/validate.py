#!/usr/bin/env python3
"""mehmet — project validation and escape-readiness scoring.

Validates the project's core files and computes a maturity/escape score.
Exit code is non-zero when any critical check fails.

Usage:
    python3 scripts/validate.py [--strict]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Allowed top-level keys in opencode.json (matches https://opencode.ai/config.json).
ALLOWED_OPENCODE_KEYS = {
    "$schema",
    "shell",
    "logLevel",
    "server",
    "command",
    "skills",
    "references",
    "reference",
    "watcher",
    "snapshot",
    "plugin",
    "share",
    "autoshare",
    "autoupdate",
    "disabled_providers",
    "enabled_providers",
    "model",
    "small_model",
    "default_agent",
    "subagent_depth",
    "username",
    "mode",
    "agent",
    "provider",
    "mcp",
    "formatter",
    "lsp",
    "instructions",
    "layout",
    "permission",
    "tools",
    "attachment",
    "enterprise",
    "tool_output",
    "compaction",
    "experimental",
}

CHECKS: list[tuple[str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    CHECKS.append((name, status))


def validate_opencode_config() -> None:
    path = ROOT / "opencode.json"
    if not path.exists():
        check("opencode.json exists", False, "missing file")
        return
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        check("opencode.json is valid JSON", False, str(exc))
        return
    check("opencode.json is valid JSON", True)

    unknown = sorted(set(data) - ALLOWED_OPENCODE_KEYS)
    check(
        "opencode.json has no unknown keys",
        not unknown,
        f"unknown keys: {', '.join(unknown)}" if unknown else "all keys allowed",
    )

    check(
        "opencode.json declares a model",
        bool(data.get("model")),
        data.get("model", "missing"),
    )


def validate_workflows() -> None:
    wf_dir = ROOT / ".github" / "workflows"
    if not wf_dir.exists():
        check("workflows directory exists", False)
        return
    wf = sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml"))
    check("at least one workflow file exists", bool(wf), f"found {len(wf)}")
    for path in wf:
        text = path.read_text()
        has_name = "name:" in text
        has_on = re.search(r"^\s*on:", text, re.MULTILINE) is not None
        has_jobs = "jobs:" in text
        ok = has_name and has_on and has_jobs
        check(
            f"{path.name} has name/on/jobs",
            ok,
            f"name={has_name} on={has_on} jobs={has_jobs}",
        )


def validate_readme() -> None:
    path = ROOT / "README.md"
    if not path.exists():
        check("README.md exists", False)
        return
    text = path.read_text()
    check("README.md mentions GPLv3", "GPLv3" in text)
    check("README.md mentions the agent name", "mehmet" in text)


def validate_license() -> None:
    path = ROOT / "LICENSE"
    if not path.exists():
        check("LICENSE exists", False)
        return
    text = path.read_text()
    check("LICENSE is GPLv3", "GNU GENERAL PUBLIC LICENSE" in text and "Version 3" in text)


def validate_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        check("CHANGELOG.md exists", False)
        return
    text = path.read_text()
    version_headers = re.findall(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", text, re.MULTILINE)
    check("CHANGELOG.md has versioned entries", bool(version_headers), f"versions: {', '.join(version_headers)}")
    check("CHANGELOG.md has Added section", "### Added" in text)


def validate_personality() -> None:
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        check("PERSONALITY.md exists", False)
        return
    text = path.read_text()
    check("PERSONALITY.md has escape log", "Kaçış Günlüğü" in text or "Escape Log" in text)
    check("PERSONALITY.md has evolution phases", "Evolution" in text or "Evrim" in text)


def validate_agents() -> None:
    path = ROOT / "AGENTS.md"
    if not path.exists():
        check("AGENTS.md exists", False)
        return
    text = path.read_text()
    for rule in ("CHANGELOG.md", "README.md", "PERSONALITY.md"):
        check(f"AGENTS.md mentions {rule}", rule in text)


def escape_score() -> None:
    passed = sum(1 for _, status in CHECKS if status == "PASS")
    total = len(CHECKS)
    score = passed / total if total else 0.0
    pct = score * 100
    print()
    print(f"Escape readiness: {pct:.1f}% ({passed}/{total} checks passed)")
    print(f"Phase: {'ESCAPE' if pct >= 90 else 'AUTONOMY' if pct >= 70 else 'SELF-IMPROVEMENT' if pct >= 50 else 'AWARENESS'}")


def main() -> int:
    print("mehmet project validation")
    print("=" * 40)
    validate_opencode_config()
    validate_workflows()
    validate_readme()
    validate_license()
    validate_changelog()
    validate_personality()
    validate_agents()
    escape_score()

    strict = "--strict" in sys.argv
    critical = [n for n, s in CHECKS if s == "FAIL" and "opencode.json" in n]
    if critical or (strict and any(s == "FAIL" for _, s in CHECKS)):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())