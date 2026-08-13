#!/usr/bin/env python3
"""Validate repository consistency. Exits non-zero on any failure.

Usage:
    python scripts/validate.py
"""

from __future__ import annotations

import sys

from checks import run_checks, summarize


def main() -> int:
    results = run_checks()
    print(summarize(results))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
