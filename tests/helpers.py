"""Shared test helpers for the mehmet project."""

import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")