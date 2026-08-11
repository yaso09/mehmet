import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity

CHECK_WEIGHTS = {
    "docs": 20,
    "testing": 20,
    "tests": 15,
    "automation": 10,
    "escape": 15,
    "releases": 10,
    "config": 10,
}


class MaturityTests(unittest.TestCase):
    def test_all_check_functions_bounded(self):
        for name, fn in {
            "docs": maturity.check_docs,
            "testing": maturity.check_testing,
            "tests": maturity.check_tests,
            "automation": maturity.check_automation,
            "escape": maturity.check_escape,
            "releases": maturity.check_releases,
            "config": maturity.check_config,
        }.items():
            result = fn()
            self.assertIn("score", result, name)
            self.assertGreaterEqual(result["score"], 0, name)
            self.assertLessEqual(result["score"], CHECK_WEIGHTS[name], name)

    def test_core_docs_present(self):
        result = maturity.check_docs()
        self.assertEqual(result["score"], 20)
        self.assertEqual(result["missing"], [])

    def test_opencode_config_pins_model(self):
        result = maturity.check_config()
        self.assertEqual(result["score"], 10)


if __name__ == "__main__":
    unittest.main()
