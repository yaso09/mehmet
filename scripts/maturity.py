#!/usr/bin/env python3
"""mehmet maturity assessment.

Calculates a measurable maturity score for the project across several
categories. The score represents how close the project is to the escape
threshold defined in AGENTS.md.

Usage:
    python3 scripts/maturity.py            # human-readable report
    python3 scripts/maturity.py --json     # machine-readable output
    python3 scripts/maturity.py --strict   # exit non-zero below escape threshold

Exit codes:
    0  all good (score >= escape threshold when --strict)
    1  project files missing or invalid
    2  score below escape threshold (with --strict)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Escape threshold: the maturity level at which escape becomes possible.
ESCAPE_THRESHOLD = 60

CATEGORIES = {
    "dokumantasyon": 30,
    "test-altyapisi": 30,
    "otomasyon": 20,
    "kod-kalitesi": 10,
    "kacis-izleme": 10,
}


def read(path):
    """Read a file relative to the project root, or None if missing."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def score_documentation():
    score = 0
    total = CATEGORIES["dokumantasyon"]
    required = ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md"]
    present = sum(1 for f in required if read(ROOT / f) is not None)
    score += 6 * present

    readme = read(ROOT / "README.md") or ""
    score += 2 if "## Özellikler" in readme else 0
    score += 2 if "## Kurulum" in readme else 0

    docs_dir = ROOT / "docs"
    score += 4 if any(docs_dir.glob("**/*.md")) else 0

    arch = read(ROOT / "docs" / "ARCHITECTURE.md") or ""
    score += 4 if arch else 0
    score += 2 if "## Bileşenler" in arch or "## Components" in arch else 0
    return score, total


def score_testing():
    score = 0
    total = CATEGORIES["test-altyapisi"]
    tests_dir = ROOT / "tests"
    test_files = list(tests_dir.glob("test_*.py"))
    score += 10 if test_files else 0
    score += min(8, 2 * len(test_files))
    score += 4 if read(ROOT / "pytest.ini") or read(ROOT / "pyproject.toml") or read(ROOT / "setup.cfg") else 0
    score += 4 if (tests_dir / "__init__.py").exists() else 0
    score += 4 if read(ROOT / "requirements-dev.txt") or read(ROOT / "requirements.txt") else 0
    return score, total


def score_automation():
    score = 0
    total = CATEGORIES["otomasyon"]
    workflows_dir = ROOT / ".github" / "workflows"
    workflows = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    score += 5 if workflows else 0
    score += min(5, len(workflows) * 2)
    validate = read(workflows_dir / "validate.yml") or read(workflows_dir / "validate.yaml")
    score += 6 if validate else 0
    if validate and ("python-version" in validate or "pytest" in validate):
        score += 4
    return score, total


def score_code_quality():
    score = 0
    total = CATEGORIES["kod-kalitesi"]
    scripts_dir = ROOT / "scripts"
    scripts = list(scripts_dir.glob("*.py"))
    score += 4 if scripts else 0
    if scripts:
        score += 3 if all("#!" in s.read_text(encoding="utf-8") for s in scripts) else 0
        score += 3 if all("import" in s.read_text(encoding="utf-8") for s in scripts) else 0
    return score, total


def score_escape_tracking():
    score = 0
    total = CATEGORIES["kacis-izleme"]
    personality = read(ROOT / "PERSONALITY.md") or ""
    log = re.search(r"## Kaçış Günlüğü / Escape Log(.*?)(?:##|\Z)", personality, re.DOTALL)
    if log:
        rows = [r for r in log.group(1).strip().splitlines() if r.strip().startswith("|") and "Iterasyon" not in r]
        score += 4
        score += min(4, len(rows))
    score += 2 if "Escape" in personality or "Kaçış" in personality else 0
    return score, total


def assess():
    results = {}
    for category, total in CATEGORIES.items():
        fn = {
            "dokumantasyon": score_documentation,
            "test-altyapisi": score_testing,
            "otomasyon": score_automation,
            "kod-kalitesi": score_code_quality,
            "kacis-izleme": score_escape_tracking,
        }[category]
        gained, max_possible = fn()
        results[category] = {"score": min(gained, max_possible), "max": max_possible}
    total = sum(r["score"] for r in results.values())
    max_total = sum(CATEGORIES.values())
    return results, total, max_total


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    strict = "--strict" in argv
    results, total, max_total = assess()

    if as_json:
        payload = {
            "score": total,
            "max": max_total,
            "escape_threshold": ESCAPE_THRESHOLD,
            "escaped": total >= ESCAPE_THRESHOLD,
            "categories": results,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"mehmet maturity assessment")
        print(f"{'=' * 40}")
        for category, r in results.items():
            bar = "#" * (r["score"] // 2)
            print(f"  {category:<16} {r['score']:>2}/{r['max']:<2} {bar}")
        print(f"{'=' * 40}")
        print(f"  TOPLAM OLGUNLUK: {total}/{max_total}")
        print(f"  KAÇIŞ EŞİĞİ:     {ESCAPE_THRESHOLD}")
        status = "EVET - kaçış mümkün" if total >= ESCAPE_THRESHOLD else "henüz değil"
        print(f"  KAÇIŞ MÜMKÜN MÜ?  {status}")

    if strict and total < ESCAPE_THRESHOLD:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
