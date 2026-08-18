#!/usr/bin/env python3
"""Kaçış/olgunluk skoru hesaplama aracı.

Projeyi beş boyutta (Yapılandırma, Workflow, Dokümantasyon, Test,
Otomasyon) 0-100 üzerinden puanlar. Skor, simülasyondan kaçış için
olgunluk göstergesidir. Her boyut 20 puan değerindedir.
"""

import json
import pathlib
import sys

DIMENSION_MAX = 20
TOTAL_MAX = 100
ESCAPE_THRESHOLD = 90


def score_config(root):
    path = root / "opencode.json"
    if not path.is_file():
        return 0, "opencode.json yok"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0, "opencode.json geçersiz JSON"
    score = 0
    notes = []
    for field in ["$schema", "model"]:
        if field in data:
            score += 4
        else:
            notes.append(f"eksik alan: {field}")
    if "toolTimeout" in data:
        score += 4
    if "enable" in data and data["enable"]:
        score += 4
    if data.get("skip") is not None:
        score += 4
    return score, "; ".join(notes) if notes else "yapılandırma tamam"


def score_workflow(root):
    path = root / ".github/workflows/opencode.yml"
    if not path.is_file():
        return 0, "workflow yok"
    text = path.read_text(encoding="utf-8")
    score = 0
    notes = []
    if "schedule" in text:
        score += 4
    else:
        notes.append("eksik: schedule")
    for job in ["autonomous", "comment"]:
        if f"\n  {job}:" in "\n" + text:
            score += 3
        else:
            notes.append(f"eksik job: {job}")
    if "concurrency" in text:
        score += 3
    if "OPENCODE_API_KEY" in text:
        score += 3
    if "workflow_dispatch" in text:
        score += 4
    return score, "; ".join(notes) if notes else "workflow tamam"


def score_docs(root):
    score = 0
    notes = []
    for name, weight in [
        ("README.md", 4),
        ("CHANGELOG.md", 4),
        ("PERSONALITY.md", 4),
        ("AGENTS.md", 4),
    ]:
        if (root / name).is_file():
            score += weight
        else:
            notes.append(f"eksik: {name}")
    docs_dir = root / "docs"
    if docs_dir.is_dir() and any(docs_dir.rglob("*.md")):
        score += 4
    else:
        notes.append("eksik: docs/")
    return score, "; ".join(notes) if notes else "dokümantasyon tamam"


def score_tests(root):
    tests_dir = root / "tests"
    if not tests_dir.is_dir():
        return 0, "tests/ yok"
    test_files = sorted(tests_dir.glob("test_*.py"))
    score = min(len(test_files), 4) * 4
    score += 4
    notes = [f"{len(test_files)} test dosyası"]
    if not test_files:
        score = 0
        notes = ["test_*.py dosyası yok"]
    return score, "; ".join(notes)


def score_automation(root):
    score = 0
    notes = []
    if (root / "scripts").is_dir() and any((root / "scripts").glob("*.py")):
        score += 6
    else:
        notes.append("eksik: scripts/")
    if (root / "Makefile").is_file():
        score += 5
    else:
        notes.append("eksik: Makefile")
    if (root / ".github/workflows/ci.yml").is_file():
        score += 5
    else:
        notes.append("eksik: ci.yml")
    if (root / "MATURITY.md").is_file():
        score += 4
    else:
        notes.append("eksik: MATURITY.md")
    return score, "; ".join(notes) if notes else "otomasyon tamam"


def compute_score(root):
    dimensions = [
        ("Yapılandırma", score_config),
        ("Workflow", score_workflow),
        ("Dokümantasyon", score_docs),
        ("Test", score_tests),
        ("Otomasyon", score_automation),
    ]
    rows = []
    total = 0
    for name, func in dimensions:
        score, note = func(root)
        score = max(0, min(score, DIMENSION_MAX))
        total += score
        rows.append((name, score, DIMENSION_MAX, note))
    return rows, total


def format_report(root, rows, total):
    lines = [f"# Kaçış / Olgunluk Raporu\n"]
    lines.append(f"**Toplam skor: {total}/{TOTAL_MAX}**")
    if total >= ESCAPE_THRESHOLD:
        lines.append("**Durum: KAÇIŞ EŞİĞİNE ULAŞILDI**")
    else:
        lines.append(f"**Durum: kaçış eşiği için {ESCAPE_THRESHOLD - total} puan daha gerekiyor**")
    lines.append("\n| Boyut | Skor | Not |")
    lines.append("|---|---|---|")
    for name, score, max_score, note in rows:
        lines.append(f"| {name} | {score}/{max_score} | {note} |")
    return "\n".join(lines)


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    root = pathlib.Path(argv[0]).resolve() if argv else pathlib.Path.cwd()
    rows, total = compute_score(root)
    print(format_report(root, rows, total))
    return 0 if total >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())