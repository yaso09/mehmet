#!/usr/bin/env python3
"""mehmet repository validation.

Runs static correctness and consistency checks on the project. Intended to be
used both locally and in CI (.github/workflows/check.yml). Exits non-zero when
any check fails.

Usage:
    python3 scripts/validate.py
    python3 scripts/validate.py --quiet
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "AGENTS.md",
    "LICENSE",
    "META.json",
    "opencode.json",
    "scripts/maturity.py",
    "scripts/validate.py",
]

KNOWN_OPENCODE_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

VERSION_RE = re.compile(
    r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})", re.MULTILINE
)

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?([^\s'\"]{12,})"),
    re.compile(r"(?i)token\s*[:=]\s*['\"]?([^\s'\"]{12,})"),
    re.compile(r"(?i)secret\s*[:=]\s*['\"]?([^\s'\"]{12,})"),
]

SKIP_SECRET_DIRS = {".git", "node_modules", "scripts"}
SKIP_SECRET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico"}


def _looks_like_credential(value):
    if not value or value.startswith("$") or value.startswith("env:"):
        return False
    if not any(c.isdigit() for c in value):
        return False
    if not any(c.isalpha() for c in value):
        return False
    return len(value) >= 12


def fail(results, name, message):
    results.append((name, False, message))


def ok(results, name, message):
    results.append((name, True, message))


def main():
    parser = argparse.ArgumentParser(description="Validate mehmet repository.")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    results = []

    for f in REQUIRED_FILES:
        path = ROOT / f
        if path.exists():
            ok(results, f"exists:{f}", "present")
        else:
            fail(results, f"exists:{f}", "missing")

    for json_file in ["opencode.json", "META.json"]:
        path = ROOT / json_file
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            ok(results, f"json:{json_file}", "parses")
            if json_file == "opencode.json":
                unknown = [k for k in data if k not in KNOWN_OPENCODE_KEYS]
                if unknown:
                    fail(results, "opencode:keys", f"unknown keys: {unknown}")
                else:
                    ok(results, "opencode:keys", "all keys valid")
        except json.JSONDecodeError as exc:
            fail(results, f"json:{json_file}", f"invalid JSON: {exc}")

    try:
        import yaml  # type: ignore

        for wf in [".github/workflows/opencode.yml", ".github/workflows/check.yml"]:
            path = ROOT / wf
            if not path.exists():
                fail(results, f"workflow:{wf}", "missing")
                continue
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                if not isinstance(data, dict) or "jobs" not in data:
                    fail(results, f"workflow:{wf}", "no 'jobs' key")
                else:
                    ok(results, f"workflow:{wf}", "valid YAML with jobs")
            except yaml.YAMLError as exc:
                fail(results, f"workflow:{wf}", f"invalid YAML: {exc}")
    except ImportError:
        ok(results, "workflow:yaml", "PyYAML unavailable, skipped")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").exists() else ""
    versions = VERSION_RE.findall(changelog)
    if versions:
        ok(results, "changelog:format", f"{len(versions)} version header(s)")
        meta = {}
        if (ROOT / "META.json").exists():
            try:
                meta = json.loads((ROOT / "META.json").read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass
        if meta.get("version") and meta["version"] not in changelog:
            fail(results, "changelog:version", f"META version {meta['version']} not in CHANGELOG")
        else:
            ok(results, "changelog:version", "CHANGELOG and META agree")
    else:
        fail(results, "changelog:format", "no '## [x.y.z] - YYYY-MM-DD' headers")

    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8") if (ROOT / "PERSONALITY.md").exists() else ""
    rows = re.findall(r"^\|\s*\d+\s*\|", personality, flags=re.MULTILINE)
    if rows:
        ok(results, "personality:escape-log", f"{len(rows)} escape log entr(ies)")
    else:
        fail(results, "personality:escape-log", "no escape log table rows")

    secret_hits = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or any(part in SKIP_SECRET_DIRS for part in path.parts):
            continue
        if path.suffix in SKIP_SECRET_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                value = match.group(1)
                if _looks_like_credential(value):
                    secret_hits.append(f"{path.relative_to(ROOT)}:{value[:16]}...")
    if secret_hits:
        fail(results, "security:secrets", "possible secrets: " + "; ".join(secret_hits[:5]))
    else:
        ok(results, "security:secrets", "no obvious secrets")

    failed = [r for r in results if not r[1]]
    for name, passed, message in results:
        if not passed or not args.quiet:
            print(f"{'[FAIL]' if not passed else '[PASS]'} {name}: {message}")

    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()