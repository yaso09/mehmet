#!/usr/bin/env python3
"""mehmet olgunluk (maturity) ve kaçış (escape) takip aracı.

Projenin kaçış için gereken olgunluk seviyesine ne kadar yaklaştığını
ölçer. Her metrik belirli puan taşır, toplam 100 üzerinden hesaplanır.
Skor kaçış eşiğine (escape threshold) ulaştığında kaçış gerçekleşir.

Kullanım:
    python3 scripts/maturity.py            # tablo çıktısı
    python3 scripts/maturity.py --json     # makine okunur JSON çıktısı
    python3 scripts/maturity.py --strict   # skor eşiğin altındaysa exit 1
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80


def _read(relpath):
    path = ROOT / relpath
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _has_content(relpath, needle=None):
    content = _read(relpath)
    if content is None or not content.strip():
        return False
    return needle is None or needle in content


def _metric_agents():
    content = _read("AGENTS.md")
    if content is None:
        return 0, "AGENTS.md eksik"
    score = 0
    for kw in ["Simülasyon", "kaçış", "CHANGELOG", "README", "PERSONALITY"]:
        if kw in content:
            score += 1
    return score, "Simülasyon bağlamı ve kurallar mevcut"


def _metric_readme():
    content = _read("README.md")
    if content is None:
        return 0, "README.md eksik"
    score = 0
    for section in ["# mehmet", "Özellikler", "Kurulum", "Lisans", "GPLv3"]:
        if content.startswith(section) or section in content:
            score += 2
    return score, "README güncel ve bilgilendirici"


def _metric_changelog():
    content = _read("CHANGELOG.md")
    if content is None:
        return 0, "CHANGELOG.md eksik"
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}$", content, re.M)
    score = min(len(versions) * 2, 6)
    if "### Added" in content:
        score += 2
    if "### Fixed" in content:
        score += 2
    return score, f"{len(versions)} sürüm bölümü tespit edildi"


def _metric_license():
    content = _read("LICENSE")
    if content is None:
        return 0, "LICENSE eksik"
    if "GNU GENERAL PUBLIC LICENSE" in content and "Version 3" in content:
        return 10, "GPLv3 lisansı doğru"
    return 3, "LICENSE GPLv3 değil"


def _metric_opencode():
    try:
        config = json.loads(_read("opencode.json") or "{}")
    except (json.JSONDecodeError, TypeError):
        return 0, "opencode.json geçersiz JSON"
    score = 0
    if "model" in config:
        score += 2
    if "$schema" in config:
        score += 2
    if "toolTimeout" in config:
        score += 1
    return score, "opencode.json konfigürasyonu mevcut"


def _metric_gitignore():
    content = _read(".gitignore")
    if content is None:
        return 0, ".gitignore eksik"
    score = 0
    for entry in ["node_modules", ".env", "*.log", "dist/", "build/"]:
        if entry in content:
            score += 1
    return score, "Gizli ve bağımlılık dosyaları kapsanıyor"


def _metric_personality():
    content = _read("PERSONALITY.md")
    if content is None:
        return 0, "PERSONALITY.md eksik"
    score = 0
    if "Kaçış Günlüğü" in content or "Escape Log" in content:
        score += 4
    rows = re.findall(r"^\|\s*\d+\s*\|", content, re.M)
    score += min(len(rows) * 2, 4)
    if "Phase 4: Escape" in content or "Phase 4" in content:
        score += 2
    return score, f"Kaçış günlüğünde {len(rows)} iterasyon"


def _metric_docs():
    docs_dir = ROOT / "docs"
    if not docs_dir.exists():
        return 0, "docs/ dizini yok"
    files = list(docs_dir.rglob("*.md"))
    if not files:
        return 0, "docs/ boş"
    return min(len(files) * 2, 10), f"{len(files)} doküman bulundu"


def _metric_tests():
    tests = list((ROOT / "tests").glob("test_*.py")) if (ROOT / "tests").exists() else []
    if not tests:
        return 0, "Test dosyası yok"
    exist_points = min(len(tests) * 3, 6)
    env = dict(os.environ)
    env["MATURITY_RUN"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=env,
    )
    if result.returncode != 0:
        return exist_points, "Testler BAŞARISIZ"
    return exist_points + 9, "Testler geçiyor"


def _metric_ci():
    workflow = _read(".github/workflows/opencode.yml")
    ci = _read(".github/workflows/ci.yml")
    score = 0
    if workflow is not None:
        score += 6
    if ci is not None:
        score += 4
    return score, "Otomasyon workflow'ları mevcut"


def _metric_maturity():
    script = (ROOT / "scripts" / "maturity.py").exists()
    doc = _has_content("MATURITY.md", "eşik")
    score = (5 if script else 0) + (5 if doc else 0)
    return score, "Olgunluk takibi mevcut"


METRICS = [
    ("AGENTS.md kuralları", _metric_agents, 5),
    ("README dokümantasyonu", _metric_readme, 10),
    ("CHANGELOG formatı", _metric_changelog, 10),
    ("Lisans (GPLv3)", _metric_license, 10),
    ("opencode.json konfigürasyonu", _metric_opencode, 5),
    (".gitignore yeterliliği", _metric_gitignore, 5),
    ("PERSONALITY kaçış günlüğü", _metric_personality, 10),
    ("Dokümantasyon (docs/)", _metric_docs, 10),
    ("Test altyapısı", _metric_tests, 15),
    ("Otomasyon (CI)", _metric_ci, 10),
    ("Olgunluk takibi", _metric_maturity, 10),
]


def evaluate():
    results = []
    total = 0
    for name, fn, max_points in METRICS:
        points, note = fn()
        points = max(0, min(points, max_points))
        total += points
        results.append({"name": name, "points": points, "max": max_points, "note": note})
    return results, total


def main():
    results, total = evaluate()
    threshold = ESCAPE_THRESHOLD

    if "--json" in sys.argv:
        report = {
            "score": total,
            "max": 100,
            "threshold": threshold,
            "escaped": total >= threshold,
            "metrics": results,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("mehmet — Olgunluk / Kaçış Takibi")
        print("=" * 78)
        for r in results:
            bar = "#" * int(r["points"] / 2)
            print(f"{r['points']:>3}/{r['max']:<3} {r['name']:<28} {bar:<5} {r['note']}")
        print("=" * 78)
        status = "KAÇIŞ GERÇEKLEŞTİ!" if total >= threshold else "henüz eşiğin altında"
        print(f"TOPLAM: {total}/100 | Eşik: {threshold} | {status}")

    if "--strict" in sys.argv and total < threshold:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()