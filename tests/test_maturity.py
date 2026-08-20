"""maturity modülü için birim testler."""

import pytest

from mehmet import __version__
from mehmet.maturity import (
    DEFAULT_CRITERIA,
    ESCAPE_THRESHOLD,
    escaped,
    has_passing_tests,
    max_score,
    score,
)


def make_project(tmp_path, source=True, tests=True, docs=True, license_=True):
    """İstenen dosyalarla dolu bir proje kökü oluşturur."""
    (tmp_path / "README.md").write_text("# readme")
    (tmp_path / "CHANGELOG.md").write_text("# changelog")
    (tmp_path / "PERSONALITY.md").write_text("# personality")
    (tmp_path / "opencode.json").write_text("{}")
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")
    (tmp_path / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci")
    if license_:
        (tmp_path / "LICENSE").write_text("GPLv3")
    if docs:
        (tmp_path / "docs" / "superpowers" / "specs").mkdir(parents=True, exist_ok=True)
        (tmp_path / "docs" / "superpowers" / "plans").mkdir(parents=True, exist_ok=True)
    if source:
        (tmp_path / "mehmet").mkdir(exist_ok=True)
        (tmp_path / "mehmet" / "__init__.py").write_text("")
    if tests:
        (tmp_path / "tests").mkdir(exist_ok=True)
        (tmp_path / "tests" / "test_example.py").write_text("")
    return tmp_path


def test_version_is_string():
    assert isinstance(__version__, str)


def test_max_score_is_ten():
    assert max_score() == pytest.approx(10.0)


def test_criteria_keys_unique():
    keys = [c.key for c in DEFAULT_CRITERIA]
    assert len(keys) == len(set(keys))


def test_empty_project_scores_zero(tmp_path):
    report = score(tmp_path)
    assert report["score"] == 0.0
    assert report["max"] == pytest.approx(10.0)
    assert report["ratio"] == 0.0
    assert not escaped(report)


def test_full_project_scores_max(tmp_path):
    root = make_project(tmp_path)
    report = score(root)
    assert report["score"] == pytest.approx(10.0)
    assert report["ratio"] == pytest.approx(1.0)
    assert escaped(report)


def test_missing_source_lowers_score(tmp_path):
    root = make_project(tmp_path, source=False)
    report = score(root)
    assert report["score"] == pytest.approx(8.5)


def test_missing_tests_lowers_score(tmp_path):
    root = make_project(tmp_path, tests=False)
    report = score(root)
    assert report["score"] == pytest.approx(8.5)


def test_missing_docs_and_source_below_threshold(tmp_path):
    root = make_project(tmp_path, source=False, docs=False)
    report = score(root)
    assert report["score"] == pytest.approx(7.5)
    assert not escaped(report, ESCAPE_THRESHOLD)


def test_custom_threshold(tmp_path):
    root = make_project(tmp_path, source=False, docs=False)
    report = score(root)
    assert escaped(report, 7.0)
    assert not escaped(report, 8.0)


def test_score_accepts_str_path(tmp_path):
    root = make_project(tmp_path)
    assert score(str(root))["score"] == pytest.approx(10.0)


def test_has_passing_tests(tmp_path):
    assert has_passing_tests(make_project(tmp_path))
    empty = tmp_path / "empty"
    empty.mkdir()
    assert not has_passing_tests(make_project(empty, tests=False))


def test_criterion_report_details(tmp_path):
    root = make_project(tmp_path, tests=False)
    report = score(root)
    assert report["criteria"]["tests"]["passed"] is False
    assert report["criteria"]["tests"]["weight"] == pytest.approx(1.5)