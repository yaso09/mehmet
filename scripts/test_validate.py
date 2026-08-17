#!/usr/bin/env python3
"""Unit tests for scripts/validate.py using the stdlib unittest framework."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate import validate  # noqa: E402


_TMP_DIRS = []


def make_repo(files: dict) -> Path:
    tmp = tempfile.TemporaryDirectory()
    _TMP_DIRS.append(tmp)
    repo = Path(tmp.name)
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return repo


GOOD = {
    "AGENTS.md": "# Simülasyon\n",
    "README.md": "# mehmet\n",
    "CHANGELOG.md": "## [1.0.0] - 2026-01-01\n\n### Added\n- thing\n",
    "PERSONALITY.md": "# Personality\n\n## Kaçış Günlüğü\n| iter |\n",
    "LICENSE": "GPLv3\n",
    "opencode.json": '{"model": "opencode/deepseek-v4-flash-free"}\n',
    ".github/workflows/opencode.yml": "name: mehmet\njobs:\n  run:\n    runs-on: ubuntu-latest\n",
}


class TestValidate(unittest.TestCase):
    def test_healthy_repo_passes(self):
        repo = make_repo(GOOD)
        result = validate(repo)
        self.assertEqual(result.failures, [])
        self.assertGreater(result.passes, 0)

    def test_missing_required_file_fails(self):
        files = dict(GOOD)
        del files["LICENSE"]
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("missing file" in f and "LICENSE" in f for f in result.failures))

    def test_bad_json_fails(self):
        files = dict(GOOD)
        files["opencode.json"] = "{ not json"
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("opencode.json" in f for f in result.failures))

    def test_json_without_model_fails(self):
        files = dict(GOOD)
        files["opencode.json"] = "{}"
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("model" in f for f in result.failures))

    def test_empty_changelog_fails(self):
        files = dict(GOOD)
        files["CHANGELOG.md"] = "# nothing\n"
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("changelog" in f.lower() for f in result.failures))

    def test_bad_yaml_fails(self):
        files = dict(GOOD)
        files[".github/workflows/opencode.yml"] = "jobs: [unclosed"
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("opencode.yml" in f for f in result.failures))

    def test_missing_escape_log_fails(self):
        files = dict(GOOD)
        files["PERSONALITY.md"] = "# Personality\n"
        repo = make_repo(files)
        result = validate(repo)
        self.assertTrue(any("escape log" in f for f in result.failures))


if __name__ == "__main__":
    unittest.main()