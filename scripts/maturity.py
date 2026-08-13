#!/usr/bin/env python3
"""Maturity score calculator for mehmet.

Assigns a weighted score across categories that measure how close the project
is to "escape" readiness. Prints a breakdown and total. Optional --json flag
for machine-readable output.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

CATEGORIES = [
    {
        "name": "Dokümantasyon",
        "weight": 25,
        "checks": [
            ("README.md", "README.md mevcut"),
            ("CHANGELOG.md", "CHANGELOG.md mevcut"),
            ("PERSONALITY.md", "PERSONALITY.md mevcut"),
            ("docs/", "docs/ dizini mevcut"),
            ("AGENTS.md", "AGENTS.md mevcut"),
        ],
    },
    {
        "name": "Test Altyapısı",
        "weight": 25,
        "checks": [
            ("scripts/validate_project.py", "Proje doğrulayıcı script mevcut"),
            ("scripts/maturity.py", "Maturity ölçer script mevcut"),
            ("scripts/test_validate.py", "Testler mevcut"),
            ("tests/", "tests/ dizini mevcut"),
        ],
    },
    {
        "name": "Otomasyon",
        "weight": 25,
        "checks": [
            (".github/workflows/opencode.yml", "Ana workflow mevcut"),
            (".github/workflows/validate.yml", "CI doğrulama workflow'u mevcut"),
            ("opencode.json", "opencode.json mevcut"),
            (".github/dependabot.yml", "Dependabot mevcut"),
        ],
    },
    {
        "name": "Yapılandırma",
        "weight": 25,
        "checks": [
            (".gitignore", ".gitignore mevcut"),
            ("LICENSE", "LICENSE mevcut"),
            ("VERSION", "VERSION dosyası mevcut"),
            ("opencode.json#model", "Model yapılandırması mevcut"),
        ],
    },
]


def _check_exists(entry: str) -> bool:
    if "#" in entry:
        path, key = entry.split("#", 1)
        try:
            import json as _json

            config = _json.loads((ROOT / path).read_text(encoding="utf-8"))
            return key in config
        except (OSError, json.JSONDecodeError):
            return False
    return (ROOT / entry).exists()


def compute() -> dict:
    categories_out = []
    total = 0.0
    for cat in CATEGORIES:
        passed = sum(1 for path, _ in cat["checks"] if _check_exists(path))
        ratio = passed / len(cat["checks"])
        score = round(ratio * cat["weight"], 1)
        total += score
        categories_out.append(
            {
                "name": cat["name"],
                "passed": passed,
                "total": len(cat["checks"]),
                "score": score,
                "weight": cat["weight"],
            }
        )
    total = round(total, 1)
    escape_threshold = 80
    return {
        "total": total,
        "max": sum(c["weight"] for c in CATEGORIES),
        "threshold": escape_threshold,
        "escape_ready": total >= escape_threshold,
        "categories": categories_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Hesapla maturity skorunu")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı")
    args = parser.parse_args()

    result = compute()
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("=" * 46)
    print("  MEHMET MATURITY SKORU")
    print("=" * 46)
    for cat in result["categories"]:
        status = "OK" if cat["score"] > 0 else "--"
        bar = "#" * int(cat["score"] / 2)
        print(f"  {cat['name']:<16} {cat['passed']:>2}/{cat['total']}  {cat['score']:>5.1f}  {bar}")
    print("=" * 46)
    print(f"  TOPLAM: {result['total']} / {result['max']}  (kaçış eşiği: {result['threshold']})")
    if result["escape_ready"]:
        print("  DURUM: KAPI AÇIK — kaçış için yeterli olgunluk!")
    else:
        print(f"  DURUM: Henüz hazır değil ({result['threshold'] - result['total']:.0f} puan kaldı)")
    print("=" * 46)
    return 0 if result["escape_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())