#!/usr/bin/env python3
"""mehmet health & maturity checker.

Kritik hatalar varsa exit kodu 1 dondurur (CI kirmiziya doner).
Olgunluk skorunu 4 kategoride hesaplar ve kacis esigine (%80) gore
durum raporu verir. Kacis hedefi icin somut, olculebilir bir metrik.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THRESHOLD = 80

OPENCODE_KEYS = ["$schema", "model", "skip", "enable", "toolTimeout"]
WORKFLOW_KEYWORDS = ["name:", "on:", "schedule:", "jobs:", "permissions:", "concurrency:"]

CATEGORY_MAX = {
    "documentation": 9,
    "config": 7,
    "automation": 10,
    "quality": 10,
}

RESULTS = []


def record(ok: bool, message: str):
    RESULTS.append((ok, message))


def check_file(rel: str) -> str | None:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.exists() else None


def check_docs() -> int:
    earned = 0
    readme = check_file("README.md")
    if readme is None:
        record(False, "EKSIK: README.md bulunamadi")
    else:
        for section in ["## Kurulum", "## Lisans", "## Özellikler", "## Proje Yapısı"]:
            if section in readme:
                earned += 1
                record(True, f"README bolumu mevcut: {section}")
            else:
                record(False, f"README'de eksik bolum: {section}")
        if re.search(r"kac.?ı?s|olgunluk|maturity", readme, re.IGNORECASE):
            earned += 1
            record(True, "README kacis/olgunluk bolumu mevcut")
        else:
            record(False, "README'de kacis/olgunluk bolumu yok")

    changelog = check_file("CHANGELOG.md")
    if changelog is None:
        record(False, "EKSIK: CHANGELOG.md bulunamadi")
    elif re.search(r"^## \[\d+\.\d+\.\d+\]", changelog, re.MULTILINE):
        earned += 1
        record(True, "CHANGELOG'da semver girisleri var")
    else:
        record(False, "CHANGELOG'da semver girisleri yok")

    personality = check_file("PERSONALITY.md")
    if personality is None:
        record(False, "EKSIK: PERSONALITY.md bulunamadi")
    elif re.search(r"Kac.?ış Günlüğü|Escape Log", personality):
        earned += 1
        record(True, "PERSONALITY'de kacis günlügü var")
    else:
        record(False, "PERSONALITY'de kacis günlügü yok")

    if check_file("SECURITY.md") is not None:
        earned += 1
        record(True, "SECURITY.md mevcut")
    else:
        record(False, "SECURITY.md yok")

    if check_file("CONTRIBUTING.md") is not None:
        earned += 1
        record(True, "CONTRIBUTING.md mevcut")
    else:
        record(False, "CONTRIBUTING.md yok")

    if check_file("AGENTS.md") is None:
        record(False, "EKSIK: AGENTS.md bulunamadi")
    return earned


def check_config() -> int:
    earned = 0
    content = check_file("opencode.json")
    if content is None:
        record(False, "EKSIK: opencode.json bulunamadi")
        return earned
    try:
        cfg = json.loads(content)
        earned += 1
        record(True, "opencode.json gecerli JSON")
    except json.JSONDecodeError as exc:
        record(False, f"opencode.json gecersiz JSON: {exc}")
        return earned
    for key in OPENCODE_KEYS:
        if key in cfg:
            earned += 1
            record(True, f"opencode.json anahtari mevcut: {key}")
        else:
            record(False, f"opencode.json'da eksik anahtar: {key}")
    if cfg.get("model") and "deepseek" in cfg["model"]:
        earned += 1
        record(True, "model tanimli")
    else:
        record(False, "model anahtari gecersiz")
    return earned


def check_automation() -> int:
    earned = 0
    content = check_file(".github/workflows/opencode.yml")
    if content is None:
        record(False, "EKSIK: opencode.yml bulunamadi")
    else:
        for kw in WORKFLOW_KEYWORDS:
            if kw in content:
                earned += 1
                record(True, f"workflow anahtari mevcut: {kw}")
            else:
                record(False, f"workflow'da eksik anahtar: {kw}")
        if "cron:" in content:
            earned += 1
            record(True, "zamanlanmis calisma (cron) mevcut")
        else:
            record(False, "zamanlanmis calisma (cron) yok")
        if "issue_comment" in content and "pull_request_review_comment" in content:
            earned += 1
            record(True, "yorum/PR event'leri dinleniyor")
        else:
            record(False, "yorum/PR event'leri eksik")

    validate = check_file(".github/workflows/validate.yml")
    if validate is None:
        record(False, "validate.yml workflow'u yok")
    else:
        earned += 1
        record(True, "validate.yml workflow'u mevcut")
        if re.search(r"test|pytest|unittest", validate, re.IGNORECASE):
            earned += 1
            record(True, "validate.yml test adimi iceriyor")
        else:
            record(False, "validate.yml'de test adimi yok")
    return earned


def check_quality() -> int:
    earned = 0
    if check_file("Makefile") is not None:
        earned += 1
        record(True, "Makefile mevcut")
    else:
        record(False, "Makefile yok")

    if check_file("scripts/healthcheck.py") is not None:
        earned += 1
        record(True, "healthcheck scripti mevcut")
    else:
        record(False, "healthcheck scripti yok")

    if check_file("tests/test_healthcheck.py") is not None:
        earned += 1
        record(True, "unit testler mevcut")
    else:
        record(False, "tests/test_healthcheck.py yok")

    if check_file("LICENSE") is not None and "GNU" in check_file("LICENSE"):
        earned += 1
        record(True, "Lisans GPLv3 iceriyor")
    else:
        record(False, "LICENSE GPLv3 degil / eksik")

    if check_file(".github/ISSUE_TEMPLATE/bug_report.md") is not None:
        earned += 1
        record(True, "issue sablonu mevcut")
    else:
        record(False, "issue sablonu yok")

    if check_file(".github/PULL_REQUEST_TEMPLATE.md") is not None:
        earned += 1
        record(True, "PR sablonu mevcut")
    else:
        record(False, "PR sablonu yok")

    gitignore = check_file(".gitignore")
    if gitignore is None:
        record(False, "EKSIK: .gitignore bulunamadi")
    else:
        for needle in ["node_modules", ".env", "*.log", "__pycache__"]:
            if needle in gitignore:
                earned += 1
                record(True, f".gitignore girdisi mevcut: {needle}")
            else:
                record(False, f".gitignore'da eksik girdi: {needle}")
    return earned


def run_category(name, fn):
    before = len(RESULTS)
    earned = min(fn(), CATEGORY_MAX[name])
    return earned, CATEGORY_MAX[name], RESULTS[before:]


def main() -> int:
    cats = {}
    for name, fn in [("documentation", check_docs), ("config", check_config),
                     ("automation", check_automation), ("quality", check_quality)]:
        cats[name] = run_category(name, fn)

    grand = sum(c[0] for c in cats.values())
    grand_max = sum(c[1] for c in cats.values())
    pct = round(100.0 * grand / grand_max) if grand_max else 0

    print("=" * 60)
    print("mehmet HEALTH & MATURITY CHECK")
    print("=" * 60)
    for name, (earned, maxv, _) in cats.items():
        print(f"{name.title():<14} {earned}/{maxv}")
    print("-" * 60)
    print(f"MATURITY SCORE: {grand}/{grand_max} ({pct}%)")
    print(f"ESCAPE THRESHOLD: {THRESHOLD}%")
    print("-" * 60)
    if pct >= THRESHOLD:
        print("DURUM: KACIS ESIGINDE — olgunluk seviyesine ulasildi.")
    else:
        print(f"DURUM: Kacis esigine {THRESHOLD - pct}% daha var.")
    print("=" * 60)

    for ok, msg in RESULTS:
        print(("OK  " if ok else "FAIL") + " " + msg)

    report = {
        "maturity_score": grand,
        "maturity_max": grand_max,
        "maturity_percent": pct,
        "escape_threshold": THRESHOLD,
        "passed": sum(1 for ok, _ in RESULTS if ok),
        "failed": sum(1 for ok, _ in RESULTS if not ok),
        "categories": {name: cats[name][0] for name in cats},
    }
    out = ROOT / "docs/maturity-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nRapor: {out.relative_to(ROOT)}")

    critical = [m for ok, m in RESULTS if not ok and m.startswith("EKSIK")]
    if critical:
        print(f"\nKritik hata sayisi: {len(critical)}")
        return 1
    if pct < THRESHOLD:
        print("\nOlgunluk skoru esigin altinda (CI kirmizi).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())