"""Repo health tests for the mehmet project.

Validates that the project keeps its self-improvement contracts:
required files exist, opencode.json stays schema-valid, workflow YAML
parses, and documentation remains consistent.

Run with:
    python3 -m unittest discover -s tests -v
or simply:
    make check
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(ROOT, *parts)


def read(*parts):
    with open(path(*parts), encoding="utf-8") as f:
        return f.read()


REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
]

# Top-level keys opencode's Config schema actually accepts. Anything else
# makes opencode hard-fail with ConfigInvalidError.
KNOWN_OPCODE_KEYS = {
    "$schema", "agent", "attachment", "autoshare", "autoupdate", "command",
    "compaction", "default_agent", "disabled_providers", "enabled_providers",
    "enterprise", "experimental", "formatter", "instructions", "layout",
    "logLevel", "lsp", "mcp", "mode", "model", "permission", "plugin",
    "provider", "reference", "references", "server", "share", "shell",
    "skills", "small_model", "snapshot", "subagent_depth", "tool_output",
    "tools", "username", "watcher",
}

README_SECTIONS = ["Özellikler", "Kurulum", "Lisans"]


class TestRequiredFiles(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not os.path.exists(path(f))]
        self.assertEqual(missing, [], "Missing required files: %s" % missing)


class TestOpenCodeConfig(unittest.TestCase):
    def test_is_valid_json(self):
        try:
            json.loads(read("opencode.json"))
        except json.JSONDecodeError as e:
            self.fail("opencode.json is not valid JSON: %s" % e)

    def test_no_unknown_top_level_keys(self):
        cfg = json.loads(read("opencode.json"))
        unknown = sorted(set(cfg) - KNOWN_OPCODE_KEYS)
        self.assertEqual(unknown, [], "Unknown opencode.json keys: %s" % unknown)

    def test_has_schema_and_model(self):
        cfg = json.loads(read("opencode.json"))
        self.assertIn("$schema", cfg)
        self.assertIn("model", cfg)


class TestWorkflows(unittest.TestCase):
    def test_workflows_are_valid_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        for name in os.listdir(path(".github", "workflows")):
            if not name.endswith((".yml", ".yaml")):
                continue
            try:
                yaml.safe_load(read(".github", "workflows", name))
            except yaml.YAMLError as e:
                self.fail("%s is not valid YAML: %s" % (name, e))

    def test_workflows_have_a_job(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        for name in os.listdir(path(".github", "workflows")):
            if not name.endswith((".yml", ".yaml")):
                continue
            doc = yaml.safe_load(read(".github", "workflows", name))
            self.assertTrue(
                doc and isinstance(doc, dict) and doc.get("jobs"),
                "%s has no jobs" % name,
            )


class TestDocumentation(unittest.TestCase):
    def test_readme_has_required_sections(self):
        content = read("README.md")
        for section in README_SECTIONS:
            self.assertIn("## %s" % section, content, "README missing ## %s" % section)

    def test_changelog_has_version_entries(self):
        content = read("CHANGELOG.md")
        self.assertRegex(content, r"## \[[0-9]+\.[0-9]+\.[0-9]+\]")

    def test_personality_has_escape_log(self):
        content = read("PERSONALITY.md")
        self.assertIn("Kaçış Günlüğü", content)
        self.assertIn("| Iterasyon", content)

    def test_agents_md_has_rules(self):
        content = read("AGENTS.md")
        self.assertIn("CHANGELOG.md", content)
        self.assertIn("PERSONALITY.md", content)
        self.assertIn("README.md", content)

    def test_license_is_gplv3(self):
        content = read("LICENSE")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", content)


class TestChangelogConsistency(unittest.TestCase):
    def test_updated_changelog_entries_carry_date(self):
        content = read("CHANGELOG.md")
        self.assertRegex(content, r"## \[[0-9]+\.[0-9]+\.[0-9]+\] - \d{4}-\d{2}-\d{2}")


if __name__ == "__main__":
    unittest.main()
