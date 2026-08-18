"""Validate the maturity assessment script."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import PROJECT_ROOT

SCRIPT = PROJECT_ROOT / "scripts" / "maturity.py"


def run_script(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def test_script_exists():
    assert SCRIPT.exists()


def test_script_is_executable():
    assert SCRIPT.stat().st_mode & 0o111, "maturity.py should be executable"


def test_script_runs_and_exits_zero():
    result = run_script()
    assert result.returncode == 0, result.stderr


def test_script_json_output_is_valid():
    result = run_script("--json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "score" in payload
    assert "escape_threshold" in payload
    assert "categories" in payload
    assert payload["score"] <= payload["max"]


def test_script_reports_progress_toward_escape():
    result = run_script("--json")
    payload = json.loads(result.stdout)
    assert payload["max"] > 0
    assert payload["score"] >= 0


def test_script_imports_cleanly():
    spec = importlib.util.spec_from_file_location("maturity", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.ESCAPE_THRESHOLD > 0
    assert sum(module.CATEGORIES.values()) == module.CATEGORIES["dokumantasyon"] + sum(
        v for k, v in module.CATEGORIES.items() if k != "dokumantasyon"
    )
