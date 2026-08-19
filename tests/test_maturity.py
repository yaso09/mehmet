import json

from mehmet import ESCAPE_THRESHOLD
from mehmet.maturity import _changelog_entries, _escape_log_rows, main, scan


def _write(repo, files):
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _minimal_repo(tmp_path):
    _write(tmp_path, {
        "AGENTS.md": "# simülasyon\n",
        "opencode.json": "{}",
        ".gitignore": "node_modules/\n",
        "LICENSE": "GPLv3\n",
        ".github/workflows/opencode.yml": "name: mehmet\n",
    })
    return tmp_path


def _escape_ready_repo(tmp_path):
    _write(tmp_path, {
        "AGENTS.md": "# simülasyon\n",
        "opencode.json": "{}",
        ".gitignore": "node_modules/\n",
        "LICENSE": "GPLv3\n",
        ".github/workflows/opencode.yml": (
            "name: mehmet\n"
            "jobs:\n"
            "  validate:\n"
            "    steps:\n"
            "      - run: make test\n"
        ),
        "README.md": "# mehmet\n",
        "CHANGELOG.md": "## [0.1.0]\n## [0.2.0]\n## [0.3.0]\n",
        "PERSONALITY.md": (
            "| Iterasyon | Tarih | İlerleme |\n"
            "|---|---|---|\n"
            "| 1 | 2026-07-04 | ilk |\n"
            "| 2 | 2026-08-19 | ikinci |\n"
        ),
        "docs/maturity.md": "# Olgunluk\n",
        "mehmet/__init__.py": '"""paket"""\n',
        "mehmet/maturity.py": '"""motor"""\n' + "def main():\n    pass\n" + ("x = 1\n" * 60),
        "tests/test_maturity.py": (
            "import mehmet\n"
            "def test_a():\n    pass\n"
            "def test_b():\n    pass\n"
            "def test_c():\n    pass\n"
        ),
        "Makefile": "test:\n\tpython -m pytest -q\n",
        "pyproject.toml": "[project]\nname = \"mehmet\"\n",
    })
    return tmp_path


def test_empty_dir_scores_zero(tmp_path):
    report = scan(tmp_path)
    assert report.total == 0
    assert report.verdict == "early"
    assert set(report.dimensions) == {"structure", "documentation", "code", "tests", "automation"}


def test_minimal_repo_scores_structure_only(tmp_path):
    repo = _minimal_repo(tmp_path)
    report = scan(repo)
    assert report.dimensions["structure"].score == 100
    assert report.dimensions["documentation"].score == 0
    assert report.dimensions["tests"].score == 0
    assert report.total == 15.0


def test_changelog_entries_counted(tmp_path):
    text = "## [0.1.0]\n## [0.2.0]\n## [0.3.0]\n"
    assert _changelog_entries(text) == 3
    assert _changelog_entries("giriş yok") == 0


def test_escape_log_rows_counted():
    content = (
        "## Kaçış Günlüğü\n"
        "| Iterasyon | Tarih | İlerleme |\n"
        "|---|---|---|\n"
        "| 1 | a | b |\n"
        "| 2 | c | d |\n"
    )
    assert _escape_log_rows(content) == 2
    assert _escape_log_rows("başlık yok") == 0


def test_escape_ready_repo_reaches_threshold(tmp_path):
    repo = _escape_ready_repo(tmp_path)
    report = scan(repo)
    assert report.total >= ESCAPE_THRESHOLD
    assert report.verdict == "escape-ready"
    assert all(dim.score == 100 for dim in report.dimensions.values())


def test_verdict_thresholds(tmp_path):
    assert scan(tmp_path).verdict == "early"
    _write(tmp_path, {"README.md": "x", "CHANGELOG.md": "## [0.1.0]\n", "PERSONALITY.md": "| a | b | c |\n", "docs/d.txt": "x"})
    report = scan(tmp_path)
    assert report.total > 0
    assert report.verdict != "escape-ready"
    assert report.total < ESCAPE_THRESHOLD


def test_cli_json_output(tmp_path, capsys):
    _minimal_repo(tmp_path)
    code = main([str(tmp_path), "--json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert code == 0
    assert data["total"] == 15.0
    assert data["dimensions"]["structure"]["score"] == 100


def test_cli_strict_exit_code(tmp_path):
    _minimal_repo(tmp_path)
    assert main([str(tmp_path), "--strict"]) == 1
    repo = _escape_ready_repo(tmp_path)
    assert main([str(repo), "--strict"]) == 0
