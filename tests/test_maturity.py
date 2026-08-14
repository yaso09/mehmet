"""Unit tests for scripts/maturity.py."""

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import maturity  # noqa: E402


class MaturityHelpersTest(unittest.TestCase):
    def test_read_text_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(maturity.read_text(pathlib.Path(tmp), "nope.md"), "")

    def test_read_text_returns_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "a.txt").write_text("hello", encoding="utf-8")
            self.assertEqual(maturity.read_text(root, "a.txt"), "hello")

    def test_is_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "opencode.json").write_text('{"model": "x"}', encoding="utf-8")
            self.assertTrue(maturity.is_valid_json(root))

    def test_is_valid_json_rejects_garbage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "opencode.json").write_text("not json", encoding="utf-8")
            self.assertFalse(maturity.is_valid_json(root))

    def test_count_versions(self):
        content = "# Changelog\n\n## [1.0.0] - 2026-01-01\n## [0.9.0] - 2025-12-01\n"
        self.assertEqual(maturity.count_versions(content), 2)

    def test_has_escape_log(self):
        self.assertTrue(maturity.has_escape_log("## Kaçış Günlüğü\n"))
        self.assertTrue(maturity.has_escape_log("## Escape Log\n"))
        self.assertFalse(maturity.has_escape_log("nothing here"))

    def test_has_section(self):
        self.assertTrue(maturity.has_section("## Özellikler", "Özellikler"))
        self.assertFalse(maturity.has_section("## Other", "Özellikler"))

    def test_workflow_has(self):
        self.assertTrue(maturity.workflow_has("a\nb\nc", "a", "c"))
        self.assertFalse(maturity.workflow_has("a\nb", "a", "z"))


class MaturityReportTest(unittest.TestCase):
    def _make_root(self) -> pathlib.Path:
        tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(tmp.name)
        (root / "AGENTS.md").write_text("# Simülasyon\n\n## Kurallar\n", encoding="utf-8")
        (root / "README.md").write_text(
            "# mehmet\n\n## Özellikler\n\n## Kurulum\n\n## Lisans\n", encoding="utf-8"
        )
        (root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.2.0] - 2026-07-04\n\n### Added\n- x\n\n## [0.1.0] - 2026-07-04\n\n### Added\n- y\n",
            encoding="utf-8",
        )
        (root / "PERSONALITY.md").write_text(
            "## Evolution\n\n## Kaçış Günlüğü\n", encoding="utf-8"
        )
        (root / "opencode.json").write_text('{"model": "x"}', encoding="utf-8")
        (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        (root / "LICENSE").write_text("GPLv3\n", encoding="utf-8")
        wf_dir = root / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "opencode.yml").write_text(
            "name: mehmet\n\n"
            "concurrency:\n  group: test\n\n"
            "on:\n  schedule:\n    - cron: \"*/10 * * * *\"\n"
            "  issues:\n    types: [opened]\n"
            "  pull_request:\n    types: [opened]\n"
            "  issue_comment:\n    types: [created]\n"
            "  pull_request_review_comment:\n    types: [created]\n"
            "  workflow_dispatch:\n\n"
            "jobs:\n  autonomous:\n    permissions:\n      contents: write\n"
            "    steps:\n      - uses: actions/checkout@v6\n"
            "        with:\n          persist-credentials: false\n"
            "      - uses: anomalyco/opencode/github@latest\n"
            "        with:\n          prompt: |\n            simülasyon\n\n"
            "  comment:\n    if: github.event_name == 'issue_comment'\n    runs-on: ubuntu-latest\n",
            encoding="utf-8",
        )
        (wf_dir / "validate.yml").write_text("name: validate\non: [push]\n", encoding="utf-8")
        scripts = root / "scripts"
        scripts.mkdir()
        (scripts / "maturity.py").write_text("escape\n", encoding="utf-8")
        tests = root / "tests"
        tests.mkdir()
        (tests / "test_x.py").write_text("def test_x(): pass\n", encoding="utf-8")
        self._tmp = tmp
        return root

    def tearDown(self):
        if hasattr(self, "_tmp"):
            self._tmp.cleanup()

    def test_full_score(self):
        report = maturity.build_report(self._make_root())
        self.assertEqual(report["score"], report["max"])

    def test_empty_root_scores_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = maturity.build_report(pathlib.Path(tmp))
            self.assertEqual(report["score"], 0)


if __name__ == "__main__":
    unittest.main()