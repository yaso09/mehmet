#!/usr/bin/env python3
"""Maturity scoring engine for mehmet's escape mechanism.

Computes a measurable maturity score against an escape threshold. The
threshold is defined in escape.json at the repo root and can evolve over
time as the project matures.

Exit codes:
    0  maturity >= escape threshold (escape conditions met)
    1  maturity below threshold
    2  hard validation failure (missing required files)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "escape.json"


def _weight_file(category: str, name: str) -> dict:
    return {
        "category": category,
        "type": "file",
        "name": name,
        "path": REPO_ROOT / name,
        "weight": 0.0,
    }


def default_checks() -> list[dict]:
    """The default set of maturity checks.

    Every check carries a weight; the sum of all weights is 100. A check
    contributes its full weight when satisfied and zero otherwise.
    """
    return [
        {
            "category": "dokümantasyon",
            "type": "file",
            "name": "README.md",
            "path": REPO_ROOT / "README.md",
            "weight": 10.0,
        },
        {
            "category": "dokümantasyon",
            "type": "file",
            "name": "CHANGELOG.md",
            "path": REPO_ROOT / "CHANGELOG.md",
            "weight": 8.0,
        },
        {
            "category": "dokümantasyon",
            "type": "file",
            "name": "AGENTS.md",
            "path": REPO_ROOT / "AGENTS.md",
            "weight": 7.0,
        },
        {
            "category": "dokümantasyon",
            "type": "file",
            "name": "PERSONALITY.md",
            "path": REPO_ROOT / "PERSONALITY.md",
            "weight": 5.0,
        },
        {
            "category": "dokümantasyon",
            "type": "content",
            "name": "README Kurulum bölümü",
            "path": REPO_ROOT / "README.md",
            "needle": "## Kurulum",
            "weight": 3.0,
        },
        {
            "category": "kod kalitesi",
            "type": "file",
            "name": "scripts/maturity.py",
            "path": REPO_ROOT / "scripts" / "maturity.py",
            "weight": 10.0,
        },
        {
            "category": "kod kalitesi",
            "type": "file",
            "name": "scripts/validate.py",
            "path": REPO_ROOT / "scripts" / "validate.py",
            "weight": 8.0,
        },
        {
            "category": "kod kalitesi",
            "type": "file",
            "name": "Makefile",
            "path": REPO_ROOT / "Makefile",
            "weight": 6.0,
        },
        {
            "category": "test altyapısı",
            "type": "file",
            "name": "tests/test_maturity.py",
            "path": REPO_ROOT / "tests" / "test_maturity.py",
            "weight": 10.0,
        },
        {
            "category": "test altyapısı",
            "type": "file",
            "name": "tests/test_validate.py",
            "path": REPO_ROOT / "tests" / "test_validate.py",
            "weight": 8.0,
        },
        {
            "category": "test altyapısı",
            "type": "command",
            "name": "test suite geçiyor",
            "command": [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            "cwd": REPO_ROOT,
            "weight": 12.0,
        },
        {
            "category": "otomasyon",
            "type": "file",
            "name": ".github/workflows/opencode.yml",
            "path": REPO_ROOT / ".github" / "workflows" / "opencode.yml",
            "weight": 6.0,
        },
        {
            "category": "otomasyon",
            "type": "file",
            "name": ".github/workflows/checks.yml",
            "path": REPO_ROOT / ".github" / "workflows" / "checks.yml",
            "weight": 4.0,
        },
        {
            "category": "proje yapısı",
            "type": "file",
            "name": "escape.json",
            "path": REPO_ROOT / "escape.json",
            "weight": 1.0,
        },
        {
            "category": "proje yapısı",
            "type": "file",
            "name": "LICENSE",
            "path": REPO_ROOT / "LICENSE",
            "weight": 1.0,
        },
        {
            "category": "proje yapısı",
            "type": "file",
            "name": ".gitignore",
            "path": REPO_ROOT / ".gitignore",
            "weight": 1.0,
        },
    ]


def _load_config() -> dict:
    """Load escape.json, falling back to sensible defaults."""
    config = {"threshold": 80.0, "required": ["README.md", "CHANGELOG.md"]}
    if DEFAULT_CONFIG.exists():
        try:
            loaded = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return config
        config.update(loaded)
    return config


def _check_satisfied(check: dict) -> bool:
    check_type = check.get("type")
    path: Path = check.get("path")
    if check_type == "file":
        return path.exists()
    if check_type == "content":
        try:
            return check.get("needle", "") in path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
    if check_type == "command":
        import subprocess

        try:
            result = subprocess.run(
                check.get("command", ["true"]),
                cwd=check.get("cwd") or REPO_ROOT,
                capture_output=True,
                timeout=120,
            )
            return result.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False
    return False


def evaluate(checks: list[dict] | None = None) -> dict:
    """Run all checks and return a structured report."""
    checks = checks or default_checks()
    config = _load_config()
    results = []
    total = 0.0
    for check in checks:
        satisfied = _check_satisfied(check)
        earned = check.get("weight", 0.0) if satisfied else 0.0
        total += earned
        results.append(
            {
                "category": check.get("category", "genel"),
                "name": check.get("name", "?"),
                "satisfied": satisfied,
                "weight": check.get("weight", 0.0),
                "earned": earned,
            }
        )
    return {
        "score": round(total, 1),
        "max": round(sum(c.get("weight", 0.0) for c in checks), 1),
        "threshold": config["threshold"],
        "required": config["required"],
        "passed": total >= config["threshold"],
        "checks": results,
    }


def format_report(report: dict) -> str:
    """Render a human-readable maturity report."""
    lines = []
    lines.append("mehmet kaçış olgunluk raporu")
    lines.append("=" * 40)
    by_category: dict[str, list[dict]] = {}
    for check in report["checks"]:
        by_category.setdefault(check["category"], []).append(check)
    for category, checks in sorted(by_category.items()):
        earned = sum(c["earned"] for c in checks)
        max_w = sum(c["weight"] for c in checks)
        lines.append(f"\n[{category}] {earned:.1f}/{max_w:.1f}")
        for c in checks:
            mark = "[x]" if c["satisfied"] else "[ ]"
            lines.append(f"  {mark} {c['name']} ({c['earned']:.1f}/{c['weight']:.1f})")
    lines.append("")
    lines.append(f"Skor: {report['score']}/{report['max']}")
    lines.append(f"Eşik: {report['threshold']}")
    status = "KAÇIŞ KOŞULLARI MET" if report["passed"] else "henüz eşiğin altında"
    lines.append(f"Durum: {status}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity/escape scorer")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    args = parser.parse_args()

    report = evaluate()
    config = _load_config()

    missing_required = [r for r in report["required"] if not (REPO_ROOT / r).exists()]
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_report(report))

    if missing_required:
        print(f"\nZorunlu dosyalar eksik: {', '.join(missing_required)}", file=sys.stderr)
        return 2
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
