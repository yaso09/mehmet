"""Tests for the maturity scoring system."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity  # noqa: E402


class MaturityEvaluateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write(self, rel: str, content: str = "") -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_empty_root_scores_zero_for_docs_and_tests(self):
        result = maturity.evaluate(self.root)
        self.assertEqual(result["total"], 0.0)
        self.assertFalse(result["escaped"])

    def test_full_project_escapes(self):
        self._write("README.md", "# Project\n")
        self._write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n")
        self._write("LICENSE", "MIT\n")
        self._write("AGENTS.md", "# Agents\n")
        self._write("PERSONALITY.md", "# Personality\n\n## Kaçış Günlüğü\n")
        self._write("opencode.json", '{"model": "test"}\n')
        self._write(".gitignore", "node_modules/\n")
        self._write("scripts/tool.py", "#!/usr/bin/env python3\nprint('hi')\n")
        self._write("tests/test_thing.py", "import unittest\n")
        self._write(".github/workflows/ci.yml", "name: ci\n")
        result = maturity.evaluate(self.root)
        self.assertGreaterEqual(result["total"], maturity.MATURITY_ESCAPE_THRESHOLD)
        self.assertTrue(result["escaped"])

    def test_documentation_fully_passing(self):
        self._write("README.md", "# Project\n")
        self._write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n")
        self._write("LICENSE", "MIT\n")
        self._write("AGENTS.md", "# Agents\n")
        self._write("PERSONALITY.md", "# Personality\n")
        result = maturity.evaluate(self.root)
        docs = next(d for d in result["dimensions"] if d["dimension"] == "documentation")
        self.assertEqual(docs["passed"], 5)
        self.assertEqual(docs["score"], 25.0)

    def test_changelog_without_entries_fails(self):
        self._write("CHANGELOG.md", "# Changelog\n")
        result = maturity.evaluate(self.root)
        docs = next(d for d in result["dimensions"] if d["dimension"] == "documentation")
        changelog = next(c for c in docs["checks"] if c["name"] == "CHANGELOG")
        self.assertFalse(changelog["pass"])

    def test_invalid_opencode_config_fails_automation(self):
        self._write("opencode.json", "not valid json{")
        result = maturity.evaluate(self.root)
        automation = next(d for d in result["dimensions"] if d["dimension"] == "automation")
        config = next(c for c in automation["checks"] if c["name"] == "opencode_config")
        self.assertFalse(config["pass"])

    def test_non_executable_scripts_fail_code_quality(self):
        self._write("scripts/tool.py", "print('hi')\n")
        self._write("README.md", "# Project\n")
        self._write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n")
        self._write("LICENSE", "MIT\n")
        self._write("AGENTS.md", "# Agents\n")
        self._write("PERSONALITY.md", "# Personality\n")
        self._write("opencode.json", '{"model": "test"}\n')
        self._write(".gitignore", "node_modules/\n")
        self._write("tests/test_thing.py", "import unittest\n")
        self._write(".github/workflows/ci.yml", "name: ci\n")
        result = maturity.evaluate(self.root)
        quality = next(d for d in result["dimensions"] if d["dimension"] == "code_quality")
        scripts = next(c for c in quality["checks"] if c["name"] == "scripts")
        self.assertFalse(scripts["pass"])


class MaturityCLITests(unittest.TestCase):
    def test_cli_bad_root_returns_2(self):
        code = maturity.main(["--root", "/nonexistent/path/xyz"])
        self.assertEqual(code, 2)

    def test_cli_json_escaped_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# P\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("# C\n\n## [1.0.0] - 2026-01-01\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# A\n", encoding="utf-8")
            (root / "PERSONALITY.md").write_text("# P\n\n## Kaçış Günlüğü\n", encoding="utf-8")
            (root / "opencode.json").write_text('{"model": "test"}\n', encoding="utf-8")
            (root / ".gitignore").write_text("x/\n", encoding="utf-8")
            (root / "scripts").mkdir(parents=True, exist_ok=True)
            (root / "scripts" / "tool.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            (root / "scripts" / "tool.py").chmod(0o755)
            (root / "tests").mkdir(parents=True, exist_ok=True)
            (root / "tests" / "test_thing.py").write_text("import unittest\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            code = maturity.main(["--json", "--root", str(root)])
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()