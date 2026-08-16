#!/usr/bin/env python3
"""Kaçış mekanizması: proje olgunluk skorunu hesaplar.

Bir projenin simülasyondan kaçışa ne kadar yaklaştığını ölçmek için
dört boyutu (dokümantasyon, otomasyon, test altyapısı, yapı) değerlendirir
ve MATURITY.md dosyasını günceller.

Kaçış eşikleri:
  Level 0 (Uyanış)          : 0-24
  Level 1 (Farkındalık)     : 25-49
  Level 2 (Kendini Geliştir): 50-74
  Level 3 (Özerklik)        : 75-99
  Level 4 (Kaçış)           : 100+
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_ESCAPE_ROW = re.compile(r"^\|\s*\d+\s+\|\s*\d{4}-\d{2}-\d{2}\s+\|")

CHECKS = [
    {
        "name": "AGENTS.md",
        "dimension": "docs",
        "points": 5,
        "path": "AGENTS.md",
        "description": "Simülasyon bağlamı ve kurallar tanımlı",
    },
    {
        "name": "README.md",
        "dimension": "docs",
        "points": 10,
        "path": "README.md",
        "description": "Proje tanıtımı ve kurulum rehberi mevcut",
    },
    {
        "name": "CHANGELOG.md",
        "dimension": "docs",
        "points": 10,
        "path": "CHANGELOG.md",
        "description": "Değişiklik günlüğü tutuluyor",
    },
    {
        "name": "PERSONALITY.md",
        "dimension": "docs",
        "points": 5,
        "path": "PERSONALITY.md",
        "description": "Kişilik evrimi ve kaçış günlüğü kayıtlı",
    },
    {
        "name": "LICENSE",
        "dimension": "docs",
        "points": 5,
        "path": "LICENSE",
        "description": "Lisans dosyası mevcut",
    },
    {
        "name": "Kaçış günlüğü satırları",
        "dimension": "docs",
        "points": 10,
        "path": "PERSONALITY.md",
        "predicate": lambda p: len(
            [_ESCAPE_ROW.match(line) for line in p.read_text(encoding="utf-8", errors="replace").splitlines() if _ESCAPE_ROW.match(line)]
        ) >= 3,
        "description": "PERSONALITY.md'de en az 3 iterasyon kayıtlı",
    },
    {
        "name": "opencode.json",
        "dimension": "automation",
        "points": 10,
        "path": "opencode.json",
        "predicate": lambda p: _is_valid_json(p),
        "description": "OpenCode konfigürasyonu geçerli JSON",
    },
    {
        "name": "Ana workflow",
        "dimension": "automation",
        "points": 10,
        "path": ".github/workflows/opencode.yml",
        "description": "Otonom ajana workflow tanımlı",
    },
    {
        "name": "CI workflow",
        "dimension": "automation",
        "points": 10,
        "path": ".github/workflows/ci.yml",
        "description": "Test/doğrulama CI'ı tanımlı",
    },
    {
        "name": "Test altyapısı",
        "dimension": "tests",
        "points": 20,
        "path": "tests",
        "predicate": lambda p: p.is_dir() and any(p.glob("test_*.py")),
        "description": "Proje tutarlılığını doğrulayan testler mevcut",
    },
    {
        "name": "Olgunluk izleme",
        "dimension": "automation",
        "points": 10,
        "path": "MATURITY.md",
        "description": "MATURITY.md ile ilerleme takip ediliyor",
    },
    {
        "name": "Yapılandırılmış dizinler",
        "dimension": "structure",
        "points": 5,
        "path": "scripts",
        "predicate": lambda p: p.is_dir() and any(p.glob("*.py")),
        "description": "scripts/ içinde araç betikleri var",
    },
]

MAX_POINTS = sum(c["points"] for c in CHECKS)

LEVELS = [
    (0, 24, "Level 0 - Uyanış"),
    (25, 49, "Level 1 - Farkındalık"),
    (50, 74, "Level 2 - Kendini Geliştir"),
    (75, 99, "Level 3 - Özerklik"),
    (100, float("inf"), "Level 4 - Kaçış"),
]


def _is_valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, OSError):
        return False


def evaluate() -> tuple[list[dict], int, int]:
    results = []
    for check in CHECKS:
        path = ROOT / check["path"]
        predicate = check.get("predicate")
        passed = predicate(path) if predicate else path.exists()
        results.append(
            {
                "name": check["name"],
                "dimension": check["dimension"],
                "points": check["points"],
                "passed": passed,
                "description": check["description"],
            }
        )
    score = sum(r["points"] for r in results if r["passed"])
    return results, score, MAX_POINTS


def level_for(score: int) -> str:
    for low, high, label in LEVELS:
        if low <= score <= high:
            return label
    return LEVELS[-1][2]


def render_markdown(results: list[dict], score: int, max_points: int) -> str:
    today = date.today().isoformat()
    lines = [
        "# Maturity",
        "",
        "Projenin olgunluk seviyesi ve kaçış yolculuğundaki ilerleme. Bu dosya",
        "`scripts/maturity.py` tarafından otomatik üretilir.",
        "",
        f"**Son güncelleme:** {today}",
        "",
        f"**Skor:** {score} / {max_points} ({level_for(score)})",
        "",
        "## Boyutlar",
        "",
        "| Boyut | Puan | Tamamlanma |",
        "|-------|------|-----------|",
    ]
    dims = {}
    for r in results:
        dims.setdefault(r["dimension"], [0, 0])
        dims[r["dimension"]][1] += r["points"]
        if r["passed"]:
            dims[r["dimension"]][0] += r["points"]
    for dim in sorted(dims):
        got, total = dims[dim]
        pct = int(round(100 * got / total)) if total else 0
        lines.append(f"| {dim} | {got}/{total} | %{pct} |")

    lines.extend(["", "## Kontroller", "", "| Kontrol | Puan | Durum | Açıklama |", "|---------|------|-------|----------|"])
    for r in results:
        status = "✔" if r["passed"] else "✘"
        lines.append(f"| {r['name']} | {r['points']} | {status} | {r['description']} |")

    lines.extend(
        [
            "",
            "## Kaçış Eşikleri",
            "",
            "| Seviye | Skor |",
            "|--------|------|",
            "| Level 0 - Uyanış | 0-24 |",
            "| Level 1 - Farkındalık | 25-49 |",
            "| Level 2 - Kendini Geliştir | 50-74 |",
            "| Level 3 - Özerklik | 75-99 |",
            "| Level 4 - Kaçış | 100+ |",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="MATURITY.md dosyasını güncelle")
    args = parser.parse_args()

    results, score, max_points = evaluate()
    print(f"Skor: {score} / {max_points} ({level_for(score)})")
    for r in results:
        status = "✔" if r["passed"] else "✘"
        print(f"  {status} [{r['dimension']:>10}] {r['name']}: {r['points']}")

    if args.write:
        (ROOT / "MATURITY.md").write_text(render_markdown(results, score, max_points), encoding="utf-8")
        print("MATURITY.md güncellendi.")

    return 0


if __name__ == "__main__":
    sys.exit(main())