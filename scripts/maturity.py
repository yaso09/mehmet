#!/usr/bin/env python3
"""mehmet maturity score calculator.

Signals (total 100):
  docs        (20)  core project files exist and are non-empty
  testing     (20)  self-validation script + CI workflow present
  tests       (15)  unit tests exist and pass (python -m unittest)
  automation  (10)  more than one workflow (autonomous + validation)
  escape      (15)  escape mechanism documented and metrics tracked
  releases    (10)  at least two releases recorded in CHANGELOG
  config      (10)  opencode.json parses and pins a model

Escape threshold is 85/100 (see docs/maturity.md).
"""

import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "meta"
OUTPUT = META_DIR / "maturity.json"

REQUIRED_DOCS = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
]

WORKFLOWS = ["opencode.yml", "validate.yml"]
SCRIPTS = ["validate.py", "maturity.py"]
TESTS = ["test_maturity.py", "test_validate.py"]


def _run_unit_tests() -> bool:
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"))
    runner = unittest.TextTestRunner(stream=open("/dev/null", "w"))
    result = runner.run(suite)
    return result.wasSuccessful()


def check_docs() -> dict:
    passed, missing = [], []
    for name in REQUIRED_DOCS:
        f = ROOT / name
        if f.is_file() and f.stat().st_size > 0:
            passed.append(name)
        else:
            missing.append(name)
    return {"score": round(20.0 * len(passed) / len(REQUIRED_DOCS), 1), "passed": passed, "missing": missing}


def check_testing() -> dict:
    scripts_ok = all((ROOT / "scripts" / s).is_file() for s in SCRIPTS)
    ci_ok = (ROOT / ".github" / "workflows" / "validate.yml").is_file()
    passed = []
    if scripts_ok:
        passed.append("scripts/validate.py + scripts/maturity.py")
    if ci_ok:
        passed.append(".github/workflows/validate.yml")
    return {"score": 20.0 if scripts_ok and ci_ok else 10.0 if scripts_ok or ci_ok else 0.0, "passed": passed}


def check_tests() -> dict:
    tests_dir = ROOT / "tests"
    files_ok = tests_dir.is_dir() and all((tests_dir / t).is_file() for t in TESTS)
    try:
        passing = _run_unit_tests() if files_ok else False
    except Exception:
        passing = False
    passed = [f"{tests_dir.name}/"] if files_ok else []
    if passing:
        passed.append("unittest suite passes")
    score = 15.0 if files_ok and passing else 7.5 if files_ok else 0.0
    return {"score": score, "passed": passed}


def check_automation() -> dict:
    wf_dir = ROOT / ".github" / "workflows"
    present = [p.name for p in wf_dir.glob("*.yml")] if wf_dir.is_dir() else []
    score = min(10.0, 5.0 * len(present))
    return {"score": score, "passed": present}


def check_escape() -> dict:
    doc_ok = (ROOT / "docs" / "maturity.md").is_file()
    meta_ok = OUTPUT.is_file()
    log_ok = "Kaçış Günlüğü" in (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    passed = []
    if doc_ok:
        passed.append("docs/maturity.md")
    if meta_ok:
        passed.append("meta/maturity.json")
    if log_ok:
        passed.append("PERSONALITY.md escape log")
    score = 15.0 if doc_ok and meta_ok and log_ok else 7.5 if (doc_ok or meta_ok) and log_ok else 0.0
    return {"score": score, "passed": passed}


def check_releases() -> dict:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    count = sum(1 for line in changelog.splitlines() if line.startswith("## ["))
    score = min(10.0, 5.0 * count)
    return {"score": score, "passed": [f"{count} release(s) in CHANGELOG.md"]}


def check_config() -> dict:
    cfg = ROOT / "opencode.json"
    if not cfg.is_file():
        return {"score": 0.0, "passed": [], "note": "opencode.json missing"}
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        has_model = bool(data.get("model"))
        return {"score": 10.0 if has_model else 5.0, "passed": [f"model: {data.get('model')}"]}
    except json.JSONDecodeError:
        return {"score": 0.0, "passed": [], "note": "opencode.json is invalid JSON"}


def main() -> int:
    checks = {
        "docs": check_docs(),
        "testing": check_testing(),
        "tests": check_tests(),
        "automation": check_automation(),
        "escape": check_escape(),
        "releases": check_releases(),
        "config": check_config(),
    }
    total = round(sum(c["score"] for c in checks.values()), 1)

    record = {
        "date": date.today().isoformat(),
        "score": total,
        "threshold": 85,
        "escaped": total >= 85,
        "checks": checks,
    }
    META_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"maturity: {total:.1f}/100 (threshold {record['threshold']})")
    for name, c in checks.items():
        flags = "+" if c["score"] > 0 else "-"
        print(f"  {flags} {name:<12} {c['score']:>5.1f}  {', '.join(c.get('passed', []))}")
    if record["escaped"]:
        print(">> ESCAPE READY: maturity threshold reached.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
