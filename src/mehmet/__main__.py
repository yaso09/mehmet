"""Command-line interface for the maturity reporter.

Usage:
    python -m mehmet [--root PATH] [--threshold PERCENT]
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Sequence

from mehmet.maturity import DEFAULT_ESCAPE_THRESHOLD, evaluate, escape_ready


def _fmt(score: float) -> str:
    return f"{score * 100:6.1f}%"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Report project maturity.")
    parser.add_argument(
        "--root",
        default=os.getcwd(),
        help="Project root directory to evaluate (default: cwd).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_ESCAPE_THRESHOLD,
        help="Escape readiness threshold in percent (default: 80).",
    )
    args = parser.parse_args(argv)

    total, results = evaluate(args.root)

    print(f"Maturity report for: {os.path.abspath(args.root)}")
    print("-" * 60)
    for cs in results:
        status = "OK" if not cs.missing else "missing: " + ", ".join(cs.missing)
        print(f"{cs.category.name:<22} {_fmt(cs.score):>7}  {status}")
    print("-" * 60)
    print(f"TOTAL SCORE: {_fmt(total)}")

    ready = escape_ready(total, args.threshold)
    if ready:
        print(f"ESCAPE READINESS: READY (>= {args.threshold:.1f}%)")
    else:
        print(f"ESCAPE READINESS: NOT READY (need >= {args.threshold:.1f}%)")
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())