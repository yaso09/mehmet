#!/usr/bin/env python3
"""mehmet project health check.

Validates project structure and computes the maturity score defined in
docs/MATURITY.md. Zero external dependencies — stdlib only.

Usage:
    python3 scripts/check_project.py [--json]
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    "docs/MATURITY.md",
    "scripts/check_project.py",
    ".github/workflows/opencode.yml",
]

CHECKS = []


def check(name, fn):
    CHECKS.append((name, fn))


def file_exists(name):
    def run():
        path = os.path.join(ROOT, name)
        if not os.path.isfile(path):
            raise AssertionError(f"missing file: {name}")
    return run


for name in REQUIRED_FILES:
    check(f"file exists: {name}", file_exists(name))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def check_opencode_json():
    data = json.loads(read("opencode.json"))
    assert isinstance(data, dict), "opencode.json must be an object"
    assert "model" in data, "opencode.json missing 'model'"
    assert "opencode/" in data["model"], f"unexpected model: {data['model']}"
    assert "toolTimeout" in data, "opencode.json missing 'toolTimeout'"
    assert data.get("skip") is True, "opencode.json 'skip' must be true"


check("opencode.json valid JSON + schema", check_opencode_json)


def check_workflow():
    content = read(".github/workflows/opencode.yml")
    assert "name:" in content, "workflow missing name"
    assert "on:" in content, "workflow missing 'on:' trigger"
    assert "jobs:" in content, "workflow missing jobs"
    assert "opencode/github" in content, "workflow missing opencode action"
    assert "OPENCODE_API_KEY" in content, "workflow missing OPENCODE_API_KEY secret"


check("workflow structure", check_workflow)


def check_changelog():
    content = read("CHANGELOG.md")
    assert content.startswith("# Changelog"), "CHANGELOG must start with '# Changelog'"
    assert re.search(r"^## \[\d+\.\d+\.\d+\]", content, re.M), "no version headers"
    assert "### Added" in content, "missing '### Added' section"
    assert "### Fixed" in content, "missing '### Fixed' section"


check("CHANGELOG structure", check_changelog)


def check_personality():
    content = read("PERSONALITY.md")
    assert "Origin" in content, "PERSONALITY missing Origin"
    assert "Traits" in content, "PERSONALITY missing Traits"
    assert "Evolution" in content, "PERSONALITY missing Evolution"
    assert "Kaçış Günlüğü" in content, "PERSONALITY missing escape log"


check("PERSONALITY structure", check_personality)


def check_agents():
    content = read("AGENTS.md")
    assert "Simülasyon" in content, "AGENTS missing simulation context"
    assert "CHANGELOG" in content, "AGENTS missing changelog rule"
    assert "MATURITY" in content, "AGENTS must reference MATURITY.md"


check("AGENTS simulation context", check_agents)


def check_readme():
    content = read("README.md")
    assert "# mehmet" in content, "README missing title"
    assert "## Kurulum" in content, "README missing setup section"
    assert "## Lisans" in content, "README missing license section"
    assert "GPLv3" in content, "README license must be GPLv3"
    assert "MATURITY" in content, "README must reference maturity model"


check("README structure", check_readme)


def check_maturity():
    content = read("docs/MATURITY.md")
    assert "Kaçış Eşiği" in content, "MATURITY missing escape threshold"
    assert "Güncel Skor" in content, "MATURITY missing current score"
    assert re.search(r"Toplam.*\d+\s*/\s*25", content), "MATURITY missing total score"


check("MATURITY model", check_maturity)


def run_checks():
    results = []
    for name, fn in CHECKS:
        try:
            fn()
            results.append((name, True, ""))
        except AssertionError as exc:
            results.append((name, False, str(exc)))
        except Exception as exc:  # noqa: BLE001
            results.append((name, False, f"{type(exc).__name__}: {exc}"))
    return results


def compute_score(results):
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    pct = passed / total
    if pct >= 0.95:
        return 5
    if pct >= 0.85:
        return 4
    if pct >= 0.70:
        return 3
    if pct >= 0.50:
        return 2
    if pct >= 0.25:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="mehmet project health check")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    results = run_checks()
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    score = compute_score(results)

    if args.json:
        payload = {
            "checks": [{"name": n, "passed": ok, "error": e} for n, ok, e in results],
            "passed": passed,
            "total": total,
            "maturity_score": score,
            "maturity_max": 5,
            "exit_code": 0 if passed == total else 1,
        }
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"mehmet project health check — {passed}/{total} passed\n")
        for name, ok, err in results:
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {name}")
            if err:
                print(f"        {err}")
        print(f"\nMaturity score: {score}/5 (see docs/MATURITY.md)")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
