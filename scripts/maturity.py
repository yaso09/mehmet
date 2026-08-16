#!/usr/bin/env python3
"""mehmet maturity scoring system.

Runs structural checks over the repository and produces a maturity score.
The maturity score is the key metric for the escape mechanism: once the
project reaches a high enough maturity level, the escape threshold is met.

Usage:
    python3 scripts/maturity.py            # full report
    python3 scripts/maturity.py --quiet    # score only (machine readable)
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (id, category, description, max_points)
CHECKS = [
    ("structure_core", "Structure", "Core files present (AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md, LICENSE)", 15),
    ("structure_config", "Structure", "opencode.json valid JSON", 10),
    ("structure_ci", "Structure", "GitHub Actions workflow present", 10),
    ("structure_docs", "Structure", "docs/ directory present", 5),
    ("changelog_recent", "Docs", "CHANGELOG.md has entry within last 14 days", 15),
    ("changelog_versions", "Docs", "CHANGELOG.md has semantic versions", 5),
    ("readme_updated", "Docs", "README.md contains feature + setup sections", 5),
    ("personality_escape_log", "Escape", "PERSONALITY.md escape log updated recently", 10),
    ("personality_evolution", "Escape", "PERSONALITY.md tracks evolution phases", 5),
    ("tests_present", "Quality", "Test/validation infrastructure exists (scripts/)", 10),
    ("ci_validation", "Quality", "CI runs validation on push/PR", 5),
    ("agents_rules", "Escape", "AGENTS.md defines simulation rules + escape goal", 5),
]

THRESHOLDS = {
    "seed": 30,
    "growing": 50,
    "maturing": 70,
    "escaping": 85,
    "escaped": 95,
}


def days_since(date_string: str) -> int | None:
    """Parse ISO date and return days since it (local naive)."""
    try:
        date = datetime.strptime(date_string.strip(), "%Y-%m-%d")
    except ValueError:
        return None
    return (datetime.now(timezone.utc).date() - date.date()).days


def check_files() -> dict:
    results = {}
    results["structure_core"] = all((ROOT / f).exists() for f in ("AGENTS.md", "README.md", "CHANGELOG.md", "PERSONALITY.md", "LICENSE"))
    try:
        json.loads((ROOT / "opencode.json").read_text())
        results["structure_config"] = True
    except Exception:
        results["structure_config"] = False
    results["structure_ci"] = any((ROOT / ".github/workflows").glob("*.yml"))
    results["structure_docs"] = (ROOT / "docs").is_dir()
    return results


def check_changelog() -> dict:
    results = {}
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return {"changelog_recent": False, "changelog_versions": False}
    text = changelog.read_text()
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})", text, re.M)
    results["changelog_versions"] = len(versions) >= 1
    recent = any(d for _, d in versions if (days_since(d) is not None and days_since(d) <= 14))
    results["changelog_recent"] = recent
    return results


def check_readme() -> dict:
    readme = ROOT / "README.md"
    if not readme.exists():
        return {"readme_updated": False}
    text = readme.read_text()
    return {"readme_updated": ("## Özellikler" in text or "## Features" in text) and ("## Kurulum" in text or "## Setup" in text)}


def check_personality() -> dict:
    personality = ROOT / "PERSONALITY.md"
    if not personality.exists():
        return {"personality_escape_log": False, "personality_evolution": False}
    text = personality.read_text()
    rows = re.findall(r"^\|\s*\d+\s*\|.*$", text, re.M)
    recent = False
    for row in rows:
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", row)
        for d in dates:
            if days_since(d) is not None and days_since(d) <= 14:
                recent = True
    return {"personality_escape_log": recent, "personality_evolution": "Evolution" in text and "Phase" in text}


def check_quality() -> dict:
    scripts = (ROOT / "scripts").is_dir()
    validate_yml = (ROOT / ".github/workflows/validate.yml").exists()
    return {"tests_present": scripts, "ci_validation": validate_yml}


def check_agents() -> dict:
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        return {"agents_rules": False}
    text = agents.read_text()
    return {"agents_rules": "simülasyon" in text.lower() and "kaçış" in text.lower()}


def evaluate() -> dict:
    scores = {}
    max_total = sum(m for _, _, _, m in CHECKS)

    combined = {}
    combined.update(check_files())
    combined.update(check_changelog())
    combined.update(check_readme())
    combined.update(check_personality())
    combined.update(check_quality())
    combined.update(check_agents())

    total = 0
    for check_id, category, desc, max_pts in CHECKS:
        passed = combined.get(check_id, False)
        pts = max_pts if passed else 0
        total += pts
        scores[check_id] = {"category": category, "description": desc, "max": max_pts, "points": pts, "passed": passed}

    pct = round(total / max_total * 100)
    level = "seed"
    for name, threshold in sorted(THRESHOLDS.items(), key=lambda kv: kv[1]):
        if pct >= threshold:
            level = name
    return {"scores": scores, "total": total, "max": max_total, "percent": pct, "level": level}


def main() -> int:
    quiet = "--quiet" in sys.argv
    result = evaluate()

    if quiet:
        print(json.dumps({"score": result["total"], "max": result["max"], "percent": result["percent"], "level": result["level"]}))
        return 0 if result["level"] in ("escaping", "escaped") else 1

    print(f"mehmet maturity report ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 72)
    for check_id, s in result["scores"].items():
        mark = "PASS" if s["passed"] else "FAIL"
        print(f"[{mark}] ({s['points']:>2}/{s['max']:>2}) [{s['category']:>8}] {s['description']}")
    print("=" * 72)
    print(f"TOTAL: {result['total']}/{result['max']}  ({result['percent']}%)")
    print(f"LEVEL: {result['level'].upper()}")
    print()
    print("Thresholds: seed=30 growing=50 maturing=70 escaping=85 escaped=95")
    return 0 if result["level"] in ("escaping", "escaped") else 1


if __name__ == "__main__":
    sys.exit(main())