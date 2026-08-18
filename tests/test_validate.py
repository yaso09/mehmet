"""Tests for scripts/validate.py."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import validate  # noqa: E402


def make_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("# Simülasyon Bağlamı\n\nKurallar.\n", encoding="utf-8")
    (root / "README.md").write_text(
        "# mehmet\n\n## Özellikler\n\n## Kurulum\n\n## Lisans\n", encoding="utf-8"
    )
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [0.3.0] - 2026-08-18\n\n### Added\n- stuff\n", encoding="utf-8"
    )
    (root / "PERSONALITY.md").write_text(
        "# Personality\n\n## Kaçış Günlüğü / Escape Log\n\n| Iterasyon | Tarih | İlerleme |\n| --- | --- | --- |\n",
        encoding="utf-8",
    )
    (root / "opencode.json").write_text(json.dumps({"model": "opencode/test"}), encoding="utf-8")
    (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    (root / "scripts").mkdir(exist_ok=True)
    (root / "scripts" / "validate.py").write_text("# validate\n", encoding="utf-8")
    (root / "scripts" / "maturity.py").write_text("# maturity\n", encoding="utf-8")
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests" / "test_x.py").write_text("# test\n", encoding="utf-8")
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "note.md").write_text("# note\n", encoding="utf-8")
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    (wf / "opencode.yml").write_text(
        "name: mehmet\n"
        "on:\n"
        "  schedule:\n"
        "    - cron: '*/10 * * * *'\n"
        "  issues:\n"
        "    types: [opened]\n"
        "  pull_request:\n"
        "    types: [opened]\n"
        "  issue_comment:\n"
        "    types: [created]\n"
        "  pull_request_review_comment:\n"
        "    types: [created]\n"
        "  workflow_dispatch:\n"
        "jobs:\n"
        "  autonomous:\n"
        "    runs-on: ubuntu-latest\n",
        encoding="utf-8",
    )
    (wf / "ci.yml").write_text("name: ci\n", encoding="utf-8")


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_repo(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, name):
        for fn_name, fn in validate.ALL_CHECKS:
            if fn_name == name:
                return fn(self.root)
        raise KeyError(name)

    def test_all_checks_pass_on_good_repo(self):
        for name, _ in validate.ALL_CHECKS:
            with self.subTest(check=name):
                ok, msg = self.check(name)
                self.assertTrue(ok, msg)

    def test_missing_required_file_fails(self):
        (self.root / "README.md").unlink()
        ok, _ = self.check("required files")
        self.assertFalse(ok)

    def test_invalid_json_fails(self):
        (self.root / "opencode.json").write_text("{not json", encoding="utf-8")
        ok, _ = self.check("opencode.json valid JSON")
        self.assertFalse(ok)

    def test_no_changelog_versions_fails(self):
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\nno versions\n", encoding="utf-8")
        ok, _ = self.check("changelog version headers")
        self.assertFalse(ok)

    def test_missing_readme_section_fails(self):
        (self.root / "README.md").write_text("# mehmet\n\n## Özellikler\n", encoding="utf-8")
        ok, _ = self.check("readme sections")
        self.assertFalse(ok)

    def test_missing_escape_log_fails(self):
        (self.root / "PERSONALITY.md").write_text("# Personality\n\nNo log here.\n", encoding="utf-8")
        ok, _ = self.check("escape log")
        self.assertFalse(ok)

    def test_no_tests_fails(self):
        for f in (self.root / "tests").iterdir():
            f.unlink()
        ok, _ = self.check("tests present")
        self.assertFalse(ok)

    def test_missing_ci_fails(self):
        (self.root / ".github" / "workflows" / "ci.yml").unlink()
        ok, _ = self.check("CI workflow present")
        self.assertFalse(ok)

    def test_missing_scripts_fails(self):
        (self.root / "scripts" / "maturity.py").unlink()
        ok, _ = self.check("scripts present")
        self.assertFalse(ok)

    def test_missing_workflow_schedule_fails(self):
        path = self.root / ".github" / "workflows" / "opencode.yml"
        path.write_text("name: mehmet\non:\n  issues:\n    types: [opened]\n", encoding="utf-8")
        ok, _ = self.check("workflow schedule")
        self.assertFalse(ok)

    def test_missing_workflow_event_fails(self):
        path = self.root / ".github" / "workflows" / "opencode.yml"
        text = path.read_text(encoding="utf-8").replace("workflow_dispatch", "nothing")
        path.write_text(text, encoding="utf-8")
        ok, _ = self.check("workflow event triggers")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
