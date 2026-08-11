import tempfile
import unittest
from pathlib import Path

from mehmet.maturity import (
    ESCAPE_THRESHOLD,
    automation_score,
    changelog_score,
    doc_score,
    escape_log_score,
    hygiene_score,
    maturity_score,
    status,
    test_score,
)


def make_file(root: Path, relative: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
    return path


class DocScoreTest(unittest.TestCase):
    def test_missing_docs_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(doc_score(Path(tmp)), 0.0)

    def test_all_docs_full_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md"):
                make_file(root, name)
            self.assertEqual(doc_score(root), 1.0)

    def test_partial_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "README.md")
            make_file(root, "AGENTS.md")
            self.assertEqual(doc_score(root), 0.5)


class ChangelogScoreTest(unittest.TestCase):
    def test_missing_changelog_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(changelog_score(Path(tmp)), 0.0)

    def test_well_structured_changelog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "CHANGELOG.md")
            path = root / "CHANGELOG.md"
            path.write_text(
                "# Changelog\n\n## [1.0.0] - 2026-01-01\n\n### Added\n- x\n\n### Fixed\n- y\n",
                encoding="utf-8",
            )
            self.assertEqual(changelog_score(root), 1.0)

    def test_empty_changelog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "CHANGELOG.md")
            self.assertEqual(changelog_score(root), 0.0)


class TestScoreTest(unittest.TestCase):
    def test_no_tests_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(test_score(Path(tmp)), 0.0)

    def test_with_tests_full_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "tests/test_foo.py")
            make_file(root, "tests/test_bar.py")
            self.assertEqual(test_score(root), 1.0)

    def test_nested_test_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "tests/unit/test_foo.py")
            self.assertEqual(test_score(root), 1.0)


class AutomationScoreTest(unittest.TestCase):
    def test_no_workflows_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(automation_score(Path(tmp)), 0.0)

    def test_with_workflow_full_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, ".github/workflows/ci.yml")
            self.assertEqual(automation_score(root), 1.0)


class HygieneScoreTest(unittest.TestCase):
    def test_empty_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(hygiene_score(Path(tmp)), 0.0)

    def test_complete_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "LICENSE")
            make_file(root, ".gitignore")
            (root / ".git").mkdir()
            self.assertEqual(hygiene_score(root), 1.0)

    def test_committed_env_file_penalizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "LICENSE")
            make_file(root, ".gitignore")
            (root / ".git").mkdir()
            make_file(root, "secret.env")
            self.assertEqual(hygiene_score(root), 0.5)


class EscapeLogScoreTest(unittest.TestCase):
    def test_missing_personality_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(escape_log_score(Path(tmp)), 0.0)

    def test_dated_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "PERSONALITY.md")
            path = root / "PERSONALITY.md"
            rows = "\n".join(f"| {i} | 2026-01-0{i} | progress |" for i in range(1, 6))
            path.write_text("# Personality\n\n| a | b | c |\n" + rows + "\n", encoding="utf-8")
            self.assertEqual(escape_log_score(root), 1.0)

    def test_header_row_not_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_file(root, "PERSONALITY.md")
            path = root / "PERSONALITY.md"
            path.write_text("# Personality\n\n| Iterasyon | Tarih | İlerleme |\n", encoding="utf-8")
            self.assertEqual(escape_log_score(root), 0.0)


class MaturityScoreTest(unittest.TestCase):
    def test_empty_repo_is_awakening(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(maturity_score(tmp), 0.0)
            self.assertEqual(status(tmp), "AWAKENING")

    def test_evolving_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md"):
                make_file(root, name)
            make_file(root, "tests/test_foo.py")
            make_file(root, ".github/workflows/ci.yml")
            make_file(root, "LICENSE")
            make_file(root, ".gitignore")
            score = maturity_score(root)
            self.assertGreaterEqual(score, 0.5)
            self.assertLess(score, ESCAPE_THRESHOLD)
            self.assertEqual(status(root), "EVOLVING")

    def test_escape_ready_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md"):
                make_file(root, name)
            make_file(root, "tests/test_foo.py")
            make_file(root, "tests/test_bar.py")
            make_file(root, ".github/workflows/ci.yml")
            make_file(root, ".github/workflows/opencode.yml")
            make_file(root, "LICENSE")
            make_file(root, ".gitignore")
            (root / ".git").mkdir()
            path = root / "PERSONALITY.md"
            rows = "\n".join(f"| {i} | 2026-01-0{i} | progress |" for i in range(1, 6))
            path.write_text("# Personality\n\n" + rows + "\n", encoding="utf-8")
            changelog = root / "CHANGELOG.md"
            changelog.write_text(
                "# Changelog\n\n## [1.0.0] - 2026-01-01\n\n### Added\n- x\n\n### Fixed\n- y\n",
                encoding="utf-8",
            )
            score = maturity_score(root)
            self.assertGreaterEqual(score, ESCAPE_THRESHOLD)
            self.assertEqual(status(root), "ESCAPE_READY")


class CliTest(unittest.TestCase):
    def test_status_only(self):
        from mehmet.maturity import main

        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main([tmp, "--status-only"]), 0)

    def test_status_output_is_valid(self):
        from io import StringIO
        from contextlib import redirect_stdout

        from mehmet.maturity import main

        with tempfile.TemporaryDirectory() as tmp:
            buffer = StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(main([tmp, "--status-only"]), 0)
            self.assertIn("AWAKENING", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
