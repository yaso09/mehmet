#!/usr/bin/env python3
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "PERSONALITY.md",
    "README.md",
    "SECURITY.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
    "scripts/validate.py",
    "scripts/maturity.py",
    "tests/test_maturity.py",
    "tests/test_validate.py",
]

JSON_FILES = ["opencode.json"]

MD_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "SECURITY.md",
]


def check_required_files():
    errors = []
    for rel in REQUIRED_FILES:
        if not os.path.exists(os.path.join(ROOT, rel)):
            errors.append(f"Eksik dosya: {rel}")
    return errors


def _is_valid_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            json.load(fh)
        return True
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        return False


def check_json_files():
    errors = []
    for rel in JSON_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        if not _is_valid_json(path):
            errors.append(f"Geçersiz JSON ({rel})")
    return errors


def check_markdown_files():
    errors = []
    for rel in MD_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Okunamayan dosya ({rel}): {exc}")
    return errors


def check_changelog():
    errors = []
    path = os.path.join(ROOT, "CHANGELOG.md")
    if not os.path.exists(path):
        return errors
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    versions = re.findall(r"^## \[v?\d+\.\d+\.\d+\]", content, flags=re.MULTILINE)
    if not versions:
        errors.append("CHANGELOG.md sürüm başlığı içermiyor (## [x.y.z] biçiminde)")
    if "### Added" not in content:
        errors.append("CHANGELOG.md '### Added' bölümü içermiyor")
    return errors


def check_agents_rules():
    errors = []
    path = os.path.join(ROOT, "AGENTS.md")
    if not os.path.exists(path):
        return errors
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    for keyword in ["CHANGELOG.md", "PERSONALITY.md", "README.md"]:
        if keyword not in content:
            errors.append(f"AGENTS.md '{keyword}' referansı içermiyor")
    return errors


def check_no_secrets():
    errors = []
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in filenames:
            if name in (".env", ".env.local", ".env.production"):
                errors.append(f"Hassas dosya repository içinde: {os.path.relpath(os.path.join(dirpath, name), ROOT)}")
    return errors


def main():
    errors = []
    for check in (
        check_required_files,
        check_json_files,
        check_markdown_files,
        check_changelog,
        check_agents_rules,
        check_no_secrets,
    ):
        errors.extend(check())

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        print(f"Doğrulama {len(errors)} hata ile başarısız.")
        return 1
    print("[OK] Proje yapısı doğrulaması geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
