"""Configuration and workflow syntax tests.

opencode.json ve GitHub Actions workflow'larının geçerli ve tutarlı olduğunu doğrular.
"""

import json
import unittest

import yaml

from tests.helpers import (
    PROJECT_ROOT,
    load_json,
    read_text,
)


class TestOpenCodeConfig(unittest.TestCase):
    def test_is_valid_json(self):
        data = load_json("opencode.json")
        self.assertIsInstance(data, dict)

    def test_has_required_keys(self):
        data = load_json("opencode.json")
        for key in ("$schema", "model", "enable"):
            self.assertIn(key, data, msg=f"opencode.json'da eksik anahtar: {key}")

    def test_model_is_set(self):
        data = load_json("opencode.json")
        self.assertTrue(data.get("model"), "model boş olmamalı")

    def test_schema_url(self):
        data = load_json("opencode.json")
        self.assertTrue(
            str(data.get("$schema", "")).startswith("https://"),
            "$schema bir URL olmalı",
        )


class TestWorkflows(unittest.TestCase):
    def test_workflows_are_valid_yaml(self):
        for wf in ("opencode.yml", "ci.yml"):
            content = read_text(f".github/workflows/{wf}")
            doc = yaml.safe_load(content)
            self.assertIsInstance(doc, dict, msg=f"{wf} geçerli bir YAML değil")
            self.assertIn("jobs", doc, msg=f"{wf} içinde jobs yok")

    def test_opencode_workflow_permissions(self):
        doc = yaml.safe_load(read_text(".github/workflows/opencode.yml"))
        job = doc["jobs"].get("autonomous", {})
        perms = job.get("permissions", {})
        for perm in ("contents", "issues", "pull-requests"):
            self.assertEqual(perms.get(perm), "write", msg=f"{perm} izni eksik")

    def test_ci_workflow_runs_tests(self):
        doc = yaml.safe_load(read_text(".github/workflows/ci.yml"))
        steps = doc["jobs"]["test"]["steps"]
        step_names = [s.get("name", "") for s in steps]
        self.assertTrue(
            any("test" in n.lower() for n in step_names),
            msg="ci.yml test adımı içermiyor",
        )


if __name__ == "__main__":
    unittest.main()