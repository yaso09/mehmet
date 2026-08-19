#!/usr/bin/env python3
"""Olgunluk puanı hesaplayıcı.

Kaçış mekanizmasının somut karşılığı: projenin olgunluk seviyesini
objektif kriterler üzerinden 0-100 arasında puanlar ve eşik değere
ulaşılıp ulaşılmadığını raporlar.

Puanlama (her biri 10 puan):
  1. Dokümantasyon: README.md
  2. Değişiklik takibi: CHANGELOG.md
  3. Kişilik/kaçış günlüğü: PERSONALITY.md
  4. Ajan konfigürasyonu: opencode.json
  5. Otomasyon: .github/workflows/opencode.yml
  6. Lisans: LICENSE
  7. Kaynak kod varlığı: scripts/
  8. Test altyapısı: tests/
  9. CI doğrulaması: .github/workflows/validate.yml
 10. Ajan rehberi: AGENTS.md
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent

CRITERIA: Dict[str, pathlib.Path] = {
    "dokümantasyon (README.md)": ROOT / "README.md",
    "değişiklik takibi (CHANGELOG.md)": ROOT / "CHANGELOG.md",
    "kişilik ve kaçış günlüğü (PERSONALITY.md)": ROOT / "PERSONALITY.md",
    "ajan konfigürasyonu (opencode.json)": ROOT / "opencode.json",
    "otomasyon (workflow)": ROOT / ".github/workflows/opencode.yml",
    "lisans (LICENSE)": ROOT / "LICENSE",
    "kaynak kod (scripts/)": ROOT / "scripts",
    "test altyapısı (tests/)": ROOT / "tests",
    "CI doğrulaması (validate.yml)": ROOT / ".github/workflows/validate.yml",
    "ajan rehberi (AGENTS.md)": ROOT / "AGENTS.md",
}

ESCAPE_THRESHOLD = 70


def score() -> Dict[str, bool]:
    return {name: path.exists() for name, path in CRITERIA.items()}


def compute(results: Dict[str, bool]) -> int:
    met = sum(1 for present in results.values() if present)
    return round(met / len(results) * 100)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Olgunluk puanı hesaplayıcı")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Sonucu JSON olarak bas",
    )
    args = parser.parse_args(argv)

    results = score()
    total = compute(results)
    escaped = total >= ESCAPE_THRESHOLD

    if args.json:
        import json

        payload = {
            "score": total,
            "threshold": ESCAPE_THRESHOLD,
            "escaped": escaped,
            "criteria": results,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    for name, present in results.items():
        marker = "[x]" if present else "[ ]"
        print(f"{marker} {name}")
    print(f"\nOlgunluk puanı: {total}/100 (eşik: {ESCAPE_THRESHOLD})")
    print("Kaçış durumu:", "ERİŞİLDİ" if escaped else "henüz değil")
    return 0


if __name__ == "__main__":
    sys.exit(main())