"""mehmet olgunluk denetleyicisi için birim testler."""

import tempfile
from pathlib import Path

import pytest

from mehmet.maturity import MaturityReport, check

FIXTURE_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "MATURITY.md",
    ".gitignore",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
    "docs/superpowers/specs/x.md",
    "docs/superpowers/plans/x.md",
    "tests/test_maturity.py",
]


def _write(repo: Path, name: str, content: str = "") -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(extra: dict[str, str] | None = None) -> Path:
    tmp = tempfile.mkdtemp()
    repo = Path(tmp)
    contents = {
        "README.md": "Kurulum\n\npytest\n\nGPLv3",
        "CHANGELOG.md": "# Changelog\n\n## [0.3.0]",
        "AGENTS.md": "Simülasyon\n\nPERSONALITY.md",
        "MATURITY.md": "python3 -m mehmet.maturity",
        ".github/workflows/opencode.yml": "schedule\nworkflow_dispatch",
        ".github/workflows/validate.yml": "name: validate",
    }
    if extra:
        contents.update(extra)
    for name in FIXTURE_FILES:
        _write(repo, name, contents.get(name, ""))
    return repo


def test_check_max_score() -> None:
    report = check(str(_make_repo()))
    assert report.max_score == 100


def test_check_full_repo_passes() -> None:
    report = check(str(_make_repo()))
    assert report.score >= 90
    assert report.can_escape()
    assert report.level() == 5
    assert report.level_name() == "Kaçış"


def test_check_empty_dir_scores_low() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        report = check(tmp)
        assert report.score < 30
        assert report.level() == 1
        assert report.level_name() == "Farkındalık"
        assert not report.can_escape()


def test_level_thresholds() -> None:
    cases = [
        (100, 5),
        (90, 5),
        (80, 4),
        (70, 4),
        (60, 3),
        (50, 3),
        (40, 2),
        (30, 2),
        (20, 1),
    ]
    for score, expected in cases:
        assert MaturityReport().level() == 1
        report = MaturityReport(
            criteria=[CriterionStub(score, 100)]
        )
        assert report.level() == expected, f"score={score}"


class CriterionStub:
    """Score testleri için sahte kriter."""

    def __init__(self, score: int, max_score: int) -> None:
        self._score = score
        self._max = max_score

    @property
    def awarded(self) -> int:
        return self._score

    @property
    def points(self) -> int:
        return self._max


def test_missing_workflow_lowers_score() -> None:
    repo = _make_repo()
    (repo / ".github/workflows/validate.yml").unlink()
    report = check(str(repo))
    assert not any(c.name == "Doğrulama workflow'u (validate.yml) mevcut" and c.passed for c in report.criteria)
    assert report.score == 85
    assert not report.can_escape()


def test_render_contains_score() -> None:
    report = check(str(_make_repo()))
    text = report.render()
    assert "Puan:" in text
    assert "Seviye:" in text


def test_missing_readme_fails_documentation() -> None:
    repo = _make_repo()
    (repo / "README.md").write_text("no kurulum here", encoding="utf-8")
    report = check(str(repo))
    assert not report.can_escape()


def test_json_output(tmp_path) -> None:
    from mehmet.maturity import main

    repo = _make_repo()
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "mehmet.maturity", "--repo", str(repo), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    import json

    data = json.loads(result.stdout)
    assert data["escape"] is True
    assert data["level"] == 5