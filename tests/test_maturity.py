#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATURITY = ROOT / "scripts" / "maturity.py"


def run_maturity(root, json_out=True):
    cmd = [sys.executable, str(MATURITY), "--root", str(root)]
    if json_out:
        cmd.append("--json")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc


def test_maturity_runs_on_repo():
    proc = run_maturity(ROOT, json_out=False)
    assert proc.returncode in (0, 1)
    assert "ESCAPE READY" in proc.stdout or "not ready" in proc.stdout


def test_maturity_json_output():
    proc = run_maturity(ROOT)
    result = json.loads(proc.stdout)
    assert "threshold" in result
    assert "total" in result
    assert "escape_ready" in result
    assert "categories" in result
    assert 0 <= result["total"] <= 100


def test_maturity_categories():
    proc = run_maturity(ROOT)
    result = json.loads(proc.stdout)
    for name in ("documentation", "code", "tests", "automation", "evolution"):
        assert name in result["categories"]
        assert 0 <= result["categories"][name]["score"] <= 1


def test_maturity_on_empty_project():
    empty = Path("/tmp") / "opencode" / "empty_proj"
    empty.mkdir(parents=True, exist_ok=True)
    proc = run_maturity(empty)
    result = json.loads(proc.stdout)
    assert result["total"] < 30


def test_missing_threshold_defaults_to_80(tmp_path):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"categories": []}))
    proc = subprocess.run(
        [sys.executable, str(MATURITY), "--root", str(tmp_path), "--config", str(config), "--json"],
        capture_output=True,
        text=True,
    )
    result = json.loads(proc.stdout)
    assert result["threshold"] == 80.0
    assert result["total"] == 0.0
