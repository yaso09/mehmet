#!/usr/bin/env python3
"""Unit tests for the project maturity checker."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from maturity import CheckResult, score_results, run_checks  # noqa: E402


def build_project(files):
    tmp = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        path = tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tmp


BASE_FILES = {
    "AGENTS.md": "# Simülasyon Bağlamı\n## Kurallar\n",
    "README.md": "## Özellikler\n## Kurulum\n## Lisans\n",
    "CHANGELOG.md": "# Changelog\n## [0.1.0] - 2026-01-01\n",
    "PERSONALITY.md": "## Traits\n## Evolution\n## Kaçış Günlüğü\n",
    "LICENSE": "GPLv3",
    "opencode.json": json.dumps({"model": "test"}),
    ".github/workflows/opencode.yml": "name: x\njobs:\n  run: {}\n",
    ".github/workflows/validate.yml": "name: validate\njobs:\n  check: {}\n",
    "scripts/maturity.py": "#!/usr/bin/env python3\n",
    "tests/test_sample.py": "import unittest\n",
}


class MaturityTest(unittest.TestCase):
    def test_healthy_project_passes_all(self):
        root = build_project(BASE_FILES)
        results = run_checks(root)
        for result in results:
            self.assertTrue(result.passed, str(result))

    def test_missing_required_file_fails(self):
        files = dict(BASE_FILES)
        del files["LICENSE"]
        root = build_project(files)
        results = run_checks(root)
        failed = [r for r in results if not r.passed]
        self.assertTrue(any("LICENSE" in r.name for r in failed))

    def test_invalid_json_fails(self):
        files = dict(BASE_FILES)
        files["opencode.json"] = "{not valid json"
        root = build_project(files)
        results = run_checks(root)
        failed = [r for r in results if not r.passed]
        self.assertTrue(any("opencode.json" in r.name and "JSON" in r.name for r in failed))

    def test_workflow_without_jobs_fails(self):
        files = dict(BASE_FILES)
        files[".github/workflows/opencode.yml"] = "name: x\n"
        root = build_project(files)
        results = run_checks(root)
        failed = [r for r in results if not r.passed]
        self.assertTrue(any("opencode.yml" in r.name for r in failed))

    def test_score_bounds(self):
        root = build_project(BASE_FILES)
        score = score_results(run_checks(root))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_empty_project_scores_zero(self):
        root = build_project({})
        score = score_results(run_checks(root))
        self.assertEqual(score, 0)

    def test_changelog_without_versions_fails(self):
        files = dict(BASE_FILES)
        files["CHANGELOG.md"] = "# Changelog\n"
        root = build_project(files)
        results = run_checks(root)
        failed = [r for r in results if not r.passed]
        self.assertTrue(any("versions" in r.name for r in failed))

    def test_escape_threshold_importable(self):
        import maturity

        self.assertGreater(maturity.ESCAPE_THRESHOLD, 0)


if __name__ == "__main__":
    unittest.main()