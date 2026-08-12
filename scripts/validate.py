#!/usr/bin/env python3
"""Project health validation for mehmet.

Checks structural conventions: required files, valid JSON/YAML, changelog
format, license consistency and secret leakage. Run with
`python3 scripts/validate.py`. Exits non-zero if any check fails.
"""

import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    ".gitignore",
    "opencode.json",
]

WORKFLOWS = [
    os.path.join(".github", "workflows", "opencode.yml"),
]

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
]

SKIP_SECRET_SCAN_DIRS = {".git", "node_modules", "__pycache__"}

CHANGELOG_HEADER_RE = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$", re.M)


def _walk_tracked(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_SECRET_SCAN_DIRS]
        for name in files:
            if name.endswith((".pyc", ".pyo")):
                continue
            yield os.path.join(base, name)


def validate(root=ROOT):
    """Run all checks; return (errors, warnings)."""
    errors = []
    warnings = []

    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            errors.append(f"Eksik dosya: {rel}")

    # JSON validity
    for rel in ("opencode.json",):
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    json.load(fh)
            except (OSError, ValueError) as exc:
                errors.append(f"{rel} geçersiz JSON: {exc}")

    # YAML workflow validity
    for rel in WORKFLOWS:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    yaml.safe_load(fh)
            except (OSError, yaml.YAMLError) as exc:
                errors.append(f"{rel} geçersiz YAML: {exc}")
        else:
            errors.append(f"Eksik workflow: {rel}")

    # CHANGELOG format
    changelog = os.path.join(root, "CHANGELOG.md")
    if os.path.isfile(changelog):
        with open(changelog, encoding="utf-8") as fh:
            content = fh.read()
        if not CHANGELOG_HEADER_RE.search(content):
            warnings.append("CHANGELOG.md başlık formatı beklendiği gibi değil (## [x.y.z] - YYYY-MM-DD)")

    # License consistency
    readme = os.path.join(root, "README.md")
    license_file = os.path.join(root, "LICENSE")
    if os.path.isfile(readme) and os.path.isfile(license_file):
        with open(license_file, encoding="utf-8") as fh:
            license_text = fh.read()
        is_gplv3 = "GNU GENERAL PUBLIC LICENSE" in license_text and "Version 3" in license_text
        with open(readme, encoding="utf-8") as fh:
            readme_text = fh.read()
        if is_gplv3 and "GPLv3" not in readme_text:
            warnings.append("README.md lisans bilgisi LICENSE ile uyumsuz (GPLv3 bekleniyor)")

    # Secret leakage scan
    for path in _walk_tracked(root):
        rel = os.path.relpath(path, root)
        if rel.startswith((".git",)) or os.path.basename(rel) in ("CHANGELOG.md",):
            continue
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(f"Gizli bilgi şüphesi ({pattern.pattern}) -> {rel}")
                break

    return errors, warnings


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    verbose = "--verbose" not in argv
    errors, warnings = validate()
    print("=" * 60)
    print("MEHMET PROJECT VALIDATION")
    print("=" * 60)
    if warnings:
        print("Uyarılar:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("Hatalar:")
        for e in errors:
            print(f"  - {e}")
    print("=" * 60)
    if errors:
        print(f"VALIDASYON BAŞARISIZ ({len(errors)} hata)")
        return 1
    print(f"VALIDASYON BAŞARILI ({len(warnings)} uyarı)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
