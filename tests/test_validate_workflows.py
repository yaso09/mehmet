#!/usr/bin/env python3
"""scripts/validate_workflows.py için unit testler."""

import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_workflows


class ValidateWorkflowsTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.orig_dir = os.getcwd()
        os.chdir(self.tmpdir.name)
        os.makedirs(".github/workflows", exist_ok=True)
        self.addCleanup(os.chdir, self.orig_dir)

    def test_valid_workflows(self):
        with open(".github/workflows/ok.yml", "w", encoding="utf-8") as fh:
            fh.write("name: ok\non:\n  push:\n")
        exit_code = validate_workflows.main()
        self.assertEqual(exit_code, 0)

    def test_invalid_workflow(self):
        with open(".github/workflows/bad.yml", "w", encoding="utf-8") as fh:
            fh.write("name: [geçersiz\n")
        exit_code = validate_workflows.main()
        self.assertEqual(exit_code, 1)

    def test_no_workflows(self):
        exit_code = validate_workflows.main()
        self.assertEqual(exit_code, 1)

    @mock.patch("sys.stdout")
    def test_pyyaml_missing(self, _stdout):
        with mock.patch.dict(sys.modules, {"yaml": None}):
            with mock.patch("validate_workflows.yaml", None):
                exit_code = validate_workflows.main()
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()