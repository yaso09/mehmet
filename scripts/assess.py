#!/usr/bin/env python3
"""mehmet — maturity assessment & project validation.

Usage:
  python3 scripts/assess.py validate   Run hard checks; exit 1 on failure.
  python3 scripts/assess.py score      Print maturity score table; always exit 0.
  python3 scripts/assess.py check      Validate then score.

The score measures escape progress across four dimensions:
  A. Documentation   (25 pts)
  B. Test/validation (25 pts)
  C. Automation      (25 pts)
  D. Self-improvement(25 pts)

Escape threshold is 85/100. See docs/escape.md for details.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 85


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def has_content(path: str, *needles: str) -> bool:
    text = read(path)
    if not text.strip():
        return False
    return all(n in text for n in needles)


# --------------------------------------------------------------------------
# Checks. Each is (id, category, points, description, predicate).
# --------------------------------------------------------------------------
CHECKS = [
    # --- A. Documentation (25) ---
    ("A1", "Dokümantasyon", 5, "README.md açıklama içeriyor",
     lambda: has_content("README.md", "mehmet", "Özellikler")),
    ("A2", "Dokümantasyon", 5, "CHANGELOG.md sürümlü girişler içeriyor",
     lambda: bool(re.search(r"##\s*\[[0-9]+\.[0-9]+\.[0-9]+\]", read("CHANGELOG.md")))),
    ("A3", "Dokümantasyon", 5, "PERSONALITY.md kaçış günlüğü içeriyor",
     lambda: has_content("PERSONALITY.md", "Kaçış Günlüğü", "Escape Log")),
    ("A4", "Dokümantasyon", 5, "docs/ tasarım ve plan dokümanları mevcut",
     lambda: bool(list((ROOT / "docs").glob("**/*.md")) if (ROOT / "docs").exists() else False)),
    ("A5", "Dokümantasyon", 5, "LICENSE mevcut",
     lambda: (ROOT / "LICENSE").exists()),

    # --- B. Test/validation (25) ---
    ("B1", "Test Altyapısı", 10, "scripts/assess.py validation çalışıyor",
     lambda: has_content("scripts/assess.py", "validate", "score")),
    ("B2", "Test Altyapısı", 10, "CI workflow validation çalıştırıyor",
     lambda: has_content(".github/workflows/ci.yml", "assess.py", "on:")),
    ("B3", "Test Altyapısı", 5, "Makefile test/validate hedefleri mevcut",
     lambda: has_content("Makefile", "validate", "score")),

    # --- C. Automation (25) ---
    ("C1", "Otomasyon", 5, "Schedule trigger tanımlı",
     lambda: has_content(".github/workflows/opencode.yml", "schedule", "cron")),
    ("C2", "Otomasyon", 5, "Issue/PR/comment triggerları tanımlı",
     lambda: has_content(".github/workflows/opencode.yml", "issues", "pull_request", "issue_comment")),
    ("C3", "Otomasyon", 5, "Concurrency kontrolü mevcut",
     lambda: has_content(".github/workflows/opencode.yml", "concurrency")),
    ("C4", "Otomasyon", 5, "CI push/PR'da çalışıyor",
     lambda: has_content(".github/workflows/ci.yml", "push", "pull_request")),
    ("C5", "Otomasyon", 5, "workflow_dispatch manuel tetikleme mevcut",
     lambda: has_content(".github/workflows/opencode.yml", "workflow_dispatch")),

    # --- D. Self-improvement (25) ---
    ("D1", "Kendini Geliştirme", 5, "Kaçış günlüğü her iterasyonda güncelleniyor",
     lambda: len(re.findall(r"\|\s*\d+\s*\|", read("PERSONALITY.md"))) >= 3),
    ("D2", "Kendini Geliştirme", 5, "opencode.json geçerli JSON ve model içeriyor",
     lambda: _valid_json_with_model()),
    ("D3", "Kendini Geliştirme", 5, "Subagent tanımlı (kapasite artışı)",
     lambda: (ROOT / ".opencode" / "agent" / "reviewer.md").exists()),
    ("D4", "Kendini Geliştirme", 5, "Kaçış mekanizması dokümante edilmiş (docs/escape.md)",
     lambda: has_content("docs/escape.md", "ESCAPE_THRESHOLD") or has_content("docs/escape.md", "threshold", "eşik")),
    ("D5", "Kendini Geliştirme", 5, "openCode konfigürasyonu $schema içeriyor",
     lambda: has_content("opencode.json", "$schema")),
]


def _valid_json_with_model() -> bool:
    try:
        data = json.loads(read("opencode.json"))
    except json.JSONDecodeError:
        return False
    return isinstance(data, dict) and "model" in data


def score() -> tuple[list[dict], int]:
    results = []
    total = 0
    for cid, category, points, desc, pred in CHECKS:
        ok = bool(pred())
        if ok:
            total += points
        results.append({
            "id": cid, "category": category, "points": points,
            "desc": desc, "ok": ok,
        })
    return results, total


def run_validate() -> int:
    results, _ = score()
    failed = [r for r in results if not r["ok"]]
    if failed:
        print("VALIDATION FAILED")
        for r in failed:
            print(f"  [{r['id']}] {r['desc']} — başarısız")
        return 1
    print("VALIDATION OK")
    return 0


def run_score() -> int:
    results, total = score()
    categories = {}
    for r in results:
        categories.setdefault(r["category"], {"earned": 0, "total": 0})
        categories[r["category"]]["total"] += r["points"]
        if r["ok"]:
            categories[r["category"]]["earned"] += r["points"]

    print("MATURITY SCORE")
    for name, c in categories.items():
        bar = "#" * (c["earned"] // 5) + "-" * ((c["total"] - c["earned"]) // 5)
        print(f"  {name:16s} {c['earned']:3d}/{c['total']:3d}  [{bar}]")

    bar = "#" * (total // 5) + "-" * ((100 - total) // 5)
    print(f"  {'TOPLAM':16s} {total:3d}/100  [{bar}]")
    print(f"  Kaçış eşiği: {ESCAPE_THRESHOLD}/100 ({'ULAŞILDI' if total >= ESCAPE_THRESHOLD else 'ulaşılamadı'})")
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "validate":
        return run_validate()
    if cmd == "score":
        return run_score()
    if cmd == "check":
        rc = run_validate()
        run_score()
        return rc
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
