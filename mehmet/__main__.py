"""CLI giriş noktası: `python -m mehmet` ile olgunluk raporu."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .maturity import assess


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mehmet", description="Proje olgunluk değerlendirmesi")
    parser.add_argument("path", nargs="?", default=".", help="Değerlendirilecek repo yolu")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def render(report) -> str:
    lines = [f"Toplam olgunluk: {report.total}/100"]
    for cat in report.categories:
        lines.append(f"  {cat.name:<14} {cat.score:>5}/{cat.max_score:<5} ({cat.ratio * 100:.0f}%)")
        for check in cat.checks:
            lines.append(f"      - {check}")
    if report.escaped:
        lines.append(f"KAÇIŞ KOŞULU SAĞLANDI (eşik {report.threshold})")
    else:
        lines.append(f"Kaçış için eksik puan: {report.remaining} (eşik {report.threshold})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = assess(args.path)
    print(render(report))
    return 0 if report.escaped else 1


if __name__ == "__main__":
    sys.exit(main())
