"""Validate PERSONALITY.md escape log integrity."""
import re
import unittest

from tests import read_text


class TestPersonality(unittest.TestCase):
    def setUp(self):
        self.text = read_text("PERSONALITY.md")
        self.assertIsNotNone(self.text, "PERSONALITY.md missing")

    def test_has_escape_log(self):
        self.assertIn("Kaçış Günlüğü", self.text)

    def test_escape_log_iterations_are_sequential(self):
        rows = re.findall(
            r"^\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", self.text, flags=re.M
        )
        self.assertTrue(rows, "escape log has no data rows")
        nums = [int(n) for n, _ in rows]
        self.assertEqual(nums, sorted(nums), "iteration numbers must be increasing")
        for i, n in enumerate(nums, start=1):
            self.assertEqual(n, i, f"iteration sequence broken at {n}")

    def test_each_iteration_has_progress(self):
        rows = re.findall(
            r"^\|\s*(\d+)\s*\|\s*[^|]+\s*\|\s*([^|]+)\s*\|$", self.text, flags=re.M
        )
        for num, progress in rows:
            self.assertTrue(progress.strip(), f"iteration {num} has empty progress")


if __name__ == "__main__":
    unittest.main()