#!/usr/bin/env python3
"""Maturity score calculator for the mehmet project.

Computes an objective 0-100 maturity score based on measurable project
health signals and writes the result to METRICS.md (append-only history).

Exit code 0 on success, 1 if the score drops below the current threshold.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "METRICS.md"


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def has(path):
    return path.is_file()


def score_project():
    checks = {}

    checks["AGENTS.md mevcut"] = has(ROOT / "AGENTS.md")
    checks["PERSONALITY.md mevcut"] = has(ROOT / "PERSONALITY.md")
    checks["CHANGELOG.md mevcut"] = has(ROOT / "CHANGELOG.md")
    checks["README.md mevcut"] = has(ROOT / "README.md")
    checks["Lisans (GPLv3)"] = "GNU GENERAL PUBLIC LICENSE" in read(ROOT / "LICENSE")
    checks["Test altyapısı mevcut"] = has(ROOT / "tests" / "test_project_health.py")

    opencode = read(ROOT / "opencode.json")
    checks["opencode.json geçerli"] = '"model"' in opencode

    changelog = read(ROOT / "CHANGELOG.md")
    versions = re.findall(r"^## \[([0-9.]+)\]", changelog, re.M)
    checks["Changelog sürüm sayısı >= 3"] = len(versions) >= 3

    personality = read(ROOT / "PERSONALITY.md")
    log_rows = re.findall(r"^\|\s*\d+\s*\|", personality, re.M)
    checks["Kaçış günlüğü girdisi >= 3"] = len(log_rows) >= 3

    ci = read(ROOT / ".github" / "workflows" / "ci.yml")
    checks["CI workflow mevcut"] = has(ROOT / ".github" / "workflows" / "ci.yml")
    checks["CI test çalıştırıyor"] = "python -m unittest" in ci

    makefile = read(ROOT / "Makefile")
    checks["Makefile mevcut"] = has(ROOT / "Makefile")
    checks["Makefile test hedefi"] = "test:" in makefile

    total = sum(1 for ok in checks.values() if ok)
    score = round(100 * total / len(checks), 1)
    return score, checks


def append_metrics(score, checks):
    line = f"| {date.today().isoformat()} | {score} | {sum(1 for ok in checks.values() if ok)}/{len(checks)} |"
    if METRICS_FILE.is_file():
        text = METRICS_FILE.read_text(encoding="utf-8")
        if not text.strip():
            text = HEADER + "\n"
    else:
        text = HEADER + "\n"
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
        METRICS_FILE.write_text(text, encoding="utf-8")


HEADER = (
    "# Maturity Metrics\n\n"
    "| Tarih | Puan | Geçen Kontrol |\n"
    "|-------|------|---------------|"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=50.0, help="Min score (default 50)")
    parser.add_argument("--no-write", action="store_true", help="Do not write METRICS.md")
    args = parser.parse_args()

    score, checks = score_project()

    print(f"Olgunluk Puanı: {score}/100")
    print()
    for name, ok in checks.items():
        print(f"  [{'✓' if ok else '✗'}] {name}")

    if not args.no_write:
        append_metrics(score, checks)

    if score < args.threshold:
        print(f"\nPuan {args.threshold} eşiğinin altında: {score}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
