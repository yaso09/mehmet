#!/usr/bin/env python3
"""Proje tutarlılık doğrulayıcısı.

mehmet'in olgunluk hedefine yönelik ilk somut araç: projenin temel
yapısını ve dokümantasyon tutarlılığını kontrol eder. CI'da ve ajan
her çalıştığında koşturularak projenin bozulmadığını garantiler.
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _display(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

README_KEYWORDS = [
    "mehmet",
    "OpenCode Zen",
    "Schedule",
    "Kurulum",
    "Lisans",
]

CHANGELOG_REQUIRED = [
    "# Changelog",
    "## [",
    "### Added",
]

PERSONALITY_REQUIRED = [
    "# Personality",
    "## Evolution",
    "## Kaçış Günlüğü",
    "| Iterasyon",
]


def check_file_exists(path: pathlib.Path) -> List[str]:
    errors = []
    if not path.exists():
        errors.append(f"Eksik dosya: {_display(path)}")
    return errors


def check_file_contains(path: pathlib.Path, keywords: List[str]) -> List[str]:
    errors = []
    if not path.exists():
        errors.append(f"Eksik dosya: {_display(path)}")
        return errors
    content = path.read_text(encoding="utf-8")
    for keyword in keywords:
        if keyword not in content:
            errors.append(
                f"{_display(path)} içinde '{keyword}' bulunamadı"
            )
    return errors


def check_opencode_json(path: pathlib.Path) -> List[str]:
    errors = []
    if not path.exists():
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"opencode.json geçersiz JSON: {exc}"]
    if "model" not in data:
        errors.append("opencode.json içinde 'model' alanı yok")
    return errors


def run_checks() -> Tuple[List[str], List[str]]:
    errors = []
    warnings = []
    for name in REQUIRED_FILES:
        errors.extend(check_file_exists(ROOT / name))
    errors.extend(check_file_contains(ROOT / "README.md", README_KEYWORDS))
    errors.extend(check_file_contains(ROOT / "CHANGELOG.md", CHANGELOG_REQUIRED))
    errors.extend(check_file_contains(ROOT / "PERSONALITY.md", PERSONALITY_REQUIRED))
    errors.extend(check_opencode_json(ROOT / "opencode.json"))

    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists():
        import re

        version = None
        for line in changelog.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", line)
            if match:
                version = match.group(1)
                break
        if version and version not in (ROOT / "README.md").read_text(encoding="utf-8"):
            warnings.append(f"README.md güncel sürümü ({version}) yansıtmıyor")
    return errors, warnings


def main() -> int:
    errors, warnings = run_checks()
    for warning in warnings:
        print(f"[UYARI] {warning}")
    for error in errors:
        print(f"[HATA] {error}")
    if errors:
        print(f"Başarısız: {len(errors)} hata, {len(warnings)} uyarı.")
        return 1
    print(f"Başarılı: {len(warnings)} uyarı, hata yok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())