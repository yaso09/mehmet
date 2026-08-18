#!/usr/bin/env python3
"""Project integrity tests for mehmet.

Validates that the repository stays healthy:
- opencode.json matches the published config schema
- GitHub Actions workflows parse and have the required structure
- CHANGELOG.md follows keep-a-changelog style version headers
- README.md and LICENSE stay consistent
- PERSONALITY.md escape log keeps growing
- Docs reference only files that exist

Run with: python -m unittest discover -s tests -v
or:        python tests/test_project.py
"""

import json
import os
import re
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent

# Top-level keys allowed in opencode.json (from https://opencode.ai/config.json)
ALLOWED_CONFIG_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

VERSION_HEADER = re.compile(
    r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", re.MULTILINE
)
ESCAPE_LOG_HEADER = re.compile(
    r"^\|\s*Iterasyon\s*\|\s*Tarih\s*\|\s*İlerleme\s*\|$", re.MULTILINE
)


class TestProject(unittest.TestCase):
    def test_opencode_json_is_valid(self):
        path = ROOT / "opencode.json"
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["$schema"], "https://opencode.ai/config.json")
        self.assertIn("model", data)
        self.assertRegex(data["model"], r"^[^/]+/[^/]+$")
        unknown = set(data) - ALLOWED_CONFIG_KEYS
        self.assertEqual(unknown, set(),
                         f"opencode.json contains schema-invalid keys: {unknown}")

    def test_workflows_parse_and_are_structured(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        workflow_dir = ROOT / ".github" / "workflows"
        self.assertTrue(workflow_dir.is_dir(), "workflows directory missing")
        files = sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml"))
        self.assertTrue(files, "no workflow files found")
        for wf in files:
            with open(wf, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            self.assertIsInstance(data, dict, f"{wf.name}: not a mapping")
            self.assertIn("jobs", data, f"{wf.name}: missing 'jobs'")
            for name, job in data["jobs"].items():
                self.assertEqual(job.get("runs-on"), "ubuntu-latest",
                                 f"{wf.name}:{name} wrong runs-on")
                self.assertIn("steps", job, f"{wf.name}:{name} missing steps")

    def test_opencode_workflow_uses_expected_action(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        wf = ROOT / ".github" / "workflows" / "opencode.yml"
        with open(wf, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        used = [s["uses"] for job in data["jobs"].values()
                for s in job["steps"] if "uses" in s]
        self.assertIn("actions/checkout@", str(used))
        self.assertTrue(any("opencode/github@latest" in str(u) for u in used),
                        "opencode github action not found in workflow")

    def test_changelog_format(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        headers = VERSION_HEADER.findall(text)
        self.assertGreaterEqual(len(headers), 2,
                                "CHANGELOG needs at least two version entries")
        versions = [v for v, _ in headers]
        self.assertEqual(versions, sorted(versions, reverse=True),
                         "CHANGELOG versions must be newest-first")
        latest_version, latest_date = headers[0]
        self.assertIn("### Added", text, "latest entry missing 'Added' section")

    def test_readme_license_consistency(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text, "LICENSE is not GPL")
        self.assertRegex(readme, r"GPLv3|GPL-3\.0", "README must reference GPLv3")

    def test_personality_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertTrue(ESCAPE_LOG_HEADER.search(text),
                        "escape log table header missing")
        rows = [ln for ln in text.splitlines()
                if re.match(r"^\|\s*\d+\s*\|", ln)]
        self.assertGreaterEqual(len(rows), 3, "escape log needs >= 3 entries")

    def test_readme_referenced_files_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for ref in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|yml))`", readme):
            self.assertTrue((ROOT / ref).exists(), f"README references {ref} but it is missing")

    def test_docs_reference_existing_files(self):
        docs = ROOT / "docs"
        if not docs.exists():
            self.skipTest("docs directory missing")
        for md in docs.rglob("*.md"):
            for ref in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|yml|json))`", md.read_text(encoding="utf-8")):
                target = ROOT / ref
                self.assertTrue(target.exists(),
                                f"{md.relative_to(ROOT)} references missing {ref}")


if __name__ == "__main__":
    unittest.main(verbosity=2)