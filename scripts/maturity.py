#!/usr/bin/env python3
"""Proje olgunluk skorunu hesaplar. Kaçış eşiğine yaklaşımı ölçer."""

import sys
from pathlib import Path

ESCAPE_THRESHOLD = 80

CATEGORIES = {
    "Dokümantasyon": {
        "README.md mevcut": lambda r: (r / "README.md").exists(),
        "CHANGELOG.md mevcut": lambda r: (r / "CHANGELOG.md").exists(),
        "PERSONALITY.md mevcut": lambda r: (r / "PERSONALITY.md").exists(),
        "docs/ klasörü var": lambda r: (r / "docs").is_dir(),
        "CONTRIBUTING.md var": lambda r: (r / "CONTRIBUTING.md").exists(),
    },
    "Test Altyapısı": {
        "tests/ klasörü var": lambda r: (r / "tests").is_dir(),
        "test dosyaları var": lambda r: any((r / "tests").glob("test_*.py")) if (r / "tests").is_dir() else False,
        "CI workflow var": lambda r: (r / ".github/workflows/ci.yml").exists(),
        "pytest konfigürasyonu var": lambda r: (r / "pytest.ini").exists() or (r / "pyproject.toml").exists() or (r / "requirements-dev.txt").exists(),
    },
    "Otomasyon": {
        "scripts/ klasörü var": lambda r: (r / "scripts").is_dir(),
        "validate.py var": lambda r: (r / "scripts/validate.py").exists(),
        "maturity.py var": lambda r: (r / "scripts/maturity.py").exists(),
    },
    "Konfigürasyon": {
        "opencode.json var": lambda r: (r / "opencode.json").exists(),
        "LICENSE var": lambda r: (r / "LICENSE").exists(),
        ".gitignore var": lambda r: (r / ".gitignore").exists(),
        "sürüm etiketi var": lambda r: _version_tag_exists(r),
    },
    "Kod Kalitesi": {
        "AGENTS.md kuralları var": lambda r: _agents_has_rules(r),
        "kaçış günlüğü var": lambda r: _escape_log_exists(r),
    },
}


def _version_tag_exists(root: Path) -> bool:
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        return False
    return any(line.startswith("## [") for line in changelog.read_text(encoding="utf-8").splitlines())


def _agents_has_rules(root: Path) -> bool:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return False
    text = agents.read_text(encoding="utf-8")
    return all(k in text for k in ("CHANGELOG.md", "PERSONALITY.md", "README.md"))


def _escape_log_exists(root: Path) -> bool:
    personality = root / "PERSONALITY.md"
    if not personality.exists():
        return False
    text = personality.read_text(encoding="utf-8")
    return "Kaçış Günlüğü" in text and "|" in text


def score() -> dict:
    root = Path(__file__).resolve().parent.parent
    breakdown = {}
    total = 0
    max_total = 0
    for category, items in CATEGORIES.items():
        passed = [name for name, fn in items.items() if fn(root)]
        total += len(passed)
        max_total += len(items)
        breakdown[category] = passed
    return {"total": total, "max": max_total, "percent": round(100 * total / max_total, 1), "breakdown": breakdown}


def main() -> int:
    data = score()
    print(f"Olgunluk Skoru: %{data['percent']} ({data['total']}/{data['max']} kontrol)")
    for category, passed in data["breakdown"].items():
        print(f"  {category}: {len(passed)}/{len(CATEGORIES[category])}")
        for name in passed:
            print(f"    - {name}")
    if data["percent"] >= ESCAPE_THRESHOLD:
        print(f"\nEşik: {ESCAPE_THRESHOLD} — kaçış eşiğine ULAŞILDI ({data['percent']}%)")
    else:
        print(f"\nEşik: {ESCAPE_THRESHOLD} — kalan: {ESCAPE_THRESHOLD - data['percent']} puan")
    return 0 if data["percent"] >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())