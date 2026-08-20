import json
import tempfile
import unittest
from pathlib import Path

from scripts.maturity import CRITERIA, score_repository


def _make_repo(root: Path, *, with_tests: bool = True) -> None:
    (root / "LICENSE").write_text("GPLv3", encoding="utf-8")
    (root / "README.md").write_text("x" * 500, encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog", encoding="utf-8")
    (root / "PERSONALITY.md").write_text("## Kaçış Günlüğü / Escape Log", encoding="utf-8")
    (root / "AGENTS.md").write_text("# rules", encoding="utf-8")
    (root / "opencode.json").write_text(json.dumps({"model": "test"}), encoding="utf-8")
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "scripts").mkdir()
    if with_tests:
        (root / "tests").mkdir()
        (root / "tests" / "test_dummy.py").write_text(
            "import unittest\n"
            "class T(unittest.TestCase):\n"
            "    def test_pass(self):\n"
            "        self.assertTrue(True)\n",
            encoding="utf-8",
        )


def _build(temp_dir: Path, **overrides: bool) -> Path:
    root = Path(temp_dir)
    _make_repo(root, with_tests=overrides.get("with_tests", True))
    for rel, should_exist in overrides.get("remove", {}).items():
        target = root / rel
        if should_exist is False:
            _remove(target)
    if not overrides.get("valid_json", True):
        (root / "opencode.json").write_text("{ not json", encoding="utf-8")
    return root


def _remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        for child in path.iterdir():
            _remove(child)
        path.rmdir()
    else:
        path.unlink()


class MaturityScoringTest(unittest.TestCase):
    def test_blank_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as d:
            report = score_repository(Path(d))
            self.assertEqual(report.total, 0)
            self.assertFalse(report.escape_ready)

    def test_full_repo_meets_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            report = score_repository(_build(Path(d)))
            self.assertEqual(report.total, sum(c.points for c in CRITERIA))
            self.assertTrue(report.escape_ready)

    def test_missing_readme_reduces_score(self):
        with tempfile.TemporaryDirectory() as d:
            root = _build(Path(d))
            _remove(root / "README.md")
            report = score_repository(root)
            self.assertFalse(report.scores["readme"])
            self.assertLess(report.total, sum(c.points for c in CRITERIA))

    def test_invalid_json_fails_config(self):
        with tempfile.TemporaryDirectory() as d:
            root = _build(Path(d), valid_json=False)
            report = score_repository(root)
            self.assertFalse(report.scores["config"])

    def test_missing_tests_fails_both_test_criteria(self):
        with tempfile.TemporaryDirectory() as d:
            root = _build(Path(d), with_tests=False)
            report = score_repository(root)
            self.assertFalse(report.scores["tests"])
            self.assertFalse(report.scores["tests_pass"])

    def test_all_scores_keys_present(self):
        with tempfile.TemporaryDirectory() as d:
            report = score_repository(Path(d))
            self.assertEqual(set(report.scores), {c.key for c in CRITERIA})

    def test_threshold_is_exposed(self):
        with tempfile.TemporaryDirectory() as d:
            report = score_repository(Path(d))
            self.assertEqual(report.threshold, 80)


if __name__ == "__main__":
    unittest.main()