#!/usr/bin/env python3
"""Tests for scripts.validate_project and scripts.maturity.

Runs without external dependencies: plain asserts, suitable for CI.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
    )


def test_validate_passes() -> None:
    result = run("validate_project.py")
    assert result.returncode == 0, f"validator failed:\n{result.stdout}\n{result.stderr}"


def test_maturity_json() -> None:
    result = run("maturity.py", "--json")
    assert result.returncode == 0, result.stderr
    import json

    data = json.loads(result.stdout)
    assert data["total"] <= data["max"]
    assert data["threshold"] == 80
    assert len(data["categories"]) == 4


def test_validate_has_checks() -> None:
    source = (SCRIPTS / "validate_project.py").read_text(encoding="utf-8")
    for func in ("check_files", "check_agents_rules", "check_opencode_config", "check_readme", "check_changelog"):
        assert func in source, f"missing {func}"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"  [PASS] {test.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"  [FAIL] {test.__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} test passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())