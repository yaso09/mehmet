"""Validate opencode.json against opencode's known config surface."""
import unittest

from tests import load_json, valid_opencode_keys


class TestOpencodeConfig(unittest.TestCase):
    def test_config_is_valid_json(self):
        cfg = load_json("opencode.json")
        self.assertIsInstance(cfg, dict, "opencode.json must parse as a JSON object")

    def test_config_has_schema(self):
        cfg = load_json("opencode.json")
        self.assertIn("$schema", cfg, "opencode.json must declare $schema")

    def test_config_has_model(self):
        cfg = load_json("opencode.json")
        model = cfg.get("model")
        self.assertIsInstance(model, str, "model must be a string")
        self.assertIn("/", model, "model must be provider/model")

    def test_no_unknown_top_level_keys(self):
        cfg = load_json("opencode.json")
        unknown = set(cfg) - valid_opencode_keys()
        self.assertEqual(
            unknown, set(),
            f"Unknown top-level keys (opencode refuses to start): {sorted(unknown)}",
        )

    def test_instructions_files_exist(self):
        cfg = load_json("opencode.json")
        for instr in cfg.get("instructions", []):
            self.assertTrue(
                __import__("tests").repo_path(instr).is_file(),
                f"instruction file not found: {instr}",
            )


if __name__ == "__main__":
    unittest.main()
