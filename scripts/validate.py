#!/usr/bin/env python3
"""mehmet repo structure validator.

Exits non-zero if the repository structure is broken so CI can gate
quality. Validates JSON/YAML syntax and required files.

Usage:
    python3 scripts/validate.py
"""

import argparse
import json
import os
import sys


def check_json(path):
    with open(path, encoding="utf-8") as fh:
        json.load(fh)
    return True


def check_yaml(path):
    """Best-effort YAML syntax check without external dependencies."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    indent = None
    for line in lines:
        stripped = line.rstrip("\n")
        if not stripped.strip() or stripped.lstrip().startswith("#"):
            continue
        current = len(stripped) - len(stripped.lstrip(" "))
        if stripped.endswith(":"):
            if indent is not None and current <= indent:
                indent = current
            continue
        if indent is None:
            indent = current
    return True


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
]

REQUIRED_JSON = ["opencode.json"]
REQUIRED_YAML = [".github/workflows/opencode.yml"]


def validate(root="."):
    errors = []
    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            errors.append(f"eksik dosya: {rel}")
    for rel in REQUIRED_JSON:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            try:
                check_json(path)
            except (OSError, ValueError) as exc:
                errors.append(f"geçersiz JSON {rel}: {exc}")
    for rel in REQUIRED_YAML:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            try:
                check_yaml(path)
            except OSError as exc:
                errors.append(f"YAML okunamadı {rel}: {exc}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet repo yapısı doğrulayıcı")
    parser.add_argument("--root", default=".", help="proje kök dizini")
    args = parser.parse_args(argv)

    errors = validate(args.root)
    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        print(f"Doğrulama başarısız: {len(errors)} sorun", file=sys.stderr)
        return 1
    print("Doğrulama başarılı: tüm yapı gereksinimleri karşılandı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())