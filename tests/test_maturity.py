import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts import maturity


class MaturityTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel_path, content=""):
        path = self.root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_score_config_missing(self):
        score, note = maturity.score_config(self.root)
        self.assertEqual(score, 0)
        self.assertIn("yok", note)

    def test_score_config_full(self):
        self._write(
            "opencode.json",
            '{"$schema": "x", "model": "y", "toolTimeout": 1, "enable": true, "skip": false}',
        )
        score, _ = maturity.score_config(self.root)
        self.assertEqual(score, 20)

    def test_score_config_invalid(self):
        self._write("opencode.json", "{bad")
        score, note = maturity.score_config(self.root)
        self.assertEqual(score, 0)
        self.assertIn("geçersiz", note)

    def test_score_workflow_missing(self):
        score, note = maturity.score_workflow(self.root)
        self.assertEqual(score, 0)
        self.assertIn("yok", note)

    def test_score_workflow_full(self):
        self._write(
            ".github/workflows/opencode.yml",
            "name: mehmet\n\nschedule: x\n\njobs:\n  autonomous:\n  comment:\n\nconcurrency: x\n\nOPENCODE_API_KEY: x\n\nworkflow_dispatch: x\n",
        )
        score, _ = maturity.score_workflow(self.root)
        self.assertEqual(score, 20)

    def test_score_docs_full(self):
        for name in ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md"]:
            self._write(name, "x")
        self._write("docs/guide.md", "x")
        score, _ = maturity.score_docs(self.root)
        self.assertEqual(score, 20)

    def test_score_tests(self):
        self._write("tests/test_a.py", "x")
        self._write("tests/test_b.py", "x")
        score, note = maturity.score_tests(self.root)
        self.assertEqual(score, 12)
        self.assertIn("2", note)

    def test_score_tests_none(self):
        score, note = maturity.score_tests(self.root)
        self.assertEqual(score, 0)
        self.assertIn("yok", note)

    def test_score_automation_full(self):
        self._write("scripts/a.py", "x")
        self._write("Makefile", "all:")
        self._write(".github/workflows/ci.yml", "on: push")
        self._write("MATURITY.md", "report")
        score, _ = maturity.score_automation(self.root)
        self.assertEqual(score, 20)

    def test_compute_score_clamps_and_totals(self):
        self._write(
            "opencode.json",
            '{"$schema": "x", "model": "y", "toolTimeout": 1, "enable": true, "skip": false}',
        )
        self._write(
            ".github/workflows/opencode.yml",
            "name: mehmet\n\nschedule: x\n\njobs:\n  autonomous:\n  comment:\n\nconcurrency: x\n\nOPENCODE_API_KEY: x\n\nworkflow_dispatch: x\n",
        )
        self._write("AGENTS.md", "x")
        self._write("README.md", "x")
        self._write("CHANGELOG.md", "x")
        self._write("PERSONALITY.md", "x")
        self._write("docs/d.md", "x")
        self._write("tests/test_a.py", "x")
        self._write("tests/test_b.py", "x")
        self._write("tests/test_c.py", "x")
        self._write("tests/test_d.py", "x")
        self._write("scripts/a.py", "x")
        self._write("Makefile", "all:")
        self._write(".github/workflows/ci.yml", "on: push")
        self._write("MATURITY.md", "report")
        rows, total = maturity.compute_score(self.root)
        self.assertEqual(total, 100)
        self.assertEqual(len(rows), 5)

    def test_escape_threshold_constant(self):
        self.assertEqual(maturity.ESCAPE_THRESHOLD, 90)


if __name__ == "__main__":
    unittest.main()