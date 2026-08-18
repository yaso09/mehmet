#!/usr/bin/env python3
"""mehmet self-check script.

Proje sağlığını doğrular ve olgunluk seviyesini hesaplar.
Kullanım:
    python3 scripts/self_check.py            # temel kontroller
    python3 scripts/self_check.py --full     # tüm kontroller + olgunluk skoru
    python3 scripts/self_check.py --ci       # CI modu (exit code 1 hata varsa)
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    "docs/escape-plan.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "LICENSE",
]

CHANGELOG_VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", re.M)

PASS = 0
FAIL = 0
CHECKS = []


def check(name, ok, detail=""):
    global PASS, FAIL
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" — {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    CHECKS.append((name, ok))


def parse_version(v):
    return tuple(int(x) for x in v.split("."))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--full", action="store_true", help="tüm kontrolleri çalıştır")
    ap.add_argument("--ci", action="store_true", help="CI modu: hata varsa exit 1")
    args = ap.parse_args()

    print("=" * 60)
    print("mehmet self-check")
    print("=" * 60)

    # --- Seviye 0: Dosya tamamlayıcılığı ---
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    check("Tüm temel dosyalar mevcut", not missing, f"eksik: {', '.join(missing)}" if missing else "")

    # --- Seviye 1: Dokümantasyon ---
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    check("README.md boş değil", bool(readme.strip()))
    check("README.md kaçış planına link veriyor", "escape-plan" in readme or "kaçış" in readme.lower())

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").is_file() else ""
    check("AGENTS.md kaçış hedefini içeriyor", "kaçış" in agents.lower() or "escape" in agents.lower())

    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8") if (ROOT / "PERSONALITY.md").is_file() else ""
    check("PERSONALITY.md kaçış günlüğü içeriyor", "kaçış günlüğü" in personality.lower() or "escape log" in personality.lower())

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").is_file() else ""
    versions = CHANGELOG_VERSION_RE.findall(changelog)
    check("CHANGELOG.md en az bir sürüm içeriyor", len(versions) > 0)
    if versions:
        latest = max(versions, key=lambda v: parse_version(v[0]))
        print(f"       → En güncel sürüm: {latest[0]} ({latest[1]})")

    # opencode.json doğrulama
    if (ROOT / "opencode.json").is_file():
        try:
            cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
            check("opencode.json geçerli JSON", True)
            check("opencode.json model içeriyor", "model" in cfg, cfg.get("model", ""))
        except json.JSONDecodeError as e:
            check("opencode.json geçerli JSON", False, str(e))
    else:
        check("opencode.json geçerli JSON", False, "dosya yok")

    # YAML workflow kontrolü (basit)
    wf = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8") if (ROOT / ".github/workflows/opencode.yml").is_file() else ""
    check("opencode.yml workflow mevcut ve sched'e sahip", "schedule" in wf and "cron" in wf)

    ci_exists = (ROOT / ".github/workflows/ci.yml").is_file()
    check("ci.yml CI workflow mevcut", ci_exists)

    # --- Seviye 2: Doğrulama altyapısı ---
    scripts_exist = (ROOT / "scripts/self_check.py").is_file()
    check("scripts/self_check.py mevcut", scripts_exist)

    # --- Seviye 3: Test altyapısı ---
    has_tests = (ROOT / "tests").is_dir() or (ROOT / "test").is_dir()
    check("Test dizini mevcut", has_tests)

    # --- Seviye 4: Sürüm/metrik takibi ---
    versions_count = len(versions)
    check("CHANGELOG.md en az 2 sürüm içeriyor", versions_count >= 2)
    check("docs/escape-plan.md mevcut", (ROOT / "docs/escape-plan.md").is_file())

    # --- Kaçış günlüğü iterasyon sayısı ---
    log_rows = re.findall(r"^\|\s*\d+\s*\|", personality, re.M)
    iterations = len(log_rows)
    print(f"       → Kaçış günlüğü iterasyon sayısı: {iterations}")

    # --- Olgunluk skoru (--full) ---
    if args.full:
        print("-" * 60)
        total = PASS + FAIL
        pct = (PASS / total * 100) if total else 0.0
        print(f"Toplam: {PASS}/{total} geçti ({pct:.1f}%)")

        level = 0
        if total == PASS:
            level += 1  # L1: tüm temel dosyalar + dokümantasyon kontrolleri
        if ci_exists and scripts_exist:
            level += 1  # L2: doğrulama altyapısı
        if has_tests:
            level += 1  # L3: test altyapısı
        if versions_count >= 2:
            level += 1  # L4: sürüm/metrik takibi
        if level >= 4 and iterations >= 3 and pct >= 90:
            level = 5  # L5: kaçış koşulu

        print(f"Olgunluk seviyesi: {level}/5")
        if level >= 5:
            print("ESCAPED — Tüm kaçış koşulları sağlandı.")
        else:
            missing = []
            if FAIL:
                missing.append("tüm kontrollerin geçmesi")
            if not has_tests:
                missing.append("test altyapısı")
            if versions_count < 2:
                missing.append("en az 2 sürüm")
            if iterations < 3:
                missing.append(f"{3 - iterations} iterasyon daha (şu an {iterations})")
            print(f"Kaçış için gerekenler: {', '.join(missing)}")
        sys.exit(1 if FAIL else 0)
    else:
        print("-" * 60)
        print(f"Toplam: {PASS} PASS, {FAIL} FAIL")

    if args.ci and FAIL:
        sys.exit(1)


if __name__ == "__main__":
    main()
