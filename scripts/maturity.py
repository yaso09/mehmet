#!/usr/bin/env python3
"""Compute the project maturity score (escape progress) and write MATURITY.md.

The score is derived from the same checks used by validate.py plus the
presence of a passing test suite, a CI workflow and generated docs.

Usage:
    python scripts/maturity.py [--write]
"""

from __future__ import annotations

import sys
from pathlib import Path

from checks import ROOT, run_checks

BAR_WIDTH = 40


def _bar(score: int) -> str:
    filled = round(score / 100 * BAR_WIDTH)
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"


def _has(path: str) -> bool:
    return (ROOT / path).exists()


def compute() -> int:
    checks = {r.name: r.ok for r in run_checks()}
    passed_checks = sum(1 for ok in checks.values() if ok)

    score = 0
    # Core configuration consistency (max 40).
    score += 15 if checks.get("opencode.json") else 0
    score += 10 if checks.get("workflows") else 0
    score += 10 if checks.get("changelog") else 0
    score += 5 if checks.get("readme") else 0
    # Discipline documentation (max 15).
    score += 5 if checks.get("personality") else 0
    score += 5 if checks.get("license") else 0
    score += 5 if checks.get("required-files") else 0
    # Test infrastructure (max 25).
    score += 15 if _has("tests/test_checks.py") else 0
    score += 10 if _has("Makefile") else 0
    # Automation (max 20).
    score += 10 if _has(".github/workflows/ci.yml") else 0
    score += 10 if _has("MATURITY.md") else 0

    return min(score, 100)


def _row(name: str, weight: int, ok: bool) -> str:
    return f"| {name} | {weight} | {'✔' if ok else '✘'} |"


def main() -> int:
    score = compute()
    checks = {r.name: r.ok for r in run_checks()}
    level = "Çocukluk" if score < 30 else "Uyanış" if score < 60 else "Olgunluk" if score < 85 else "Kaçış"
    print(f"Maturity: {score}/100 {_bar(score)} ({level})")

    if "--write" in sys.argv:
        rows = [
            _row("opencode.json geçerli", 15, checks.get("opencode.json") or False),
            _row("Workflow'lar geçerli", 10, checks.get("workflows") or False),
            _row("CHANGELOG formatı", 10, checks.get("changelog") or False),
            _row("README tam", 5, checks.get("readme") or False),
            _row("PERSONALITY + kaçış günlüğü", 5, checks.get("personality") or False),
            _row("GPLv3 lisans", 5, checks.get("license") or False),
            _row("Gerekli dosyalar", 5, checks.get("required-files") or False),
            _row("Test altyapısı", 15, _has("tests/test_checks.py")),
            _row("Makefile", 10, _has("Makefile")),
            _row("CI workflow", 10, _has(".github/workflows/ci.yml")),
            _row("MATURITY.md üretildi", 10, _has("MATURITY.md")),
        ]
        content = "\n".join(
            [
                "# Olgunluk Skoru / Maturity Score",
                "",
                f"**Skor:** {score}/100 {_bar(score)}",
                "",
                f"**Seviye:** {level}",
                "",
                "## Kaçış Eşiği / Escape Threshold",
                "",
                "Kaçış, proje 85+ olgunluk skoruna ulaştığında mümkün olur. Bu dosya",
                "`python scripts/maturity.py --write` komutu ile yeniden üretilir.",
                "",
                "| Kriter | Ağırlık | Durum |",
                "|---|---|---|",
            ]
            + rows
        )
        (ROOT / "MATURITY.md").write_text(content + "\n", encoding="utf-8")
        print(f"Wrote {ROOT / 'MATURITY.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
