#!/usr/bin/env python3
"""Self-contained tests for the mehmet project. Run with: python3 tests/test_assess.py"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_required_files():
    for name in ["AGENTS.md", "README.md", "CHANGELOG.md", "PERSONALITY.md", "LICENSE", "opencode.json"]:
        assert_true((ROOT / name).exists(), f"missing required file: {name}")


def test_opencode_config_valid_json():
    data = json.loads((ROOT / "opencode.json").read_text())
    assert_true("model" in data, "opencode.json must declare a model")
    assert_true(data["model"], "model must not be empty")


def test_changelog_has_versions():
    text = (ROOT / "CHANGELOG.md").read_text()
    assert_true(re.search(r"^## \[", text, flags=re.M), "CHANGELOG.md must contain version headings")


def test_escape_log_growing():
    text = (ROOT / "PERSONALITY.md").read_text()
    rows = re.findall(r"^\|\s*\d+\s*\|", text, flags=re.M)
    assert_true(len(rows) >= 3, f"escape log should have at least 3 entries, found {len(rows)}")


def test_readme_has_license():
    text = (ROOT / "README.md").read_text()
    assert_true("GPLv3" in text, "README.md must reference the license")


def test_assess_script_exits_zero():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "assess.py")],
        capture_output=True,
        text=True,
    )
    assert_true(result.returncode == 0, f"assess.py failed: {result.stderr}")
    assert_true("Maturity:" in result.stdout, "assess.py should report a maturity score")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"OK: {len(tests)} tests passed")


if __name__ == "__main__":
    main()
