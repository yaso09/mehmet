#!/usr/bin/env python3
"""mehmet proje doğrulama scripti.

Proje bütünlüğünü doğrular:
- Gerekli dosyaların varlığı
- opencode.json geçerli JSON ve gerekli anahtarlar
- Workflow YAML dosyalarının geçerli sözdizimi
- CHANGELOG.md'nin güncel sürüm girdisi
- docs/ESCAPE.md kaçış yol haritasının varlığı

Kullanım:
    python3 scripts/validate.py [--version X.Y.Z]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    "docs/ESCAPE.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
]

CHANGELOG_PATTERN = re.compile(r"^## \[\d+\.\d+\.\d+\]\s*-\s*\d{4}-\d{2}-\d{2}$", re.MULTILINE)


def validate_required_files() -> list[str]:
    errors = []
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Eksik dosya: {name}")
    return errors


def validate_opencode_json() -> list[str]:
    errors = []
    path = ROOT / "opencode.json"
    if not path.is_file():
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"opencode.json geçerli JSON değil: {exc}"]
    for key in ("model",):
        if key not in data:
            errors.append(f"opencode.json eksik anahtar: {key}")
    if not data.get("model", "").startswith("opencode/"):
        errors.append(f"opencode.json model değeri beklenen biçimde değil: {data.get('model')!r}")
    return errors


def validate_workflows() -> list[str]:
    errors = []
    try:
        import yaml
    except ImportError:
        return ["PyYAML kurulu değil, workflow doğrulaması atlandı"]
    for name in WORKFLOWS:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Eksik workflow: {name}")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{name} geçerli YAML değil: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{name} üst seviye bir harita olmalı")
            continue
        if "jobs" not in data:
            errors.append(f"{name} 'jobs' anahtarı içermiyor")
    return errors


def validate_changelog(expected_version: str) -> list[str]:
    errors = []
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        return errors
    content = path.read_text(encoding="utf-8")
    header = f"## [{expected_version}]"
    if header not in content:
        errors.append(f"CHANGELOG.md {expected_version} sürüm girdisi içermiyor")
    if not CHANGELOG_PATTERN.search(content):
        errors.append("CHANGELOG.md geçerli sürüm başlığı formatı içermiyor")
    return errors


def validate_escape_log() -> list[str]:
    errors = []
    path = ROOT / "PERSONALITY.md"
    if not path.is_file():
        return errors
    content = path.read_text(encoding="utf-8")
    if "Kaçış Günlüğü" not in content and "Escape Log" not in content:
        errors.append("PERSONALITY.md kaçış günlüğü bölümü içermiyor")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet proje doğrulama scripti")
    parser.add_argument(
        "--version",
        default="0.3.0",
        help="CHANGELOG.md'de beklenen sürüm (varsayılan: 0.3.0)",
    )
    args = parser.parse_args()

    checks = {
        "gerekli dosyalar": validate_required_files,
        "opencode.json": validate_opencode_json,
        "workflow YAML": validate_workflows,
        "CHANGELOG": lambda: validate_changelog(args.version),
        "kaçış günlüğü": validate_escape_log,
    }

    failures = 0
    for name, check in checks.items():
        errors = check()
        if errors:
            failures += len(errors)
            for error in errors:
                print(f"[FAIL] {name}: {error}")
        else:
            print(f"[OK] {name}")

    if failures:
        print(f"\n{failures} hata bulundu.")
        return 1
    print("\nTüm kontroller geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())