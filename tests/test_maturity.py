from pathlib import Path

from mehmet.maturity import (
    ESCAPE_THRESHOLD,
    MAX_SCORE,
    assess,
    score_automation,
    score_code,
    score_docs,
    score_governance,
    score_test,
)


def _write(path: Path, *parts: str, content: str = "") -> Path:
    target = path.joinpath(*parts)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return target


def _module(n_funcs: int = 12, body_lines: int = 10) -> str:
    body = "\n".join(f"    value = {i}" for i in range(body_lines))
    return "\n".join(f"def fn{i}():\n{body}\n    return {i}\n" for i in range(n_funcs))


def _minimal_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _write(root, "README.md", content="# repo")
    return root


def test_empty_repo_scores_zero(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    for scorer in (score_code, score_test, score_docs, score_automation, score_governance):
        assert scorer(root).score == 0.0
    report = assess(root)
    assert report.total == 0.0
    assert not report.escaped


def test_score_code_scales_with_files(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "mehmet", "__init__.py", content='"""pkg."""\n\n__version__ = "0.1.0"\n')
    cat = score_code(root)
    assert cat.score > 0.0
    assert cat.max_score == 30.0


def test_score_code_has_headroom(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "mehmet", "__init__.py", content='"""pkg."""\n')
    _write(root, "mehmet", "a.py", content=_module(n_funcs=3, body_lines=1))
    cat = score_code(root)
    assert cat.score < cat.max_score


def test_score_test_counts_functions(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "pyproject.toml", content="[project]\n")
    for fname in ("test_a.py", "test_b.py", "test_c.py"):
        _write(root, "tests", fname, content="\n".join(
            f"def test_{i}():\n    assert True\n" for i in range(5)))
    cat = score_test(root)
    assert cat.score == 25.0


def test_score_test_no_tests_zero(tmp_path: Path) -> None:
    assert score_test(_minimal_repo(tmp_path)).score == 0.0


def test_score_docs_readme_full(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "README.md", content="\n".join(f"line {i}" for i in range(30)))
    _write(root, "LICENSE")
    cat = score_docs(root)
    assert cat.score >= 11.0
    assert "README" in " ".join(cat.checks)


def test_score_automation_workflows(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    ci = "name: ci\nrun: |\n  pytest\n  ruff check .\n  mehmet .\n"
    _write(root, ".github", "workflows", "ci.yml", content=ci)
    _write(root, ".github", "workflows", "release.yml", content="name: release\n")
    _write(root, ".github", "workflows", "deps.yml", content="name: deps\n")
    _write(root, ".gitignore")
    cat = score_automation(root)
    assert cat.score == 15.0


def test_score_governance_versions(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "AGENTS.md")
    _write(root, "CHANGELOG.md", content="\n".join(f"## [{v}.0.0]\n" for v in range(4)))
    cat = score_governance(root)
    assert cat.score == 10.0


def test_assess_full_project_escapes(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _write(root, "mehmet", "__init__.py",
           content='"""pkg."""\n\n__version__ = "0.1.0"\n')
    for mod in ("core.py", "utils.py", "service.py"):
        _write(root, "mehmet", mod, content=_module())
    _write(root, "pyproject.toml", content="[project]\n")
    for fname in ("test_a.py", "test_b.py", "test_c.py"):
        _write(root, "tests", fname, content="\n".join(
            f"def test_{i}():\n    assert True\n" for i in range(5)))
    _write(root, "README.md", content="\n".join(f"line {i}" for i in range(30)))
    _write(root, "CHANGELOG.md", content="\n".join(f"## [{v}.0.0]\n" for v in range(5)))
    _write(root, "LICENSE")
    _write(root, "AGENTS.md")
    _write(root, "PERSONALITY.md")
    ci = "name: ci\nrun: |\n  pytest\n  ruff check .\n  mehmet .\n"
    _write(root, ".github", "workflows", "ci.yml", content=ci)
    _write(root, ".github", "workflows", "release.yml", content="name: release\n")
    _write(root, ".github", "workflows", "deps.yml", content="name: deps\n")
    _write(root, ".gitignore")

    report = assess(root)
    assert report.escaped
    assert report.total >= ESCAPE_THRESHOLD


def test_assess_real_project_shape() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    report = assess(repo_root)
    assert 0.0 <= report.total <= MAX_SCORE
    assert len(report.categories) == 5
    assert abs(sum(c.score for c in report.categories) - report.total) < 0.01
    for cat in report.categories:
        assert cat.score <= cat.max_score


def test_report_remaining_when_not_escaped() -> None:
    report = assess(Path("/nonexistent/path"))
    assert report.remaining > 0.0
    assert not report.escaped
    assert report.remaining == round(ESCAPE_THRESHOLD - report.total, 1)
