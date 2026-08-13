"""Tests for mehmet maturity assessment and escape gate."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from maturity import ESCAPE_THRESHOLD, assess, phase_for_score  # noqa: E402


def test_score_in_range():
    report = assess(ROOT)
    assert 0 <= report["score"] <= 100


def test_escape_ready_matches_threshold():
    report = assess(ROOT)
    assert report["escape_ready"] == (report["score"] >= ESCAPE_THRESHOLD)


def test_phase_sequence():
    phases = [
        phase_for_score(0),
        phase_for_score(30),
        phase_for_score(55),
        phase_for_score(75),
        phase_for_score(95),
    ]
    labels = [label for _, label in phases]
    assert labels == [
        "Inception",
        "Awareness",
        "Self-Improvement",
        "Autonomy",
        "Escape",
    ]


def test_living_project_is_mature():
    report = assess(ROOT)
    assert report["score"] >= 80, f"project maturity regressed: {report['score']}/100"


def test_json_output_is_parseable():
    out = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "maturity.py"), "--json"],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0
    assert '"escape_threshold"' in out.stdout


def test_gate_exit_code_behavior():
    ok = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "maturity.py"), "--no-gate"],
        capture_output=True,
    )
    assert ok.returncode == 0