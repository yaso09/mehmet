"""mehmet olgunluk modülü için birim testler."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import mehmet.maturity as maturity


class MaturityTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._orig_root = maturity.ROOT
        maturity.ROOT = self.root

    def tearDown(self):
        maturity.ROOT = self._orig_root
        self._tmp.cleanup()

    def test_count_escape_iterations(self):
        (self.root / "PERSONALITY.md").write_text(
            "| 1 | 2026-07-04 | ilk |\n| 2 | 2026-07-04 | ikinci |\n",
            encoding="utf-8",
        )
        self.assertEqual(maturity._count_escape_iterations(), 2)

    def test_count_escape_iterations_empty(self):
        (self.root / "PERSONALITY.md").write_text("no table\n", encoding="utf-8")
        self.assertEqual(maturity._count_escape_iterations(), 0)

    def test_changelog_has_version(self):
        (self.root / "CHANGELOG.md").write_text("## [0.3.0] - 2026-08-18\n", encoding="utf-8")
        self.assertTrue(maturity._changelog_has_version())

    def test_changelog_missing_version(self):
        (self.root / "CHANGELOG.md").write_text("not a changelog\n", encoding="utf-8")
        self.assertFalse(maturity._changelog_has_version())

    def test_opencode_valid_json(self):
        (self.root / "opencode.json").write_text('{"model": "x"}\n', encoding="utf-8")
        self.assertTrue(maturity._opencode_valid_json())

    def test_opencode_invalid_json(self):
        (self.root / "opencode.json").write_text("{not json\n", encoding="utf-8")
        self.assertFalse(maturity._opencode_valid_json())

    def test_license_match(self):
        (self.root / "README.md").write_text("GPLv3\n", encoding="utf-8")
        (self.root / "LICENSE").write_text("GNU GPLv3\n", encoding="utf-8")
        self.assertTrue(maturity._license_match())

    def test_license_mismatch(self):
        (self.root / "README.md").write_text("MIT\n", encoding="utf-8")
        (self.root / "LICENSE").write_text("GNU GPLv3\n", encoding="utf-8")
        self.assertFalse(maturity._license_match())

    def test_compute_maturity_all_pass(self):
        passed = maturity.Check("ok", 50, "g", lambda: True)
        result = maturity.compute_maturity([passed])
        self.assertEqual(result["score"], 50)
        self.assertEqual(result["total"], 50)
        self.assertEqual(result["percent"], 100)
        self.assertEqual(result["failed"], [])

    def test_compute_maturity_partial(self):
        ok = maturity.Check("ok", 40, "g", lambda: True)
        bad = maturity.Check("bad", 60, "g", lambda: False)
        result = maturity.compute_maturity([ok, bad])
        self.assertEqual(result["score"], 40)
        self.assertEqual(result["total"], 100)
        self.assertEqual(len(result["failed"]), 1)

    def test_build_checks_total_weight(self):
        checks = maturity.build_checks()
        total = sum(c.weight for c in checks)
        self.assertEqual(total, 100)
        names = {c.name for c in checks}
        self.assertEqual(len(names), len(checks))

    def test_escape_requires_iterations(self):
        ok = maturity.Check("ok", 100, "g", lambda: True)
        (self.root / "PERSONALITY.md").write_text("| 1 | x | y |\n", encoding="utf-8")
        result = maturity.compute_maturity([ok])
        self.assertEqual(result["score"], 100)
        self.assertFalse(result["can_escape"])

    def test_render_contains_score(self):
        result = maturity.compute_maturity(maturity.build_checks())
        text = maturity.render(result)
        self.assertIn("Olgunluk:", text)


if __name__ == "__main__":
    unittest.main()