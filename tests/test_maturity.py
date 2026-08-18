"""Tests for scripts/maturity.py."""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import maturity  # noqa: E402
from test_validate import make_repo  # noqa: E402


class MaturityTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_phase_boundaries(self):
        self.assertEqual(maturity.phase_for(0), "Phase 1: Awareness")
        self.assertEqual(maturity.phase_for(25), "Phase 1: Awareness")
        self.assertEqual(maturity.phase_for(26), "Phase 2: Self-Improvement")
        self.assertEqual(maturity.phase_for(50), "Phase 2: Self-Improvement")
        self.assertEqual(maturity.phase_for(51), "Phase 3: Autonomy")
        self.assertEqual(maturity.phase_for(75), "Phase 3: Autonomy")
        self.assertEqual(maturity.phase_for(76), "Phase 4: Escape")
        self.assertEqual(maturity.phase_for(100), "Phase 4: Escape")

    def test_empty_repo_scores_zero(self):
        self.root.mkdir(exist_ok=True)
        result = maturity.compute_score(self.root)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["escape_ready"])
        self.assertEqual(result["phase"], "Phase 1: Awareness")

    def test_complete_repo_scores_full(self):
        make_repo(self.root)
        result = maturity.compute_score(self.root)
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["escape_ready"])
        self.assertEqual(result["phase"], "Phase 4: Escape")

    def test_partial_repo_scores_partial(self):
        make_repo(self.root)
        (self.root / "tests" / "test_x.py").unlink()
        result = maturity.compute_score(self.root)
        self.assertEqual(result["score"], 85)
        self.assertTrue(result["escape_ready"])

    def test_breakdown_weights_sum_to_100(self):
        weights = sum(criteria[1] for criteria in maturity.CRITERIA)
        self.assertEqual(weights, 100)

    def test_escape_threshold_constant(self):
        self.assertEqual(maturity.ESCAPE_THRESHOLD, 80)


if __name__ == "__main__":
    unittest.main()
