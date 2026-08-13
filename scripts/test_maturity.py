#!/usr/bin/env python3
"""scripts/maturity.py için unit testler."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from maturity import WEIGHTS, compute_scores, overall_score


def make_repo(tmp):
    root = Path(tmp)
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "docs" / "design").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "tests").mkdir()
    (root / "VERSION").write_text("0.3.0")
    (root / "README.md").write_text("# repo\n\nGPLv3\n")
    (root / "CHANGELOG.md").write_text("## [0.3.0] - 2026-08-13\n")
    (root / "LICENSE").write_text("GPL")
    (root / ".gitignore").write_text("node_modules/\n")
    (root / "opencode.json").write_text(json.dumps({"model": "m", "toolTimeout": 120000, "skip": True, "enable": True}))
    (root / "PERSONALITY.md").write_text(
        "## Kaçış Günlüğü\n"
        "| 1 | 2026-07-04 | a |\n"
        "| 2 | 2026-07-04 | b |\n"
        "| 3 | 2026-08-13 | c |\n"
        "| 4 | 2026-08-13 | d |\n"
    )
    (root / "scripts" / "app.py").write_text("print('hi')\n")
    (root / "scripts" / "util.py").write_text("def f():\n    return 1\n")
    (root / "scripts" / "main.py").write_text("import util\n")
    (root / "tests" / "test_app.py").write_text("def test_x():\n    assert True\n")
    (root / ".github" / "workflows" / "opencode.yml").write_text(
        "name: mehmet\nconcurrency:\n  group: x\nschedule:\n  - cron: '*/10 * * * *'\n"
        "jobs:\n  a:\n    uses: anomalyco/opencode\n  b:\n    uses: anomalyco/opencode\n"
    )
    return root


class MaturityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_repo(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_fully_qualified_repo_scores_high(self):
        scores = compute_scores(self.root)
        for key in WEIGHTS:
            self.assertGreaterEqual(scores[key], 90, msg=f"{key} beklenen yüksek skor")
        self.assertGreaterEqual(overall_score(scores), 90)

    def test_empty_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as empty:
            scores = compute_scores(Path(empty))
            self.assertEqual(overall_score(scores), 0)

    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(WEIGHTS.values()), 1.0, places=6)

    def test_cli_json_output(self):
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent / "maturity.py"),
             "--root", self.tmp.name, "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIn("overall", data)
        self.assertIn("scores", data)

    def test_cli_threshold_exit_codes(self):
        script = str(Path(__file__).resolve().parent / "maturity.py")
        low = subprocess.run([sys.executable, script, "--root", self.tmp.name, "--threshold", "999"],
                             capture_output=True, text=True, check=False)
        self.assertEqual(low.returncode, 1)
        high = subprocess.run([sys.executable, script, "--root", self.tmp.name, "--threshold", "1"],
                              capture_output=True, text=True, check=False)
        self.assertEqual(high.returncode, 0)

    def test_cli_missing_dir_errors(self):
        script = str(Path(__file__).resolve().parent / "maturity.py")
        proc = subprocess.run([sys.executable, script, "--root", "/yok/böyle/dizin"],
                              capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()