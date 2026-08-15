from mehmet.scanner import scan


def test_scan_empty_dir_has_opportunities(tmp_path):
    result = scan(tmp_path)
    assert not result.has_source
    assert not result.has_tests
    assert result.files == []
    areas = {i.area for i in result.improvements}
    assert {"source_code", "tests", "documentation", "automation", "changelog"} <= areas


def test_scan_with_source_and_tests(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    (tmp_path / "pkg" / "core.py").write_text("def f():\n    return 1\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_core.py").write_text("def test_f():\n    assert True\n")

    result = scan(tmp_path)
    assert result.has_source
    assert result.has_tests
    assert not any(i.area == "source_code" for i in result.improvements)
    assert not any(i.area == "tests" for i in result.improvements)


def test_scan_counts_todos(tmp_path):
    (tmp_path / "code.py").write_text("def f():\n    # TODO fix this\n    return 1\n")
    result = scan(tmp_path)
    assert result.todo_count >= 1
    assert any(i.area == "cleanup" for i in result.improvements)


def test_scan_ignores_hidden_dirs(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x")
    (tmp_path / "real.py").write_text("print(1)\n")
    result = scan(tmp_path)
    assert all(".git" not in str(p) for p in result.files)


def test_opportunities_returns_copy(tmp_path):
    result = scan(tmp_path)
    result.opportunities().append(None)
    assert len(result.improvements) == len(result.opportunities())