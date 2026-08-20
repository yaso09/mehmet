#!/usr/bin/env python3
"""Zero-dependency test runner for the mehmet project.

Discovers and runs all tests under the ``tests`` directory using the
standard library ``unittest`` module, so no third-party packages are
required.
"""

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(TESTS))
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())