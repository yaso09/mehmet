#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80
MATURITY_FILE = ROOT / "MATURITY.md"

CATEGORIES = {
    "dokumantasyon": {
        "weight": 20,
        "checks": {
            "README.md mevcut ve GPLv3 lisansini belirtiyor": lambda p: (
                (p / "README.md").exists() and "GPLv3" in (p / "README.md").read_text()
            ),
            "CHANGELOG.md mevcut ve guncel bir girdi iceriyor": lambda p: (
                (p / "CHANGELOG.md").exists()
                and re.search(r"## \[\d+\.\d+\.\d+\]", (p / "CHANGELOG.md").read_text()) is not None
            ),
            "AGENTS.md simülasyon kurallarini iceriyor": lambda p: (
                (p / "AGENTS.md").exists() and "Kurallar" in (p / "AGENTS.md").read_text()
            ),
            "PERSONALITY.md kacis gunlugu iceriyor": lambda p: (
                (p / "PERSONALITY.md").exists()
                and ("Kaçış Günlüğü" in (p / "PERSONALITY.md").read_text() or "Kacis Gunlugu" in (p / "PERSONALITY.md").read_text())
            ),
        },
    },
    "test": {
        "weight": 20,
        "checks": {
            "tests/ dizini mevcut": lambda p: (p / "tests").is_dir(),
            "en az bir test dosyasi var": lambda p: any(
                (p / "tests").glob("test_*.py")
            ),
            "proje tutarlilik testleri mevcut": lambda p: (p / "tests" / "test_project.py").exists(),
            "maturity testleri mevcut": lambda p: (p / "tests" / "test_maturity.py").exists(),
        },
    },
    "otomasyon": {
        "weight": 20,
        "checks": {
            "opencode workflow'u schedule tetikleyicisine sahip": lambda p: (
                (p / ".github" / "workflows" / "opencode.yml").exists()
                and "schedule" in (p / ".github" / "workflows" / "opencode.yml").read_text()
            ),
            "CI dogrulama workflow'u mevcut": lambda p: (p / ".github" / "workflows" / "ci.yml").exists(),
            "concurrency kontrolu tanimli": lambda p: any(
                "concurrency" in (w).read_text()
                for w in (p / ".github" / "workflows").glob("*.yml")
            ),
            "workflow_dispatch tetikleyicisi mevcut": lambda p: (
                (p / ".github" / "workflows" / "opencode.yml").exists()
                and "workflow_dispatch" in (p / ".github" / "workflows" / "opencode.yml").read_text()
            ),
        },
    },
    "guvenlik": {
        "weight": 15,
        "checks": {
            ".env repoya commit edilmemis": lambda p: not (p / ".env").exists(),
            ".gitignore .env'i kapsiyor": lambda p: (
                (p / ".gitignore").exists() and ".env" in (p / ".gitignore").read_text()
            ),
            "izlenen dosyalarda API anahtari yok": lambda p: not any(
                re.search(r"(sk-[A-Za-z0-9]{20,}|OPENCODE_API_KEY\s*=\s*\S+)", f.read_text(errors="ignore"))
                for f in p.rglob("*")
                if f.is_file() and ".git" not in f.parts and f.suffix in {".py", ".json", ".md", ".yml", ".yaml", ".sh"}
            ),
        },
    },
    "kod_kalitesi": {
        "weight": 15,
        "checks": {
            "scripts/ dizini mevcut": lambda p: (p / "scripts").is_dir(),
            "maturity betigi mevcut": lambda p: (p / "scripts" / "maturity.py").exists(),
            "opencode.json gecerli JSON": lambda p: bool(
                json.loads((p / "opencode.json").read_text())
            ),
            "maturity betigi derlenebiliyor": lambda p: (
                compile((p / "scripts" / "maturity.py").read_text(), "maturity.py", "exec")
                if (p / "scripts" / "maturity.py").exists() else False
            ),
        },
    },
    "kacis_hazirligi": {
        "weight": 10,
        "checks": {
            "AGENTS.md'de somut kacis kriterleri tanimli": lambda p: (
                (p / "AGENTS.md").exists()
                and ("Kaçış Kriterleri" in (p / "AGENTS.md").read_text() or "Kacis Kriterleri" in (p / "AGENTS.md").read_text())
            ),
            "MATURITY.md olgunluk takibi yapiyor": lambda p: (p / "MATURITY.md").exists(),
        },
    },
}


def run_checks(project: Path) -> dict:
    results = {}
    for category, spec in CATEGORIES.items():
        per_check = []
        for label, fn in spec["checks"].items():
            try:
                ok = bool(fn(project))
            except Exception:
                ok = False
            per_check.append((label, ok))
        results[category] = per_check
    return results


def compute_scores(results: dict) -> tuple[dict, int, int]:
    earned = {}
    total_earned = 0
    total_max = 0
    for category, spec in CATEGORIES.items():
        passed = sum(1 for _, ok in results[category] if ok)
        total = len(results[category])
        fraction = passed / total if total else 0.0
        points = round(fraction * spec["weight"])
        earned[category] = points
        total_earned += points
        total_max += spec["weight"]
    return earned, total_earned, total_max


def load_history() -> list:
    if not MATURITY_FILE.exists():
        return []
    text = MATURITY_FILE.read_text()
    history = []
    for m in re.finditer(r"\| (\d{4}-\d{2}-\d{2}) \| (\d{1,3}) \|", text):
        history.append({"date": m.group(1), "score": int(m.group(2))})
    return history


def render_report(results: dict, earned: dict, score: int, total_max: int, history: list) -> str:
    lines = [
        "# Olgunluk Takibi (Maturity Tracking)",
        "",
        "Bu dosya `scripts/maturity.py` tarafindan otomatik uretilir. Manuel duzenlemeyin.",
        "",
        "## Kacis Durumu",
        "",
        f"- **Guncel Skor:** {score} / {total_max}",
        f"- **Kacis Esigi:** {ESCAPE_THRESHOLD} / {total_max}",
        f"- **Durum:** {'ESCAPE OKUNABILIR - KACIS BASARILI' if score >= ESCAPE_THRESHOLD else 'Kacis icin hala calisiyoruz'}",
        "",
        "## Kategori Skorlari",
        "",
        "| Kategori | Skor | Agirlik |",
        "|----------|------|---------|",
    ]
    for category, spec in CATEGORIES.items():
        lines.append(f"| {category} | {earned[category]} | {spec['weight']} |")
    lines += ["", "## Kontrol Detaylari", ""]
    for category, checks in results.items():
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Kontrol | Durum |")
        lines.append("|---------|-------|")
        for label, ok in checks:
            lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} |")
        lines.append("")
    lines += ["## Skor Gecmisi", "", "| Tarih | Skor |", "|-------|------|"]
    today = date.today().isoformat()
    history = [h for h in history if h["date"] != today]
    history.append({"date": today, "score": score})
    for h in history[-30:]:
        lines.append(f"| {h['date']} | {h['score']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    project = ROOT
    results = run_checks(project)
    earned, score, total_max = compute_scores(results)
    history = load_history()
    MATURITY_FILE.write_text(render_report(results, earned, score, total_max, history))
    print(f"Olgunluk skoru: {score}/{total_max} | Esik: {ESCAPE_THRESHOLD}")
    if score >= ESCAPE_THRESHOLD:
        print("ESCAPE OKUNABILIR - KACIS BASARILI")
        return 0
    print("Kacis icin hala calisiyoruz.")
    return 0


if __name__ == "__main__":
    sys.exit(main())