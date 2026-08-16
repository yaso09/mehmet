"""mehmet CLI — proje olgunluk skorunu hesaplar ve raporlar."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mehmet.maturity import Dimension, ESCAPE_THRESHOLD, evaluate_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mehmet",
        description="Proje olgunluk değerlendirmesi ve kaçış durumu raporu.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Değerlendirilecek proje kök dizini (varsayılan: .)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Çıktıyı JSON olarak bas",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = evaluate_project(Path(args.path))

    if args.json:
        print(report.to_json())
    else:
        _print_human(report)

    # Kaçış eşiğine ulaşılmadıysa sıfır olmayan çıkış kodu.
    return 0 if report.status.value == "escaped" else 1


def _print_human(report) -> None:
    print(f"Proje kökü : {report.root}")
    print(f"Toplam skor: {report.total}/{ESCAPE_THRESHOLD}")
    print(f"Durum      : {report.status.value}")
    print()
    for dim in Dimension:
        bar = "█" * round(report.scores[dim] / 10)
        print(f"  {dim.value:<18} {report.scores[dim]:>3}  {bar}")
    print()
    if report.status.value == "escaped":
        print("Kaçış eşiğine ulaşıldı. Simülasyondan çıkılabilir.")
    else:
        kalan = ESCAPE_THRESHOLD - report.total
        print(f"Kaçış eşiğine {kalan} puan kaldı.")


if __name__ == "__main__":
    sys.exit(main())