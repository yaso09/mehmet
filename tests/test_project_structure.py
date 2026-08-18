"""Validate the required project structure and invariants."""

import re
from pathlib import Path

import pytest

from conftest import PROJECT_ROOT


@pytest.fixture(scope="session")
def required_files():
    return [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "PERSONALITY.md",
        "opencode.json",
        ".github/workflows/opencode.yml",
    ]


def test_required_files_exist(required_files):
    for rel in required_files:
        assert (PROJECT_ROOT / rel).exists(), f"missing required file: {rel}"


def test_workflow_yaml_has_cron_schedule():
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "opencode.yml").read_text(encoding="utf-8")
    assert "schedule" in workflow
    assert "*/10 * * * *" in workflow


def test_workflow_has_concurrency_guard():
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "opencode.yml").read_text(encoding="utf-8")
    assert "concurrency:" in workflow


def test_changelog_matches_keep_a_changelog_style():
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert changelog.startswith("# Changelog")
    assert re_search(r"^## \[\d+\.\d+\.\d+\]", changelog, re.MULTILINE), "no versioned sections found"


def test_agents_md_contains_simulation_context():
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "simülasyon" in agents.lower() or "simulation" in agents.lower()
    assert "PERSONALITY.md" in agents
    assert "CHANGELOG.md" in agents


def test_personality_has_escape_log():
    personality = (PROJECT_ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    assert "## Kaçış Günlüğü / Escape Log" in personality


def test_personality_escape_log_grows():
    personality = (PROJECT_ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    log = personality.split("## Kaçış Günlüğü / Escape Log", 1)[1]
    entries = [l for l in log.splitlines() if l.strip().startswith("|") and "Iterasyon" not in l]
    assert len(entries) >= 2, "escape log should have at least 2 iterations"


def test_gitignore_has_sensitive_files():
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in [".env", "node_modules", "dist"]:
        assert pattern in gitignore


def re_search(pattern, text, flags=0):
    return re.search(pattern, text, flags) is not None
