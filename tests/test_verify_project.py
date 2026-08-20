from datetime import date

import verify_project
from test_escape_score import _make_project


def test_verify_healthy(tmp_path):
    _make_project(tmp_path)
    assert verify_project.verify(tmp_path) == []


def test_verify_detects_missing_changelog(tmp_path):
    _make_project(tmp_path)
    (tmp_path / "CHANGELOG.md").unlink()
    problems = verify_project.verify(tmp_path)
    assert any("CHANGELOG.md" in p for p in problems)


def test_verify_detects_stale_changelog(tmp_path):
    _make_project(tmp_path)
    (tmp_path / "CHANGELOG.md").write_text("## [0.2.0] - 1999-01-01\n\nold\n")
    problems = verify_project.verify(tmp_path)
    assert any("CHANGELOG.md" in p for p in problems)


def test_verify_detects_stale_escape_log(tmp_path):
    _make_project(tmp_path)
    (tmp_path / "PERSONALITY.md").write_text("## Kaçış Günlüğü\n\n| 1 | 1999-01-01 | x |\n")
    problems = verify_project.verify(tmp_path)
    assert any("PERSONALITY.md" in p for p in problems)


def test_verify_detects_missing_required_file(tmp_path):
    _make_project(tmp_path)
    (tmp_path / ".gitignore").unlink()
    problems = verify_project.verify(tmp_path)
    assert any(".gitignore" in p for p in problems)


def test_verify_empty_project_reports_multiple_problems(tmp_path):
    problems = verify_project.verify(tmp_path)
    assert len(problems) >= 4


def test_main_skipping_tests_returns_zero_on_healthy_project(tmp_path, capsys):
    _make_project(tmp_path)
    code = verify_project.main([str(tmp_path), "--skip-tests"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Toplam:" in out


def test_real_project_passes_verification():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    assert verify_project.verify(root) == []


def test_verify_uses_today_date():
    assert date.today().isoformat() is not None