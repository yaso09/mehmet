import subprocess
import sys
from pathlib import Path

import pytest

from scripts import maturity

ROOT = Path(__file__).resolve().parent.parent


def _run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "maturity.py"), *args],
        capture_output=True,
        text=True,
    )


class TestThreshold:
    def test_threshold_value(self):
        assert maturity.ESCAPE_THRESHOLD == 100.0

    def test_min_iterations(self):
        assert maturity.MIN_ITERATIONS == 5

    def test_threshold_flag(self):
        result = _run_script("--threshold")
        assert result.returncode == 0
        assert result.stdout.strip() == "100.0"


class TestScoreProject:
    def test_result_shape(self):
        result = maturity.score_project(ROOT)
        assert result["overall"] >= 0 and result["overall"] <= 100
        assert result["threshold"] == 100.0
        assert "escaped" in result
        assert len(result["dimensions"]) == 5

    def test_weights_sum_to_one(self):
        weights = [dim["weight"] for dim in maturity.DIMENSIONS]
        assert sum(weights) == pytest.approx(1.0)

    def test_every_dimension_has_checks(self):
        for dim in maturity.DIMENSIONS:
            assert len(dim["checks"]) >= 3

    def test_escape_not_yet_achieved(self):
        result = maturity.score_project(ROOT)
        assert result["escaped"] is False

    def test_sustained_evolution_required(self):
        result = maturity.score_project(ROOT)
        documentation = next(d for d in result["dimensions"] if d["name"] == "documentation")
        assert documentation["passed"] < documentation["total"]


class TestCli:
    def test_check_exits_nonzero_below_threshold(self):
        result = _run_script("--check")
        assert result.returncode == 1

    def test_json_output_is_valid(self):
        import json

        result = _run_script("--json")
        assert result.returncode == 0
        parsed = json.loads(result.stdout)
        assert "overall" in parsed
        assert "dimensions" in parsed
