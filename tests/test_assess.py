import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import assess


class AssessTest(unittest.TestCase):
    def test_load_changelog_returns_text(self):
        self.assertTrue(hasattr(assess.load_changelog(), "startswith"))

    def test_run_checks_has_all_dimensions(self):
        results = assess.run_checks()
        self.assertIn("documentation", results)
        self.assertIn("change_tracking", results)
        self.assertIn("automation", results)
        self.assertIn("testing", results)
        self.assertIn("code_quality", results)

    def test_score_total_within_range(self):
        results = assess.run_checks()
        scored = assess.score(results)
        self.assertGreaterEqual(scored["total"], 0)
        self.assertLessEqual(scored["total"], 100)
        self.assertEqual(len(scored["catalog"]), 5)

    def test_score_reflects_missing_documentation(self):
        results = assess.run_checks()
        mutated = {
            "documentation": {"files": {"AGENTS.md": False, "README.md": False, "PERSONALITY.md": False}, "escape_log_present": False},
            "change_tracking": results["change_tracking"],
            "automation": results["automation"],
            "testing": results["testing"],
            "code_quality": results["code_quality"],
        }
        scored = assess.score(mutated)
        doc_score = next(i["score"] for i in scored["catalog"] if i["dimension"] == "documentation")
        self.assertEqual(doc_score, 0)
        self.assertLess(scored["total"], assess.score(results)["total"])

    def test_main_returns_zero_for_healthy_project(self):
        code = assess.main([])
        self.assertEqual(code, 0)

    def test_render_summary_contains_total(self):
        catalog = [{"dimension": "testing", "score": 20}]
        rendered = assess.render_summary(catalog, 20)
        self.assertIn("TOTAL SCORE: 20/100", rendered)


if __name__ == "__main__":
    unittest.main()