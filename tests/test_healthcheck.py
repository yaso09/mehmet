"""mehmet healthcheck icin birim testleri."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import healthcheck  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HealthcheckTest(unittest.TestCase):
    def test_real_repo_all_checks_pass(self):
        checks = healthcheck.run_checks(REPO_ROOT)
        failed = [c for c in checks if not c["ok"]]
        self.assertEqual(failed, [], "tum kontroller gecmeli: %r" % failed)

    def test_real_repo_score_above_established(self):
        checks = healthcheck.run_checks(REPO_ROOT)
        score = sum(c["weight"] for c in checks if c["ok"])
        self.assertGreaterEqual(score, 70, "olgunluk skoru Established seviyesinin altinda")

    def test_empty_dir_scores_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            checks = healthcheck.run_checks(tmp)
            score = sum(c["weight"] for c in checks if c["ok"])
            self.assertLess(score, 30)

    def test_latest_version_parsing(self):
        changelog = (
            "# Changelog\n"
            "\n"
            "## [0.3.0] - 2026-08-19\n"
            "\n"
            "### Added\n"
            "- Ornek\n"
        )
        self.assertEqual(healthcheck.latest_version(changelog), "0.3.0")
        self.assertIsNone(healthcheck.latest_version("# bos"))


class LevelTest(unittest.TestCase):
    def test_level_boundaries(self):
        self.assertEqual(healthcheck.level_for(0), "Falling Apart")
        self.assertEqual(healthcheck.level_for(29), "Falling Apart")
        self.assertEqual(healthcheck.level_for(30), "Foundation")
        self.assertEqual(healthcheck.level_for(50), "Growing")
        self.assertEqual(healthcheck.level_for(70), "Established")
        self.assertEqual(healthcheck.level_for(90), "Autonomous")
        self.assertEqual(healthcheck.level_for(100), "Escape Ready")


if __name__ == "__main__":
    unittest.main()