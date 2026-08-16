import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from maturity import CHECKS, MAX_POINTS, evaluate, level_for  # noqa: E402


@pytest.fixture(scope="module")
def results() -> tuple[list[dict], int, int]:
    return evaluate()


def test_required_files_exist() -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "PERSONALITY.md",
        "LICENSE",
        "opencode.json",
        ".github/workflows/opencode.yml",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"eksik dosya: {rel}"


def test_changelog_has_entries() -> None:
    content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [" in content, "CHANGELOG.md sürüm başlığı içermiyor"


def test_readme_not_empty() -> None:
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    assert len(content.strip()) > 50, "README.md çok kısa"


def test_personality_has_escape_log() -> None:
    content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    assert "Kaçış Günlüğü" in content or "Escape Log" in content


def test_opencode_config_is_valid_json() -> None:
    data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    assert "model" in data


def test_license_is_gpl() -> None:
    content = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in content


def test_workflow_has_autonomous_job() -> None:
    content = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
    assert "autonomous:" in content
    assert "schedule" in content


def test_maturity_checks_consistent() -> None:
    total = sum(c["points"] for c in CHECKS)
    assert total == MAX_POINTS
    names = [c["name"] for c in CHECKS]
    assert len(names) == len(set(names)), "maturity kontrollerinde isim çakışması"


def test_evaluate_returns_bounded_score(results) -> None:
    _, score, max_points = results
    assert 0 <= score <= max_points


def test_maturity_levels_complete() -> None:
    assert level_for(0).startswith("Level 0")
    assert level_for(MAX_POINTS).startswith("Level 4")