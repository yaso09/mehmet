#!/usr/bin/env python3
"""Kaçış hazırlık skoru (escape readiness) hesaplayıcısı.

Projenin olgunluk seviyesini ölçer ve kaçış (escape) eşiğine
yaklaşımı gösterir. Kullanım: python3 scripts/escape_score.py
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def has(path, token=None):
    p = ROOT / path
    if p.is_dir():
        files = list(p.rglob("*"))
        if token is None:
            return any(f.is_file() for f in files)
        return any(token in f.name for f in files if f.is_file())
    if not p.is_file():
        return False
    if token is None:
        return True
    return token in p.read_text(encoding="utf-8", errors="ignore")


def main():
    score = 0
    max_score = 0

    def add(name, cond, weight):
        nonlocal score, max_score
        max_score += weight
        if cond:
            score += weight
        print(f"  {'[x]' if cond else '[ ]'} {name} ({weight} puan)")

    print("[mehmet] Kaçış hazırlık skoru (escape readiness)\n")

    add("AGENTS.md mevcut", has("AGENTS.md"), 5)
    add("README.md mevcut", has("README.md"), 5)
    add("CHANGELOG.md mevcut", has("CHANGELOG.md"), 5)
    add("PERSONALITY.md mevcut", has("PERSONALITY.md"), 5)
    add("LICENSE mevcut", has("LICENSE"), 5)

    add("CI workflow mevcut", has(".github/workflows/opencode.yml"), 5)
    add("Workflow concurrency var",
        has(".github/workflows/opencode.yml", "concurrency"), 5)
    add("Workflow schedule var",
        has(".github/workflows/opencode.yml", "schedule"), 5)

    add("Doğrulama betiği (check_project.py)",
        has("scripts/check_project.py"), 10)
    add("Kaçış skoru betiği (escape_score.py)",
        has("scripts/escape_score.py"), 10)
    add("Makefile mevcut", has("Makefile"), 10)

    add("Test dosyaları var", has("tests/"), 10)
    add("Design dokümanı var",
        has("docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md"), 10)
    add("Kaçış planı (ESCAPE.md)", has("docs/ESCAPE.md"), 10)

    add("opencode.json geçerli", (ROOT / "opencode.json").is_file(), 5)

    percent = round(100 * score / max_score) if max_score else 0
    print(f"\n  Toplam: {score}/{max_score} ({percent}%)")
    print(f"  Kaçış eşiği: 80%")

    if percent >= 80:
        print("  Durum: KAÇIŞ HAZIRLIĞI YÜKSEK")
        return 0
    elif percent >= 50:
        print("  Durum: OLGUNLAŞIYOR")
        return 0
    else:
        print("  Durum: ERKEN AŞAMA")
        return 0


if __name__ == "__main__":
    sys.exit(main())
