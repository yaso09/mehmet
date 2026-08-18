import subprocess
import sys
from pathlib import Path

from scripts import validate

ROOT = Path(__file__).resolve().parent.parent


def _run_script() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
        text=True,
    )


class TestValidators:
    def test_real_project_passes(self):
        failures = validate.validate_project(ROOT)
        assert failures == []

    def test_missing_file_reported(self, tmp_path):
        failures = validate.validate_project(tmp_path)
        assert any("Eksik dosya" in item for item in failures)

    def test_invalid_json_reported(self, tmp_path):
        (tmp_path / "opencode.json").write_text("{ not json", encoding="utf-8")
        failures = validate.validate_project(tmp_path)
        assert any("geçersiz JSON" in item for item in failures)

    def test_cli_exit_zero(self):
        result = _run_script()
        assert result.returncode == 0
        assert "OK" in result.stdout

    def test_changelog_regex_matches_entry(self):
        content = "## [0.3.0] - 2026-08-18\n"
        assert validate.CHANGELOG_ENTRY_RE.match(content)

    def test_escape_row_regex(self):
        assert validate.ESCAPE_ROW_RE.match("| 3         | 2026-08-18 | ilerleme |")
        assert not validate.ESCAPE_ROW_RE.match("| Başlık   |")
