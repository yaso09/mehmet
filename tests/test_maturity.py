"""Tests for the maturity scoring system."""

import json
from pathlib import Path

import pytest

from scripts.maturity import ESCAPE_THRESHOLD, assess, main


def _scaffold_project(root: Path) -> None:
    """Create a minimal but complete project skeleton."""
    (root / "README.md").write_text("line\n" * 60, encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog\n\n## [1.0.0]\n- change one\n- change two\n", encoding="utf-8")
    (root / "PERSONALITY.md").write_text("# Personality\n" * 20, encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n" * 20, encoding="utf-8")
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (root / "opencode.json").write_text('{"model": "test"}\n', encoding="utf-8")
    (root / "requirements.txt").write_text("pytest>=8\n", encoding="utf-8")
    (root / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\ntestpaths = ['tests']\n", encoding="utf-8"
    )
    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "lib.py").write_text(
        "def helper():\n    return 42\n\n" * 40, encoding="utf-8"
    )
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_lib.py").write_text("def test_x():\n    pass\n", encoding="utf-8")
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text(
        "name: ci\non: [push]\njobs:\n  test:\n    steps:\n      - run: pytest\n",
        encoding="utf-8",
    )


def test_assess_returns_full_shape(tmp_path):
    _scaffold_project(tmp_path)
    report = assess(tmp_path)
    assert set(report) == {
        "version",
        "total",
        "threshold",
        "escaped",
        "dimensions",
        "details",
    }
    assert report["version"] == "1.0.0"


def test_assess_empty_project_scores_zero(tmp_path):
    report = assess(tmp_path)
    assert report["total"] == 0.0
    assert not report["escaped"]


def test_assess_mature_project_scores_high(tmp_path):
    _scaffold_project(tmp_path)
    report = assess(tmp_path)
    assert report["total"] >= 95
    assert report["escaped"]


def test_escape_threshold_is_reachable(tmp_path):
    _scaffold_project(tmp_path)
    report = assess(tmp_path)
    assert report["total"] >= ESCAPE_THRESHOLD


def test_dimensions_never_exceed_max(tmp_path):
    _scaffold_project(tmp_path)
    report = assess(tmp_path)
    assert report["dimensions"]["documentation"] <= 25
    assert report["dimensions"]["code"] <= 25
    assert report["dimensions"]["tests"] <= 25
    assert report["dimensions"]["automation"] <= 15
    assert report["dimensions"]["configuration"] <= 10


def test_missing_workflow_loses_automation_points(tmp_path):
    _scaffold_project(tmp_path)
    (tmp_path / ".github" / "workflows" / "ci.yml").unlink()
    report = assess(tmp_path)
    assert report["dimensions"]["automation"] == 0


def test_invalid_opencode_json_is_detected(tmp_path):
    _scaffold_project(tmp_path)
    (tmp_path / "opencode.json").write_text("{not valid json\n", encoding="utf-8")
    report = assess(tmp_path)
    assert report["dimensions"]["configuration"] < 6
    assert any(
        "invalid" in note for note in report["details"]["configuration"]
    )


def test_missing_test_suite_loses_points(tmp_path):
    _scaffold_project(tmp_path)
    import shutil

    shutil.rmtree(tmp_path / "tests")
    report = assess(tmp_path)
    assert report["dimensions"]["tests"] == 0


def test_unknown_version_when_missing(tmp_path):
    report = assess(tmp_path)
    assert report["version"] == "unknown"


def test_main_json_output(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["maturity.py", "--json"])
    from scripts.maturity import ROOT

    monkeypatch.setattr("scripts.maturity.ROOT", tmp_path)
    assert main(["--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert "total" in out and "dimensions" in out


def test_main_exit_code_zero(tmp_path, monkeypatch):
    monkeypatch.setattr("scripts.maturity.ROOT", tmp_path)
    assert main([]) == 0