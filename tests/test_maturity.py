import tempfile
import unittest
from pathlib import Path

from scripts.maturity import assess, ESCAPE_THRESHOLD


def _mini_project() -> Path:
    tmp = Path(tempfile.mkdtemp())
    (tmp / ".github/workflows").mkdir(parents=True)
    (tmp / "tests").mkdir()
    (tmp / "scripts").mkdir()
    (tmp / "docs").mkdir()
    wf = tmp / ".github/workflows/opencode.yml"
    wf.write_text("name: mehmet\non:\n  schedule:\n    - cron: '*/10 * * * *'\n")
    (tmp / "README.md").write_text("x" * 300)
    (tmp / "CHANGELOG.md").write_text("# Changelog\n")
    (tmp / "AGENTS.md").write_text("# Agents\n")
    (tmp / "VERSION").write_text("1.0.0\n")
    (tmp / ".gitignore").write_text("node_modules/\n")
    (tmp / "LICENSE").write_text("GPLv3\n")
    return tmp


class MaturityTest(unittest.TestCase):
    def test_score_bounds(self):
        report = assess()
        self.assertGreaterEqual(report["score"], 0)
        self.assertLessEqual(report["score"], 100)

    def test_ready_requires_threshold(self):
        report = assess()
        self.assertEqual(report["ready"], report["score"] >= ESCAPE_THRESHOLD
                         and report["mandatory_satisfied"])

    def test_empty_project_scores_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = assess(Path(tmp))
            self.assertLess(report["score"], ESCAPE_THRESHOLD)
            self.assertFalse(report["ready"])

    def test_rich_project_scores_high(self):
        root = _mini_project()
        report = assess(root)
        self.assertGreater(report["score"], 0)

    def test_mandatory_workflow_security(self):
        root = _mini_project()
        wf = root / ".github/workflows/opencode.yml"
        wf.write_text(wf.read_text() + "permissions:\n  id-token: write\n")
        report = assess(root)
        self.assertFalse(report["mandatory_satisfied"])


if __name__ == "__main__":
    unittest.main()