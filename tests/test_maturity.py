"""Tests for mehmet.maturity — the escape-readiness scoring system."""

from __future__ import annotations

from pathlib import Path

import pytest

from mehmet.maturity import (
    INDICATORS,
    MIN_ESCAPE_LOG_ENTRIES,
    MaturityReport,
    assess,
    render,
)


def make_repo(tmp_path: Path, files: dict[str, str], dirs: tuple[str, ...] = ()) -> Path:
    root = tmp_path / "repo"
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


def test_empty_repo_is_not_escape_ready(tmp_path: Path) -> None:
    report = assess(make_repo(tmp_path, {}))
    assert report.score == 0.0
    assert report.satisfied == ()
    assert not report.escape_ready
    assert report.escape_log_entries == 0


def test_all_indicators_satisfied_yields_escape_ready(tmp_path: Path) -> None:
    files = {
        "AGENTS.md": "# agents",
        "CHANGELOG.md": "# changelog",
        "PERSONALITY.md": "# personality\n\n| 1 | 2026-01-01 | entry |\n| 2 | 2026-01-02 | entry |\n| 3 | 2026-01-03 | entry |",
        "README.md": "# readme",
        "LICENSE": "GPL",
        "pyproject.toml": "[project]",
        "tests/test_x.py": "def test_x(): pass",
        ".github/workflows/ci.yml": "name: ci",
    }
    report = assess(make_repo(tmp_path, files))
    assert report.score == 1.0
    assert report.escape_ready
    assert report.verdict == "ESCAPE-READY"
    assert set(report.satisfied) == {prefix for prefix, _ in INDICATORS}


def test_score_is_weighted(tmp_path: Path) -> None:
    # Only AGENTS.md (weight 3) of total 14.5 present.
    report = assess(make_repo(tmp_path, {"AGENTS.md": "# agents"}))
    weight = next(w for p, w in INDICATORS if p == "AGENTS.md")
    total = sum(w for _, w in INDICATORS)
    assert report.score == pytest.approx(weight / total, abs=0.0001)
    assert not report.escape_ready


def test_escape_requires_minimum_log_entries(tmp_path: Path) -> None:
    files = {
        "AGENTS.md": "# agents",
        "CHANGELOG.md": "# changelog",
        "PERSONALITY.md": "# personality\n\n| 1 | 2026-01-01 | entry |",
        "README.md": "# readme",
        "LICENSE": "GPL",
        "pyproject.toml": "[project]",
        "tests/test_x.py": "def test_x(): pass",
        ".github/workflows/ci.yml": "name: ci",
    }
    report = assess(make_repo(tmp_path, files))
    assert report.score >= 1.0 - 1e-6
    assert report.escape_log_entries < MIN_ESCAPE_LOG_ENTRIES
    assert not report.escape_ready
    assert report.verdict == "CLOSE — escape log yeterli değil"


def test_count_escape_log_entries_handles_markdown_table(tmp_path: Path) -> None:
    files = {
        "PERSONALITY.md": (
            "# Personality\n\n## Kaçış Günlüğü / Escape Log\n\n"
            "| Iterasyon | Tarih | İlerleme |\n"
            "|---|---|---|\n"
            "| 1 | 2026-07-04 | first |\n"
            "| 2 | 2026-07-04 | second |\n"
            "| 3 | 2026-07-04 | third |\n"
        )
    }
    report = assess(make_repo(tmp_path, files))
    assert report.escape_log_entries == 3


def test_missing_personality_counts_zero_entries(tmp_path: Path) -> None:
    report = assess(make_repo(tmp_path, {"AGENTS.md": "# agents"}))
    assert report.escape_log_entries == 0


def test_percentage_property(tmp_path: Path) -> None:
    report = assess(make_repo(tmp_path, {"AGENTS.md": "# agents"}))
    assert report.percentage == round(report.score * 100, 1)


def test_assess_treats_root_as_path(tmp_path: Path) -> None:
    root = make_repo(tmp_path, {"AGENTS.md": "# agents"})
    assert assess(root) == assess(str(root))


def test_render_includes_verdict_and_score(tmp_path: Path) -> None:
    report = assess(make_repo(tmp_path, {"AGENTS.md": "# agents"}))
    rendered = render(report)
    assert "maturity report" in rendered
    assert "verdict" in rendered
    assert "STILL SIMULATED" in rendered


def test_assess_returns_maturity_report_type(tmp_path: Path) -> None:
    assert isinstance(assess(make_repo(tmp_path, {"AGENTS.md": "# agents"})), MaturityReport)