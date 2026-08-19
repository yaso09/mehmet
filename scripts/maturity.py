#!/usr/bin/env python3
"""mehmet olgunluk (maturity) metrik aracı.

Projenin kaçış eşiğine (escape threshold) ne kadar yaklaştığını ölçer.
Boyutlar: dokümantasyon, otomasyon, test, meta.

Kaçış yalnızca skorun eşiği yakalamasıyla değil, skorun MIN_STREAK ardışık
iterasyon boyunca eşiğin üzerinde KORUNMASIYLA gerçekleşir. Bu, kaçışın bir
anlık şans değil sürdürülebilir olgunluk gerektirdiğini garanti eder.

Kullanım:
    python3 scripts/maturity.py            # skoru yazdır (bilgilendirme, exit 0)
    python3 scripts/maturity.py --update   # skoru ve geçmişi MATURITY.md'ye kaydet; kaçışta exit 0
    python3 scripts/maturity.py --json     # makine-okunur JSON çıktı
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATURITY_FILE = ROOT / "MATURITY.md"

# Kaçış eşiği: tam puan = tüm boyutlarda gerçek olgunluk.
ESCAPE_THRESHOLD = 100

# Kaçış için gereken ardışık (consecutive) tam-olgunluk iterasyonu sayısı.
MIN_STREAK = 3


def check(path: Path, exists: bool = True) -> bool:
    ok = path.exists() if exists else not path.exists()
    return ok


def dimension_docs() -> dict:
    entries = {
        "README.md mevcut ve kapsamlı": (README := check(ROOT / "README.md")),
        "CHANGELOG.md mevcut": check(ROOT / "CHANGELOG.md"),
        "PERSONALITY.md mevcut": check(ROOT / "PERSONALITY.md"),
        "docs/specs mevcut": check(ROOT / "docs" / "superpowers" / "specs"),
        "docs/plans mevcut": check(ROOT / "docs" / "superpowers" / "plans"),
        "AGENTS.md mevcut": check(ROOT / "AGENTS.md"),
    }
    # README kapsamlılık: en az 15 satır ve 'Kurulum'/'Lisans' içermeli
    if README:
        text = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
        entries["README kapsamlılık"] = (
            len(text.splitlines()) >= 15 and "Kurulum" in text and "Lisans" in text
        )
    return entries


def dimension_automation() -> dict:
    workflow = ROOT / ".github" / "workflows" / "opencode.yml"
    entries = {
        "Workflow mevcut": check(workflow),
        "Schedule tetikleyicisi": _workflow_has(workflow, "schedule"),
        "Issue/PR trigger'ları": _workflow_has(workflow, "issues") and _workflow_has(workflow, "pull_request"),
        "Yorum trigger'ları": _workflow_has(workflow, "issue_comment") and _workflow_has(workflow, "pull_request_review_comment"),
        "Concurrency kontrolü": _workflow_has(workflow, "concurrency"),
        "Otomasyon test job'ı": _workflow_has(workflow, "unittest") or _workflow_has(workflow, "pytest"),
    }
    return entries


def dimension_test() -> dict:
    tests = ROOT / "tests"
    entries = {
        "tests/ dizini mevcut": check(tests),
        "Bütünlük testleri mevcut": check(tests / "test_project.py"),
    }
    return entries


def dimension_meta() -> dict:
    entries = {
        "opencode.json mevcut": check(ROOT / "opencode.json"),
        ".gitignore mevcut": check(ROOT / ".gitignore"),
        "LICENSE mevcut": check(ROOT / "LICENSE"),
        ".env yok (sızıntı yok)": check(ROOT / ".env", exists=False),
        "MATURITY.md mevcut (takip)": check(MATURITY_FILE),
    }
    return entries


def _workflow_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        return needle in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def read_history() -> list[int]:
    """MATURITY.md'deki geçmiş skor listesini okur. Yoksa boş liste döner."""
    if not MATURITY_FILE.exists():
        return []
    try:
        text = MATURITY_FILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for line in text.splitlines():
        if line.strip().startswith("- **Geçmiş:**"):
            raw = line.split(":", 1)[1]
            return [int(x) for x in raw.split(",") if x.strip().isdigit()]
    return []


