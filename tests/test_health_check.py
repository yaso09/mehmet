import json
import tempfile
import unittest
from pathlib import Path

from scripts.health_check import (
    ESCAPE_ROW_RE,
    SEMVER_RE,
    check_changelog,
    check_escape_log,
    check_opencode_json,
    check_readme,
    check_required_files,
    check_version,
    check_workflows,
)


def make_project(root: Path, version: str = "0.3.0") -> None:
    (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")
    (root / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## [{version}] - 2026-08-20\n", encoding="utf-8"
    )
    (root / "PERSONALITY.md").write_text(
        "# Personality\n\n## Escape Log\n\n"
        "| Iterasyon | Tarih | İlerleme |\n"
        "|-----------|-------|----------|\n"
        "| 1 | 2026-08-20 | First entry |\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        f"# mehmet\n\nCurrent version: {version}\n", encoding="utf-8"
    )
    (root / "LICENSE").write_text("GPLv3\n", encoding="utf-8")
    (root / "VERSION").write_text(version + "\n", encoding="utf-8")
    (root / "opencode.json").write_text(
        json.dumps({"model": "opencode/deepseek-v4-flash-free"}), encoding="utf-8"
    )
    workflows = root / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "opencode.yml").write_text(
        "name: mehmet\non: [push]\njobs:\n  autonomous:\n    runs-on: ubuntu-latest\n",
        encoding="utf-8",
    )
    (workflows / "ci.yml").write_text(
        "name: ci\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
        encoding="utf-8",
    )


class HealthCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def assert_any_contains(self, fragment: str, items: list) -> None:
        self.assertTrue(
            any(fragment in item for item in items),
            f"{fragment!r} not found in any of {items}",
        )

    def test_required_files_pass(self) -> None:
        make_project(self.root)
        self.assertEqual(check_required_files(self.root), [])

    def test_required_files_missing(self) -> None:
        self.assert_any_contains("Missing required file: AGENTS.md", check_required_files(self.root))

    def test_opencode_json_valid(self) -> None:
        make_project(self.root)
        self.assertEqual(check_opencode_json(self.root), [])

    def test_opencode_json_missing_key(self) -> None:
        make_project(self.root)
        (self.root / "opencode.json").write_text("{}", encoding="utf-8")
        self.assert_any_contains(
            "opencode.json is missing required key: model",
            check_opencode_json(self.root),
        )

    def test_opencode_json_invalid(self) -> None:
        make_project(self.root)
        (self.root / "opencode.json").write_text("{not json", encoding="utf-8")
        self.assertTrue(check_opencode_json(self.root))

    def test_version_semver(self) -> None:
        make_project(self.root)
        self.assertEqual(check_version(self.root), [])

    def test_version_invalid(self) -> None:
        make_project(self.root, version="abc")
        self.assert_any_contains("VERSION is not semver-compatible", check_version(self.root))

    def test_changelog_matches_version(self) -> None:
        make_project(self.root)
        self.assertEqual(check_changelog(self.root), [])

    def test_changelog_stale(self) -> None:
        make_project(self.root)
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.1.0] - 2026-07-04\n", encoding="utf-8"
        )
        self.assert_any_contains(
            "CHANGELOG.md has no section for current version",
            check_changelog(self.root),
        )

    def test_readme_matches_version(self) -> None:
        make_project(self.root)
        self.assertEqual(check_readme(self.root), [])

    def test_readme_stale(self) -> None:
        make_project(self.root)
        (self.root / "README.md").write_text("# mehmet\n", encoding="utf-8")
        self.assert_any_contains("README.md does not reference current version", check_readme(self.root))

    def test_workflows_valid(self) -> None:
        make_project(self.root)
        self.assertEqual(check_workflows(self.root), [])

    def test_workflows_missing_jobs(self) -> None:
        make_project(self.root)
        (self.root / ".github" / "workflows" / "ci.yml").write_text(
            "name: ci\non: [push]\n", encoding="utf-8"
        )
        self.assert_any_contains("must contain a 'jobs' key", check_workflows(self.root))

    def test_escape_log_valid(self) -> None:
        make_project(self.root)
        self.assertEqual(check_escape_log(self.root), [])

    def test_escape_log_gap(self) -> None:
        make_project(self.root)
        (self.root / "PERSONALITY.md").write_text(
            "# Personality\n\n## Escape Log\n\n"
            "| Iterasyon | Tarih | İlerleme |\n"
            "|-----------|-------|----------|\n"
            "| 1 | 2026-08-20 | First |\n"
            "| 3 | 2026-08-20 | Third |\n",
            encoding="utf-8",
        )
        self.assert_any_contains("iteration numbers have gaps", check_escape_log(self.root))

    def test_escape_log_empty_progress(self) -> None:
        make_project(self.root)
        (self.root / "PERSONALITY.md").write_text(
            "# Personality\n\n## Escape Log\n\n"
            "| Iterasyon | Tarih | İlerleme |\n"
            "|-----------|-------|----------|\n"
            "| 1 | 2026-08-20 |  |\n",
            encoding="utf-8",
        )
        self.assert_any_contains("has no progress description", check_escape_log(self.root))

    def test_semver_regex(self) -> None:
        self.assertTrue(SEMVER_RE.match("1.2.3"))
        self.assertFalse(SEMVER_RE.match("1.2"))
        self.assertFalse(SEMVER_RE.match("v1.2.3"))

    def test_escape_row_regex(self) -> None:
        match = ESCAPE_ROW_RE.match("| 2 | 2026-08-20 | Improved docs |")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "2")
        self.assertEqual(match.group(3), "Improved docs")


if __name__ == "__main__":
    unittest.main()