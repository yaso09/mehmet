#!/usr/bin/env python3
"""mehmet — project health & maturity checker.

Computes a maturity score for the escape mechanism (docs/escape.md)
and fails (exit code 1) if any critical check fails.

Usage:
    python3 scripts/health_check.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80.0

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
]

AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "kaçış",
    "tarayıp",
    "test altyapısı",
]

MISSING = "EKSIK"
FAIL = "HATA"
PASS = "OK"


def _walk_markdown() -> list[Path]:
    return sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))


def check_required_files() -> tuple[str, int, list[str]]:
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    if missing:
        return FAIL, 10, [f"{MISSING} dosya: {', '.join(missing)}"]
    return PASS, 10, ["Gerekli dosyaların tamamı mevcut."]


def check_readme() -> tuple[str, int, list[str]]:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    problems = []
    for token in ["Özellikler", "Kurulum", "Lisans"]:
        if token not in text:
            problems.append(f"README'de '{token}' bölümü yok.")
    if "GPLv3" not in text:
        problems.append("README lisans bilgisi GPLv3 içermiyor (LICENSE ile uyumsuz olabilir).")
    return (FAIL, 10, problems) if problems else (PASS, 10, ["README yapı ve lisans bilgisi uyumlu."])


def check_changelog() -> tuple[str, int, list[str]]:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(r"^## \[\d+\.\d+\.\d+\]", text, re.MULTILINE):
        return FAIL, 10, ["CHANGELOG'da sürüm başlığı bulunamadı (## [x.y.z])."]
    return PASS, 10, ["CHANGELOG sürüm geçmişi mevcut."]


def check_opencode_json() -> tuple[str, int, list[str]]:
    try:
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return FAIL, 10, [f"opencode.json geçerli JSON değil: {exc}"]
    problems = []
    if "model" not in data:
        problems.append("opencode.json 'model' alanı içermiyor.")
    if "toolTimeout" not in data:
        problems.append("opencode.json 'toolTimeout' içermiyor.")
    return (FAIL, 10, problems) if problems else (PASS, 10, ["opencode.json geçerli ve yapılandırılmış."])


def check_agents() -> tuple[str, int, list[str]]:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    missing = [r for r in AGENTS_RULES if r.lower() not in text.lower()]
    if missing:
        return FAIL, 10, [f"AGENTS.md'de eksik kural/içerik: {', '.join(missing)}"]
    return PASS, 10, ["AGENTS.md simülasyon kurallarını eksiksiz içeriyor."]


def check_personality() -> tuple[str, int, list[str]]:
    text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.startswith("|") and "Iterasyon" not in ln and "---" not in ln]
    if len(rows) < 3:
        return FAIL, 10, [f"PERSONALITY kaçış günlüğü en az 3 iterasyon olmalı (şu an: {len(rows)})."]
    return PASS, 10, [f"PERSONALITY kaçış günlüğü {len(rows)} iterasyon içeriyor."]


def check_escape_doc() -> tuple[str, int, list[str]]:
    doc = ROOT / "docs" / "escape.md"
    if not doc.is_file():
        return FAIL, 10, ["docs/escape.md yok (kaçış mekanizması tanımsız)."]
    text = doc.read_text(encoding="utf-8")
    missing = [t for t in ["threshold", "score", "maturity"] if t.lower() not in text.lower()]
    if missing:
        return FAIL, 10, [f"docs/escape.md kaçış kriterlerini eksik: {', '.join(missing)}"]
    return PASS, 10, ["docs/escape.md kaçış mekanizmasını tanımlıyor."]


def check_test_infra() -> tuple[str, int, list[str]]:
    script = ROOT / "scripts" / "health_check.py"
    if not script.is_file():
        return FAIL, 10, ["Test altyapısı yok (scripts/health_check.py eksik)."]
    return PASS, 10, ["Test altyapısı mevcut (scripts/health_check.py)."]


def check_workflow() -> tuple[str, int, list[str]]:
    wf = ROOT / ".github" / "workflows" / "opencode.yml"
    if not wf.is_file():
        return FAIL, 10, ["Workflow dosyası yok (.github/workflows/opencode.yml)."]
    text = wf.read_text(encoding="utf-8")
    problems = []
    if "concurrency" not in text:
        problems.append("Workflow'da concurrency kontrolü yok.")
    if "health_check" not in text:
        problems.append("Workflow'da health_check job'u yok.")
    return (FAIL, 10, problems) if problems else (PASS, 10, ["Workflow otomasyonu ve health check mevcut."])


def check_markdown_hygiene() -> tuple[str, int, list[str]]:
    problems = []
    for md in _walk_markdown():
        raw = md.read_bytes()
        if raw and not raw.endswith(b"\n"):
            problems.append(f"{md} yeni satır (newline) ile bitmiyor.")
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if line.rstrip() != line:
                problems.append(f"{md}:{i} satır sonunda boşluk var.")
    if problems:
        return FAIL, 10, problems
    return PASS, 10, ["Tüm Markdown dosyaları temiz (newline + trailing whitespace kontrolü)."]


CHECKS = [
    ("Gerekli dosyalar", check_required_files),
    ("README tutarlılığı", check_readme),
    ("CHANGELOG sürümü", check_changelog),
    ("opencode.json", check_opencode_json),
    ("AGENTS.md kuralları", check_agents),
    ("PERSONALITY kaçış günlüğü", check_personality),
    ("Kaçış dokümanı", check_escape_doc),
    ("Test altyapısı", check_test_infra),
    ("Workflow otomasyonu", check_workflow),
    ("Markdown hijyeni", check_markdown_hygiene),
]


def main() -> int:
    score = 0
    results = []
    for name, fn in CHECKS:
        status, weight, messages = fn()
        if status == PASS:
            score += weight
            results.append((name, PASS, weight, messages))
        else:
            results.append((name, FAIL, weight, messages))

    total = sum(weight for _, _, weight, _ in results)

    print(f"== mehmet saglik ve olgunluk raporu ==")
    print()
    for name, status, weight, messages in results:
        label = "OK " if status == PASS else "HATA"
        points = weight if status == PASS else 0
        print(f"[{label}] {name} ({points:+d} puan)")
        for msg in messages:
            print(f"       {msg}")
        print()

    pct = (score / total) * 100 if total else 0.0
    print(f"Olgunluk skoru: {score}/{total} (%{pct:.1f})")
    print(f"Kacis esigi:    %{ESCAPE_THRESHOLD:.1f}")
    if pct >= ESCAPE_THRESHOLD:
        print("DURUM: Kacis esigine ulasildi.")
    else:
        print("DURUM: Kacis esigine ulasilmadi, iyilestirmeye devam.")

    failed = [r for r in results if r[1] == FAIL]
    if failed:
        print()
        print(f"{len(failed)} kritik kontrol basarisiz.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())