"""mehmet CLI — olgunluk kontrolünü çalıştırır.

Kullanım:
    python -m mehmet [--json] [--threshold N] [PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .maturity import ESCAPE_THRESHOLD, escaped, score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mehmet",
        description="Proje olgunluk seviyesini ölçer ve kaçış eşiğini test eder.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Proje kökü (varsayılan: .)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Çıktıyı JSON formatında yazdır.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=ESCAPE_THRESHOLD,
        help=f"Kaçış eşiği (varsayılan: {ESCAPE_THRESHOLD}).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = score(Path(args.path))
    success = escaped(report, args.threshold)

    if args.json:
        payload = {
            "version": __version__,
            "path": str(Path(args.path)),
            "threshold": args.threshold,
            "escaped": success,
            **report,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if success else 1

    print(f"Olgunluk: {report['score']:.1f} / {report['max']:.1f} "
          f"({report['ratio'] * 100:.0f}%)")
    print(f"Kaçış eşiği: {args.threshold}")

    for key, item in report["criteria"].items():
        status = "OK" if item["passed"] else "MISS"
        print(f"  [{status}] {item['label']} (+{item['weight']})")

    print("Kaçış " + ("SAĞLANDI" if success else "HENÜZ SAĞLANMADI"))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())