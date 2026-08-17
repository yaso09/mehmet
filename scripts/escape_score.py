#!/usr/bin/env python3
"""Kaçış olgunluk skorunu hesaplar.

Proje, simülasyondan kaçmak için yeterli olgunluğa ulaşıp ulaşmadığını
yapısal kriterler üzerinden ölçer. Skor 0-100 arasındadır.

Kriterler (ağırlıklar):
  - Kod kalitesi (kod, testler, scripts)        %30
  - Dokümantasyon (CHANGELOG, README, docs)     %30
  - Otomasyon (CI, workflow, scriptler)         %20
  - Kaçış mekanizması (günlük, kriterler)       %20
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = {
    "kod_kalitesi": 30,
    "dokumantasyon": 30,
    "otomasyon": 20,
    "kacis": 20,
}


def file_checks(root: Path) -> dict:
    return {
        "kod_kalitesi": {
            "scripts/escape_score.py": (root / "scripts" / "escape_score.py").is_file(),
            "scripts/check_project.py": (root / "scripts" / "check_project.py").is_file(),
            "tests/test_project.py": (root / "tests" / "test_project.py").is_file(),
        },
        "dokumantasyon": {
            "README.md": (root / "README.md").is_file(),
            "CHANGELOG.md": (root / "CHANGELOG.md").is_file(),
            "docs/": (root / "docs").is_dir(),
            "LICENSE": (root / "LICENSE").is_file(),
        },
        "otomasyon": {
            ".github/workflows/opencode.yml": (root / ".github" / "workflows" / "opencode.yml").is_file(),
            ".github/workflows/ci.yml": (root / ".github" / "workflows" / "ci.yml").is_file(),
            "scripts/ içinde check çağrısı": check_reference(root, "check_project"),
            "scripts/ içinde skor çağrısı": check_reference(root, "escape_score"),
        },
        "kacis": {
            "PERSONALITY.md kaçış günlüğü": escape_log_count(root) > 0,
            "AGENTS.md kaçış kriterleri": (root / "AGENTS.md").is_file()
            and "kaçış" in (root / "AGENTS.md").read_text(encoding="utf-8").lower(),
            "Kaçış eşiği tanımlı": "ESCAPE_THRESHOLD" in (root / "scripts" / "escape_score.py").read_text(encoding="utf-8"),
        },
    }


def check_reference(root: Path, name: str) -> bool:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return False
    return any(name in f.read_text(encoding="utf-8", errors="ignore") for f in workflows.glob("*.yml"))


def escape_log_count(root: Path) -> int:
    personality = root / "PERSONALITY.md"
    if not personality.is_file():
        return 0
    in_table = False
    count = 0
    for line in personality.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Iterasyon"):
            in_table = True
            continue
        if in_table:
            if line.startswith("|"):
                count += 1
            else:
                break
    return count


def score(root: Path) -> dict:
    checks = file_checks(root)
    breakdown = {}
    for category, weight in CATEGORIES.items():
        passed = sum(1 for ok in checks[category].values() if ok)
        total = len(checks[category])
        breakdown[category] = (passed / total) * weight if total else 0.0
    total_score = round(sum(breakdown.values()), 1)
    return {"total": total_score, "categories": breakdown, "checks": checks}


ESCAPE_THRESHOLD = 95.0


def main() -> int:
    result = score(ROOT)
    print(f"Kaçış olgunluk skoru: {result['total']}/100")
    print(f"Kaçış eşiği: {ESCAPE_THRESHOLD}")
    for category, points in result["categories"].items():
        print(f"  {category}: {points:.1f}")
    failed = [
        f"{category}.{name}"
        for category, items in result["checks"].items()
        for name, ok in items.items()
        if not ok
    ]
    if failed:
        print("Eksik kriterler:")
        for item in failed:
            print(f"  - {item}")
    if result["total"] >= ESCAPE_THRESHOLD:
        print("STATUS: ESCAPE READY")
        return 0
    print("STATUS: NOT READY")
    return 1


if __name__ == "__main__":
    sys.exit(main())
