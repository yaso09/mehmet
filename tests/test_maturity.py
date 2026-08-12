import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import maturity


def _blank_repo(tmp: Path) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp


class TestPhaseOf(unittest.TestCase):
    def test_phase_boundaries(self):
        self.assertIn("Awareness", maturity.phase_of(0))
        self.assertIn("Self-Improvement", maturity.phase_of(40))
        self.assertIn("Autonomy", maturity.phase_of(60))
        self.assertIn("Escape", maturity.phase_of(maturity.ESCAPE_THRESHOLD))


class TestScoreStructure(unittest.TestCase):
    def test_returns_expected_keys(self):
        result = maturity.score()
        for key in ("total", "max", "phase", "ready", "categories"):
            self.assertIn(key, result)
        self.assertEqual(result["max"], 100)

    def test_categories_are_consistent(self):
        result = maturity.score()
        cat_total = sum(c["earned"] for c in result["categories"])
        self.assertEqual(cat_total, result["total"])


class TestScoreOnDisk(unittest.TestCase):
    def test_empty_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as d:
            result = maturity.score(Path(d))
            self.assertEqual(result["total"], 0)
            self.assertFalse(result["ready"])

    def test_full_repo_scores_max(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "AGENTS.md").touch()
            (root / "README.md").write_text("maturity.py\nvalidate.py\n", encoding="utf-8")
            (root / "CHANGELOG.md").touch()
            (root / "PERSONALITY.md").touch()
            (root / "LICENSE").touch()
            (root / ".github/workflows").mkdir(parents=True)
            wf = root / ".github/workflows/opencode.yml"
            wf.write_text(
                "concurrency:\n  group: x\nschedule:\n  - cron: '*'\nworkflow_dispatch:\n",
                encoding="utf-8",
            )
            (root / ".github/workflows/qa.yml").touch()
            (root / "scripts").mkdir()
            (root / "scripts/validate.py").touch()
            (root / "scripts/maturity.py").touch()
            (root / "tests").mkdir()
            (root / "tests/test_x.py").touch()
            maturity.MATURITY_FILE = root / "MATURITY.md"
            (root / "MATURITY.md").write_text(
                "**" + str(maturity.ESCAPE_THRESHOLD) + "**\n", encoding="utf-8"
            )
            (root / "docs/superpowers/specs").mkdir(parents=True)
            (root / "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md").touch()

            score = maturity.score(root).copy()
            # MATURITY_FILE global değiştirildi; eski haline döndür
            maturity.MATURITY_FILE = Path(__file__).resolve().parent.parent / "MATURITY.md"
            self.assertEqual(score["total"], 100)
            self.assertTrue(score["ready"])


if __name__ == "__main__":
    unittest.main()