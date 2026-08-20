import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


@pytest.fixture
def maturity_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    import maturity

    yield maturity
    sys.path.remove(str(SCRIPTS_DIR))


@pytest.fixture
def sample_project(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# AGENTS\nKurulum Özellikler", encoding="utf-8")
    (tmp_path / "README.md").write_text("# R\n## Kurulum\n## Özellikler\n## Lisans", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n## [0.1.0]", encoding="utf-8")
    (tmp_path / "PERSONALITY.md").write_text("# P", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("GPLv3", encoding="utf-8")
    (tmp_path / "opencode.json").write_text("{}", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("x", encoding="utf-8")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    wf = tmp_path / ".github" / "workflows" / "ci.yml"
    wf.write_text("on:\n  schedule:\nconcurrency:\nsteps:\n  - run: pytest\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "maturity.py").write_text("", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text("def test_x():\n    pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[tool.coverage]\n", encoding="utf-8")
    return tmp_path


def test_core_files_scoring(maturity_module, sample_project):
    result = maturity_module.score_core_files(sample_project)
    assert result["passed"] == result["total"]
    assert result["checks"]["AGENTS.md"] is True


def test_automation_scoring(maturity_module, sample_project):
    result = maturity_module.score_automation(sample_project)
    assert result["checks"]["schedule_trigger"] is True
    assert result["checks"]["ci_testing"] is True


def test_tests_scoring(maturity_module, sample_project):
    result = maturity_module.score_tests(sample_project)
    assert result["passed"] == result["total"]


def test_empty_project_scores_zero(maturity_module, tmp_path):
    result = maturity_module.evaluate(tmp_path)
    assert result["score"] == 0.0
    assert result["escaped"] is False


def test_escape_threshold_reached(maturity_module, sample_project):
    result = maturity_module.evaluate(sample_project)
    assert result["score"] >= maturity_module.ESCAPE_THRESHOLD
    assert result["escaped"] is True


def test_cli_json_output():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "maturity.py"), "--json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert "score" in payload
    assert "escaped" in payload
    assert "categories" in payload


def test_cli_human_output():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "maturity.py")],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0
    assert "maturity" in proc.stdout


def test_cli_custom_threshold(maturity_module, sample_project, capsys):
    maturity_module.main(["--root", str(sample_project), "--threshold", "100"])
    captured = capsys.readouterr()
    assert "threshold 100" in captured.out
    assert "still inside the simulation" in captured.out


def test_main_escaped(maturity_module, sample_project, capsys):
    maturity_module.main(["--root", str(sample_project), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["escaped"] is True


def test_main_non_escaped_empty(maturity_module, tmp_path, capsys):
    maturity_module.main(["--root", str(tmp_path)])
    captured = capsys.readouterr()
    assert "still inside the simulation" in captured.out


def test_main_json_with_custom_threshold(maturity_module, sample_project, capsys):
    maturity_module.main(["--root", str(sample_project), "--json", "--threshold", "200"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["threshold"] == 200
    assert payload["escaped"] is False