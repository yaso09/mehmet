#!/usr/bin/env python3
"""Olgunluk matrisini hesaplar ve kaçış koşullarını değerlendirir.

MATURITY.md dosyasındaki kontrol listesini ayrıştırır, kategori bazında ve
toplam skoru hesaplar, `[ESCAPE]` etiketli zorunlu maddeleri kontrol eder.

Kullanım:
    python3 scripts/maturity.py               # rapor yazdırır
    python3 scripts/maturity.py --check       # dosya formatını doğrular
    python3 scripts/maturity.py --strict      # kaçış koşullarını zorlar
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MATURITY = ROOT / "MATURITY.md"
ESCAPE_TAG = "[ESCAPE]"

HEADING_RE = re.compile(r"^##\s+(.+)$")
ITEM_RE = re.compile(r"^-\s+\[( |x)\]\s+(.+)$")


@dataclass
class Item:
    """Tek bir kontrol listesi maddesi."""

    text: str
    done: bool
    escape: bool


@dataclass
class Category:
    """Kategori adı ve altındaki maddeler."""

    name: str
    items: List[Item] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def done(self) -> int:
        return sum(1 for i in self.items if i.done)

    @property
    def score(self) -> float:
        if self.total == 0:
            return 0.0
        return self.done / self.total * 100


def parse_maturity(text: str) -> List[Category]:
    """MATURITY.md içeriğini kategori listesine ayrıştırır."""
    categories: List[Category] = []
    current: Category | None = None

    def flush() -> None:
        nonlocal current
        if current is not None and current.items:
            categories.append(current)
        current = None

    for raw in text.splitlines():
        line = raw.rstrip()
        heading = HEADING_RE.match(line)
        if heading:
            flush()
            current = Category(name=heading.group(1).strip())
            continue

        item = ITEM_RE.match(line)
        if item:
            if current is None:
                raise ValueError(
                    "Kontrol listesi maddesi bir kategori başlığı altında olmalı: "
                    f"{line!r}"
                )
            content = item.group(2).strip()
            current.items.append(
                Item(
                    text=content,
                    done=item.group(1) == "x",
                    escape=ESCAPE_TAG in content,
                )
            )

    flush()

    if not categories:
        raise ValueError("MATURITY.md içinde kategori bulunamadı.")

    return categories


def validate(categories: List[Category]) -> List[str]:
    """Format doğrulaması yapar; sorunları liste olarak döndürür."""
    errors: List[str] = []

    for cat in categories:
        if not cat.items:
            errors.append(f"'{cat.name}' kategorisinde madde yok.")

    if not any(cat.items for cat in categories):
        errors.append("Hiçbir kategoride kontrol listesi maddesi yok.")

    return errors


def compute_stats(categories: List[Category]) -> dict:
    """Toplam istatistikleri hesaplar."""
    total = sum(c.total for c in categories)
    done = sum(c.done for c in categories)
    escape_items = [i for c in categories for i in c.items if i.escape]
    escape_done = sum(1 for i in escape_items if i.done)

    return {
        "total": total,
        "done": done,
        "score": (done / total * 100) if total else 0.0,
        "escape_total": len(escape_items),
        "escape_done": escape_done,
    }


def escape_conditions_met(stats: dict) -> bool:
    """Kaçış koşullarının sağlanıp sağlanmadığını döndürür."""
    mandatory_ok = (
        stats["escape_total"] > 0
        and stats["escape_done"] == stats["escape_total"]
    )
    return mandatory_ok and stats["score"] >= 80


def print_report(categories: List[Category], stats: dict) -> None:
    """İnsan tarafından okunabilir raporu stdout'a yazar."""
    width = max(len(c.name) for c in categories)
    print("Olgunluk Matrisi Raporu")
    print("=" * (width + 24))
    for cat in categories:
        print(
            f"{cat.name:<{width}}  {cat.done:>2}/{cat.total:<2}  "
            f"%{cat.score:5.1f}"
        )
    print("=" * (width + 24))
    print(f"Toplam        {stats['done']}/{stats['total']}  %{stats['score']:5.1f}")
    print(f"Zorunlu       {stats['escape_done']}/{stats['escape_total']}")
    print()
    if escape_conditions_met(stats):
        print("KAÇIŞ KOŞULLARI SAĞLANDI.")
    else:
        remaining = stats["score"] if stats["score"] < 80 else 0
        print(
            "Kaçış koşulları henüz sağlanmadı: "
            f"skor %{stats['score']:.1f}/80, "
            f"zorunlu {stats['escape_done']}/{stats['escape_total']}."
        )
        if remaining and stats["escape_done"] < stats["escape_total"]:
            print("  -> Zorunlu [ESCAPE] maddeleri tamamlayın.")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="dosya formatını doğrula"
    )
    parser.add_argument(
        "--strict", action="store_true", help="kaçış koşullarını zorla"
    )
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_MATURITY, help="MATURITY.md yolu"
    )
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"Hata: {args.file} bulunamadı.", file=sys.stderr)
        return 1

    try:
        categories = parse_maturity(args.file.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1

    problems = validate(categories)
    for problem in problems:
        print(f"Uyarı: {problem}", file=sys.stderr)

    stats = compute_stats(categories)

    if args.check:
        if problems:
            print(f"Hata: {len(problems)} format sorunu bulundu.", file=sys.stderr)
            return 1
        print(f"Format geçerli: {len(categories)} kategori, {stats['total']} madde.")
        return 0

    if args.strict:
        if not escape_conditions_met(stats):
            print("Hata: Kaçış koşulları sağlanmadı.", file=sys.stderr)
            return 1

    print_report(categories, stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())