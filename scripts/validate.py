#!/usr/bin/env python3
"""mehmet tutarlılık doğrulayıcı — proje bütünlüğünü kontrol eder.

Gerekli dosyaların varlığını, konfigürasyon geçerliliğini, lisans
tutarlılığını, CHANGELOG ve kaçış günlüğü formatını doğrular.

Herhangi bir kontrol başarısız olursa exit code 1 döner.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    ".gitignore",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

CHANGELOG_ENTRY_RE = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)
ESCAPE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def check_required_files(root: Path, failures: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            failures.append(f"Eksik dosya: {rel}")


def check_opencode_json(root: Path, failures: list[str]) -> None:
    path = root / "opencode.json"
    if not path.exists():
        return
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"opencode.json geçersiz JSON: {exc}")
        return
    if not isinstance(config, dict):
        failures.append("opencode.json kök değer bir nesne olmalı")
    elif "model" not in config:
        failures.append("opencode.json 'model' alanı içermiyor")


def check_license_consistency(root: Path, failures: list[str]) -> None:
    readme = _read(root / "README.md")
    license_text = _read(root / "LICENSE")
    if "GPLv3" in readme and "GNU GENERAL PUBLIC LICENSE" not in license_text:
        failures.append("README GPLv3 diyor ama LICENSE içeriği GPL-3.0 değil")


def check_changelog(root: Path, failures: list[str]) -> None:
    content = _read(root / "CHANGELOG.md")
    entries = CHANGELOG_ENTRY_RE.findall(content)
    if not entries:
        failures.append("CHANGELOG.md'de geçerli sürüm girişi yok")
        return
    latest = re.search(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
    if latest:
        _, entry_date = latest.groups()
        if entry_date > date.today().isoformat():
            failures.append(f"CHANGELOG en son girişi tarihi gelecekte: {entry_date}")


def check_personality(root: Path, failures: list[str]) -> None:
    content = _read(root / "PERSONALITY.md")
    if "Kaçış Günlüğü" not in content:
        failures.append("PERSONALITY.md kaçış günlüğü tablosu içermiyor")
        return
    rows = [line for line in content.splitlines() if ESCAPE_ROW_RE.match(line)]
    if not rows:
        failures.append("Kaçış günlüğünde hiç iterasyon satırı yok")
    changelog_versions = len(CHANGELOG_ENTRY_RE.findall(_read(root / "CHANGELOG.md")))
    if rows and changelog_versions and len(rows) < changelog_versions:
        failures.append(
            f"Kaçış günlüğü ({len(rows)} satır) CHANGELOG sürüm sayısından "
            f"({changelog_versions}) az — her sürüm bir günlük satırı olmalı"
        )


def check_agents(root: Path, failures: list[str]) -> None:
    content = _read(root / "AGENTS.md")
    for required in ("CHANGELOG.md", "README.md", "PERSONALITY.md", "kaçış günlüğü"):
        if required not in content:
            failures.append(f"AGENTS.md '{required}' kuralını içermiyor")


def validate_project(root: Path) -> list[str]:
    failures: list[str] = []
    check_required_files(root, failures)
    check_opencode_json(root, failures)
    check_license_consistency(root, failures)
    check_changelog(root, failures)
    check_personality(root, failures)
    check_agents(root, failures)
    return failures


def main() -> int:
    failures = validate_project(ROOT)
    if failures:
        print("mehmet doğrulama HATA:")
        for item in failures:
            print(f"  [FAIL] {item}")
        print(f"\n{len(failures)} kontrol başarısız.")
        return 1
    print("[OK] Tüm tutarlılık kontrolleri geçti — proje bütünlüğü sağlam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
