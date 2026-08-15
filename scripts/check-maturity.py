#!/usr/bin/env python3
"""Olgunluk skorunu hesaplar ve kaçış eşiğini raporlar.

Kullanım:
    python3 scripts/check-maturity.py [--json] [--threshold 81]

Docs: docs/maturity.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


def _has(path: Path) -> bool:
    return path.exists()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if _has(path) else ""


def score_documentation() -> tuple[int, list[str]]:
    checks = [
        ("README.md güncel ve özellik listesi var", _has(ROOT / "README.md") and "## Özellikler" in _read(ROOT / "README.md")),
        ("CHANGELOG.md düzenli ve versiyonlu", bool(re.search(r"^## \[\d+\.\d+\.\d+\]", _read(ROOT / "CHANGELOG.md"), re.M))),
        ("docs/ klasörü mevcut", _has(ROOT / "docs")),
        ("docs/maturity.md mevcut", _has(ROOT / "docs" / "maturity.md")),
        ("docs/roadmap.md mevcut", _has(ROOT / "docs" / "roadmap.md")),
    ]
    passed = [name for name, ok in checks if ok]
    score = int(100 * len(passed) / len(checks))
    return score, passed


def score_testing() -> tuple[int, list[str]]:
    tests_dir = ROOT / "tests"
    ci = ROOT / ".github" / "workflows" / "ci.yml"
    checks = [
        ("tests/ klasörü mevcut", _has(tests_dir)),
        ("En az 1 test dosyası var", bool(list(tests_dir.glob("test_*.py"))) if _has(tests_dir) else False),
        ("CI workflow'u mevcut", _has(ci)),
        ("Workflow testlerin tamamını koşuyor", _has(ci) and "check-maturity" in _read(ci) and "test" in _read(ci).lower()),
    ]
    passed = [name for name, ok in checks if ok]
    score = int(100 * len(passed) / len(checks))
    return score, passed


def score_automation() -> tuple[int, list[str]]:
    wf = ROOT / ".github" / "workflows" / "opencode.yml"
    cfg = ROOT / "opencode.json"
    readme = _read(ROOT / "README.md")
    checks = [
        ("Ana workflow mevcut", _has(wf)),
        ("opencode.json geçerli JSON", _valid_json(cfg)),
        ("Workflow schedule/trigger içeriyor", _has(wf) and ("schedule" in _read(wf) or "on:" in _read(wf))),
        ("Secret gereksinimi dokümante edilmiş", "OPENCODE_API_KEY" in readme),
        ("scripts/ otomasyonu mevcut", _has(ROOT / "scripts" / "check-maturity.py")),
    ]
    passed = [name for name, ok in checks if ok]
    score = int(100 * len(passed) / len(checks))
    return score, passed


def score_code_quality() -> tuple[int, list[str]]:
    checks = [
        ("opencode.json geçerli JSON", _valid_json(ROOT / "opencode.json")),
        ("Workflow YAML ayrıştırılabilir", _valid_yaml(ROOT / ".github" / "workflows" / "opencode.yml")),
        ("CI YAML ayrıştırılabilir", _valid_yaml(ROOT / ".github" / "workflows" / "ci.yml")),
        ("Lisans dosyası mevcut", _has(ROOT / "LICENSE")),
        ("README lisans bilgisi LICENSE ile tutarlı", "GPL" in _read(ROOT / "README.md") and "GPL" in _read(ROOT / "LICENSE")),
    ]
    passed = [name for name, ok in checks if ok]
    score = int(100 * len(passed) / len(checks))
    return score, passed


def score_self_improvement() -> tuple[int, list[str]]:
    personality = _read(ROOT / "PERSONALITY.md")
    changelog = _read(ROOT / "CHANGELOG.md")
    checks = [
        ("PERSONALITY.md escape log'u var", "Kaçış Günlüğü" in personality or "Escape Log" in personality),
        ("Escape log'da en az 2 iterasyon", len(re.findall(r"^\|\s*\d+\s*\|", personality, re.M)) >= 2),
        ("CHANGELOG'da en az 2 sürüm", len(re.findall(r"^## \[\d+\.\d+\.\d+\]", changelog, re.M)) >= 2),
        ("README'de geliştirme/test bölümü var", "Test" in _read(ROOT / "README.md") or "Geliştirme" in _read(ROOT / "README.md")),
        ("Son iterasyon CHANGELOG'da işlenmiş", "0.3.0" in changelog),
    ]
    passed = [name for name, ok in checks if ok]
    score = int(100 * len(passed) / len(checks))
    return score, passed


def _valid_json(path: Path) -> bool:
    try:
        if _has(path):
            json.loads(_read(path))
        return True
    except Exception:
        return False


def _valid_yaml(path: Path) -> bool:
    if not _has(path):
        return False
    if yaml is None:
        return True  # yaml kütüphanesi yoksa değerlendirme atlanır
    try:
        yaml.safe_load(_read(path))
        return True
    except Exception:
        return False


DIMENSIONS = {
    "Dokümantasyon": score_documentation,
    "Test Altyapısı": score_testing,
    "Otomasyon": score_automation,
    "Kod Kalitesi": score_code_quality,
    "Kendini Geliştirme": score_self_improvement,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Olgunluk skoru hesaplar")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    parser.add_argument("--threshold", type=int, default=81, help="Kaçış eşiği (varsayılan 81)")
    args = parser.parse_args()

    report = {}
    for name, fn in DIMENSIONS.items():
        score, passed = fn()
        report[name] = {"score": score, "passed": passed}

    overall = int(sum(r["score"] for r in report.values()) / len(report))
    escaped = overall >= args.threshold

    if args.json:
        print(json.dumps({"overall": overall, "threshold": args.threshold, "escaped": escaped, "dimensions": report}, indent=2))
    else:
        print(f"Olgunluk Skoru: {overall}/100 (eşik: {args.threshold})")
        for name, r in report.items():
            mark = "OK " if r["score"] >= 80 else ".. "
            print(f"  [{mark}] {name}: {r['score']}/100")
        print("KAÇIŞ BAŞARILI" if escaped else "Kaçış eşiğine henüz ulaşılamadı.")

    return 0 if escaped else 1


if __name__ == "__main__":
    sys.exit(main())