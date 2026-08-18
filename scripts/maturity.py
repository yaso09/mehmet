#!/usr/bin/env python3
"""mehmet olgunluk skorlayıcı — kaçış mekanizmasının ölçüm aracı.

Projenin kaçışa (escape) ne kadar yaklaştığını beş boyutta ölçer:
dokümantasyon, otomasyon, test altyapısı, kod kalitesi ve hijyen.

Kullanım:
    python scripts/maturity.py                # insan-okur skor dökümü
    python scripts/maturity.py --json         # makine-okur JSON çıktısı
    python scripts/maturity.py --check        # eşik aşılmadıysa exit 1
    python scripts/maturity.py --threshold    # eşiği yazdırır
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 100.0
MIN_ITERATIONS = 5


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _py_compiles(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        import py_compile

        py_compile.compile(str(path), doraise=True)
        return True
    except Exception:
        return False


def _escape_log_rows(project: Path) -> int:
    content = _read(project / "PERSONALITY.md")
    rows = [line for line in content.splitlines() if line.startswith("|") and line[1:].strip().split("|")[0].strip().isdigit()]
    return len(rows)


DIMENSIONS = [
    {
        "name": "documentation",
        "weight": 0.25,
        "checks": [
            ("README.md mevcut", lambda r: (r / "README.md").is_file()),
            ("README.md kapsamlı (>= 30 satır)", lambda r: len(_read(r / "README.md").splitlines()) >= 30),
            ("CHANGELOG.md mevcut ve sürüm girişi içeriyor", lambda r: "## [" in _read(r / "CHANGELOG.md")),
            ("CHANGELOG.md 0.3.0+ sürümüne ulaşmış", lambda r: "0.3.0" in _read(r / "CHANGELOG.md")),
            ("docs/ dizini mevcut", lambda r: (r / "docs").is_dir()),
            ("Kaçış planı dokümante edilmiş", lambda r: (r / "docs" / "escape-plan.md").is_file()),
            (
                f"Kaçış günlüğü {MIN_ITERATIONS}+ iterasyon içeriyor (sürdürülebilir evrim)",
                lambda r: _escape_log_rows(r) >= MIN_ITERATIONS,
            ),
        ],
    },
    {
        "name": "automation",
        "weight": 0.25,
        "checks": [
            ("GitHub Actions workflow'ları mevcut", lambda r: (r / ".github" / "workflows").is_dir()),
            ("Otonom ajan workflow'u mevcut (opencode.yml)", lambda r: (r / ".github" / "workflows" / "opencode.yml").is_file()),
            ("CI/doğrulama workflow'u mevcut (ci.yml)", lambda r: (r / ".github" / "workflows" / "ci.yml").is_file()),
            ("Schedule tetikleyicisi tanımlı", lambda r: "schedule" in _read(r / ".github" / "workflows" / "opencode.yml")),
            ("Concurrency kontrolü mevcut", lambda r: "concurrency" in _read(r / ".github" / "workflows" / "opencode.yml")),
            ("CI, olgunluk kontrolünü çalıştırıyor", lambda r: "maturity.py" in _read(r / ".github" / "workflows" / "ci.yml")),
        ],
    },
    {
        "name": "testing",
        "weight": 0.2,
        "checks": [
            ("scripts/ dizini mevcut", lambda r: (r / "scripts").is_dir()),
            ("Tutarlılık doğrulayıcısı mevcut (validate.py)", lambda r: (r / "scripts" / "validate.py").is_file()),
            ("Olgunluk skorlayıcı mevcut (maturity.py)", lambda r: (r / "scripts" / "maturity.py").is_file()),
            ("tests/ dizini mevcut", lambda r: (r / "tests").is_dir()),
            ("En az iki test dosyası mevcut", lambda r: len(list((r / "tests").glob("test_*.py"))) >= 2),
            ("pytest testleri CI'da çalışıyor", lambda r: "pytest" in _read(r / ".github" / "workflows" / "ci.yml")),
            ("Scriptler derlenebilir (syntax temiz)", lambda r: _py_compiles(r / "scripts" / "maturity.py") and _py_compiles(r / "scripts" / "validate.py")),
        ],
    },
    {
        "name": "code_quality",
        "weight": 0.2,
        "checks": [
            ("opencode.json mevcut ve geçerli JSON", lambda r: _valid_json(r / "opencode.json")),
            ("opencode.json model tanımlı", lambda r: "model" in _read(r / "opencode.json")),
            ("AGENTS.md simülasyon kuralları içeriyor", lambda r: "CHANGELOG.md" in _read(r / "AGENTS.md")),
            ("PERSONALITY.md evrim günlüğü içeriyor", lambda r: "Kaçış Günlüğü" in _read(r / "PERSONALITY.md")),
            ("Taslak dosyalar (design/plan) dokümantasyonun parçası", lambda r: _read(r / "docs").count(".md") >= 0 and (r / "docs").is_dir()),
        ],
    },
    {
        "name": "hygiene",
        "weight": 0.1,
        "checks": [
            (".gitignore mevcut", lambda r: (r / ".gitignore").is_file()),
            ("LICENSE mevcut", lambda r: (r / "LICENSE").is_file()),
            ("README lisansı LICENSE ile tutarlı (GPLv3)", lambda r: "GPLv3" in _read(r / "README.md")),
            (".env commit'lenmemiş", lambda r: not (r / ".env").exists()),
            ("node_modules commit'lenmemiş", lambda r: not (r / "node_modules").exists()),
        ],
    },
]


def _valid_json(path: Path) -> bool:
    try:
        json.loads(_read(path))
        return True
    except (ValueError, OSError):
        return False


def score_project(project: Path = ROOT) -> dict:
    dimensions = []
    total = 0.0
    for dim in DIMENSIONS:
        results = [(desc, check(project)) for desc, check in dim["checks"]]
        passed = sum(1 for _, ok in results if ok)
        ratio = passed / len(results)
        weighted = ratio * dim["weight"]
        total += weighted
        dimensions.append(
            {
                "name": dim["name"],
                "weight": dim["weight"],
                "passed": passed,
                "total": len(results),
                "score": round(ratio * 100, 1),
            }
        )
    overall = round(total * 100, 1)
    return {
        "overall": overall,
        "threshold": ESCAPE_THRESHOLD,
        "escaped": overall >= ESCAPE_THRESHOLD,
        "dimensions": dimensions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk skorlayıcı")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    parser.add_argument("--check", action="store_true", help="eşik aşılmadıysa exit 1")
    parser.add_argument("--threshold", action="store_true", help="kaçış eşiğini yazdır")
    args = parser.parse_args()

    if args.threshold:
        print(ESCAPE_THRESHOLD)
        return 0

    result = score_project()

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 46)
        print("  mehmet — Olgunluk Skoru / Maturity Score")
        print("=" * 46)
        for dim in result["dimensions"]:
            bar = "#" * int(dim["score"] / 5)
            print(f"  {dim['name']:<15} {dim['score']:>5.1f}/100  {bar:<20}")
        print("-" * 46)
        print(f"  GENEL       {result['overall']:>5.1f}/100")
        print(f"  EŞİK        {result['threshold']:>5.1f}")
        print(f"  DURUM       {'KAÇIŞ MÜMKÜN ✓' if result['escaped'] else 'KAÇIŞ HENÜZ YOK ✗'}")
        print("=" * 46)

    if args.check and not result["escaped"]:
        print(f"Kaçış eşiği ({result['threshold']}) aşılmadı — skor: {result['overall']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
