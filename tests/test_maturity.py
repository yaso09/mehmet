#!/usr/bin/env python3
"""scripts/maturity.py için unit test'ler.

Kendi başına çalıştırılabilir:  python3 tests/test_maturity.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
SCRIPT = SCRIPT_DIR / "scripts" / "maturity.py"

sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

import maturity  # noqa: E402


class MaturityScoreTest(unittest.TestCase):
    def _make_project(self, complete: bool) -> Path:
        tmp = Path(tempfile.mkdtemp())
        paths = [
            "README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md",
            "opencode.json", ".gitignore", "LICENSE",
            ".github/workflows/opencode.yml",
            ".github/workflows/quality.yml",
            "scripts/maturity.py", "docs", "tests",
        ]
        for path in paths:
            target = tmp / path
            if path.endswith(".yml") or path.endswith(".json"):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}" if path.endswith(".json") else "name: x\n")
            elif path.endswith(".md"):
                target.write_text("# x\n")
            elif path == ".gitignore":
                target.write_text("node_modules/\n")
            elif path == "scripts/maturity.py":
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# maketest\n")
            else:
                target.mkdir(parents=True, exist_ok=True)
                (target / "doc.md").write_text("# doc\n")
        if not complete:
            (tmp / "README.md").unlink()
        return tmp

    def test_full_project_escapes(self):
        tmp = self._make_project(complete=True)
        try:
            result = maturity.score(tmp)
            self.assertTrue(result["all_checks_done"])
            self.assertTrue(result["escaped"])
            self.assertEqual(result["total"], 100.0)
        finally:
            shutil.rmtree(tmp)

    def test_incomplete_project_does_not_escape(self):
        tmp = self._make_project(complete=False)
        try:
            result = maturity.score(tmp)
            self.assertFalse(result["all_checks_done"])
            self.assertFalse(result["escaped"])
            self.assertLess(result["total"], 100.0)
        finally:
            shutil.rmtree(tmp)

    def test_invalid_json_fails_configuration(self):
        tmp = self._make_project(complete=True)
        try:
            (tmp / "opencode.json").write_text("{ not valid json")
            result = maturity.score(tmp)
            cfg = result["categories"]["configuration"]
            by_path = {c["path"]: c["ok"] for c in cfg["checks"]}
            self.assertFalse(by_path["opencode.json"])
            self.assertTrue(by_path[".gitignore"])
            self.assertTrue(by_path["LICENSE"])
            self.assertFalse(result["escaped"])
        finally:
            shutil.rmtree(tmp)

    def test_cli_json(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self._make_project(True)), "--json"],
            capture_output=True, text=True,
        )
        data = json.loads(proc.stdout)
        self.assertIn("total", data)
        self.assertIn("escaped", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)