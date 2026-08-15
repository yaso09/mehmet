from mehmet.maturity import MaturityReport, evaluate


def _build_full_project(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    (tmp_path / "pkg" / "core.py").write_text("x = 1\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_core.py").write_text("def test_x():\n    assert True\n")
    (tmp_path / "README.md").write_text("# readme\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("guide\n")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n")
    (tmp_path / "opencode.json").write_text("{}\n")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci\n")
    return tmp_path


def test_empty_project_is_not_ready(tmp_path):
    report = evaluate(tmp_path)
    assert not report.ready
    assert report.total < 0.9
    assert report.missing()


def test_full_project_is_ready(tmp_path):
    root = _build_full_project(tmp_path)
    report = evaluate(root, test_passed=True)
    assert report.ready
    assert report.total >= 0.9
    assert report.missing() == []


def test_missing_reports_unmet_criteria(tmp_path):
    report = evaluate(tmp_path)
    keys = {c.key for c in report.missing()}
    assert {"source_code", "tests", "automation", "documentation", "changelog", "config"} == keys


def test_test_score_requires_pass(tmp_path):
    root = _build_full_project(tmp_path)
    report_failed = evaluate(root, test_passed=False)
    assert not report_failed.ready


def test_empty_criteria_report_total_is_zero():
    report = MaturityReport(criteria=[])
    assert report.total == 0.0
    assert not report.ready


def test_criterion_contribution():
    from mehmet.maturity import Criterion

    c = Criterion("x", "X", 0.5, 0.8)
    assert c.contribution == 0.4