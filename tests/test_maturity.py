import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity


def make_repo(files: dict[str, str], dirs: list[str] | None = None) -> Path:
    tmp = Path(tempfile.mkdtemp())
    for rel in dirs or []:
        (tmp / rel).mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp


CODE = '''"""Module."""

def add(a: int, b: int) -> int:
    return a + b

def sub(a: int, b: int) -> int:
    return a - b

def mul(a: int, b: int) -> int:
    return a * b

def div(a: int, b: int) -> int:
    return a / b
'''

TEST = '''import unittest

class T(unittest.TestCase):
    def test_x(self):
        self.assertEqual(1, 1)
'''

QUALITY = """name: quality
concurrency:
  group: quality
  cancel-in-progress: true
on: [push]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: python -m unittest discover -s tests -t .
      - run: python scripts/maturity.py
"""

OPENCODE = """name: mehmet
concurrency:
  group: x
on:
  schedule:
    - cron: \"*/10 * * * *\"
jobs:
  autonomous:
    runs-on: ubuntu-latest
    steps:
      - uses: anomalyco/opencode/github@latest
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
"""

DOCS = {
    "README.md": "# mehmet\n\n## Ozellikler\n",
    "CHANGELOG.md": "# Changelog\n\n## [0.1.0] - 2026-01-01\n",
    "PERSONALITY.md": "# Personality\n\n## Kaçış Günlüğü\n",
    "docs/maturity.md": "# Maturity\n\nescape mechanism\n",
}


def full_repo() -> Path:
    return make_repo(
        files={**DOCS, "scripts/tool.py": CODE, "tests/test_tool.py": TEST, ".github/workflows/quality.yml": QUALITY, ".github/workflows/opencode.yml": OPENCODE},
        dirs=["scripts", "tests"],
    )


class ComputeScoreTest(unittest.TestCase):
    def test_compute_score_normalizes_to_100(self):
        results = {g: (25.0, 25.0, []) for g in maturity.CODES}
        self.assertEqual(maturity.compute_score(results), 100.0)

    def test_compute_score_half(self):
        results = {g: (12.5, 25.0, []) for g in maturity.CODES}
        self.assertEqual(maturity.compute_score(results), 50.0)

    def test_compute_score_zero_max(self):
        self.assertEqual(maturity.compute_score({}), 0.0)


class EvaluateCodeTest(unittest.TestCase):
    def test_empty_scripts_scores_zero(self):
        earned, maximum, _ = maturity.evaluate_code(make_repo({}))
        self.assertEqual((earned, maximum), (0.0, 25.0))

    def test_full_scripts_scores_max(self):
        earned, maximum, _ = maturity.evaluate_code(make_repo({"scripts/tool.py": CODE}))
        self.assertEqual(maximum, 25.0)
        self.assertGreaterEqual(earned, 20.0)

    def test_syntax_error_detected(self):
        bad = "def broken(:\n"
        earned, _maximum, _ = maturity.evaluate_code(make_repo({"scripts/tool.py": bad}))
        self.assertLess(earned, 15.0)


class EvaluateDocsTest(unittest.TestCase):
    def test_docs_full_scores_max(self):
        earned, maximum, _ = maturity.evaluate_docs(make_repo(DOCS))
        self.assertEqual(maximum, 25.0)
        self.assertEqual(earned, 25.0)

    def test_docs_empty_scores_zero(self):
        earned, _maximum, _ = maturity.evaluate_docs(make_repo({}))
        self.assertEqual(earned, 0.0)


class EvaluateAutomationTest(unittest.TestCase):
    def test_full_scores_max(self):
        earned, maximum, _ = maturity.evaluate_automation(
            make_repo({".github/workflows/quality.yml": QUALITY, ".github/workflows/opencode.yml": OPENCODE})
        )
        self.assertEqual(maximum, 25.0)
        self.assertEqual(earned, 25.0)

    def test_missing_quality_workflow_scores_well_below_max(self):
        earned, maximum, _ = maturity.evaluate_automation(make_repo({".github/workflows/opencode.yml": OPENCODE}))
        self.assertEqual(maximum, 25.0)
        self.assertLess(earned, 15.0)

    def test_no_workflows_scores_zero(self):
        earned, _maximum, _ = maturity.evaluate_automation(make_repo({}))
        self.assertEqual(earned, 0.0)


class HistoryTest(unittest.TestCase):
    def test_append_and_load(self):
        path = Path(tempfile.mkdtemp()) / "history.json"
        maturity.append_history(path, 42.0)
        history = maturity.load_history(path)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["score"], 42.0)

    def test_load_missing_returns_empty(self):
        self.assertEqual(maturity.load_history(Path(tempfile.mkdtemp()) / "nope.json"), [])

    def test_repeated_same_day_same_score_is_deduplicated(self):
        path = Path(tempfile.mkdtemp()) / "history.json"
        maturity.append_history(path, 42.0)
        history = maturity.append_history(path, 42.0)
        self.assertEqual(len(history), 1)


class SustainedEscapeTest(unittest.TestCase):
    def test_three_consecutive_qualifying_is_escape_ready(self):
        history = [{"score": 10.0}, {"score": 85.0}, {"score": 90.0}, {"score": 95.0}]
        self.assertEqual(maturity.sustained_qualifying_entries(history), 3)
        self.assertTrue(maturity._escape_ready(95.0, history))

    def test_interruption_resets_sustained_count(self):
        history = [{"score": 95.0}, {"score": 40.0}, {"score": 88.0}]
        self.assertEqual(maturity.sustained_qualifying_entries(history), 1)

    def test_below_threshold_counts_zero(self):
        self.assertEqual(maturity.sustained_qualifying_entries([{"score": 50.0}]), 0)

    def test_empty_history_counts_zero(self):
        self.assertEqual(maturity.sustained_qualifying_entries([]), 0)


class FullEvalTest(unittest.TestCase):
    def test_full_repo_is_escape_ready(self):
        data = maturity.report(full_repo())
        self.assertGreaterEqual(data["score"], data["threshold"])


if __name__ == "__main__":
    unittest.main()