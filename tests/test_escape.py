from pathlib import Path

from mehmet.escape import (
    CRITERIA,
    ESCAPE_THRESHOLD,
    Criterion,
    CriterionResult,
    EscapeReport,
    format_report,
    main,
    scan,
)


def _build_project(root: Path, *, include_source: bool = True) -> Path:
    root.mkdir(parents=True)
    for name in ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE", "opencode.json"]:
        (root / name).write_text("x", encoding="utf-8")
    for name in ["docs", "tests", ".github/workflows"]:
        (root / name).mkdir(parents=True)
    if include_source:
        (root / "mehmet").mkdir()
    return root


def test_complete_project_scores_full(tmp_path):
    root = _build_project(tmp_path / "proj")
    report = scan(root)
    assert report.score == report.max_score
    assert report.escaped


def test_empty_project_scores_zero(tmp_path):
    root = tmp_path / "proj"
    root.mkdir()
    report = scan(root)
    assert report.score == 0.0
    assert not report.escaped
    assert len(report.weak_criteria) == len(CRITERIA)


def test_weights_sum_to_100():
    assert round(sum(c.weight for c in CRITERIA), 1) == 100.0


def test_missing_single_criterion_reduces_score(tmp_path):
    root = _build_project(tmp_path / "proj")
    (root / "LICENSE").unlink()
    report = scan(root)
    assert report.score == report.max_score - 5.0
    assert report.weak_criteria == (Criterion("LICENSE", 5.0, "Legality: license declared"),)


def test_source_code_is_required(tmp_path):
    root = _build_project(tmp_path / "proj", include_source=False)
    report = scan(root)
    assert report.score == report.max_score - 10.0
    assert any(c.key == "mehmet" for c in report.weak_criteria)


def test_threshold_constant():
    assert ESCAPE_THRESHOLD == 80.0


def test_scan_defaults_to_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    report = scan()
    assert report.root == str(tmp_path)


def test_report_is_formatted(tmp_path):
    root = _build_project(tmp_path / "proj")
    report = scan(root)
    text = format_report(report)
    assert "mehmet maturity scan" in text
    assert "Score:" in text
    assert "Status:" in text


def test_main_exit_codes(tmp_path, capsys):
    root = _build_project(tmp_path / "proj")
    assert main([str(root)]) == 0
    capsys.readouterr()

    empty = tmp_path / "empty"
    empty.mkdir()
    assert main([str(empty)]) == 1


def test_escaped_flag():
    report = EscapeReport(
        root=".",
        results=tuple(CriterionResult(c, True) for c in CRITERIA),
        threshold=ESCAPE_THRESHOLD,
    )
    assert report.escaped
