import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.maturity as maturity


def test_criteria_weights_sum_to_max_score():
    report = maturity.evaluate()
    assert report["score"] <= report["max_score"]
    assert report["max_score"] == 100


def test_criteria_ids_are_unique():
    ids = [c["id"] for c in maturity.CRITERIA]
    assert len(ids) == len(set(ids))


def test_criteria_have_required_fields():
    for c in maturity.CRITERIA:
        assert set(c) >= {"id", "category", "weight", "check", "detail"}
        assert c["weight"] > 0
        assert isinstance(c["check"](), bool)


def test_evaluate_returns_valid_shape():
    report = maturity.evaluate()
    assert 0 <= report["score"] <= report["max_score"]
    assert report["threshold"] == maturity.ESCAPE_THRESHOLD
    assert "criteria" in report and "categories" in report
    assert len(report["criteria"]) == len(maturity.CRITERIA)
    assert report["categories"]
    for r in report["criteria"]:
        assert r["earned"] in (0, r["weight"])
        assert r["passed"] == (r["earned"] > 0)


def test_escaped_flag_matches_threshold():
    report = maturity.evaluate()
    assert report["escaped"] == (report["score"] >= maturity.ESCAPE_THRESHOLD)


def test_main_returns_int():
    assert isinstance(maturity.main(["--json"]), int)


def test_main_json_output_is_valid():
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exit_code = maturity.main(["--json", "--threshold", "0"])
    data = json.loads(buf.getvalue())
    assert exit_code == 0
    assert "score" in data
    assert data["escaped"] is True


def test_all_categories_represented_in_report():
    report = maturity.evaluate()
    for c in maturity.CRITERIA:
        assert c["category"] in report["categories"]