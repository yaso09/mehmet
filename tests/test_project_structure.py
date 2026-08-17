"""Project structure tests.

Projenin temel yapısının (dosya/dizin düzeni) olgunluk seviyesini koruduğunu doğrular.
"""

import unittest

from tests.helpers import (
    REQUIRED_DIRS,
    REQUIRED_FILES,
    WORKFLOW_FILES,
    PROJECT_ROOT,
    assert_file_exists,
)


class TestProjectStructure(unittest.TestCase):
    def test_required_files_exist(self):
        for f in REQUIRED_FILES:
            assert_file_exists(self, f)

    def test_required_dirs_exist(self):
        for d in REQUIRED_DIRS:
            self.assertTrue(
                PROJECT_ROOT.joinpath(d).is_dir(),
                msg=f"Eksik dizin: {d}",
            )

    def test_workflow_files_exist(self):
        for wf in WORKFLOW_FILES:
            assert_file_exists(self, f".github/workflows/{wf}")

    def test_no_ds_store_files(self):
        for p in PROJECT_ROOT.rglob(".DS_Store"):
            self.fail(f"Repo'da yasak dosya: {p}")

    def test_gitignore_covers_artifacts(self):
        content = PROJECT_ROOT.joinpath(".gitignore").read_text(encoding="utf-8")
        for artifact in ("node_modules", ".env", "*.log", "dist/", "build/"):
            self.assertIn(artifact, content)


if __name__ == "__main__":
    unittest.main()