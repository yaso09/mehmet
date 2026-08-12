import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src import maturity


def write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_repo(root: Path) -> None:
    write(root / "README.md", "line\n" * 12)
    write(
        root / "CHANGELOG.md",
        "# Changelog\n\n## [0.3.0] - 2026-08-12\n\n### Added\n- thing\n\n## [0.2.0] - 2026-07-04\n",
    )
    write(
        root / "PERSONALITY.md",
        "## Escape Log\n\n| Iterasyon | Tarih | İlerleme |\n"
        "| 1 | 2026-07-04 | a |\n| 2 | 2026-07-04 | b |\n| 3 | 2026-08-12 | c |\n",
    )
    write(root / "opencode.json", json.dumps({"model": "m"}))
    write(root / ".github/workflows/opencode.yml", "name: mehmet\n\non:\n  push:\n")
    write(root / "Makefile", "test:\n\tpython -m unittest discover\n")
    write(root / "scripts/check.py", "print('ok')\n")
    write(root / "src/maturity.py", "VERSION = 1\n")
    write(
        root / "tests/test_sample.py",
        "import unittest\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        assert True\n",
    )
    write(root / "tests/__init__.py", "")


class EmptyRepoTests(unittest.TestCase):
    def test_empty_repo_scores_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            engine = maturity.MaturityEngine(Path(tmp))
            report = engine.report()
        self.assertEqual(report.total, 0.0)
        self.assertFalse(report.escaped)

    def test_empty_repo_renders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = maturity.MaturityEngine(Path(tmp)).report()
        self.assertIn("not yet escaped", report.render())


class ComponentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory()
        build_repo(Path(self.root.name))
        self.engine = maturity.MaturityEngine(Path(self.root.name))

    def tearDown(self) -> None:
        self.root.cleanup()

    def test_documentation_full(self) -> None:
        self.assertEqual(self.engine.measure_documentation(), 1.0)

    def test_documentation_partial(self) -> None:
        write(Path(self.root.name) / "README.md", "x\n")
        fraction = self.engine.measure_documentation()
        self.assertEqual(fraction, 1 / 8)

    def test_changelog_full(self) -> None:
        self.assertEqual(self.engine.measure_changelog(), 1.0)

    def test_personality_full(self) -> None:
        self.assertEqual(self.engine.measure_personality(), 1.0)

    def test_personality_empty(self) -> None:
        write(Path(self.root.name) / "PERSONALITY.md", "no log here\n")
        self.assertEqual(self.engine.measure_personality(), 0.0)

    def test_agent_config_invalid_json(self) -> None:
        write(Path(self.root.name) / "opencode.json", "{broken")
        self.assertEqual(self.engine.measure_agent_config(), 0.0)

    def test_workflow_full(self) -> None:
        self.assertEqual(self.engine.measure_workflow(), 1.0)

    def test_workflow_missing(self) -> None:
        import shutil

        shutil.rmtree(Path(self.root.name) / ".github")
        self.assertEqual(self.engine.measure_workflow(), 0.0)

    def test_automation_full(self) -> None:
        self.assertEqual(self.engine.measure_automation(), 1.0)

    def test_code_full(self) -> None:
        self.assertEqual(self.engine.measure_code(), 1.0)

    @mock.patch("src.maturity.subprocess.run")
    def test_tests_passing(self, run) -> None:
        run.return_value.returncode = 0
        self.assertEqual(self.engine.measure_tests(), 1.0)

    @mock.patch("src.maturity.subprocess.run")
    def test_tests_failing(self, run) -> None:
        run.return_value.returncode = 1
        self.assertEqual(self.engine.measure_tests(), 0.0)


class ReportTests(unittest.TestCase):
    def test_full_repo_escapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_repo(Path(tmp))
            report = maturity.MaturityEngine(Path(tmp)).report()
        self.assertTrue(report.escaped)
        self.assertEqual(report.total, 10.0)
        self.assertIn("ESCAPED", report.render())

    def test_to_dict_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = maturity.MaturityEngine(Path(tmp)).report()
        payload = report.to_dict()
        self.assertEqual(payload["total"], report.total)
        self.assertFalse(payload["escaped"])
        self.assertIn("documentation", payload["components"])

    def test_threshold_boundary(self) -> None:
        report = maturity.Report(
            generated_on="2026-08-12",
            components={},
            total=maturity.ESCAPE_THRESHOLD,
            max_score=maturity.MAX_SCORE,
            escape_threshold=maturity.ESCAPE_THRESHOLD,
            escaped=maturity.ESCAPE_THRESHOLD >= maturity.ESCAPE_THRESHOLD,
        )
        self.assertTrue(report.escaped)


if __name__ == "__main__":
    unittest.main(verbosity=2)