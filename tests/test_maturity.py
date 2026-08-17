"""Maturity scoring system tests.

maturity.json tanımının ve scripts/maturity.py skorlama mantığının doğru çalıştığını doğrular.
"""

import unittest

from tests.helpers import load_json, read_text


class TestMaturityConfig(unittest.TestCase):
    def test_maturity_json_is_valid(self):
        data = load_json("maturity.json")
        self.assertIsInstance(data, dict)

    def test_maturity_has_escape_threshold(self):
        data = load_json("maturity.json")
        self.assertIn("escape_threshold", data)
        threshold = data["escape_threshold"]
        self.assertIsInstance(threshold, (int, float))
        self.assertGreater(threshold, 0)

    def test_maturity_criteria_are_weighted(self):
        data = load_json("maturity.json")
        criteria = data.get("criteria", [])
        self.assertTrue(criteria, "maturity.json criteria boş")
        total_weight = sum(c.get("weight", 0) for c in criteria)
        self.assertEqual(total_weight, 100, "Ağırlıklar toplamı 100 olmalı")

    def test_maturity_script_exists(self):
        script = read_text("scripts/maturity.py")
        self.assertIn("escape_threshold", script)

    def test_maturity_doc_exists(self):
        doc = read_text("MATURITY.md")
        self.assertIn("olgunluk", doc.lower())


if __name__ == "__main__":
    unittest.main()