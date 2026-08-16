import json

import pytest

from scripts import check_health


def build_project(tmp_path, mutate=None):
    """Create a minimal passing project layout in tmp_path.

    `mutate` is a callable receiving (root, content_dict) that can add or
    replace file contents before the directory is populated.
    """
    content = {
        "AGENTS.md": "# Simülasyon Bağlamı\nkaçış\nCHANGELOG.md\nPERSONALITY.md\n",
        "CHANGELOG.md": "# Changelog\n## [0.1.0] - 2026-07-04\n",
        "PERSONALITY.md": "## Origin\n## Evolution\n## Kaçış Günlüğü / Escape Log\n",
        "README.md": "## Özellikler\n## Kurulum\n## Lisans\nGPLv3\n",
        "LICENSE": "GNU GENERAL PUBLIC LICENSE\n",
        "opencode.json": json.dumps({"model": "opencode/deepseek-v4-flash-free"}),
        ".github/workflows/opencode.yml": "name: mehmet\non: [workflow_dispatch]\n",
        ".gitignore": "node_modules/\n.env\n",
    }
    if mutate:
        mutate(content)
    for name, text in content.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


@pytest.fixture
def good_project(tmp_path):
    return build_project(tmp_path)


def test_all_checks_pass_on_good_project(good_project):
    checks = check_health.run_checks(good_project)
    assert checks
    assert all(c.ok for c in checks)
    assert check_health.maturity_score(checks) == 100.0


def test_missing_required_file_fails(good_project):
    (good_project / "AGENTS.md").unlink()
    checks = check_health.run_checks(good_project)
    failed = [c for c in checks if not c.ok]
    names = {c.name for c in failed}
    assert any(n == "file:AGENTS.md" for n in names)


def test_readme_marker_missing_fails(good_project):
    readme = (good_project / "README.md")
    readme.write_text("## Özellikler\n## Kurulum\n## Lisans\n", encoding="utf-8")
    checks = check_health.run_checks(good_project)
    failed = [c for c in checks if not c.ok]
    names = {c.name for c in failed}
    assert "readme:GPLv3" in names


def test_invalid_opencode_json_fails(good_project):
    (good_project / "opencode.json").write_text("{not json", encoding="utf-8")
    checks = check_health.run_checks(good_project)
    opencode_checks = [c for c in checks if c.name == "opencode:model"]
    assert opencode_checks and not opencode_checks[0].ok


def test_maturity_score_partial(good_project):
    (good_project / "CHANGELOG.md").unlink()
    checks = check_health.run_checks(good_project)
    score = check_health.maturity_score(checks)
    assert 0.0 < score < 100.0


def test_maturity_score_empty():
    assert check_health.maturity_score([]) == 0.0


def test_main_json_output(good_project, monkeypatch, capsys):
    monkeypatch.chdir(good_project)
    rc = check_health.main(["--json"])
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["threshold"] == check_health.MIN_PASSING_SCORE
    assert rc in (0, 1)