"""Unit tests for the mehmet maturity scoring engine."""

from __future__ import annotations

import os
import tempfile
import unittest

from mehmet.maturity import CATEGORIES, escape_ready, evaluate, score_project

FILE_PATHS = {
    "README.md",
    "CHANGELOG.md",
    "AGENTS.md",
    "PERSONALITY.md",
    "LICENSE",
    "docs/ARCHITECTURE.md",
    "tests/test_maturity.py",
    "Makefile",
    ".github/workflows/ci.yml",
    ".github/workflows/opencode.yml",
    "src/mehmet/maturity.py",
    ".editorconfig",
    ".gitignore",
    "opencode.json",
}


def _make_project(root: str) -> None:
    """Create a project satisfying every maturity check."""
    for category in CATEGORIES:
        for path in category.paths:
            target = os.path.join(root, path)
            if path in FILE_PATHS:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as handle:
                    handle.write("")
            else:
                os.makedirs(target, exist_ok=True)


class EvaluateTest(unittest.TestCase):
    def test_empty_project_scores_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            total, results = evaluate(tmp)
            self.assertEqual(total, 0.0)
            self.assertEqual(len(results), len(CATEGORIES))
            for cs in results:
                self.assertEqual(cs.score, 0.0)
                self.assertEqual(cs.present, [])

    def test_full_project_scores_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _make_project(tmp)
            total, results = evaluate(tmp)
            self.assertAlmostEqual(total, 1.0)
            for cs in results:
                self.assertEqual(cs.score, 1.0)
                self.assertEqual(cs.missing, [])
                self.assertGreaterEqual(len(cs.present), 1)

    def test_partial_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "tests"), exist_ok=True)
            total, results = evaluate(tmp)
            by_name = {cs.category.name: cs for cs in results}
            self.assertEqual(by_name["test-infrastructure"].score, 0.25)
            self.assertEqual(by_name["documentation"].score, 0.0)
            self.assertAlmostEqual(total, 0.0625)

    def test_custom_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _make_project(tmp)
            self.assertEqual(score_project(tmp), 1.0)


class EscapeReadyTest(unittest.TestCase):
    def test_ready_at_threshold(self) -> None:
        self.assertTrue(escape_ready(0.8, 80.0))
        self.assertTrue(escape_ready(1.0, 80.0))

    def test_not_ready_below_threshold(self) -> None:
        self.assertFalse(escape_ready(0.79, 80.0))
        self.assertFalse(escape_ready(0.0, 80.0))

    def test_default_threshold_is_eighty(self) -> None:
        self.assertFalse(escape_ready(0.799))
        self.assertTrue(escape_ready(0.8))

    def test_custom_threshold(self) -> None:
        self.assertTrue(escape_ready(0.5, 50.0))
        self.assertFalse(escape_ready(0.49, 50.0))


class CategoryWeightsTest(unittest.TestCase):
    def test_weights_sum_to_one(self) -> None:
        self.assertAlmostEqual(sum(c.weight for c in CATEGORIES), 1.0)

    def test_names_are_unique(self) -> None:
        names = [c.name for c in CATEGORIES]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()