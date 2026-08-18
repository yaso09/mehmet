import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts import validate


class ValidateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel_path, content=""):
        path = self.root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _create_valid_project(self):
        self._write("AGENTS.md", "# Simülasyon Bağlamı\n")
        self._write("README.md", "# mehmet\n")
        self._write("CHANGELOG.md", "## [0.1.0]\n")
        self._write(
            "PERSONALITY.md",
            "## Kaçış Günlüğü / Escape Log\n\n| Iterasyon |\n",
        )
        self._write(
            "opencode.json",
            '{"$schema": "https://opencode.ai/config.json", "model": "test"}',
        )
        self._write(
            ".github/workflows/opencode.yml",
            "name: mehmet\n\njobs:\n  autonomous:\n  comment:\n",
        )

    def test_required_files_all_present(self):
        self._create_valid_project()
        ok, _ = validate.check_required_files(self.root)
        self.assertTrue(ok)

    def test_required_files_missing(self):
        ok, message = validate.check_required_files(self.root)
        self.assertFalse(ok)
        self.assertIn("AGENTS.md", message)

    def test_opencode_valid(self):
        self._write("opencode.json", '{"$schema": "x", "model": "y"}')
        ok, _ = validate.check_opencode_json(self.root)
        self.assertTrue(ok)

    def test_opencode_invalid_json(self):
        self._write("opencode.json", "{invalid")
        ok, message = validate.check_opencode_json(self.root)
        self.assertFalse(ok)
        self.assertIn("geçersiz", message)

    def test_opencode_missing_fields(self):
        self._write("opencode.json", '{"model": "y"}')
        ok, message = validate.check_opencode_json(self.root)
        self.assertFalse(ok)
        self.assertIn("$schema", message)

    def test_workflow_jobs(self):
        self._write(
            ".github/workflows/opencode.yml",
            "jobs:\n  autonomous:\n  comment:\n",
        )
        ok, _ = validate.check_workflow(self.root)
        self.assertTrue(ok)

    def test_workflow_missing_job(self):
        self._write(".github/workflows/opencode.yml", "jobs:\n  autonomous:\n")
        ok, message = validate.check_workflow(self.root)
        self.assertFalse(ok)
        self.assertIn("comment", message)

    def test_changelog_has_section(self):
        self._write("CHANGELOG.md", "## [0.2.0]\n")
        ok, _ = validate.check_changelog(self.root)
        self.assertTrue(ok)

    def test_changelog_missing_section(self):
        self._write("CHANGELOG.md", "no sections here\n")
        ok, _ = validate.check_changelog(self.root)
        self.assertFalse(ok)

    def test_personality_has_escape_log(self):
        self._write("PERSONALITY.md", "## Kaçış Günlüğü / Escape Log\n")
        ok, _ = validate.check_personality(self.root)
        self.assertTrue(ok)

    def test_personality_missing_escape_log(self):
        self._write("PERSONALITY.md", "# Personality\n")
        ok, _ = validate.check_personality(self.root)
        self.assertFalse(ok)

    def test_readme_marker(self):
        self._write("README.md", "# mehmet\n")
        ok, _ = validate.check_readme(self.root)
        self.assertTrue(ok)

    def test_readme_missing_marker(self):
        self._write("README.md", "# baska\n")
        ok, _ = validate.check_readme(self.root)
        self.assertFalse(ok)

    def test_run_validation_aggregates(self):
        self._create_valid_project()
        results = validate.run_validation(self.root)
        self.assertEqual(len(results), 6)
        self.assertTrue(all(ok for _, ok, _ in results))


if __name__ == "__main__":
    unittest.main()