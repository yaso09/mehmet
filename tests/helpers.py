"""Shared helpers for the mehmet test suite."""

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    "maturity.json",
]

REQUIRED_DIRS = [
    ".github/workflows",
    "docs",
    "scripts",
    "tests",
]

WORKFLOW_FILES = [
    "opencode.yml",
    "ci.yml",
]


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)


def read_text(rel_path: str) -> str:
    return project_path(rel_path).read_text(encoding="utf-8")


def load_json(rel_path: str):
    with project_path(rel_path).open(encoding="utf-8") as fh:
        return json.load(fh)


def assert_file_exists(testcase, rel_path: str, msg: str = None):
    path = project_path(rel_path)
    testcase.assertTrue(
        path.is_file(),
        msg or f"Eksik dosya: {rel_path}",
    )