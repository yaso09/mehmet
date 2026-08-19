#!/usr/bin/env python3
"""validate.py ve maturity.py için testler."""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import maturity  # noqa: E402
import validate  # noqa: E402


class TestValidate(unittest.TestCase):
    def test_required_files_exist(self):
        for name in validate.REQUIRED_FILES:
            self.assertTrue(
                (validate.ROOT / name).exists(), f"{name} eksik"
            )

    def test_run_checks_no_errors_on_real_project(self):
        errors, _ = validate.run_checks()
        self.assertEqual(errors, [])

    def test_check_file_exists_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "missing.md"
            errors = validate.check_file_exists(path)
            self.assertEqual(len(errors), 1)

    def test_check_file_contains_missing_keyword(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "x.md"
            path.write_text("hello", encoding="utf-8")
            errors = validate.check_file_contains(path, ["hello", "nope"])
            self.assertEqual(len(errors), 1)
            self.assertIn("nope", errors[0])

    def test_check_opencode_json_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "opencode.json"
            path.write_text("{not json", encoding="utf-8")
            errors = validate.check_opencode_json(path)
            self.assertEqual(len(errors), 1)

    def test_version_mismatch_produces_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            changelog = tmp_path / "CHANGELOG.md"
            changelog.write_text(
                "# Changelog\n\n## [9.9.9] - 2026-08-19\n", encoding="utf-8"
            )
            readme = tmp_path / "README.md"
            readme.write_text("# mehmet\n\nNo version here\n", encoding="utf-8")
            old_root = validate.ROOT
            validate.ROOT = tmp_path
            try:
                _, warnings = validate.run_checks()
            finally:
                validate.ROOT = old_root
            self.assertTrue(
                any("güncel sürümü" in w for w in warnings)
            )


class TestMaturity(unittest.TestCase):
    def test_compute_all_met(self):
        results = {name: True for name in maturity.CRITERIA}
        self.assertEqual(maturity.compute(results), 100)

    def test_compute_none_met(self):
        results = {name: False for name in maturity.CRITERIA}
        self.assertEqual(maturity.compute(results), 0)

    def test_compute_half(self):
        items = list(maturity.CRITERIA)
        results = {
            name: (i % 2 == 0) for i, name in enumerate(items)
        }
        self.assertEqual(maturity.compute(results), 50)

    def test_real_project_above_threshold(self):
        total = maturity.compute(maturity.score())
        self.assertGreaterEqual(total, maturity.ESCAPE_THRESHOLD)

    def test_json_output(self):
        import io
        import contextlib

        with tempfile.TemporaryDirectory() as tmp:
            old_root = maturity.ROOT
            maturity.ROOT = pathlib.Path(tmp)
            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = maturity.main(["--json"])
                out = json.loads(buf.getvalue())
            finally:
                maturity.ROOT = old_root
            self.assertEqual(rc, 0)
            self.assertIn("score", out)
            self.assertIn("criteria", out)


if __name__ == "__main__":
    unittest.main()