"""Tests for the maturity evaluator."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.maturity import evaluate, main, render


@pytest.fixture
def sample_root(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    (root / "AGENTS.md").write_text("# Simülasyon\n", encoding="utf-8")
    (root / "LICENSE").write_text("GPLv3\n", encoding="utf-8")
    (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    (root / "opencode.json").write_text('{"model": "opencode/test"}', encoding="utf-8")
    (root / "README.md").write_text("# proje\n\n## Kurulum\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "spec.md").write_text("design", encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog\n\n## [0.1.0] - 2026-01-01\n", encoding="utf-8")
    (root / "PERSONALITY.md").write_text("kacis gunlugu\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_maturity.py").write_text("def test_x():\n    pass\n", encoding="utf-8")
    (root / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts" / "maturity.py").write_text("", encoding="utf-8")
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "opencode.yml").write_text(
        "concurrency: x\n"
        "steps:\n"
        "  - run: python -m pytest\n"
        "  - run: python3 scripts/maturity.py\n",
        encoding="utf-8",
    )
    return root


def test_empty_project_scores_zero(tmp_path: Path) -> None:
    result, _ = evaluate(tmp_path)
    assert result["total"] == 0


def test_complete_project_scores_high(sample_root: Path) -> None:
    result, categories = evaluate(sample_root)
    best = sum(sum(c["points"] for c in cat["checks"]) for cat in categories)
    assert result["total"] > 0
    assert result["total"] <= best


def test_render_contains_threshold(sample_root: Path) -> None:
    result, categories = evaluate(sample_root)
    out = render(categories, result["total"], 80, result["best"])
    assert "Toplam: 50/100" not in out
    assert f"**Toplam: {result['total']}/{result['best']}**" in out


def test_main_escape_exit_code(sample_root: Path, capsys: pytest.CaptureFixture) -> None:
    code = main(["--root", str(sample_root), "--threshold", "0", "--no-metric"])
    captured = capsys.readouterr()
    assert code == 42
    assert "ESCAPE_THRESHOLD_REACHED" in captured.out


def test_main_json_output(sample_root: Path, capsys: pytest.CaptureFixture) -> None:
    code = main(["--root", str(sample_root), "--json", "--no-metric", "--threshold", "100"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert "total" in payload and "reached" in payload
    assert payload["reached"] is False


def test_main_missing_root_returns_error(capsys: pytest.CaptureFixture) -> None:
    code = main(["--root", "/nonexistent/xyz"])
    assert code == 2
