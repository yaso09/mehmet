import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md"]


class ValidateTests(unittest.TestCase):
    def test_required_files_exist(self):
        for name in REQUIRED:
            f = ROOT / name
            self.assertTrue(f.is_file(), f"{name} missing")
            self.assertGreater(f.stat().st_size, 0, f"{name} is empty")

    def test_changelog_has_versions(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        headings = [line for line in text.splitlines() if line.startswith("## [")]
        self.assertGreaterEqual(len(headings), 2, "need at least two releases")

    def test_workflows_exist(self):
        wf = ROOT / ".github" / "workflows"
        self.assertTrue((wf / "opencode.yml").is_file())
        self.assertTrue((wf / "validate.yml").is_file())


if __name__ == "__main__":
    unittest.main()
