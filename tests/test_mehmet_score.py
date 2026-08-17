import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from mehmet_score import CRITERIA, EscapeScore


class TestEscapeScore(unittest.TestCase):
    def setUp(self):
        self.scorer = EscapeScore()

    def test_score_is_bounded(self):
        score = self.scorer.compute()
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_report_shape(self):
        self.scorer.compute()
        report = self.scorer.report()
        for key in ("score", "threshold", "escaped", "passed", "total",
                    "config_valid", "criteria"):
            self.assertIn(key, report)
        self.assertEqual(report["total"], len(CRITERIA))

    def test_passed_matches_score(self):
        self.scorer.compute()
        report = self.scorer.report()
        expected = round((report["passed"] / report["total"]) * 100, 2)
        self.assertEqual(report["score"], expected)

    def test_core_files_present(self):
        for name in ("AGENTS.md", "PERSONALITY.md", "CHANGELOG.md", "README.md"):
            self.assertTrue((ROOT / name).exists(), f"{name} bulunamadı")

    def test_script_is_importable_and_runnable(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "mehmet_score.py"), "--score"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(0 <= float(result.stdout.strip()) <= 100)


if __name__ == "__main__":
    unittest.main()
