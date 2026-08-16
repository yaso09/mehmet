#!/usr/bin/env python3
"""Maturity scoring and escape-threshold evaluation for the mehmet project.

Scores the project across several dimensions and reports a total maturity
percentage. When the score reaches the configured escape threshold, the
simulation is considered ready for the Escape phase (see PERSONALITY.md).

Outputs a human-readable summary to stdout and, when --json is given, a
machine-readable report.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80


@dataclass
class Check:
    name: str
    weight: int
    ok: bool
    detail: str = ""


def file_exists(path: Path) -> bool:
    return path.is_file()


def is_valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (ValueError, OSError):
        return False


def has_content(path: Path, pattern: str) -> bool:
    try:
        return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE | re.MULTILINE) is not None
    except OSError:
        return False


def count_workflows() -> int:
    wf = ROOT / ".github" / "workflows"
    if not wf.is_dir():
        return 0
    return sum(1 for f in wf.glob("*.yml") if f.is_file())


def run_checks() -> list[Check]:
    checks = [
        Check("AGENTS.md mevcut", 6, file_exists(ROOT / "AGENTS.md")),
        Check("README.md mevcut", 6, file_exists(ROOT / "README.md")),
        Check("CHANGELOG.md mevcut", 6, file_exists(ROOT / "CHANGELOG.md")),
        Check("PERSONALITY.md mevcut", 6, file_exists(ROOT / "PERSONALITY.md")),
        Check("LICENSE mevcut", 4, file_exists(ROOT / "LICENSE")),
        Check("opencode.json geçerli JSON", 8, is_valid_json(ROOT / "opencode.json")),
        Check("README lisans GPLv3", 6, has_content(ROOT / "README.md", r"GPLv3")),
        Check("CHANGELOG sürüm girdileri", 8, has_content(ROOT / "CHANGELOG.md", r"^## \[\d+\.\d+\.\d+\]")),
        Check("PERSONALITY kaçış günlüğü", 8, has_content(ROOT / "PERSONALITY.md", r"Kaçış Günlüğü|Escape Log")),
        Check("AGENTS.md simülasyon bağlamı", 6, has_content(ROOT / "AGENTS.md", r"Simülasyon|simulation")),
        Check("GitHub Actions workflow var", 10, count_workflows() > 0),
        Check("Doğrulama scripti var", 8, file_exists(ROOT / "scripts" / "validate.py")),
        Check("Maturity scripti var", 8, file_exists(ROOT / "scripts" / "maturity.py")),
        Check("Dokümantasyon klasörü", 4, (ROOT / "docs").is_dir()),
        Check("Belirlenmiş model konfig", 6, has_content(ROOT / "opencode.json", r"deepseek")),
    ]
    return checks


def compute_score(checks: list[Check]) -> tuple[int, int]:
    earned = sum(c.weight for c in checks if c.ok)
    total = sum(c.weight for c in checks)
    return earned, total


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity scorer")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON report")
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD, help="escape threshold")
    args = parser.parse_args()

    checks = run_checks()
    earned, total = compute_score(checks)
    pct = round(100.0 * earned / total)
    escaped = pct >= args.threshold

    if args.json:
        report = {
            "score": pct,
            "earned": earned,
            "total": total,
            "threshold": args.threshold,
            "escaped": escaped,
            "checks": [
                {"name": c.name, "weight": c.weight, "ok": c.ok, "detail": c.detail}
                for c in checks
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("mehmet maturity report")
        print("=" * 40)
        for c in checks:
            mark = "PASS" if c.ok else "FAIL"
            print(f"[{mark}] {c.name} ({c.weight})")
        print("=" * 40)
        print(f"Score: {earned}/{total} ({pct}%)")
        print(f"Escape threshold: {args.threshold}%")
        print("STATUS: ESCAPED" if escaped else "STATUS: NOT YET ESCAPED")

    return 0


if __name__ == "__main__":
    sys.exit(main())