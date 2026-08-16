"""Maturity motoru için birim testler."""

import tempfile
import unittest
from pathlib import Path

from mehmet.maturity import (
    Dimension,
    EscapeStatus,
    ESCAPE_THRESHOLD,
    evaluate_project,
)


class ProjectBuilder:
    """Geçici proje dizinleri oluşturur; dizin ömrünü test süresince korur."""

    def __init__(self) -> None:
        self._dirs: list[tempfile.TemporaryDirectory[str]] = []

    def make(self, files: dict[str, str]) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self._dirs.append(tmp)
        root = Path(tmp.name)
        for relpath, content in files.items():
            target = root / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return root

    def cleanup(self) -> None:
        for tmp in self._dirs:
            tmp.cleanup()
        self._dirs.clear()


class TestMaturity(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = ProjectBuilder()

    def tearDown(self) -> None:
        self.builder.cleanup()

    def test_empty_project_is_locked(self):
        root = self.builder.make({})
        report = evaluate_project(root)
        self.assertEqual(report.total, 0)
        self.assertEqual(report.status, EscapeStatus.LOCKED)

    def test_fully_mature_project_escapes(self):
        files = {
            "README.md": "# proje",
            "CHANGELOG.md": "# Changelog",
            "AGENTS.md": "# ajan",
            "PERSONALITY.md": "# kişilik",
            "docs/index.md": "dok",
            "tests/test_demo.py": "def test_x():\n    pass",
            "pyproject.toml": "[tool.pytest.ini_options]",
            "Makefile": "test:\n\tpython -m pytest\ntest:\nvalidate:\n\tpython -m pytest",
            ".github/workflows/ci.yml": "on: push",
            ".github/workflows/opencode.yml": "on: schedule",
            "Makefile": "test:\nvalidate:\n\tpython -m pytest",
            "src/mehmet/__init__.py": "x = 1",
            "src/mehmet/core.py": "def f() -> int:\n    return 1",
            "opencode.json": "{}",
            ".gitignore": "*.pyc",
            "LICENSE": "MIT",
        }
        root = self.builder.make(files)
        report = evaluate_project(root)
        self.assertGreaterEqual(report.total, ESCAPE_THRESHOLD)
        self.assertEqual(report.status, EscapeStatus.ESCAPED)

    def test_documentation_scoring(self):
        files = {"README.md": "# x", "CHANGELOG.md": "# c"}
        root = self.builder.make(files)
        report = evaluate_project(root)
        self.assertEqual(report.scores[Dimension.DOCUMENTATION], 40)

    def test_total_is_weighted_sum(self):
        files = {"README.md": "# x"}
        root = self.builder.make(files)
        report = evaluate_project(root)
        expected = round(
            20 * 0.20
            + 0 * 0.30
            + 0 * 0.20
            + 0 * 0.20
            + 0 * 0.10
        )
        self.assertEqual(report.total, expected)

    def test_json_serialization(self):
        root = self.builder.make({})
        report = evaluate_project(root)
        data = report.to_dict()
        self.assertIn("total", data)
        self.assertIn("status", data)
        self.assertEqual(data["threshold"], ESCAPE_THRESHOLD)


if __name__ == "__main__":
    unittest.main()