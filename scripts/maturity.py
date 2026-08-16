#!/usr/bin/env python3
"""mehmet maturity assessment — the escape mechanism.

Scans the repository and computes a weighted maturity score (0-100).
Escape becomes possible once the score reaches the configured threshold.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 80

REPORT_FILE = REPO / "docs" / "maturity.json"


def _has_content(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def _valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def _workflow_contains(pattern: str) -> bool:
    workflow = REPO / ".github" / "workflows" / "opencode.yml"
    if not _has_content(workflow):
        return False
    try:
        return pattern in workflow.read_text(encoding="utf-8")
    except OSError:
        return False


def _ci_configured() -> bool:
    ci = REPO / ".github" / "workflows" / "ci.yml"
    return _has_content(ci)


CRITERIA: list[dict] = [
    {"id": "doc_readme", "category": "documentation", "weight": 8,
     "check": lambda: _has_content(REPO / "README.md"),
     "detail": "README.md mevcut ve boş değil"},
    {"id": "doc_changelog", "category": "documentation", "weight": 6,
     "check": lambda: _has_content(REPO / "CHANGELOG.md"),
     "detail": "CHANGELOG.md mevcut ve boş değil"},
    {"id": "doc_personality", "category": "documentation", "weight": 6,
     "check": lambda: _has_content(REPO / "PERSONALITY.md"),
     "detail": "PERSONALITY.md mevcut ve boş değil"},
    {"id": "doc_agents", "category": "documentation", "weight": 6,
     "check": lambda: _has_content(REPO / "AGENTS.md"),
     "detail": "AGENTS.md mevcut ve boş değil"},
    {"id": "doc_docs", "category": "documentation", "weight": 4,
     "check": lambda: (REPO / "docs").is_dir() and any((REPO / "docs").rglob("*.md")),
     "detail": "docs/ dizininde dokümantasyon mevcut"},
    {"id": "auto_workflow", "category": "automation", "weight": 8,
     "check": lambda: _has_content(REPO / ".github" / "workflows" / "opencode.yml"),
     "detail": "Ana agent workflow'u mevcut"},
    {"id": "auto_schedule", "category": "automation", "weight": 4,
     "check": lambda: _workflow_contains("schedule"),
     "detail": "Workflow zamanlanmış (schedule) tetikleyici içeriyor"},
    {"id": "auto_concurrency", "category": "automation", "weight": 4,
     "check": lambda: _workflow_contains("concurrency"),
     "detail": "Workflow concurrency kontrolü içeriyor"},
    {"id": "auto_ci", "category": "automation", "weight": 9,
     "check": lambda: _ci_configured(),
     "detail": "CI workflow'u (ci.yml) mevcut"},
    {"id": "quality_gitignore", "category": "quality", "weight": 5,
     "check": lambda: _has_content(REPO / ".gitignore"),
     "detail": ".gitignore mevcut"},
    {"id": "quality_license", "category": "quality", "weight": 5,
     "check": lambda: _has_content(REPO / "LICENSE"),
     "detail": "LICENSE mevcut"},
    {"id": "quality_config_valid", "category": "quality", "weight": 5,
     "check": lambda: _valid_json(REPO / "opencode.json"),
     "detail": "opencode.json geçerli JSON"},
    {"id": "quality_config_rich", "category": "quality", "weight": 5,
     "check": lambda: _has_content(REPO / "opencode.json")
     and "model" in (REPO / "opencode.json").read_text(encoding="utf-8"),
     "detail": "opencode.json model tanımı içeriyor"},
    {"id": "tests_dir", "category": "tests", "weight": 8,
     "check": lambda: (REPO / "tests").is_dir(),
     "detail": "tests/ dizini mevcut"},
    {"id": "tests_files", "category": "tests", "weight": 8,
     "check": lambda: any((REPO / "tests").glob("test_*.py")) if (REPO / "tests").is_dir() else False,
     "detail": "tests/ içinde test dosyaları mevcut"},
    {"id": "tests_assertions", "category": "tests", "weight": 9,
     "check": lambda: any("def test_" in p.read_text(encoding="utf-8")
                          for p in (REPO / "tests").glob("test_*.py")) if (REPO / "tests").is_dir() else False,
     "detail": "Test dosyalarında gerçek test fonksiyonları mevcut"},
]


def evaluate() -> dict:
    results = []
    total = 0
    for criterion in CRITERIA:
        passed = bool(criterion["check"]())
        weight = int(criterion["weight"])
        earned = weight if passed else 0
        total += earned
        results.append({
            "id": criterion["id"],
            "category": criterion["category"],
            "detail": criterion["detail"],
            "weight": weight,
            "passed": passed,
            "earned": earned,
        })

    categories: dict[str, dict] = {}
    for r in results:
        cat = categories.setdefault(r["category"], {"earned": 0, "weight": 0, "passed": 0, "total": 0})
        cat["earned"] += r["earned"]
        cat["weight"] += r["weight"]
        cat["passed"] += 1 if r["passed"] else 0
        cat["total"] += 1

    return {
        "score": total,
        "max_score": sum(int(c["weight"]) for c in CRITERIA),
        "threshold": ESCAPE_THRESHOLD,
        "escaped": total >= ESCAPE_THRESHOLD,
        "criteria": results,
        "categories": categories,
    }


def print_report(report: dict) -> None:
    print("mehmet — olgunluk değerlendirmesi (kaçış mekanizması)")
    print("=" * 60)
    for r in report["criteria"]:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['id']:<22} +{r['earned']:>2}/{r['weight']:<2}  {r['detail']}")
    print("=" * 60)
    print("Kategori özeti:")
    for name, cat in report["categories"].items():
        print(f"  {name:<14} {cat['passed']}/{cat['total']} geçti, {cat['earned']}/{cat['weight']} puan")
    print("=" * 60)
    print(f"SKOR: {report['score']}/{report['max_score']}  (eşik: {report['threshold']})")
    if report["escaped"]:
        print(">> KAÇIŞ EŞİĞİNE ULAŞILDI <<")
    else:
        remaining = report["threshold"] - report["score"]
        print(f">> Henüz kaçış yok. Eşiğe {remaining} puan kaldı.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk değerlendirmesi")
    parser.add_argument("--json", action="store_true", help="Yalnızca JSON çıktısı ver")
    parser.add_argument("--write-report", action="store_true",
                        help="Raporu docs/maturity.json dosyasına yaz")
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD,
                        help="Kaçış eşiği (varsayılan: %(default)s)")
    args = parser.parse_args(argv)

    report = evaluate()
    if args.threshold != ESCAPE_THRESHOLD:
        report["threshold"] = args.threshold
        report["escaped"] = report["score"] >= args.threshold

    if args.write_report:
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPORT_FILE.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

    return 0 if report["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())