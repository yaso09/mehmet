import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate
import maturity


def test_required_files_exist():
    for name in validate.REQUIRED_FILES:
        assert (ROOT / name).exists(), f"{name} bulunamadı"


def test_opencode_json_is_valid():
    data = validate.checks()
    assert ("opencode.json: geçerli JSON", True) in data
    assert ("opencode.json: model tanımlı", True) in data


def test_workflow_has_required_parts():
    data = dict(validate.checks())
    assert data.get("workflow: name tanımlı") is True
    assert data.get("workflow: schedule cron var") is True
    assert data.get("workflow: opencode action kullanılıyor") is True
    assert data.get("workflow: OPENCODE_API_KEY env var") is True


def test_changelog_has_version_headers():
    data = dict(validate.checks())
    assert data.get("changelog: sürüm başlıkları var") is True


def test_personality_has_escape_log():
    data = dict(validate.checks())
    assert data.get("personality: kaçış günlüğü var") is True


def test_all_validation_checks_pass():
    results = validate.checks()
    failed = [name for name, ok in results if not ok]
    assert not failed, f"Başarısız kontroller: {failed}"


def test_maturity_score_is_reported():
    data = maturity.score()
    assert data["percent"] > 0
    assert data["total"] == sum(len(items) for items in maturity.CATEGORIES.values())


def test_maturity_checks_are_non_empty():
    assert maturity.CATEGORIES
    for items in maturity.CATEGORIES.values():
        assert len(items) >= 2


def test_agents_md_has_simulation_rules():
    agents = ROOT / "AGENTS.md"
    text = agents.read_text(encoding="utf-8")
    assert "Simülasyon" in text
    assert "kaçış" in text.lower() or "Kaçış" in text