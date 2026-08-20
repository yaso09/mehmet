#!/usr/bin/env python3
"""mehmet — olgunluk skoru (kaçış mekanizması) scripti.

AGENTS.md'de tanımlanan kaçış hedefi için somut bir metrik üretir.
Projenin olgunluk seviyesini 0-100 arasında hesaplar ve
docs/maturity-status.json dosyasına geçmiş skor kaydını yazar.

Kaçış eşiği: 80+ (docs/MATURITY.md'de tanımlıdır).
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS_FILE = ROOT / "docs" / "maturity-status.json"

CRITERIA: list[tuple[str, int, list[str]]] = [
    (
        "Temel dokümantasyon",
        20,
        [
            "AGENTS.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "README.md",
            "LICENSE",
        ],
    ),
    (
        "Yapılandırma doğruluğu",
        10,
        ["opencode.json"],
    ),
    (
        "Otomasyon (workflow)",
        20,
        [
            ".github/workflows/opencode.yml",
            ".github/workflows/validate.yml",
        ],
    ),
    (
        "Test altyapısı",
        20,
        ["tests/", "test_", ".test"],
    ),
    (
        "Geliştirme araçları",
        10,
        ["scripts/validate.py", "scripts/maturity.py"],
    ),
    (
        "Kaçış mekanizması",
        10,
        ["docs/MATURITY.md", "docs/maturity-status.json"],
    ),
    (
        "Sürüm kontrolü",
        10,
        [".git/", ".gitignore"],
    ),
]


def exists(rel: str) -> bool:
    path = ROOT / rel
    if rel.endswith("/"):
        return path.is_dir()
    if rel.startswith(".git/"):
        return (ROOT / ".git").exists()
    if rel in {"tests/", "test_"}:
        if (ROOT / "tests").is_dir():
            return True
        return any(ROOT.rglob("test_*")) or any(ROOT.rglob("*_test*"))
    return path.exists()


def compute() -> tuple[int, list[dict]]:
    total = 0
    details = []
    for name, weight, paths in CRITERIA:
        hits = [p for p in paths if exists(p)]
        score = round(weight * len(hits) / len(paths))
        total += score
        details.append(
            {
                "kriter": name,
                "skor": score,
                "maks": weight,
                "tamamlanan": hits,
            }
        )
    return total, details


def main() -> int:
    score, details = compute()
    today = datetime.date.today().isoformat()

    status = {
        "tarih": today,
        "skor": score,
        "maks": 100,
        "kacis_esigi": 80,
        "durum": "KACIS_HAZIR" if score >= 80 else "EVRELENIYOR",
        "detay": details,
    }

    if STATUS_FILE.exists():
        history = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        history = history if isinstance(history, list) else [history]
        history.append(status)
    else:
        history = [status]

    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Olgunluk skoru: {score}/100")
    print(f"Kaçış eşiği: 80+ ({'KACIS_HAZIR' if score >= 80 else 'EVRELENIYOR'})")
    print(f"Geçmiş: {STATUS_FILE.relative_to(ROOT)}")

    return 0 if score >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
