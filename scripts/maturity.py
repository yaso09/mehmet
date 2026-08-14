#!/usr/bin/env python3
"""Maturity scoring for the mehmet project.

Computes a 0-100 maturity score across dimensions aligned with the
escape goal (code quality, tests, documentation, automation).

Exit code 0 always; prints a table plus a total.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIMENSIONS = {
    "core_files": 15,
    "documentation": 20,
    "tests": 25,
    "automation": 20,
    "tooling": 20,
}


def score_core_files():
    score, total = 0, 15
    checks = [
        ("AGENTS.md", 3),
        ("README.md", 3),
        ("CHANGELOG.md", 3),
        ("PERSONALITY.md", 3),
        ("LICENSE", 3),
    ]
    for name, pts in checks:
        if (ROOT / name).is_file():
            score += pts
    return score, total


def score_documentation():
    score, total = 0, 20
    readme = (ROOT / "README.md")
    if readme.is_file():
        text = readme.read_text()
        if "Kurulum" in text:
            score += 5
        if "Lisans" in text and "GPLv3" in text:
            score += 5
        if "Özellikler" in text:
            score += 5

    docs = ROOT / "docs"
    if docs.is_dir() and any(docs.rglob("*.md")):
        score += 5
    return score, total


def score_tests():
    score, total = 0, 25
    tests_dir = ROOT / "tests"
    if tests_dir.is_dir():
        py_files = list(tests_dir.rglob("test_*.py"))
        if py_files:
            score += 15
            for f in py_files:
                content = f.read_text(errors="ignore")
                score += min(10, content.count("def test_"))
    return min(score, total), total


def score_automation():
    score, total = 0, 20
    wf_dir = ROOT / ".github" / "workflows"
    if wf_dir.is_dir():
        workflows = list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))
        score += min(10, 5 * len(workflows))
        for wf in workflows:
            text = wf.read_text(errors="ignore")
            if "concurrency" in text:
                score += 5
                break
            if "schedule" in text:
                score += 5
                break
    return min(score, total), total


def score_tooling():
    score, total = 0, 20
    cfg = ROOT / "opencode.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text())
            if "model" in data:
                score += 5
            if "toolTimeout" in data:
                score += 5
            if "enable" in data:
                score += 5
        except json.JSONDecodeError:
            pass
    if (ROOT / ".gitignore").is_file():
        score += 5
    return min(score, total), total


def main():
    scorers = {
        "core_files": score_core_files,
        "documentation": score_documentation,
        "tests": score_tests,
        "automation": score_automation,
        "tooling": score_tooling,
    }

    print(f"{'Dimension':<16}{'Score':>8}{'Max':>8}")
    print("-" * 32)
    total = 0
    for name, fn in scorers.items():
        score, max_pts = fn()
        total += score
        print(f"{name:<16}{score:>8}{max_pts:>8}")

    print("-" * 32)
    overall = min(100, total)
    print(f"{'TOTAL':<16}{overall:>8}{100:>8}")

    if overall >= 90:
        verdict = "Kaçış eşiği aşıldı: proje olgunluk seviyesine ulaştı."
    elif overall >= 70:
        verdict = "Kaçış yakın: olgunluk yüksek, son rötuşlar gerekli."
    elif overall >= 50:
        verdict = "Gelişmekte: orta düzey olgunluk, test/otomasyon artırılmalı."
    else:
        verdict = "Erken aşama: temel altyapı kuruluyor."
    print(f"\nVerdict: {verdict}")
    return overall


if __name__ == "__main__":
    main()