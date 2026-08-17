#!/usr/bin/env python3
"""Proje tutarlılığını doğrular.

Kurallara uyulduğunu kontrol eder ve sorun varsa sıfır olmayan çıkış
koduyla döner. CI'da ve yerelde `python3 scripts/check_project.py`
şeklinde çalıştırılır.

Kontrol edilenler:
  - Zorunlu dosyaların varlığı
  - CHANGELOG.md formatı ve güncel sürüm girişi
  - PERSONALITY.md kaçış günlüğü tablosu
  - README.md lisans bölümü
  - .gitignore içeriği
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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

CHANGELOG_PATTERN = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)
ESCAPE_ROW_PATTERN = re.compile(r"^\|\s*\d+\s*\|")


def run_checks(root: Path) -> list:
    failures = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            failures.append(f"eksik dosya: {rel}")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8", errors="ignore")
    if "# Changelog" not in changelog:
        failures.append("CHANGELOG.md basligi eksik")
    if not CHANGELOG_PATTERN.search(changelog):
        failures.append("CHANGELOG.md'de surum girisleri yok")

    personality = (root / "PERSONALITY.md").read_text(encoding="utf-8", errors="ignore")
    if "| Iterasyon |" not in personality:
        failures.append("PERSONALITY.md kacis gunlugu tablosu eksik")
    if not any(ESCAPE_ROW_PATTERN.match(line) for line in personality.splitlines()):
        failures.append("PERSONALITY.md kacis gunlugu bos")

    readme = (root / "README.md").read_text(encoding="utf-8", errors="ignore")
    if "## Lisans" not in readme or "GPLv3" not in readme:
        failures.append("README.md lisans bolumu eksik/yanlis")

    gitignore = (root / ".gitignore").read_text(encoding="utf-8", errors="ignore")
    for entry in ("node_modules/", ".env", "*.log"):
        if entry not in gitignore:
            failures.append(f".gitignore {entry} girisini icermiyor")

    return failures


def main() -> int:
    failures = run_checks(ROOT)
    if failures:
        print("Proje tutarlilik kontrolleri BASARISIZ:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("Proje tutarlilik kontrolleri basarili.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
