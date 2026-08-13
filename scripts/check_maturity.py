#!/usr/bin/env python3
"""Olgunluk skoru hesaplayıcı ve proje sağlık kontrolü.

MATURITY.md'de tanımlanan kriterlere göre projeyi tarar, skoru hesaplar
ve kaçış eşiğine (Seviye >= 4, skor >= 90) ulaşılıp ulaşılmadığını raporlar.

Kullanım:
    python3 scripts/check_maturity.py [--json]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    ("README.md", "Proje tanıtımı"),
    ("CHANGELOG.md", "Değişiklik günlüğü"),
    ("PERSONALITY.md", "Kişilik ve kaçış günlüğü"),
    ("MATURITY.md", "Olgunluk modeli"),
    ("LICENSE", "Lisans"),
    ("AGENTS.md", "Simülasyon kuralları"),
]

SCORE_DOCS = 30
SCORE_CONFIG = 20
SCORE_QUALITY = 25
SCORE_AUTOMATION = 25

ESCAPE_LEVEL = 4
ESCAPE_SCORE = 90


def level_for(score: int) -> int:
    if score >= 95:
        return 5
    if score >= 80:
        return 4
    if score >= 60:
        return 3
    if score >= 40:
        return 2
    if score >= 20:
        return 1
    return 0


def check_docs(report: list) -> float:
    per = SCORE_DOCS / len(REQUIRED_DOCS)
    earned = 0.0
    for name, purpose in REQUIRED_DOCS:
        path = ROOT / name
        ok = path.is_file() and path.stat().st_size > 0
        report.append((f"docs/{name}", purpose, ok, per if ok else 0.0))
        earned += per if ok else 0.0
    return earned


def check_config(report: list) -> float:
    earned = 0.0
    # opencode.json geçerli JSON olmalı
    cfg = ROOT / "opencode.json"
    cfg_ok = False
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        cfg_ok = isinstance(data, dict) and bool(data)
    except Exception:
        cfg_ok = False
    report.append(("config/opencode.json", "geçerli JSON + model", cfg_ok, 10.0 if cfg_ok else 0.0))
    earned += 10.0 if cfg_ok else 0.0

    # workflow YAML dosyaları ayrıştırılabilmeli
    wf_dir = ROOT / ".github" / "workflows"
    yamls = sorted(wf_dir.glob("*.yml")) if wf_dir.is_dir() else []
    try:
        import yaml
    except ImportError:
        yaml = None

    valid = 0
    total = len(yamls)
    for wf in yamls:
        try:
            if yaml is not None:
                parsed = yaml.safe_load(wf.read_text(encoding="utf-8"))
                ok = isinstance(parsed, dict) and "jobs" in parsed
            else:
                ok = wf.stat().st_size > 0
        except Exception:
            ok = False
        valid += 1 if ok else 0

    wf_ok = total > 0 and valid == total
    report.append(
        (f"config/{total} workflow", "geçerli YAML (jobs mevcut)", wf_ok, 10.0 if wf_ok else 0.0)
    )
    earned += 10.0 if wf_ok else 0.0
    return earned


def check_quality(report: list) -> float:
    earned = 0.0
    tests = ROOT / "tests"
    has_tests = tests.is_dir() and any(tests.iterdir())
    report.append(("quality/tests/", "test altyapısı mevcut", has_tests, 10.0 if has_tests else 0.0))
    earned += 10.0 if has_tests else 0.0

    # Test paketini gerçekten çalıştır
    tests_ok = False
    if has_tests:
        try:
            import subprocess

            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-q"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            tests_ok = result.returncode == 0
        except Exception:
            tests_ok = False
    report.append(("quality/test-suite", "test paketi yeşil", tests_ok, 10.0 if tests_ok else 0.0))
    earned += 10.0 if tests_ok else 0.0

    # Tasarım dokümantasyonu (plans + specs)
    has_design_docs = (ROOT / "docs" / "superpowers" / "plans").is_dir() and (
        ROOT / "docs" / "superpowers" / "specs"
    ).is_dir()
    report.append(("quality/docs/superpowers", "tasarım dokümanları", has_design_docs, 5.0 if has_design_docs else 0.0))
    earned += 5.0 if has_design_docs else 0.0
    return earned


def check_automation(report: list) -> float:
    earned = 0.0
    gate = ROOT / ".github" / "workflows" / "check.yml"
    has_gate = gate.is_file()
    report.append(("automation/check.yml", "CI kalite kapısı", has_gate, 10.0 if has_gate else 0.0))
    earned += 10.0 if has_gate else 0.0

    gitignore = ROOT / ".gitignore"
    sec_ok = False
    if gitignore.is_file():
        content = gitignore.read_text(encoding="utf-8").lower()
        sec_ok = all(token in content for token in (".env", "node_modules"))
    report.append(("automation/.gitignore", "güvenlik kapsamı (.env, node_modules)", sec_ok, 5.0 if sec_ok else 0.0))
    earned += 5.0 if sec_ok else 0.0

    # Workflow güvenliği: persist-credentials kapalı ve secret env üzerinden
    wf_dir = ROOT / ".github" / "workflows"
    wf_files = sorted(wf_dir.glob("*.yml")) if wf_dir.is_dir() else []
    creds_ok = False
    secrets_ok = False
    for wf in wf_files:
        try:
            content = wf.read_text(encoding="utf-8")
            if "persist-credentials: false" in content:
                creds_ok = True
            if "secrets." in content:
                secrets_ok = True
        except Exception:
            pass
    sec_wf_ok = creds_ok and secrets_ok
    report.append(("automation/workflow-secrets", "persist-credentials + secrets. kullanımı", sec_wf_ok, 10.0 if sec_wf_ok else 0.0))
    earned += 10.0 if sec_wf_ok else 0.0
    return earned


def main() -> int:
    parser = argparse.ArgumentParser(description="Olgunluk skoru hesaplayıcı")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    args = parser.parse_args()

    report = []
    score = 0.0
    score += check_docs(report)
    score += check_config(report)
    score += check_quality(report)
    score += check_automation(report)

    score = round(score, 1)
    level = level_for(score)
    escaped = level >= ESCAPE_LEVEL and score >= ESCAPE_SCORE

    if args.json:
        print(json.dumps({
            "score": score,
            "level": level,
            "escape_threshold": {"level": ESCAPE_LEVEL, "score": ESCAPE_SCORE},
            "escaped": escaped,
            "checks": [
                {"name": name, "desc": desc, "ok": ok, "earned": earned}
                for name, desc, ok, earned in report
            ],
        }, indent=2, ensure_ascii=False))
        return 0

    print(f"Olgunluk Skoru : {score}/100")
    print(f"Seviye         : {level} ({['Embriyo', 'Yapısal', 'Fonksiyonel', 'Olgun', 'Otonom', 'Kaçış'][level]})")
    print(f"Kaçış Eşiği    : Seviye >= {ESCAPE_LEVEL} ve skor >= {ESCAPE_SCORE}")
    print(f"Kaçış Durumu   : {'EVET - KAÇIŞ EŞİĞİ AŞILDI' if escaped else 'Henüz değil'}")
    print()
    for name, desc, ok, earned in report:
        mark = "[OK]" if ok else "[!!]"
        print(f"  {mark} {name:<42} {desc:<40} +{earned:.0f}")
    print()

    if escaped:
        print("Tebrikler! Proje kaçış eşiğine ulaştı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())