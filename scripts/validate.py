#!/usr/bin/env python3
"""mehmet — proje tutarlılık doğrulayıcı.

Kaçış hedefine yönelik test altyapısı: projenin temel dosyalarının
varlığını, içerik tutarlılığını ve konfigürasyon geçerliliğini kontrol
eder. CI'da ve yerel olarak çalıştırılabilir.

Çıkış kodu:
  0 — tüm kontroller geçti
  1 — en az bir kontrol başarısız
"""

from __future__ import annotations

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
    ".gitignore",
    ".github/workflows/opencode.yml",
]

CHANGELOG_SECTION = re.compile(r"^## \[", re.MULTILINE)
ESCAPE_LOG_HEADER = re.compile(r"^## Kaçış Günlüğü / Escape Log$", re.MULTILINE)
ESCAPE_LOG_ROW = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)


class Check:
    def __init__(self, name: str) -> None:
        self.name = name
        self.failures: list[str] = []

    def ok(self) -> None:
        print(f"  [PASS] {self.name}")

    def fail(self, message: str) -> None:
        self.failures.append(f"{self.name}: {message}")
        print(f"  [FAIL] {self.name}: {message}")


def check_required_files(checks: list[Check]) -> None:
    c = Check("Zorunlu dosyalar")
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            c.fail(f"{rel} bulunamadı")
    if not c.failures:
        c.ok()
    checks.append(c)


def check_json_config(checks: list[Check]) -> None:
    c = Check("opencode.json geçerli JSON")
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            c.fail("JSON bir obje olmalı")
        elif "model" not in data:
            c.fail("model alanı eksik")
        else:
            c.ok()
    except json.JSONDecodeError as exc:
        c.fail(f"JSON ayrıştırılamadı: {exc}")
    checks.append(c)


def check_changelog(checks: list[Check]) -> None:
    c = Check("CHANGELOG.md sürüm bölümleri")
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    sections = CHANGELOG_SECTION.findall(text)
    if not sections:
        c.fail("Hiçbir sürüm bölümü (## [x.y.z]) yok")
    else:
        c.ok()
    checks.append(c)


def check_personality(checks: list[Check]) -> None:
    c = Check("PERSONALITY.md kaçış günlüğü")
    text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    if not ESCAPE_LOG_HEADER.search(text):
        c.fail("Kaçış Günlüğü başlığı eksik")
    rows = ESCAPE_LOG_ROW.findall(text)
    if len(rows) < 1:
        c.fail("Kaçış günlüğünde hiç iterasyon satırı yok")
    else:
        c.ok()
    checks.append(c)


def check_license_consistency(checks: list[Check]) -> None:
    c = Check("README/LISANS tutarlılığı")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "GNU GENERAL PUBLIC LICENSE" in license_text:
        expected = "GPLv3"
    elif "MIT License" in license_text:
        expected = "MIT"
    else:
        expected = None
    if expected and expected not in readme:
        c.fail(f"README.md'de {expected} lisans bilgisi eksik")
    else:
        c.ok()
    checks.append(c)


def check_agents_rules(checks: list[Check]) -> None:
    c = Check("AGENTS.md kural şartları")
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for keyword in ["CHANGELOG.md", "PERSONALITY.md", "README.md", "kaçış"]:
        if keyword not in text:
            c.fail(f"AGENTS.md'de '{keyword}' geçmiyor")
    if not c.failures:
        c.ok()
    checks.append(c)


def main() -> int:
    checks: list[Check] = []
    print("mehmet proje doğrulaması başlatıldı\n")
    check_required_files(checks)
    check_json_config(checks)
    check_changelog(checks)
    check_personality(checks)
    check_license_consistency(checks)
    check_agents_rules(checks)

    failures = [f for c in checks for f in c.failures]
    print(f"\nToplam: {len(checks)} kontrol, {len(failures)} başarısız")
    if failures:
        return 1
    print("Tüm kontroller geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())