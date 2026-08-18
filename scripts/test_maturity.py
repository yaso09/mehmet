#!/usr/bin/env python3
"""Unit tests for scripts/maturity.py (stdlib unittest)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import maturity  # noqa: E402


class MaturityCheckTests(unittest.TestCase):
    def test_file_nonempty(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("x")
            path = Path(f.name)
        self.assertTrue(maturity.file_nonempty(path))
        path.unlink()
        self.assertFalse(maturity.file_nonempty(path))

    def test_has_markdown_section_multiline(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text("# Head\n\n## [0.1.0] - 2026-01-01\n", encoding="utf-8")
            self.assertTrue(maturity.has_markdown_section(p, r"^##\s+\[\d+\.\d+\.\d+\]"))
            self.assertFalse(maturity.has_markdown_section(p, r"^##\s+\[\d+\.\d+\.\d+\]" + r"xxx"))

    def test_load_json_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "good.json"
            good.write_text('{"model": "x"}', encoding="utf-8")
            bad = Path(d) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            self.assertEqual(maturity.load_json(good), {"model": "x"})
            self.assertIsNone(maturity.load_json(bad))
            self.assertIsNone(maturity.load_json(Path(d) / "missing.json"))

    def test_compute_score(self):
        checks = [
            maturity.Check("a", 10, True, ""),
            maturity.Check("b", 10, False, ""),
        ]
        score, passed, total = maturity.compute_score(checks)
        self.assertEqual((score, passed, total), (50, 10, 20))

    def test_run_checks_weights_sum_to_100(self):
        checks = maturity.run_checks()
        total = sum(c.weight for c in checks)
        self.assertEqual(total, 100, "ağırlıkların toplamı 100 olmalı")


if __name__ == "__main__":
    unittest.main(verbosity=2)