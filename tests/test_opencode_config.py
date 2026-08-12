"""Validate opencode.json configuration."""

import unittest

from tests.helpers import ROOT, load_json


class TestOpenCodeConfig(unittest.TestCase):

    def setUp(self):
        self.config = load_json("opencode.json")

    def test_json_is_valid(self):
        self.assertTrue(ROOT.joinpath("opencode.json").exists())
        self.assertIsInstance(self.config, dict)

    def test_has_schema(self):
        self.assertIn("$schema", self.config)
        self.assertEqual(
            self.config["$schema"],
            "https://opencode.ai/config.json",
        )

    def test_has_model(self):
        self.assertIn("model", self.config)
        self.assertTrue(self.config["model"].startswith("opencode/"))


if __name__ == "__main__":
    unittest.main()