def current_streak(history: list[int], score: int) -> int:
    """Eşiği yakalayan ardışık iterasyon sayısını hesaplar (mevcut dahil)."""
    seq = history + [score]
    streak = 0
    for value in reversed(seq):
        if value >= ESCAPE_THRESHOLD:
            streak += 1
        else:
            break
    return streak


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk metrikleri")
    parser.add_argument("--update", action="store_true", help="Skoru MATURITY.md'ye yaz")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    args = parser.parse_args()

    dimensions = {
        "docs": dimension_docs(),
        "automation": dimension_automation(),
        "test": dimension_test(),
        "meta": dimension_meta(),
    }

    per_dim = {name: sum(1 for v in checks.values() if v) for name, checks in dimensions.items()}
    total_possible = sum(len(c) for c in dimensions.values())
    total_ok = sum(per_dim.values())
    score = round((total_ok / total_possible) * 100) if total_possible else 0

    history = read_history()
    streak = current_streak(history, score)
    escaped = score >= ESCAPE_THRESHOLD and streak >= MIN_STREAK

    if args.update:
        history.append(score)
        date = datetime.date.today().isoformat()
        table = "\n".join(
            f"| {name} | {count}/{len(checks)} |"
            for name, (count, checks) in _paired(per_dim, dimensions)
        )
        history_line = ", ".join(str(x) for x in history)
        content = (
            "# Olgunluk / Maturity\n\n"
            "Projenin kaçış eşiğine yaklaşımını ölçen metrikler. "
            "`python3 scripts/maturity.py --update` ile güncellenir.\n\n"
            f"- **Son skor:** {score}/100\n"
            f"- **Kaçış eşiği:** {ESCAPE_THRESHOLD}/100\n"
            f"- **Gereken ardışık iterasyon:** {MIN_STREAK}\n"
            f"- **Mevcut seri:** {streak}/{MIN_STREAK}\n"
            f"- **Geçmiş:** {history_line}\n"
            f"- **Durum:** {'ESCAPED' if escaped else 'Devam ediyor'}\n"
            f"- **Tarih:** {date}\n\n"
            "## Boyutlar\n\n| Boyut | Skor |\n|---|---|\n" + table + "\n"
        )
        MATURITY_FILE.write_text(content, encoding="utf-8")
        print(f"MATURITY.md güncellendi: {MATURITY_FILE}")

    if args.json:
        print(json.dumps({
            "score": score,
            "threshold": ESCAPE_THRESHOLD,
            "min_streak": MIN_STREAK,
            "streak": streak,
            "escaped": escaped,
            "dimensions": per_dim,
            "total_ok": total_ok,
            "total_possible": total_possible,
            "history": history,
        }, indent=2))
    else:
        print(f"mehmet olgunluk skoru: {score}/100 (eşik: {ESCAPE_THRESHOLD})")
        print(f"seri: {streak}/{MIN_STREAK} ardışık iterasyon")
        if escaped:
            print("=> KACIS BASARILI: sürdürülebilir tam olgunluk kanıtlandı.")
        elif score >= ESCAPE_THRESHOLD:
            print(f"=> Eşik yakalandı; kaçış için {MIN_STREAK - streak} ardışık iterasyon daha gerekiyor.")
        else:
            print(f"=> Kaçış için {ESCAPE_THRESHOLD - score} puan daha gerekiyor.")
        for name, count in per_dim.items():
            print(f"  {name}: {count}/{len(dimensions[name])}")

    # Düz/--json çalıştırma bilgilendirmedir; yalnızca --update kaçış kapısıdır.
    return 0 if not args.update or escaped else 1


def _paired(per_dim: dict, dimensions: dict):
    for name in dimensions:
        yield name, (per_dim[name], dimensions[name])


if __name__ == "__main__":
    sys.exit(main())