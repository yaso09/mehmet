import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import validate


class TestJSONValidation(unittest.TestCase):
    def test_valid_json_passes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "a.json"
            path.write_text('{"model": "x"}', encoding="utf-8")
            self.assertIsNone(validate.validate_one_json(path))

    def test_invalid_json_reports(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "a.json"
            path.write_text("{broken", encoding="utf-8")
            self.assertIsNotNone(validate.validate_one_json(path))


class TestYAMLValidation(unittest.TestCase):
    def test_valid_yaml_passes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "w.yaml"
            path.write_text("name: x\non: {}\n", encoding="utf-8")
            self.assertIsNone(validate.validate_one_yaml(path))

    def test_invalid_yaml_reports(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "w.yaml"
            path.write_text("a: [unclosed", encoding="utf-8")
            self.assertIsNotNone(validate.validate_one_yaml(path))


class TestRequiredFiles(unittest.TestCase):
    def test_missing_files_detected(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIn("README.md", validate.validate_required(Path(d)))

    def test_all_present(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for rel in validate.REQUIRED:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            self.assertEqual(validate.validate_required(root), [])


class TestSecrets(unittest.TestCase):
    def test_finds_hardcoded_key(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "config.json"
            path.write_text('{"OPENCODE_API_KEY": "sk-abcdefghij1234567890"}', encoding="utf-8")
            self.assertIn(str(path), validate.find_secrets(Path(d)))

    def test_no_secrets_in_clean_tree(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "notes.md"
            path.write_text("merhaba dünya", encoding="utf-8")
            self.assertEqual(validate.find_secrets(Path(d)), [])


class TestWorkflowSecret(unittest.TestCase):
    def test_secret_reference_ok(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            wf = root / ".github/workflows/opencode.yml"
            wf.parent.mkdir(parents=True)
            wf.write_text("env:\n  OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}\n", encoding="utf-8")
            self.assertIsNone(validate.validate_workflow_secret(root))

    def test_missing_secret_reference_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            wf = root / ".github/workflows/opencode.yml"
            wf.parent.mkdir(parents=True)
            wf.write_text("name: x\non: {}\n", encoding="utf-8")
            self.assertIsNotNone(validate.validate_workflow_secret(root))


if __name__ == "__main__":
    unittest.main()