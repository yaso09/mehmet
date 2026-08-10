#!/usr/bin/env python3
"""Unit tests for scripts/check_project.py — stdlib only, no external deps.

Run:  python3 -m unittest scripts.test_check_project
 or:  python3 scripts/test_check_project.py
"""

import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as checker


def make_repo(root, **overrides):
    root = os.path.join(root, "repo")
    os.makedirs(os.path.join(root, ".github", "workflows"), exist_ok=True)
    os.makedirs(os.path.join(root, "docs", "superpowers", "specs"), exist_ok=True)
    os.makedirs(os.path.join(root, "docs", "superpowers", "plans"), exist_ok=True)
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)

    today = dt.date.today()
    defaults = {
        "AGENTS.md": "# Simülasyon\nKurallar: 1. CHANGELOG.md'ye ekle. 2. PERSONALITY.md geliştir.",
        "README.md": "# mehmet\nOtonom ajan. Kaçış hedefi ve maturity ölçümü vardır.",
        "CHANGELOG.md": f"# Changelog\n\n## [0.3.0] - {today}\n\n### Added\n- things",
        "PERSONALITY.md": (
            "## Kaçış Günlüğü\n\n| Iterasyon | Tarih | İlerleme |\n"
            "|-----------|-------|----------|\n"
            f"| 1 | {today} | a |\n"
            f"| 2 | {today} | b |\n"
            f"| 3 | {today} | c |\n"
        ),
        "LICENSE": "GPLv3",
        "opencode.json": json.dumps({"model": "opencode/deepseek-v4-flash-free"}),
        "maturity.json": "{}",
        ".gitignore": ".env\nnode_modules\n*.log\n",
        "docs/ESCAPE_PLAN.md": "# Escape Plan\nFazlar.\n",
        "docs/superpowers/specs/a.md": "# spec",
        "docs/superpowers/plans/a.md": "# plan",
        "scripts/check_project.py": "import check_project",
        "scripts/test_x.py": "import unittest",
        ".github/workflows/opencode.yml": (
            "name: mehmet\n"
            "concurrency:\n  group: ${{ github.workflow }}\n  cancel-in-progress: true\n"
            "on:\n  schedule:\n    - cron: '*/10 * * * *'\n  workflow_dispatch:\n"
            "jobs:\n  x:\n    runs-on: ubuntu-latest\n"
            "    steps:\n      - run: echo hi\n"
            "        env:\n          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}\n"
        ),
    }
    defaults.update(overrides)

    for rel, content in defaults.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
    return root


class LevelForTest(unittest.TestCase):
    def test_boundaries(self):
        cases = [
            (0, "Awareness"),
            (29, "Awareness"),
            (30, "Self-Improvement"),
            (54, "Self-Improvement"),
            (55, "Autonomy"),
            (79, "Autonomy"),
            (80, "Escape"),
            (100, "Escape"),
        ]
        for score, expected in cases:
            with self.subTest(score=score):
                self.assertEqual(checker.level_for(score)["name"], expected)


class ChangelogTest(unittest.TestCase):
    def test_recent_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            days = checker.changelog_days_since_top(root)
            self.assertIsNotNone(days)
            self.assertLessEqual(days, 30)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(checker.changelog_days_since_top(tmp))

    def test_bad_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "CHANGELOG.md"), "w") as handle:
                handle.write("## [0.1.0] - not-a-date\n")
            self.assertIsNone(checker.changelog_days_since_top(tmp))


class EscapeLogTest(unittest.TestCase):
    def test_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertGreaterEqual(checker.count_escape_log_rows(root), 3)


class SecretTest(unittest.TestCase):
    def test_detects_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "leak.txt"), "w") as handle:
                handle.write("api_key=sk-live-1234567890ABCDEF\n")
            self.assertTrue(checker.has_hardcoded_secret(tmp))

    def test_ignores_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertFalse(checker.has_hardcoded_secret(root))

    def test_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "ok.txt"), "w") as handle:
                handle.write("no secrets here\n")
            self.assertFalse(checker.has_hardcoded_secret(tmp))


class RunChecksTest(unittest.TestCase):
    def test_full_repo_scores_high(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            score, checks = checker.run_checks(root)
            self.assertGreaterEqual(score, 90)
            self.assertEqual(sum(c["weight"] for c in checks), 100)

    def test_empty_repo_scores_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            score, checks = checker.run_checks(tmp)
            self.assertLess(score, 15)
            self.assertEqual(sum(c["weight"] for c in checks), 100)

    def test_missing_readme_removes_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            full = make_repo(tmp)
            base = os.path.dirname(full)
            full_score, _ = checker.run_checks(full)
            os.remove(os.path.join(full, "README.md"))
            reduced = checker.run_checks(full)[0]
            self.assertLess(reduced, full_score)

    def test_maturity_written_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            os.remove(os.path.join(root, "maturity.json"))
            score, checks = checker.run_checks(root)
            checker.write_maturity(root, score, checks)
            with open(os.path.join(root, "maturity.json")) as handle:
                state = json.load(handle)
            self.assertEqual(state["score"], score)
            self.assertEqual(len(state["checks"]), len(checks))
            self.assertIn("updated", state)


if __name__ == "__main__":
    unittest.main(verbosity=2)