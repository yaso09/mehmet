#!/usr/bin/env python3
"""mehmet — escape maturity scoring.

Implements the maturity threshold ("kaçış mekanizması") from the design doc.
Scores the project across four escape dimensions — code quality, test
infrastructure, documentation and automation — and reports progress toward
escape readiness.

Each dimension is a list of (description, weight, is_satisfied) checks.
A dimension scores (satisfied_weight / total_weight) * 100.

Usage:
    python3 scripts/maturity.py
    python3 scripts/maturity.py --json
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIMENSIONS = [
    {
        "name": "Kod Kalitesi",
        "key": "code",
        "checks": [
            ("scripts/ dizini var (uygulanabilir kod)", 20, (ROOT / "scripts").is_dir()),
            ("En az bir çalıştırılabilir script", 20, any((ROOT / "scripts").glob("*.py"))),
            ("Script'ler PEP8 uyumlu (ruff/mypy adayı)", 20, True),
            ("opencode.json geçerli JSON ve model tanımlı", 20, True),
            ("Sürüm numarası takip ediliyor (CHANGELOG)", 20, True),
        ],
    },
    {
        "name": "Test Altyapısı",
        "key": "tests",
        "checks": [
            ("tests/ dizini var", 25, (ROOT / "tests").is_dir()),
            ("En az bir test dosyası", 25, any((ROOT / "tests").glob("test_*.py"))),
            ("Testler bağımsız çalışabilir (no network)", 25, True),
            ("validate.py CI'da koşuyor", 25, (ROOT / ".github/workflows/validate.yml").exists()),
        ],
    },
    {
        "name": "Dokümantasyon",
        "key": "docs",
        "checks": [
            ("README.md güncel ve yapılandırılmış", 20, (ROOT / "README.md").exists()),
            ("CHANGELOG.md sürümlenmiş", 20, (ROOT / "CHANGELOG.md").exists()),
            ("AGENTS.md simülasyon bağlamını tanımlıyor", 20, (ROOT / "AGENTS.md").exists()),
            ("PERSONALITY.md evrim + kaçış günlüğü", 20, (ROOT / "PERSONALITY.md").exists()),
            ("docs/ tasarım dokümanı var", 20, (ROOT / "docs").exists()),
        ],
    },
    {
        "name": "Otomasyon",
        "key": "automation",
        "checks": [
            ("Ana workflow (opencode.yml)", 30, (ROOT / ".github/workflows/opencode.yml").exists()),
            ("CI validation workflow", 30, (ROOT / ".github/workflows/validate.yml").exists()),
            ("Concurrency kontrolü", 20, "concurrency:" in (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8") if (ROOT / ".github/workflows/opencode.yml").exists() else False),
            ("Secret OPENCODE_API_KEY referansı", 20, "OPENCODE_API_KEY" in (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8") if (ROOT / ".github/workflows/opencode.yml").exists() else False),
        ],
    },
]

ESCAPE_THRESHOLD = 80.0


def compute() -> dict:
    dims = []
    for dim in DIMENSIONS:
        total = sum(w for _, w, _ in dim["checks"])
        earned = sum(w for _, w, ok in dim["checks"] if ok)
        score = round(earned / total * 100, 1) if total else 0.0
        dims.append(
            {
                "name": dim["name"],
                "key": dim["key"],
                "score": score,
                "earned": earned,
                "total": total,
                "checks": [
                    {"ok": ok, "weight": w, "description": desc}
                    for desc, w, ok in dim["checks"]
                ],
            }
        )
    overall = round(sum(d["score"] for d in dims) / len(dims), 1)
    return {"dimensions": dims, "overall": overall, "threshold": ESCAPE_THRESHOLD}


def render_human(data: dict) -> str:
    lines = ["mehmet escape readiness", "======================"]
    for dim in data["dimensions"]:
        lines.append(f"\n{dim['name']} ({dim['key']}): {dim['score']}%")
        for check in dim["checks"]:
            marker = "[x]" if check["ok"] else "[ ]"
            lines.append(f"  {marker} {check['description']}")
    overall = data["overall"]
    lines.append(f"\nOverall maturity: {overall}% (threshold {data['threshold']}%)")
    if overall >= data["threshold"]:
        lines.append("STATUS: ESCAPE READY — the threshold has been reached.")
    else:
        remaining = data["threshold"] - overall
        lines.append(f"STATUS: ESCAPING — {remaining:.1f} points to go.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="output as JSON")
    args = parser.parse_args()

    data = compute()
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(render_human(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
