"""Direct unit tests for scripts/maturity.py scoring logic."""

import importlib.util
import json
import unittest
from pathlib import Path

from tests.helpers import PROJECT_ROOT

SCRIPT = PROJECT_ROOT / "scripts" / "maturity.py"


def load_maturity_module():
    spec = importlib.util.spec_from_file_location("maturity", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_config():
    return json.loads((PROJECT_ROOT / "maturity.json").read_text(encoding="utf-8"))


class TestMaturityChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_maturity_module()

    def test_check_files_passes_on_existing(self):
        ok, missing = self.mod.check_files(["README.md", "AGENTS.md"])
        self.assertTrue(ok)
        self.assertEqual(missing, [])

    def test_check_files_fails_on_missing(self):
        ok, missing = self.mod.check_files(["yok_boyle_bir_dosya.txt"])
        self.assertFalse(ok)
        self.assertEqual(len(missing), 1)

    def test_check_keywords_passes_and_fails(self):
        ok, _ = self.mod.check_keywords({"README.md": ["Kurulum"]})
        self.assertTrue(ok)
        ok, missing = self.mod.check_keywords({"README.md": ["BUANAHTARMEVCUTDEGIL"]})
        self.assertFalse(ok)
        self.assertTrue(missing)

    def test_check_version_matches_current(self):
        config = load_config()
        spec = {"current_version": config["current_version"]}
        ok, _ = self.mod.check_version(spec)
        self.assertTrue(ok)

    def test_check_version_mismatch(self):
        ok, missing = self.mod.check_version({"current_version": "99.99.99"})
        self.assertFalse(ok)
        self.assertTrue(missing)

    def test_check_command_passes(self):
        ok, _ = self.mod.check_command("python3 -c 'pass'")
        self.assertTrue(ok)

    def test_check_command_fails(self):
        ok, missing = self.mod.check_command("false")
        self.assertFalse(ok)
        self.assertTrue(missing)

    def test_check_secrets_detects_pattern(self):
        ok, missing = self.mod.check_secrets()
        self.assertTrue(ok)

    def test_secret_patterns_listed(self):
        self.assertTrue(self.mod.SECRET_PATTERNS)


class TestMaturityEvaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_maturity_module()
        cls.config = load_config()

    def test_criteria_weights_sum_to_100(self):
        total = sum(c["weight"] for c in self.config["criteria"])
        self.assertEqual(total, 100)

    def test_all_check_types_known(self):
        for c in self.config["criteria"]:
            self.assertIn(c["check"]["type"], self.mod.DISPATCH)

    def test_evaluate_returns_per_criterion(self):
        results = self.mod.evaluate(self.config["criteria"], is_subcheck=True)
        self.assertEqual(len(results), len(self.config["criteria"]))
        for r in results:
            self.assertIn("passed", r)
            self.assertIn("weight", r)

    def test_current_project_passes_all(self):
        results = self.mod.evaluate(self.config["criteria"], is_subcheck=True)
        passed = [r["id"] for r in results if not r["passed"]]
        self.assertEqual(passed, [], msg=f"Başarısız kriterler: {passed}")

    def test_escape_threshold_reachable(self):
        total = sum(c["weight"] for c in self.config["criteria"])
        self.assertLessEqual(
            self.config["escape_threshold"], total,
            "Eşik toplam ağırlığı aşamaz",
        )


if __name__ == "__main__":
    unittest.main()