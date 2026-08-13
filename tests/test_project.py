#!/usr/bin/env python3
"""Test runner for mehmet project health.

Delegates to scripts/test_validate.py and asserts the maturity score stays
above the escape threshold configuration.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    print("> Running script-level tests")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "test_validate.py")],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return result.returncode

    print("> Checking maturity score")
    maturity = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "maturity.py")],
        capture_output=True,
        text=True,
    )
    print(maturity.stdout)
    return maturity.returncode


if __name__ == "__main__":
    sys.exit(main())
