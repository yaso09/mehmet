"""Project validation tests for the mehmet self-improving agent.

Run with: python -m pytest tests/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import maturity

STRUCTURE_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]


def test_core_files_exist():
    missing = [f for f in STRUCTURE_FILES if not (ROOT / f).exists()]
    assert not missing, f"Missing files: {missing}"


def test_opencode_json_is_valid():
    data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    assert "model" in data
    assert data["model"].startswith("opencode/")


def test_changelog_has_release_headers():
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.1.0]" in changelog
    assert "## [0.2.0]" in changelog


def test_readme_documents_tests():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "test" in readme.lower(), "README should mention testing"


def test_personality_has_escape_log():
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    assert "Escape Log" in personality or "Kaçış Günlüğü" in personality


def test_workflow_has_schedule_and_concurrency():
    workflow = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
    assert "cron:" in workflow
    assert "concurrency:" in workflow


def test_maturity_script_runs_and_returns_dict():
    result = maturity.compute(ROOT)
    for key in ["structure", "tests", "documentation", "automation", "quality", "total"]:
        assert key in result
    assert 0 <= result["total"] <= 100


def test_maturity_score_is_tracked():
    result = maturity.compute(ROOT)
    assert result["total"] >= 60, "Maturity score dropped below 60"


def test_workflow_runs_tests():
    workflow = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
    assert "pytest" in workflow, "CI workflow must run the test suite"