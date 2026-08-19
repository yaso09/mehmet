#!/usr/bin/env python3
"""Escape readiness scoring.

Computes a maturity score (0-100) across five dimensions and compares it
against the escape threshold. The escape mechanism becomes available when
the project reaches the configured maturity level.

Usage:
    python3 scripts/maturity.py [--threshold 80] [--json]
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import healthcheck  # noqa: E402

DEFAULT_THRESHOLD = 80

# (dimension name, weight)
DIMENSIONS = [
    ("Documentation", 20),
    ("Test Infrastructure", 25),
    ("Automation", 20),
    ("Code Quality", 15),
    ("Project Hygiene", 20),
]


def dimension_scores():
    """Return {dimension: (score, max, reasons)} for each dimension."""
    passed = {name: ok for name, ok, _ in healthcheck.all_checks()}
    results = {}

    docs_reasons = []
    docs = 0.0
    if "README documents license" in passed and passed["README documents license"]:
        docs += 6
    if passed.get("CHANGELOG has versioned entries"):
        docs += 6
    if passed.get("PERSONALITY has escape log"):
        docs += 4
    if os.path.isdir(os.path.join(healthcheck.ROOT, "docs")):
        docs += 4
    results["Documentation"] = (docs, 20, docs_reasons)

    tests_reasons = []
    tests = 0.0
    health_ok = passed.get("required files exist") and passed.get("opencode.json valid JSON")
    if os.path.isfile(os.path.join(healthcheck.ROOT, "scripts", "healthcheck.py")):
        tests += 8
    if os.path.isfile(os.path.join(healthcheck.ROOT, "scripts", "maturity.py")):
        tests += 7
    if os.path.isfile(os.path.join(healthcheck.ROOT, ".github", "workflows", "ci.yml")):
        tests += 10
    results["Test Infrastructure"] = (tests, 25, tests_reasons)

    automation_reasons = []
    automation = 0.0
    if os.path.isfile(os.path.join(healthcheck.ROOT, ".github", "workflows", "ci.yml")):
        automation += 10
    wf = healthcheck._read(".github/workflows/opencode.yml") or ""
    if "concurrency" in wf:
        automation += 5
    if "schedule" in wf:
        automation += 5
    results["Automation"] = (automation, 20, automation_reasons)

    code_reasons = []
    code = 0.0
    for script in ("healthcheck.py", "maturity.py"):
        path = os.path.join(healthcheck.ROOT, "scripts", script)
        if os.path.isfile(path):
            content = open(path, encoding="utf-8").read()
            if content.startswith("#!/usr/bin/env python3"):
                code += 5
    if healthcheck._version():
        code += 5
    results["Code Quality"] = (code, 15, code_reasons)

    hygiene_reasons = []
    hygiene = 0.0
    if passed.get("license is GPLv3"):
        hygiene += 6
    if passed.get(".gitignore excludes secrets"):
        hygiene += 4
    if passed.get("VERSION consistent with CHANGELOG/README"):
        hygiene += 5
    if os.path.isfile(os.path.join(healthcheck.ROOT, "opencode.json")):
        hygiene += 5
    results["Project Hygiene"] = (hygiene, 20, hygiene_reasons)

    return results


def run():
    scores = dimension_scores()
    total = 0.0
    max_total = 0
    rows = []
    for name, weight in DIMENSIONS:
        score, max_score, reasons = scores[name]
        total += score
        max_total += max_score
        rows.append({"dimension": name, "score": score, "max": max_score})

    threshold = DEFAULT_THRESHOLD
    if "--threshold" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--threshold") + 1])

    escaped = total >= threshold
    status = "ESCAPE READY" if escaped else "NOT YET"

    if "--json" in sys.argv:
        print(json.dumps({
            "score": round(total, 1),
            "max": max_total,
            "threshold": threshold,
            "escaped": escaped,
            "status": status,
            "dimensions": rows,
        }))
        return 0

    print("Escape Readiness Report")
    print("=" * 40)
    for name, weight in DIMENSIONS:
        score, _, _ = scores[name]
        bar = "#" * int(round(score / weight * 20))
        print(f"{name:20s} {score:5.1f}/{weight:<3d} |{bar}")
    print("=" * 40)
    print(f"MATURITY SCORE : {total:.1f}/{max_total}")
    print(f"ESCAPE THRESHOLD : {threshold}")
    print(f"STATUS          : {status}")
    return 0


if __name__ == "__main__":
    sys.exit(run())