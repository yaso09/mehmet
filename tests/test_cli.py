"""CLI için entegrasyon testleri."""

import json

import pytest

from mehmet.cli import main

from test_maturity import make_project


def test_cli_human_output_success(tmp_path, capsys):
    root = make_project(tmp_path)
    rc = main([str(root)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Olgunluk: 10.0" in out
    assert "Kaçış SAĞLANDI" in out


def test_cli_human_output_failure(tmp_path, capsys):
    root = make_project(tmp_path, source=False, docs=False)
    rc = main([str(root)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "Kaçış HENÜZ SAĞLANMADI" in out


def test_cli_json_output(tmp_path, capsys):
    root = make_project(tmp_path)
    rc = main(["--json", str(root)])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["escaped"] is True
    assert payload["score"] == 10.0
    assert payload["version"]


def test_cli_custom_threshold(tmp_path, capsys):
    root = make_project(tmp_path, source=False, docs=False)
    rc = main(["--threshold", "7.0", str(root)])
    assert rc == 0
    assert "Kaçış SAĞLANDI" in capsys.readouterr().out


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "mehmet" in out