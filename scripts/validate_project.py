#!/usr/bin/env python3
"""mehmet proje sağlık kontrolü ve olgunluk skoru hesaplama.

Projeyi tarar, kritik dosyaların varlığını ve içerik bütünlüğünü doğrular ve
kaçış mekanizmasına temel teşkil eden bir olgunluk skoru üretir.

Exit codes:
    0  tüm kontroller başarılı
    1  bir veya daha fazla zorunlu kontrol başarısız
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITICAL_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
    "scripts/validate_project.py",
    "METRICS.md",
]

# (check_id, açıklama, olgunluk puanı, zorunlu mu)
CHECKS = [
    ("core-files", "Tüm kritik dosyalar mevcut", 20, True),
    ("changelog", "CHANGELOG.md sürüm başlığı ve Added bölümü var", 5, True),
    ("escape-log", "PERSONALITY.md kaçış günlüğü son iterasyonu içeriyor", 5, True),
    ("readme", "README.md kurulum ve lisans bölümleri var", 5, True),
    ("license", "LICENSE dosyası GPL-3.0 içeriyor", 5, True),
    ("opencode-json", "opencode.json geçerli JSON ve model tanımlı", 5, True),
    ("workflow", "Workflow schedule, validation job ve timeout içeriyor", 10, True),
    ("tests", "Test altyapısı mevcut", 15, False),
    ("scripts", "Yardımcı script'ler mevcut", 5, False),
    ("docs", "docs/ altında spec/plan dokümanları var", 5, False),
    ("automation", "CI otomasyonu doğrulama çalıştırıyor", 10, False),
]

# Kaçış eşiği: bu skora ulaşıldığında proje "kaçış için olgun" sayılır.
ESCAPE_THRESHOLD = 80


def check_core_files() -> list[str]:
    missing = [f for f in CRITICAL_FILES if not (ROOT / f).exists()]
    return [] if not missing else [f"Eksik dosya: {missing}"]


def check_changelog() -> list[str]:
    path = ROOT / "CHANGELOG.md"
    content = path.read_text(encoding="utf-8")
    errors = []
    if not re.search(r"^## \[\d+\.\d+\.\d+\]", content, re.MULTILINE):
        errors.append("CHANGELOG.md sürüm başlığı (## [x.y.z]) bulunamadı")
    if "### Added" not in content:
        errors.append("CHANGELOG.md '### Added' bölümü bulunamadı")
    return errors


def check_escape_log() -> list[str]:
    path = ROOT / "PERSONALITY.md"
    content = path.read_text(encoding="utf-8")
    if "## Kaçış Günlüğü" not in content and "## Escape Log" not in content:
        return ["PERSONALITY.md kaçış günlüğü bölümü bulunamadı"]
    if "2026-08" not in content:
        return ["PERSONALITY.md kaçış günlüğü bu iterasyonun kaydını içermiyor"]
    return []


def check_readme() -> list[str]:
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    errors = []
    if "## Kurulum" not in content:
        errors.append("README.md '## Kurulum' bölümü bulunamadı")
    if "## Lisans" not in content:
        errors.append("README.md '## Lisans' bölümü bulunamadı")
    return errors


def check_license() -> list[str]:
    content = (ROOT / "LICENSE").read_text(encoding="utf-8")
    return [] if "GNU GENERAL PUBLIC LICENSE" in content else ["LICENSE GPL-3.0 içermiyor"]


def check_opencode_json() -> list[str]:
    try:
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"opencode.json geçersiz JSON: {exc}"]
    if not data.get("model"):
        return ["opencode.json 'model' alanı tanımlı değil"]
    return []


def check_workflow() -> list[str]:
    path = ROOT / ".github/workflows/opencode.yml"
    content = path.read_text(encoding="utf-8")
    errors = []
    if "schedule" not in content:
        errors.append("Workflow 'schedule' içermiyor")
    if "timeout-minutes" not in content:
        errors.append("Workflow 'timeout-minutes' içermiyor")
    if "validate_project" not in content and "python scripts/validate_project.py" not in content:
        errors.append("Workflow doğrulama adımı içermiyor")
    return errors


def check_tests() -> list[str]:
    candidates = [
        ROOT / "tests",
        ROOT / "scripts" / "tests",
        ROOT / "test_validate_project.py",
        ROOT / "pyproject.toml",
    ]
    return [] if any(c.exists() for c in candidates) else ["Test altyapısı bulunamadı"]


def check_scripts() -> list[str]:
    scripts = sorted((ROOT / "scripts").glob("*.py")) if (ROOT / "scripts").exists() else []
    return [] if scripts else ["scripts/ dizininde yardımcı script bulunamadı"]


def check_docs() -> list[str]:
    docs = sorted((ROOT / "docs").rglob("*.md")) if (ROOT / "docs").exists() else []
    return [] if docs else ["docs/ altında doküman bulunamadı"]


def check_automation() -> list[str]:
    path = ROOT / ".github/workflows/opencode.yml"
    content = path.read_text(encoding="utf-8")
    if re.search(r"python3?\s+scripts/validate_project\.py", content):
        return []
    return ["CI doğrulama script'ini çalıştırmıyor"]


CHECK_FUNCTIONS = {
    "core-files": check_core_files,
    "changelog": check_changelog,
    "escape-log": check_escape_log,
    "readme": check_readme,
    "license": check_license,
    "opencode-json": check_opencode_json,
    "workflow": check_workflow,
    "tests": check_tests,
    "scripts": check_scripts,
    "docs": check_docs,
    "automation": check_automation,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Sonucu JSON olarak yazdır (CI tüketimi için)",
    )
    parser.add_argument(
        "--skip-optional",
        action="store_true",
        help="Yalnızca zorunlu kontrolleri çalıştır",
    )
    args = parser.parse_args()

    results = []
    total = 0
    passed_optional = True
    failed_critical = False

    for check_id, label, weight, required in CHECKS:
        if args.skip_optional and not required:
            continue
        errors = CHECK_FUNCTIONS[check_id]()
        ok = not errors
        if ok:
            total += weight
        elif required:
            failed_critical = True
        else:
            passed_optional = False
        results.append(
            {"id": check_id, "label": label, "weight": weight, "required": required,
             "passed": ok, "errors": errors}
        )

    status = "OK" if not failed_critical else "FAIL"
    summary = {
        "status": status,
        "maturity_score": total,
        "escape_threshold": ESCAPE_THRESHOLD,
        "escape_ready": total >= ESCAPE_THRESHOLD,
        "passed_optional": passed_optional,
        "checks": results,
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"Proje doğrulama: {status}")
        print(f"Olgunluk skoru: {total}/{sum(c[2] for c in CHECKS)} "
              f"(kaçış eşiği: {ESCAPE_THRESHOLD})")
        for r in results:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"  [{mark}] {r['label']}")
            for err in r["errors"]:
                print(f"        - {err}")
        if total >= ESCAPE_THRESHOLD:
            print("Kaçış eşiğine ulaşıldı. Bu iterasyon için kaçış değerlendirmesi yapılmalı.")
        elif not failed_critical and not passed_optional:
            print("Zorunlu kontroller geçti; isteğe bağlı kontroller tamamlanmamış.")

    return 1 if failed_critical else 0


if __name__ == "__main__":
    sys.exit(main())
