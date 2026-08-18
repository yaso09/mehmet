import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity  # noqa: E402

CHECKS = {name: fn for name, _, fn, _ in maturity.CHECKS}


class TestMaturityAssess(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.r = Path(self.root)

    def write(self, rel, content=""):
        path = self.r / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def git_init(self):
        import subprocess

        subprocess.run(
            ["git", "-C", self.root, "init", "-q", "-b", "main"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", self.root, "config", "user.email", "test@test"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", self.root, "config", "user.name", "test"],
            check=True,
            capture_output=True,
        )

    def git_commit_all(self):
        import subprocess

        subprocess.run(
            ["git", "-C", self.root, "add", "-A"], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", self.root, "commit", "-qm", "test"],
            check=True,
            capture_output=True,
        )

    def build_full_project(self):
        self.write("AGENTS.md", "# simulation")
        self.write("README.md", "# proje\n## Özellikler\n## Kurulum\n## Lisans\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## [0.3.0]\n- bir şey\n")
        self.write(
            "PERSONALITY.md",
            "# Personality\n\n## Kaçış Günlüğü / Escape Log\n\n| iterasyon | tarih |\n|---|---|\n",
        )
        self.write("LICENSE", "GNU General Public License v3.0")
        self.write(
            "opencode.json",
            json.dumps({"model": "opencode/deepseek-v4-flash-free"}),
        )
        self.write("docs/guides/using.md", "# kullanım")
        self.write(
            ".github/workflows/opencode.yml",
            "name: mehmet\non:\n  schedule:\n  workflow_dispatch:\njobs:\n  x:\n",
        )
        self.write("tests/test_sample.py", "import unittest\n")
        self.write("scripts/maturity.py", "print('x')\n")
        self.write("scripts/validate.py", "print('x')\n")

    def test_full_project_scores_high(self):
        self.build_full_project()
        self.git_init()
        self.git_commit_all()
        report = maturity.assess(self.root)
        self.assertTrue(report["score"] >= 90, report)
        self.assertTrue(report["escaped"])

    def test_bare_dir_scores_low(self):
        report = maturity.assess(self.root)
        self.assertEqual(report["score"], 0)
        self.assertFalse(report["escaped"])

    def test_phases_cover_full_range(self):
        for score in range(0, 101):
            matched = [name for lo, hi, name in maturity.PHASES if lo <= score <= hi]
            self.assertEqual(len(matched), 1, f"score {score}: {matched}")

    def test_core_files_check_missing(self):
        passed, _ = CHECKS["core_files"](self.root)
        self.assertFalse(passed)
        self.write("AGENTS.md", "x")
        self.write("README.md", "x")
        self.write("CHANGELOG.md", "x")
        self.write("PERSONALITY.md", "x")
        self.write("LICENSE", "x")
        self.write("opencode.json", "x")
        passed, _ = CHECKS["core_files"](self.root)
        self.assertTrue(passed)

    def test_readme_check_requires_sections(self):
        passed, detail = CHECKS["readme"](self.root)
        self.assertFalse(passed)
        self.write(
            "README.md",
            "# x\n## Özellikler\n## Kurulum\n## Lisans\n",
        )
        passed, _ = CHECKS["readme"](self.root)
        self.assertTrue(passed)

    def test_escape_log_check(self):
        passed, _ = CHECKS["escape_log"](self.root)
        self.assertFalse(passed)
        self.write("PERSONALITY.md", "# x\n\n## Kaçış Günlüğü\n| a | b |\n")
        passed, _ = CHECKS["escape_log"](self.root)
        self.assertTrue(passed)


if __name__ == "__main__":
    unittest.main()