"""CLI entry point: python -m mehmet"""

import sys

from .escape import main

if __name__ == "__main__":
    sys.exit(main())
