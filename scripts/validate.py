#!/usr/bin/env python3
"""
mehmet repository validator.

Zorunlu dosyaları, JSON/YAML sözdizimini, workflow güvenlik kullanımını ve
sızabilecek bilinen secret kalıplarını denetler.

Çıkış kodu: 0 = sorun yok, 1 = sorun var
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = (
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
)

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".firecrawl", "__pycache__", "tests"}
SKIP_FILES = {".gitignore", "LICENSE"}

SECRET_PATTERNS = (
    re.compile(r"OPENCODE_API_KEY\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
)


def iter_files(root: Path = ROOT):
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        yield path


def json_files(root: Path = ROOT):
    return [p for p in iter_files(root) if p.suffix == ".json"]


def yaml_files(root: Path = ROOT):
    return [p for p in iter_files(root) if p.suffix in (".yml", ".yaml")]


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_required(root: Path = ROOT):
    return [rel for rel in REQUIRED if not (root / rel).exists()]


def validate_one_json(path: Path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return f"{_rel(path)}: {exc}"
    return None


def validate_one_yaml(path: Path):
    try:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except (OSError, yaml.YAMLError) as exc:
        return f"{_rel(path)}: {exc}"
    return None


def validate_workflow_secret(root: Path = ROOT):
    wf = root / ".github/workflows/opencode.yml"
    if not wf.exists():
        return None
    text = wf.read_text(encoding="utf-8")
    if "secrets.OPENCODE_API_KEY" in text:
        return None
    return "opencode.yml: OPENCODE_API_KEY secret'a referans vermiyor"


def find_secrets(root: Path = ROOT):
    hits = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hits.append(str(path))
                break
    return hits


def validate(root: Path = ROOT):
    problems = []

    missing = validate_required(root)
    if missing:
        problems.append("Zorunlu dosyalar eksik: " + ", ".join(missing))

    for path in json_files(root):
        err = validate_one_json(path)
        if err:
            problems.append(err)

    for path in yaml_files(root):
        err = validate_one_yaml(path)
        if err:
            problems.append(err)

    problem = validate_workflow_secret(root)
    if problem:
        problems.append(problem)

    hits = find_secrets(root)
    if hits:
        problems.append("Secret kalıbı bulundu: " + ", ".join(hits))

    return problems


def main(argv=None) -> int:
    problems = validate()
    if problems:
        print(f"FAIL ({len(problems)} sorun):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK: tüm denetimler geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())