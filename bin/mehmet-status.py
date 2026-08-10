#!/usr/bin/env python3
"""mehmet status CLI.

Queries the project's state files and prints a human-readable status
summary plus the current escape score. Relies only on the Python stdlib.

Usage:
    python3 bin/mehmet-status.py            # full report
    python3 bin/mehmet-status.py --score    # score only
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    path = ROOT / name
    return path.read_text() if path.is_file() else ""


def count_changelog_versions() -> int:
    return len(re.findall(r"^## \[\d+\.\d+\.\d+\]", read("CHANGELOG.md"), re.MULTILINE))


def count_escape_log_entries() -> int:
    text = read("PERSONALITY.md")
    return len(re.findall(r"^\|\s*\d+\s*\|", text, re.MULTILINE))


def latest_version() -> str:
    matches = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", read("CHANGELOG.md"), re.MULTILINE)
    return matches[0] if matches else "0.0.0"


def escape_score() -> int:
    """Computes the score according to docs/kaçış-metrikleri.md.

    Each (label, weight, satisfied) tuple mirrors one row of the maturity
    table so the CLI and the doc can never disagree.
    """
    workflow = read(".github/workflows/opencode.yml")
    verify = read("tests/verify.py")

    criteria = [
        ("README", 10, bool(read("README.md").strip())),
        ("CHANGELOG", 10, bool(read("CHANGELOG.md").strip())),
        ("PERSONALITY+escape log", 5, "Kaçış Günlüğü" in read("PERSONALITY.md")),
        ("design/plan docs", 5, (ROOT / "docs/superpowers").is_dir()),
        ("integrity test suite", 10, (ROOT / "tests/verify.py").is_file()),
        ("tests run in CI", 10, "needs: verify" in workflow),
        ("test coverage", 5, "test_workflow" in verify),
        ("workflow event types", 10, "schedule" in workflow),
        ("concurrency + secret", 5, "concurrency" in workflow and "OPENCODE_API_KEY" in workflow),
        ("semver changelog", 5, bool(re.findall(r"^## \[\d+\.\d+\.\d+\]", read("CHANGELOG.md"), re.MULTILINE))),
        ("application code", 5, (ROOT / "bin/mehmet-status.py").is_file()),
    ]
    return sum(weight for _, weight, ok in criteria if ok)


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet project status")
    parser.add_argument("--score", action="store_true", help="print score only")
    args = parser.parse_args()

    score = escape_score()
    if args.score:
        print(score)
        return 0

    print(f"mehmet v{latest_version()}")
    print(f"versions in CHANGELOG : {count_changelog_versions()}")
    print(f"escape log entries    : {count_escape_log_entries()}")
    print(f"escape score          : {score}/100")
    if score < 80:
        print(f"status: ESCAPE THRESHOLD {score}/100 -> keep improving")
    else:
        print("status: ESCAPE THRESHOLD REACHED")
    try:
        model = json.loads(read("opencode.json")).get("model", "")
        print(f"model                 : {model}")
    except json.JSONDecodeError:
        print("model                 : (invalid config)")
    return 0


if __name__ == "__main__":
    sys.exit(main())