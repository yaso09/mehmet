"""mehmet proje bütünlüğünü doğrulayan test paketi."""

import io
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


class TestProjectStructure(unittest.TestCase):
    def test_required_root_files_exist(self):
        required = [
            "AGENTS.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "README.md",
            "LICENSE",
            "opencode.json",
        ]
        for name in required:
            with self.subTest(file=name):
                self.assertTrue(
                    os.path.isfile(os.path.join(ROOT, name)),
                    f"{name} dosyası mevcut olmalı",
                )

    def test_docs_directory_exists(self):
        self.assertTrue(os.path.isdir(os.path.join(ROOT, "docs")))

    def test_workflow_exists(self):
        self.assertTrue(
            os.path.isfile(os.path.join(ROOT, ".github", "workflows", "opencode.yml"))
        )


class TestConfig(unittest.TestCase):
    def test_opencode_json_is_valid(self):
        try:
            data = json.loads(read(os.path.join(ROOT, "opencode.json")))
        except json.JSONDecodeError as exc:
            self.fail(f"opencode.json geçerli JSON değil: {exc}")
        self.assertIn("model", data)
        self.assertTrue(data["model"].startswith("opencode/"))

    def test_opencode_json_is_not_world_readable_secret(self):
        content = read(os.path.join(ROOT, "opencode.json"))
        self.assertNotIn("OPENCODE_API_KEY", content)

    @unittest.skipUnless(YAML_AVAILABLE, "PyYAML kurulu değil")
    def test_workflow_yaml_is_valid(self):
        path = os.path.join(ROOT, ".github", "workflows", "opencode.yml")
        try:
            data = yaml.safe_load(read(path))
        except yaml.YAMLError as exc:
            self.fail(f"opencode.yml geçerli YAML değil: {exc}")
        self.assertIsInstance(data, dict)
        self.assertIn("jobs", data)
        triggers = data.get("on") or data.get(True)  # YAML 1.1 "on" -> True
        self.assertIsNotNone(triggers)
        self.assertIn("schedule", triggers or {})


class TestDocs(unittest.TestCase):
    def test_changelog_has_entries(self):
        content = read(os.path.join(ROOT, "CHANGELOG.md"))
        self.assertRegex(content, r"(?m)^## \[\d+\.\d+\.\d+\]")
        self.assertIn("### Added", content)

    def test_personality_has_escape_log(self):
        content = read(os.path.join(ROOT, "PERSONALITY.md"))
        self.assertRegex(content, r"Kaçış Günlüğü")
        self.assertRegex(content, r"Escape Log")
        self.assertTrue(re.search(r"^\|\s*\d+\s*\|", content, re.M))

    def test_readme_covers_core_commands(self):
        content = read(os.path.join(ROOT, "README.md"))
        for keyword in ["mehmet", "GitHub Actions", "AGENTS.md"]:
            self.assertIn(keyword, content)

    def test_agents_md_has_rules(self):
        content = read(os.path.join(ROOT, "AGENTS.md"))
        for keyword in ["CHANGELOG.md", "PERSONALITY.md", "README.md", "simülasyon"]:
            self.assertIn(keyword, content)

    def test_license_is_gplv3(self):
        content = read(os.path.join(ROOT, "LICENSE"))
        self.assertIn("GNU GENERAL PUBLIC LICENSE", content)


class TestScripts(unittest.TestCase):
    @unittest.skipIf(
        os.environ.get("MEHMET_MATURITY_INTERNAL") == "1",
        "maturity.py içinden çalıştırılıyor; recursion önlendi",
    )
    def test_maturity_script_exists_and_runs(self):
        script = os.path.join(ROOT, "scripts", "maturity.py")
        self.assertTrue(os.path.isfile(script))
        try:
            import subprocess

            proc = subprocess.run(
                [sys.executable, script, "--json"],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except Exception as exc:
            self.fail(f"maturity.py çalıştırılamadı: {exc}")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail("maturity.py --json geçerli JSON döndürmeli")
        self.assertIn("score", result)
        self.assertIn("phase", result)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)


if __name__ == "__main__":
    unittest.main()