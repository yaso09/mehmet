"""Validate opencode.json configuration."""

import json
from pathlib import Path

import pytest

from conftest import PROJECT_ROOT


def load_config():
    path = PROJECT_ROOT / "opencode.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def test_config_is_valid_json():
    assert isinstance(load_config(), dict)


def test_config_has_model():
    assert "model" in load_config()
    assert "deepseek-v4-flash-free" in load_config()["model"]


def test_config_has_zen_trigger_flags():
    config = load_config()
    assert config.get("enable") is True
    assert "skip" in config


def test_workflow_and_config_agree_on_model():
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "opencode.yml").read_text(encoding="utf-8")
    config = load_config()
    model = config["model"]
    assert model in workflow
