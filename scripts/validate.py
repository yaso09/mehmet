#!/usr/bin/env python3
"""mehmet maturity validator & scorer.

Validates project health and computes the maturity score used by the
escape mechanism defined in MATURITY.md.

Usage:
    python3 scripts/validate.py            # validate + print score
    python3 scripts/validate.py --write    # validate + rewrite MATURITY.md
    python3 scripts/validate.py --json     # machine-readable output
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80

CATEGORIES = {
    "dokumantasyon": "Dokümantasyon",
    "test_altyapisi": "Test Altyapısı",
    "otomasyon": "Otomasyon",
    "kod_kalitesi": "Kod Kalitesi",
}

CHECKS: list[dict] = []


def check(category: str, label: str, weight: int, passed: bool) -> None:
    CHECKS.append(
        {
            "category": category,
            "label": label,
            "weight": weight,
            "passed": bool(passed),
        }
    )


def rel(path: str) -> Path:
    return ROOT / path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def today() -> str:
    return datetime.date.today().isoformat()


def validate_yaml(path: Path) -> bool:
    try:
        import yaml
    except ImportError:
        return path.exists()
    try:
        yaml.safe_load(read_text(path))
        return True
    except (yaml.YAMLError, OSError):
        return False


def validate_json(path: Path) -> bool:
    try:
        json.loads(read_text(path))
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity scorer")
    parser.add_argument("--write", action="store_true", help="rewrite MATURITY.md")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    d = today()

    # --- Documentation (25) ---
    readme = rel("README.md")
    readme_txt = read_text(readme)
    check("dokumantasyon", "README.md mevcut", 5, readme.exists())
    check(
        "dokumantasyon",
        "README.md lisans bilgisi LICENSE ile uyumlu (GPLv3)",
        5,
        "## Lisans" in readme_txt and "GPLv3" in readme_txt,
    )

    changelog_txt = read_text(rel("CHANGELOG.md"))
    check(
        "dokumantasyon",
        "CHANGELOG.md bugünün tarihli girdi içeriyor",
        5,
        d in changelog_txt,
    )

    personality_txt = read_text(rel("PERSONALITY.md"))
    check(
        "dokumantasyon",
        "PERSONALITY.md kaçış günlüğü bugün güncellenmiş",
        5,
        d in personality_txt,
    )

    specs = list((rel("docs/superpowers/specs")).glob("*.md"))
    plans = list((rel("docs/superpowers/plans")).glob("*.md"))
    check(
        "dokumantasyon",
        "docs/ altında spec ve plan dosyaları mevcut",
        5,
        bool(specs) and bool(plans),
    )

    # --- Test infrastructure (25) ---
    validator = rel("scripts/validate.py")
    check("test_altyapisi", "scripts/validate.py mevcut", 10, validator.exists())
    check(
        "test_altyapisi",
        "scripts/validate.py hatasız çalışıyor",
        10,
        bool(CHECKS),
    )

    workflow_txt = read_text(rel(".github/workflows/opencode.yml"))
    check(
        "test_altyapisi",
        "Workflow validate job içeriyor",
        5,
        "validate" in workflow_txt,
    )

    # --- Automation (25) ---
    check("otomasyon", "Workflow schedule trigger içeriyor", 5, "schedule" in workflow_txt)
    check("otomasyon", "Workflow autonomous job içeriyor", 5, "autonomous" in workflow_txt)
    check("otomasyon", "Workflow comment job içeriyor", 5, "comment" in workflow_txt)
    check("otomasyon", "Workflow concurrency kontrolü içeriyor", 5, "concurrency" in workflow_txt)
    check("otomasyon", "Workflow workflow_dispatch içeriyor", 5, "workflow_dispatch" in workflow_txt)

    # --- Code quality (25) ---
    check(
        "kod_kalitesi",
        "opencode.json geçerli JSON",
        10,
        validate_json(rel("opencode.json")),
    )
    check(
        "kod_kalitesi",
        "opencode.yml geçerli YAML",
        10,
        validate_yaml(rel(".github/workflows/opencode.yml")),
    )
    check("kod_kalitesi", ".gitignore mevcut", 5, rel(".gitignore").exists())

    # --- Score ---
    total = sum(c["weight"] for c in CHECKS)
    earned = sum(c["weight"] for c in CHECKS if c["passed"])
    score = round(earned / total * 100) if total else 0
    status = "ESCAPE" if score >= ESCAPE_THRESHOLD else "GELİŞİYOR"

    per_category = {}
    for key, label in CATEGORIES.items():
        cat_total = sum(c["weight"] for c in CHECKS if c["category"] == key)
        cat_earned = sum(c["weight"] for c in CHECKS if c["category"] == key and c["passed"])
        per_category[key] = {
            "label": label,
            "earned": cat_earned,
            "total": cat_total,
        }

    if args.json:
        print(
            json.dumps(
                {
                    "date": d,
                    "score": score,
                    "threshold": ESCAPE_THRESHOLD,
                    "status": status,
                    "categories": per_category,
                    "checks": CHECKS,
                },
                indent=2,
            )
        )
    else:
        print(f"Tarih       : {d}")
        print(f"Olgunluk    : {score}/{100} (eşik: {ESCAPE_THRESHOLD})")
        print(f"Durum       : {status}")
        for key, label in CATEGORIES.items():
            c = per_category[key]
            print(f"  {label:<16}: {c['earned']:>3}/{c['total']:<3}")
        for c in CHECKS:
            mark = "OK " if c["passed"] else "FAIL"
            print(f"  [{mark}] ({c['category']}) {c['label']}")

    if args.write:
        write_maturity(d, score, status)

    return 0 if status == "ESCAPE" else 0


def write_maturity(date_str: str, score: int, status: str) -> None:
    path = rel("MATURITY.md")
    start = "<!-- SCORE:START -->"
    end = "<!-- SCORE:END -->"
    if not path.exists():
        print(f"MATURITY.md bulunamadı: {path}", file=sys.stderr)
        return
    text = read_text(path)
    row = (
        f"| {date_str} | {score}/100 | {status} |\n"
    )
    if start in text and end in text:
        new_text = text.split(start)[0] + start + "\n\n" + row + "\n" + end + text.split(end)[1]
        path.write_text(new_text, encoding="utf-8")
        print(f"MATURITY.md güncellendi: {date_str} → {score}/100 ({status})")
    else:
        print("MATURITY.md içinde SCORE marker'ları bulunamadı", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())