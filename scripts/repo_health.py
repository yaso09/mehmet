#!/usr/bin/env python3
"""mehmet repo health checker.

Validates that the project maintains a healthy structure so the agent can
track its own maturity over time. Exits non-zero if any check fails.

Usage:
    python3 scripts/repo_health.py [--root PATH]
"""

import argparse
import json
import os
import re
import sys

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"OPENCODE_API_KEY\s*[:=]\s*['\"]?[^'\"]{16,}"),
]

CHECK_MARK = "[OK]"
FAIL_MARK = "[FAIL]"


class HealthError(Exception):
    pass


def check_required_files(root):
    for relpath in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, relpath)):
            raise HealthError(f"eksik dosya: {relpath}")


def check_changelog(root):
    path = os.path.join(root, "CHANGELOG.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if not re.search(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}", content, re.MULTILINE):
        raise HealthError("CHANGELOG.md'de geçerli bir sürüm başlığı bulunamadı")


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


def check_opencode_json(root):
    path = os.path.join(root, "opencode.json")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not data.get("model"):
        raise HealthError("opencode.json'da 'model' tanımlı değil")
    unknown = sorted(set(data) - ALLOWED_OPENCODE_KEYS)
    if unknown:
        raise HealthError(
            "opencode.json'da geçersiz anahtar(lar): " + ", ".join(unknown)
        )


def check_personality(root):
    path = os.path.join(root, "PERSONALITY.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if "Kaçış Günlüğü" not in content and "Escape Log" not in content:
        raise HealthError("PERSONALITY.md'de kaçış günlüğü bölümü yok")


def check_readme(root):
    path = os.path.join(root, "README.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if "mehmet" not in content:
        raise HealthError("README.md'de proje adı geçmiyor")


def check_no_secrets(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", ".firecrawl", "tests")]
        for name in filenames:
            if name.endswith(".pyc"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in SECRET_PATTERNS:
                for match in pattern.finditer(content):
                    if "${{" in match.group(0):
                        continue
                    raise HealthError(f"şüpheli secret bulundu: {path}")


CHECKS = [
    ("Zorunlu dosyalar", check_required_files),
    ("CHANGELOG formatı", check_changelog),
    ("opencode.json geçerliliği", check_opencode_json),
    ("PERSONALITY kaçış günlüğü", check_personality),
    ("README içeriği", check_readme),
    ("Secret sızıntısı", check_no_secrets),
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="proje kök dizini")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    failures = 0
    for name, check in CHECKS:
        try:
            check(root)
            print(f"{CHECK_MARK} {name}")
        except HealthError as exc:
            failures += 1
            print(f"{FAIL_MARK} {name}: {exc}")

    total = len(CHECKS)
    print(f"\n{total - failures}/{total} kontrol başarılı")
    if failures:
        print(f"{failures} kontrol BAŞARISIZ oldu")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
