"""scripts/maturity.py için birim testler."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.maturity import (
    ESCAPE_TAG,
    compute_stats,
    escape_conditions_met,
    parse_maturity,
    print_report,
    validate,
)

SAMPLE = """# Olgunluk Matrisi

## Dokümantasyon

- [x] README var
- [ ] ADR dokümantasyonu var

## Test Altyapısı

- [x] Birim testler var
- [ ] Coverage takibi var
- [x] **[ESCAPE]** CI yeşil
"""


class ParseMaturityTest(unittest.TestCase):
    def test_parses_categories_and_items(self):
        cats = parse_maturity(SAMPLE)
        self.assertEqual(len(cats), 2)
        self.assertEqual(cats[0].name, "Dokümantasyon")
        self.assertEqual(cats[1].name, "Test Altyapısı")
        self.assertEqual(len(cats[0].items), 2)
        self.assertEqual(len(cats[1].items), 3)

    def test_done_state(self):
        cats = parse_maturity(SAMPLE)
        self.assertTrue(cats[0].items[0].done)
        self.assertFalse(cats[0].items[1].done)
        self.assertTrue(cats[1].items[0].done)

    def test_escape_tag_detected(self):
        cats = parse_maturity(SAMPLE)
        escapes = [i for c in cats for i in c.items if i.escape]
        self.assertEqual(len(escapes), 1)
        self.assertIn(ESCAPE_TAG, escapes[0].text)

    def test_item_without_category_raises(self):
        with self.assertRaises(ValueError):
            parse_maturity("- [ ] başlıksız madde\n")

    def test_empty_document_raises(self):
        with self.assertRaises(ValueError):
            parse_maturity("# sadece başlık\n")

    def test_informational_sections_ignored(self):
        text = """## Dokümantasyon

- [x] README var

## Skor Hesaplama

Toplam madde otomatik hesaplanır.

## Kaçış Koşulu

Tüm zorunlu maddeler tamamlanmalı.
"""
        cats = parse_maturity(text)
        self.assertEqual(len(cats), 1)
        self.assertEqual(cats[0].name, "Dokümantasyon")


class ComputeStatsTest(unittest.TestCase):
    def setUp(self):
        self.cats = parse_maturity(SAMPLE)
        self.stats = compute_stats(self.cats)

    def test_totals(self):
        self.assertEqual(self.stats["total"], 5)
        self.assertEqual(self.stats["done"], 3)
        self.assertAlmostEqual(self.stats["score"], 60.0)

    def test_escape_counts(self):
        self.assertEqual(self.stats["escape_total"], 1)
        self.assertEqual(self.stats["escape_done"], 1)


class EscapeConditionsTest(unittest.TestCase):
    def test_met_when_score_high_and_escape_done(self):
        stats = {"score": 90.0, "escape_total": 2, "escape_done": 2}
        self.assertTrue(escape_conditions_met(stats))

    def test_not_met_when_score_low(self):
        stats = {"score": 70.0, "escape_total": 2, "escape_done": 2}
        self.assertFalse(escape_conditions_met(stats))

    def test_not_met_when_mandatory_missing(self):
        stats = {"score": 90.0, "escape_total": 2, "escape_done": 1}
        self.assertFalse(escape_conditions_met(stats))

    def test_not_met_when_no_mandatory(self):
        stats = {"score": 100.0, "escape_total": 0, "escape_done": 0}
        self.assertFalse(escape_conditions_met(stats))


class ValidateTest(unittest.TestCase):
    def test_empty_category_reported(self):
        cats = [parse_maturity(SAMPLE)[0]]
        cats[0].items = []
        self.assertTrue(validate(cats))

    def test_ok_categories(self):
        cats = parse_maturity(SAMPLE)
        self.assertEqual(validate(cats), [])


class PrintReportTest(unittest.TestCase):
    def test_prints_without_error(self):
        cats = parse_maturity(SAMPLE)
        stats = compute_stats(cats)
        print_report(cats, stats)


class CliTest(unittest.TestCase):
    def run_cli(self, *args, stdin_text=None):
        script = str(Path(__file__).resolve().parents[1] / "scripts" / "maturity.py")
        if "--file" in args:
            result = subprocess.run(
                [sys.executable, script, *args],
                capture_output=True,
                text=True,
            )
            return result
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write(stdin_text or SAMPLE)
            path = fh.name
        try:
            result = subprocess.run(
                [sys.executable, script, *args, "--file", path],
                capture_output=True,
                text=True,
            )
            return result
        finally:
            Path(path).unlink()

    def test_default_exit_zero(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("Olgunluk Matrisi Raporu", result.stdout)

    def test_check_valid(self):
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Format geçerli", result.stdout)

    def test_strict_unmet_returns_nonzero(self):
        result = self.run_cli("--strict")
        self.assertNotEqual(result.returncode, 0)

    def test_missing_file_returns_nonzero(self):
        result = self.run_cli("--file", "/nonexistent/MATURITY.md")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()