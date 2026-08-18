import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate  # noqa: E402


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.r = Path(self.root)

    def write(self, rel, content):
        path = self.r / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def build_valid_tree(self):
        for name in validate.REQUIRED_FILES:
            self.write(name, "x")
        self.write(
            "opencode.json",
            '{"model": "opencode/deepseek-v4-flash-free"}',
        )
        self.write(
            ".github/workflows/opencode.yml",
            "name: mehmet\non:\n  workflow_dispatch:\n",
        )

    def test_valid_tree_returns_no_errors(self):
        self.build_valid_tree()
        self.assertEqual(validate.validate(self.root), [])

    def test_missing_file_reported(self):
        self.build_valid_tree()
        (self.r / "README.md").unlink()
        errors = validate.validate(self.root)
        self.assertTrue(any("README.md" in e for e in errors))

    def test_invalid_json_reported(self):
        self.build_valid_tree()
        self.write("opencode.json", "{broken")
        errors = validate.validate(self.root)
        self.assertTrue(any("opencode.json" in e for e in errors))


if __name__ == "__main__":
    unittest.main()