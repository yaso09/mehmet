#!/usr/bin/env python3
"""Project structure and consistency tests for mehmet.

Run with:  python3 -m unittest discover -s tests -v
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import scripts.maturity as maturity  # noqa: E402


class TestStructure(unittest.TestCase):
    def test_required_root_files(self):
        for name in ("AGENTS.md", "README.md", "CHANGELOG.md", "PERSONALITY.md",
                     "LICENSE", "opencode.json", ".gitignore"):
            self.assertTrue((ROOT / name).exists(), f"{name} eksik")

    def test_docs_directory(self):
        self.assertTrue((ROOT / "docs").is_dir(), "docs/ dizini yok")

    def test_scripts_directory(self):
        self.assertTrue((ROOT / "scripts").is_dir(), "scripts/ dizini yok")

    def test_tests_directory(self):
        self.assertTrue((ROOT / "tests").is_dir(), "tests/ dizini yok")


class TestConsistency(unittest.TestCase):
    def test_license_matches_readme(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8", errors="replace")
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)
        self.assertIn("GPLv3", readme_text)

    def test_opencode_json_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", data)
        self.assertTrue(data["model"])

    def test_changelog_has_version_header(self):
        lines = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(line.startswith("## ") for line in lines))

    def test_personality_has_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", text)

    def test_workflow_has_concurrency_and_schedule(self):
        text = (ROOT / ".github" / "workflows" / "opencode.yml").read_text(encoding="utf-8")
        self.assertIn("concurrency", text)
        self.assertIn("*/10 * * * *", text)
        self.assertIn("workflow_dispatch", text)

    def test_no_hardcoded_secrets(self):
        for p in ROOT.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".json", ".yml", ".yaml", ".md", ".toml"}:
                text = p.read_text(encoding="utf-8", errors="ignore")
                self.assertNotIn("sk-" + "ant-", text)
                self.assertNotIn("BEGIN " + "PRIVATE KEY", text)


class TestMaturityEngine(unittest.TestCase):
    def test_evaluate_returns_score(self):
        report = maturity.evaluate()
        self.assertIn("score", report)
        self.assertIn("dimensions", report)
        self.assertGreaterEqual(report["score"], 0)
        self.assertLessEqual(report["score"], 100)

    def test_dimensions_covered(self):
        report = maturity.evaluate()
        self.assertEqual(set(report["dimensions"]), set(maturity.DIMENSIONS))

    def test_criteria_all_run(self):
        report = maturity.evaluate()
        total_criteria = sum(len(v) for v in report["dimensions"].values())
        self.assertEqual(total_criteria, len(maturity.CRITERIA))

    def test_docs_passed(self):
        report = maturity.evaluate()
        results = report["dimensions"]["documentation"]
        self.assertTrue(all(r["passed"] for r in results),
                        [r["detail"] for r in results if not r["passed"]])

    def test_engine_present(self):
        passed, detail = maturity.c_maturity_engine()
        self.assertTrue(passed, detail)

    def test_cli_json_output(self):
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = maturity.main(["--json"])
        self.assertEqual(code, 0 if maturity.evaluate()["score"] >= maturity.DEFAULT_THRESHOLD else 1)
        parsed = json.loads(buf.getvalue())
        self.assertIn("escape_ready", parsed)
        self.assertIn("score", parsed)


if __name__ == "__main__":
    unittest.main()