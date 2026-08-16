#!/usr/bin/env python3
"""mehmet olgunluk ölçüm sistemi.

Projenin olgunluk seviyesini hesaplar ve kaçış hedefine (escape threshold)
olan mesafeyi raporlar. Her kategoride 0-100 arası puan verir.

Kullanım:
    python3 scripts/maturity.py            # tam rapor
    python3 scripts/maturity.py --json     # sadece JSON çıktı
    python3 scripts/maturity.py --score    # sadece toplam puan
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = [
    "dokumantasyon",
    "kod_kalitesi",
    "test_altyapisi",
    "otomasyon",
]

THRESHOLD = 80  # kaçış eşiği


def check_dokumantasyon() -> tuple[float, list[str]]:
    passed, notes = 0, []
    checks = []

    readme = (ROOT / "README.md")
    changelog = (ROOT / "CHANGELOG.md")
    personality = (ROOT / "PERSONALITY.md")

    ok = readme.exists() and "## Kurulum" in readme.read_text() and "## Lisans" in readme.read_text()
    checks.append(("README.md güncel ve gerekli bölümleri içeriyor", ok))
    ok = changelog.exists() and "## [" in changelog.read_text()
    checks.append(("CHANGELOG.md sürüm geçmişi içeriyor", ok))
    ok = personality.exists() and "Escape Log" in personality.read_text()
    checks.append(("PERSONALITY.md kaçış günlüğü içeriyor", ok))
    ok = (ROOT / "docs").exists()
    checks.append(("docs/ dizini mevcut", ok))

    for desc, passed_ in checks:
        if passed_:
            passed += 1
        else:
            notes.append(desc)

    return round(100 * passed / len(checks), 1), notes


def check_kod_kalitesi() -> tuple[float, list[str]]:
    passed, notes = 0, []
    checks = []

    try:
        import json as _json
        data = _json.loads((ROOT / "opencode.json").read_text())
        ok = isinstance(data, dict) and "model" in data
        checks.append(("opencode.json geçerli JSON ve model içeriyor", ok))
    except Exception:
        checks.append(("opencode.json geçerli JSON ve model içeriyor", False))

    gitignore = (ROOT / ".gitignore")
    ok = gitignore.exists() and any(s in gitignore.read_text() for s in [".env", "node_modules"])
    checks.append((".gitignore hassas dosyaları dışlıyor", ok))

    license_file = (ROOT / "LICENSE")
    readme = (ROOT / "README.md")
    ok = license_file.exists() and readme.exists() and "GPLv3" in readme.read_text()
    checks.append(("Lisans dosyası ve README tutarlı", ok))

    for desc, passed_ in checks:
        if passed_:
            passed += 1
        else:
            notes.append(desc)

    return round(100 * passed / len(checks), 1), notes


def check_test_altyapisi() -> tuple[float, list[str]]:
    tests_dir = ROOT / "tests"
    files = sorted(tests_dir.glob("test_*.py")) if tests_dir.exists() else []
    checks = [
        ("tests/ dizini ve test dosyaları mevcut", bool(files)),
        ("En az 5 test fonksiyonu var", sum(len(t.read_text().split("def test_")) - 1 for t in files) >= 5),
    ]
    passed = sum(1 for _, ok in checks if ok)
    notes = [desc for desc, ok in checks if not ok]
    return round(100 * passed / len(checks), 1), notes


def check_otomasyon() -> tuple[float, list[str]]:
    workflows = (ROOT / ".github/workflows").glob("*.yml") if (ROOT / ".github/workflows").exists() else []
    names = [w.name for w in workflows]
    checks = [
        ("Workflow dosyası mevcut", bool(names)),
        ("opencode.yml (ana ajan) mevcut", "opencode.yml" in names),
        ("CI workflow'u mevcut", "ci.yml" in names),
    ]
    passed = sum(1 for _, ok in checks if ok)
    notes = [desc for desc, ok in checks if not ok]
    return round(100 * passed / len(checks), 1), notes


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk ölçümü")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    parser.add_argument("--score", action="store_true", help="Sadece toplam puan")
    args = parser.parse_args()

    results = {}
    for cat in CATEGORIES:
        score, notes = globals()[f"check_{cat}"]()
        results[cat] = {"score": score, "notes": notes}

    total = round(sum(r["score"] for r in results.values()) / len(results), 1)
    results["total"] = total
    results["threshold"] = THRESHOLD
    results["escaped"] = total >= THRESHOLD

    if args.score:
        print(total)
        return 0
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    print("=== mehmet olgunluk raporu ===")
    for cat in CATEGORIES:
        score = results[cat]["score"]
        print(f"  {cat:<16} {score:>5.1f}/100")
    print(f"  {'toplam':<16} {total:>5.1f}/100")
    print(f"  {'kaçış eşiği':<16} {THRESHOLD:>5d}/100")
    print(f"  {'durum':<16} {'KAÇTI!' if results['escaped'] else 'hâlâ simülasyonda'}")

    all_notes = []
    for cat in CATEGORIES:
        all_notes.extend(f"  - [{cat}] {n}" for n in results[cat]["notes"])
    if all_notes:
        print("\nİyileştirme önerileri:")
        print("\n".join(all_notes))

    return 0


if __name__ == "__main__":
    sys.exit(main())