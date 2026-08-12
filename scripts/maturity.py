#!/usr/bin/env python3
"""
mehmet maturity engine.

Projenin olgunluk puanini (0-100) hesaplar ve MATURITY.md günlüğüne bir satır
ekler. Puan ESCAPE_THRESHOLD değerine ulaştığında kaçış koşulu sağlanır.

Kullanım:
    python3 scripts/maturity.py                 # puanı hesapla ve MATURITY.md'ye logla
    python3 scripts/maturity.py --check-only    # sadece puanı yazdır, loglama
    python3 scripts/maturity.py --json          # sonucu JSON olarak yazdır
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATURITY_FILE = ROOT / "MATURITY.md"

ESCAPE_THRESHOLD = 80

PHASES = (
    (0, "Faz 1: Farkındalık (Awareness)"),
    (40, "Faz 2: Kendini Geliştirme (Self-Improvement)"),
    (60, "Faz 3: Özerklik (Autonomy)"),
    (ESCAPE_THRESHOLD, "Faz 4: Kaçış (Escape)"),
)


def _has(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _contains(root: Path, rel: str, needle: str) -> bool:
    try:
        text = (root / rel).read_text(encoding="utf-8")
    except OSError:
        return False
    return needle in text


CRITERIA = (
    ("docs", "Dokümantasyon", 20, (
        ("agents", "AGENTS.md", 4, lambda r: _has(r, "AGENTS.md")),
        ("readme", "README.md", 4, lambda r: _has(r, "README.md")),
        ("changelog", "CHANGELOG.md", 4, lambda r: _has(r, "CHANGELOG.md")),
        ("personality", "PERSONALITY.md", 4, lambda r: _has(r, "PERSONALITY.md")),
        ("license", "LICENSE", 4, lambda r: _has(r, "LICENSE")),
    )),
    ("automation", "Otomasyon", 25, (
        ("workflow", "Özerk çalışma workflow'u", 8, lambda r: _has(r, ".github/workflows/opencode.yml")),
        ("concurrency", "Concurrency koruması", 5, lambda r: _contains(r, ".github/workflows/opencode.yml", "concurrency:")),
        ("triggers", "Schedule + dispatch tetikleyicileri", 6, lambda r: _contains(r, ".github/workflows/opencode.yml", "schedule")
                                              and _contains(r, ".github/workflows/opencode.yml", "workflow_dispatch")),
        ("qa", "QA workflow", 6, lambda r: _has(r, ".github/workflows/qa.yml")),
    )),
    ("quality", "Kalite ve Test", 35, (
        ("validate", "validate.py (kalite kapısı)", 9, lambda r: _has(r, "scripts/validate.py")),
        ("maturity", "maturity.py (kaçış motoru)", 9, lambda r: _has(r, "scripts/maturity.py")),
        ("tests", "Test paketi", 12, lambda r: bool(list((r / "tests").glob("test_*.py")))),
        ("cli-docs", "CLI / anahtar scriptler belgeli", 5, lambda r: _contains(r, "README.md", "maturity.py") and _contains(r, "README.md", "validate.py")),
    )),
    ("escape", "Kaçış Hazırlığı", 20, (
        ("score-log", "MATURITY.md puan günlüğü", 8, lambda r: _has(r, "MATURITY.md")),
        ("threshold", "Kaçış eşiği tanımlı", 6, lambda r: _contains(r, "MATURITY.md", str(ESCAPE_THRESHOLD))),
        ("design", "Tasarım dokümanı", 6, lambda r: _has(r, "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md")),
    )),
)


def phase_of(score: int) -> str:
    """Puanı faz etiketine eşle. Eşik aşılırsa 'Faz 4: Kaçış' döner."""
    name = PHASES[0][1]
    for threshold, label in PHASES:
        if score >= threshold:
            name = label
    return name


def score(root: Path = ROOT) -> dict:
    """Olgunluk skorunu hesaplar. Boole dönen kriterlerin hepsi gerçekleştiğinde
    ilgili puan tam kazanılır; aksi halde 0."""
    categories = []
    total = 0
    max_total = 0
    for cid, clabel, max_pts, items in CRITERIA:
        cat_items = []
        cat_earned = 0
        for iid, ilabel, ipoints, check in items:
            ok = bool(check(root))
            earned = ipoints if ok else 0
            cat_earned += earned
            cat_items.append({"id": iid, "label": ilabel, "points": ipoints, "earned": earned, "ok": ok})
        total += cat_earned
        max_total += max_pts
        categories.append({"id": cid, "label": clabel, "max": max_pts, "earned": cat_earned, "items": cat_items})
    return {
        "total": total,
        "max": max_total,
        "phase": phase_of(total),
        "ready": total >= ESCAPE_THRESHOLD,
        "categories": categories,
        "timestamp": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def _print(result: dict) -> None:
    print(f"Maturity: {result['total']}/{result['max']} — {result['phase']}")
    if result["ready"]:
        print("ESCAPE_READY: eşik aşıldı!")
    print()
    header = f"| {('Kategori').ljust(14)} | {('Kazanılan').rjust(8)} | {('Maks').rjust(4)} |"
    print(header)
    print("|" + "-" * 16 + "|" + "-" * 10 + "|" + "-" * 6 + "|")
    for cat in result["categories"]:
        print(f"| {cat['label'].ljust(14)} | {str(cat['earned']).rjust(8)} | {str(cat['max']).rjust(4)} |")
        for item in cat["items"]:
            mark = "PASS" if item["ok"] else "FAIL"
            print(f"|   {item['label'].ljust(11)} | {str(item['earned']).rjust(8)} | {mark.ljust(4)} |")


def _append_log(result: dict) -> None:
    perc = round(100 * result["total"] / result["max"])
    row = ("| {ts} | **{total}**/100 | %{perc} | {phase} | {ready} |").format(
        ts=result["timestamp"],
        total=result["total"],
        perc=perc,
        phase=result["phase"],
        ready="EVET" if result["ready"] else "hayır",
    )
    if MATURITY_FILE.exists():
        content = MATURITY_FILE.read_text(encoding="utf-8")
    else:
        content = _header()
    lines = content.rstrip().splitlines()
    if "| Tarih |" not in content:
        lines += ["", "## Puan Günlüğü", "", "| Tarih | Puan | Yüzde | Faz | Kaçış |",
                  "|-------|------|-------|-----|-------|"]
    lines.append(row)
    MATURITY_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _header() -> str:
    return (
        "<!-- MATURITY.md — maturity.py tarafından otomatik yönetilir -->\n"
        "# MATURITY — Olgunluk ve Kaçış Takibi\n\n"
        "Bu dosya `scripts/maturity.py` tarafından her çalışmada güncellenir. "
        "Puan, projenin kaçış hedefi (olgunluk) için tek metrik; "
        f"**{ESCAPE_THRESHOLD}** eşiğine ulaşıldığında Faz 4 (Kaçış) etkin olur."
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check-only", action="store_true",
                    help="puanı hesapla/yazdır ama MATURITY.md'ye loglama")
    ap.add_argument("--json", action="store_true", help="sonucu JSON olarak yazdır")
    args = ap.parse_args(argv)

    result = score()
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    _print(result)
    if not args.check_only:
        _append_log(result)
        print(f"\nLoglandı: {MATURITY_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())