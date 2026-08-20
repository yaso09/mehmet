from datetime import date
from pathlib import Path

import pytest

import escape_score

TODAY = date.today().isoformat()


def _make_project(root: Path, *, with_tests: bool = True) -> None:
    (root / "README.md").write_text("# readme\n")
    (root / "CHANGELOG.md").write_text(f"## [0.3.0] - {TODAY}\n\nstuff\n")
    (root / "PERSONALITY.md").write_text(f"## Kaçış Günlüğü\n\n| 1 | {TODAY} | x |\n")
    (root / "AGENTS.md").write_text("# agents\n")

    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "spec.md").write_text("# spec\n")
    (docs / "ESCAPE.md").write_text("# escape\n")

    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "tool.py").write_text("print('hi')\n")

    if with_tests:
        tests = root / "tests"
        tests.mkdir()
        (tests / "test_x.py").write_text("def test_x(): pass\n")

    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "opencode.yml").write_text(
        "name: mehmet\n"
        "concurrency:\n"
        "  group: x\n"
        "jobs:\n"
        "  verify:\n"
        "    runs-on: ubuntu-latest\n"
    )

    (root / "opencode.json").write_text('{"model": "test"}\n')
    (root / ".gitignore").write_text("*.pyc\n")


def test_complete_project_scores_full(tmp_path):
    _make_project(tmp_path)
    report = escape_score.build_report(tmp_path)
    assert report.total == report.max_total == 100
    assert report.escaped
    assert report.level == "kaçışa hazır"
    assert report.failed_checks() == []


def test_empty_project_scores_zero(tmp_path):
    report = escape_score.build_report(tmp_path, tests_passed=False)
    assert report.total == 5
    assert not report.escaped
    assert report.level == "yeni doğan"


@pytest.mark.parametrize(
    "score,expected",
    [
        (0, "yeni doğan"),
        (29, "yeni doğan"),
        (30, "farkında"),
        (49, "farkında"),
        (50, "gelişen"),
        (69, "gelişen"),
        (70, "olgun"),
        (89, "olgun"),
        (90, "kaçışa hazır"),
        (100, "kaçışa hazır"),
    ],
)
def test_classify_boundaries(score, expected):
    assert escape_score.classify(score) == expected


def test_failing_tests_reduce_score(tmp_path):
    _make_project(tmp_path)
    report = escape_score.build_report(tmp_path, tests_passed=False)
    assert report.total == 85
    assert not report.escaped
    assert report.level == "olgun"


def test_missing_escape_doc_reduces_score(tmp_path):
    _make_project(tmp_path)
    (tmp_path / "docs" / "ESCAPE.md").unlink()
    report = escape_score.build_report(tmp_path)
    assert report.total == 94


def test_missing_tests_reduce_score(tmp_path):
    _make_project(tmp_path, with_tests=False)
    report = escape_score.build_report(tmp_path)
    assert report.total == 75
    assert not report.escaped
    assert report.level == "olgun"


def test_secret_leak_detected(tmp_path):
    _make_project(tmp_path)
    (tmp_path / "config.py").write_text('API_KEY = "abcdefghijklmnopqrstuvwxyz123456"\n')
    assert escape_score._has_secret_leak(tmp_path)


def test_secret_reference_not_a_leak(tmp_path):
    _make_project(tmp_path)
    (tmp_path / ".github" / "workflows" / "other.yml").write_text(
        "env:\n  OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}\n"
    )
    assert not escape_score._has_secret_leak(tmp_path)


def test_real_project_is_escape_ready():
    root = Path(__file__).resolve().parents[1]
    report = escape_score.build_report(root)
    assert report.escaped
    assert report.total >= 90


def test_render_report_mentions_score(tmp_path):
    _make_project(tmp_path)
    text = escape_score.render_report(escape_score.build_report(tmp_path))
    assert "Toplam:" in text
    assert "kaçışa hazır" in text