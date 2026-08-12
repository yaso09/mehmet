"""CLI wrapper that prints mehmet's maturity report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from src import maturity  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Print mehmet's maturity report")
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero below the escape threshold"
    )
    args = parser.parse_args()

    report = maturity.MaturityEngine(REPO).report()
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.render())

    if args.strict and not report.escaped:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())