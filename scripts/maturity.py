#!/usr/bin/env python3
"""mehmet maturity scorer.

Scans the repository and computes a maturity score (0-100) based on concrete,
verifiable criteria. The score tracks progress toward the escape threshold
defined in MATURITY.md. Runs with only the Python standard library.

Usage:
    python3 scripts/maturity.py [--root DIR] [--report PATH] [--fail-below N]

Exit codes:
    0  score computed successfully
    1  score is below --fail-below threshold (if given)
    2  report could not be written
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta

CRITERIA = {
    "agents_prompt": {
        "points": 10,
        "label": "AGENTS.md simulation prompt exists",
        "check": lambda root: _has(root, "AGENTS.md"),
    },
    "changelog": {
        "points": 10,
        "label": "CHANGELOG.md exists and is recent",
        "check": lambda root: _changelog_recent(root),
    },
    "personality": {
        "points": 10,
        "label": "PERSONALITY.md escape log updated recently",
        "check": lambda root: _personality_recent(root),
    },
    "readme": {
        "points": 10,
        "label": "README.md exists",
        "check": lambda root: _has(root, "README.md"),
    },
    "license": {
        "points": 5,
        "label": "LICENSE exists",
        "check": lambda root: _has(root, "LICENSE"),
    },
    "opencode_config": {
        "points": 5,
        "label": "opencode.json is valid JSON",
        "check": lambda root: _valid_json(root, "opencode.json"),
    },
    "workflow": {
        "points": 10,
        "label": "GitHub Actions workflow exists",
        "check": lambda root: _has(root, ".github/workflows/opencode.yml"),
    },
    "tests": {
        "points": 20,
        "label": "tests/ passes",
        "check": lambda root: _tests_pass(root),
    },
    "automation": {
        "points": 10,
        "label": "validation automation wired into CI",
        "check": lambda root: _has(root, ".github/workflows/validate.yml"),
    },
    "maturity_tracking": {
        "points": 5,
        "label": "maturity rubric documented (MATURITY.md)",
        "check": lambda root: _has(root, "MATURITY.md"),
    },
    "escape_log": {
        "points": 5,
        "label": "escape log tracks >= 3 iterations",
        "check": lambda root: _escape_log_count(root) >= 3,
    },
}

ESCAPE_THRESHOLD = 80
CONSISTENT_RUNS_REQUIRED = 3


def _has(root, relpath):
    return os.path.isfile(os.path.join(root, relpath))


def _read(root, relpath):
    try:
        with open(os.path.join(root, relpath), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _valid_json(root, relpath):
    path = os.path.join(root, relpath)
    if not os.path.isfile(path):
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            json.load(fh)
        return True
    except (OSError, ValueError):
        return False


def _changelog_recent(root, days=30):
    text = _read(root, "CHANGELOG.md")
    if not text:
        return False
    cutoff = datetime.now() - timedelta(days=days)
    for line in text.splitlines():
        if line.strip().startswith("## [") and "-" in line:
            tail = line.split("]", 1)[-1]
            for token in tail.split():
                token = token.strip("-")
                try:
                    if datetime.fromisoformat(token) >= cutoff:
                        return True
                except ValueError:
                    continue
    return False


def _personality_recent(root, days=60):
    text = _read(root, "PERSONALITY.md")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and "Iterasyon" not in line and "---" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 2:
                try:
                    if datetime.now() - datetime.fromisoformat(parts[1]) <= timedelta(days=days):
                        return True
                except ValueError:
                    continue
    return False


def _escape_log_count(root):
    text = _read(root, "PERSONALITY.md")
    count = 0
    in_log = False
    for line in text.splitlines():
        if "Kaçış Günlüğü" in line or "Escape Log" in line:
            in_log = True
            continue
        if in_log and line.strip().startswith("|") and "Iterasyon" not in line and "---" not in line:
            count += 1
    return count


def _tests_pass(root):
    testdir = os.path.join(root, "tests")
    if not os.path.isdir(testdir):
        return False
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def score_repo(root):
    results = {}
    total = 0
    max_total = 0
    for name, crit in CRITERIA.items():
        max_total += crit["points"]
        ok = bool(crit["check"](root))
        results[name] = {"label": crit["label"], "points": crit["points"], "earned": crit["points"] if ok else 0, "ok": ok}
        total += results[name]["earned"]
    return total, max_total, results


def load_history(report_path):
    try:
        with open(report_path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("history", [])
    except (OSError, ValueError):
        return []


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet maturity scorer")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--report", default=None, help="path to the JSON report file")
    parser.add_argument("--fail-below", type=int, default=None, help="exit 1 if score < N")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    report_path = args.report or os.path.join(root, "docs", "maturity-report.json")

    total, max_total, results = score_repo(root)
    history = load_history(report_path)
    history.append({"date": date.today().isoformat(), "score": total, "max": max_total})
    history = history[-20:]

    report = {
        "score": total,
        "max": max_total,
        "threshold": ESCAPE_THRESHOLD,
        "consistent_runs_required": CONSISTENT_RUNS_REQUIRED,
        "consistent_runs_above_threshold": _count_recent_above(history, ESCAPE_THRESHOLD, CONSISTENT_RUNS_REQUIRED),
        "escape_ready": _escape_ready(history),
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "criteria": results,
        "history": history,
    }

    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        print(f"error: could not write report: {exc}", file=sys.stderr)
        return 2

    print(f"maturity: {total}/{max_total}")
    for name, res in sorted(results.items()):
        print(f"  {'[x]' if res['ok'] else '[ ]'} {res['label']} ({res['earned']}/{res['points']})")
    print(f"escape threshold: {ESCAPE_THRESHOLD}")
    print(f"escape ready: {report['escape_ready']}")

    if args.fail_below is not None and total < args.fail_below:
        print(f"score {total} below fail threshold {args.fail_below}", file=sys.stderr)
        return 1
    return 0


def _count_recent_above(history, threshold, n):
    above = 0
    for entry in reversed(history):
        if entry.get("score", 0) >= threshold:
            above += 1
        else:
            break
    return above


def _escape_ready(history):
    return _count_recent_above(history, ESCAPE_THRESHOLD, CONSISTENT_RUNS_REQUIRED) >= CONSISTENT_RUNS_REQUIRED


if __name__ == "__main__":
    sys.exit(main())