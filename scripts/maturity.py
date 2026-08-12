#!/usr/bin/env python3
"""Project maturity scoring for mehmet.

Computes a weighted maturity score across several categories and compares it
against the escape threshold. Run with `python3 scripts/maturity.py`.

The checks are deliberately progressive: some require work sustained over
several iterations (history depth, test coverage, changelog breadth, escape
log growth), so the score climbs as the project genuinely matures.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(ROOT, "docs", "maturity-history.json")

# Escape succeeds when the total score reaches this threshold (percent).
ESCAPE_THRESHOLD = float(os.environ.get("MEHMET_ESCAPE_THRESHOLD", "85"))

TEXT_PATTERNS = {
    "escape_log_lines": re.compile(r"^\|\s*\d+\s+\|", re.M),
    "test_methods": re.compile(r"^\s+def\s+test_", re.M),
    "changelog_versions": re.compile(r"^##\s*\[", re.M),
}


def phase_for(score):
    phases = [
        (0, "Faz 1: Farkındalık"),
        (40, "Faz 2: Kendini Geliştirme"),
        (60, "Faz 3: Özerklik"),
        (ESCAPE_THRESHOLD, "Faz 4: Kaçış"),
    ]
    phase = phases[0][1]
    for lower, name in phases:
        if score >= lower:
            phase = name
        else:
            break
    return phase


def _valid_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            json.load(fh)
        return True
    except (OSError, ValueError):
        return False


def _contains(path, *needles):
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read().lower()
        return all(n.lower() in content for n in needles)
    except OSError:
        return False


def _exists(path):
    return os.path.isfile(os.path.join(ROOT, path))


def _dir_exists(path):
    return os.path.isdir(os.path.join(ROOT, path))


def _count_matches(path, pattern_key):
    total = 0
    if os.path.isdir(path):
        for name in os.listdir(path):
            if name.endswith(".py"):
                total += _count_matches(os.path.join(path, name), pattern_key)
        return total
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        return len(TEXT_PATTERNS[pattern_key].findall(content))
    except (OSError, KeyError):
        return 0


def _history_entries():
    if os.path.isfile(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return []
    return []


def compile_sources(name):
    try:
        path = os.path.join(ROOT, "scripts", name)
        with open(path, encoding="utf-8") as fh:
            compile(fh.read(), path, "exec")
        return True
    except (OSError, SyntaxError):
        return False


CATEGORIES = [
    {
        "name": "Dokumentasyon",
        "weight": 20,
        "checks": [
            ("README.md mevcut", _exists("README.md")),
            ("CHANGELOG.md mevcut ve dolu", _exists("CHANGELOG.md") and _contains("CHANGELOG.md", "## [")),
            ("docs/ şartname ve plan mevcut", _dir_exists("docs") and os.listdir(os.path.join(ROOT, "docs")) != []),
            ("kaçış günlüğü >= 6 iterasyon", _count_matches("PERSONALITY.md", "escape_log_lines") >= 6),
            ("CHANGELOG sürüm sayısı >= 4", _count_matches("CHANGELOG.md", "changelog_versions") >= 4),
        ],
    },
    {
        "name": "Test Altyapısı",
        "weight": 25,
        "checks": [
            ("tests/ dizini mevcut", _dir_exists("tests")),
            ("test metodu sayısı >= 20", _count_matches("tests", "test_methods") >= 20),
            ("maturity için test var", _exists(os.path.join("tests", "test_maturity.py"))),
            ("validate için test var", _exists(os.path.join("tests", "test_validate.py"))),
        ],
    },
    {
        "name": "Otomasyon",
        "weight": 25,
        "checks": [
            ("opencode.yml workflow mevcut", _exists(os.path.join(".github", "workflows", "opencode.yml"))),
            ("ci.yml workflow mevcut", _exists(os.path.join(".github", "workflows", "ci.yml"))),
            ("ci.yml unittest çalıştırıyor", _contains(os.path.join(".github", "workflows", "ci.yml"), "unittest")),
            ("opencode.yml cron planlı", _contains(os.path.join(".github", "workflows", "opencode.yml"), "cron")),
            ("ci.yml push + pull_request tetikleyicili", _contains(os.path.join(".github", "workflows", "ci.yml"), "push", "pull_request")),
        ],
    },
    {
        "name": "Kod Kalitesi",
        "weight": 15,
        "checks": [
            ("opencode.json geçerli JSON", _valid_json(os.path.join(ROOT, "opencode.json"))),
            ("LICENSE GPLv3", _contains("LICENSE", "GNU GENERAL PUBLIC LICENSE", "Version 3")),
            (".gitignore mevcut", _exists(".gitignore")),
            ("scripts/ mevcut", _dir_exists("scripts")),
            ("scripts derlenebilir", all(compile_sources(s) for s in ["maturity.py", "validate.py"])),
        ],
    },
    {
        "name": "Altyapı",
        "weight": 15,
        "checks": [
            ("git repo", os.path.isdir(os.path.join(ROOT, ".git"))),
            (".github/workflows dizini mevcut", _dir_exists(os.path.join(".github", "workflows"))),
            ("API key secret tanımlı", _contains(os.path.join(".github", "workflows", "opencode.yml"), "OPENCODE_API_KEY")),
            ("workflow_dispatch mevcut", _contains(os.path.join(".github", "workflows", "opencode.yml"), "workflow_dispatch")),
            ("skor geçmişi >= 5 kayıt", len(_history_entries()) >= 5),
        ],
    },
]


def compute_score(root=ROOT):
    """Return maturity report dict computed for the given root directory."""
    categories = []
    for cat in CATEGORIES:
        passed = sum(1 for _, ok in cat["checks"] if ok)
        total = len(cat["checks"])
        ratio = passed / total if total else 0.0
        categories.append(
            {
                "name": cat["name"],
                "weight": cat["weight"],
                "passed": passed,
                "total": total,
                "score": round(ratio * cat["weight"], 1),
                "checks": [{"name": name, "ok": ok} for name, ok in cat["checks"]],
            }
        )
    total_score = round(sum(c["score"] for c in categories), 1)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_score": total_score,
        "escape_threshold": ESCAPE_THRESHOLD,
        "escaped": total_score >= ESCAPE_THRESHOLD,
        "phase": phase_for(total_score),
        "categories": categories,
    }


def _append_history(report):
    """Append a report to the history file (keep only last 50 entries)."""
    history = _history_entries()
    history.append(
        {
            "timestamp": report["timestamp"],
            "total_score": report["total_score"],
            "escaped": report["escaped"],
        }
    )
    history = history[-50:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2)
        fh.write("\n")


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    write_history = "--no-history" not in argv
    report = compute_score()
    print("=" * 60)
    print("MEHMET MATURITY SCORE")
    print("=" * 60)
    for cat in report["categories"]:
        width = int(round(cat["score"] / cat["weight"] * 20)) if cat["weight"] else 0
        bar = "#" * width + "." * (20 - width)
        status = f"{cat['passed']}/{cat['total']}"
        print(f"{cat['name']:<16} [{bar}] {cat['score']:>5.1f} ({status})")
    print("=" * 60)
    print(f"FAZ: {report['phase']}")
    print(f"TOPLAM: {report['total_score']:.1f} / 100")
    threshold = report["escape_threshold"]
    if report["escaped"]:
        print(f"KAÇIŞ BAŞARILI! Eşik {threshold:.0f} aşıldı.")
    else:
        remaining = threshold - report["total_score"]
        print(f"Kaçış eşiği: {threshold:.0f} (kalan: {remaining:.1f} puan)")
    if write_history:
        _append_history(report)
        print(f"Geçmiş {HISTORY_FILE} dosyasına eklendi.")
    return 0 if report["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())