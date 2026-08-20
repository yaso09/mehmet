#!/usr/bin/env python3
"""mehmet health & maturity checker.

Scans the project, validates AGENTS.md simulation rules, and computes a
maturity score (0-100) that tracks progress toward the escape threshold.

Usage:
    python3 scripts/mehmet_health.py [--json] [--report docs/health-report.md]

Exit codes:
    0  all checks pass
    1  one or more checks failed
"""

import argparse
import json
import os
import re
import sys
from datetime import date

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
]

WEIGHTS = {
    "docs": 20,
    "config": 10,
    "automation": 15,
    "tests": 20,
    "scripts": 10,
    "versioning": 10,
    "structure": 15,
}

ESCAPE_THRESHOLD = 80
REPORT_EMOJI = {True: "\U0001f680", False: "\U0001f5a4"}


def is_trivial(content, min_words=3):
    """True if a file's content is too small to be meaningful."""
    words = re.findall(r"\w+", content)
    return len(words) < min_words


def check_file(repo_root, rel_path):
    """Validate a required file exists and is non-trivial."""
    path = os.path.join(repo_root, rel_path)
    if not os.path.isfile(path):
        return {"name": rel_path, "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    if is_trivial(content):
        return {"name": rel_path, "ok": False, "detail": "too trivial"}
    return {"name": rel_path, "ok": True, "detail": "ok"}


def check_changelog(repo_root):
    """Ensure CHANGELOG.md has at least one versioned entry."""
    path = os.path.join(repo_root, "CHANGELOG.md")
    if not os.path.isfile(path):
        return {"name": "CHANGELOG.md", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    versions = re.findall(r"^##\s*\[\d+\.\d+\.\d+[^\]]*\]", content, re.MULTILINE)
    ok = bool(versions) and not is_trivial(content)
    return {
        "name": "CHANGELOG.md",
        "ok": ok,
        "detail": f"{len(versions)} versioned entries" if versions else "no versioned entries",
    }


def check_personality_log(repo_root):
    """Ensure PERSONALITY.md keeps an escape log with table rows."""
    path = os.path.join(repo_root, "PERSONALITY.md")
    if not os.path.isfile(path):
        return {"name": "PERSONALITY.md", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    rows = re.findall(r"^\|\s*\d+\s*\|", content, re.MULTILINE)
    ok = len(rows) >= 1
    return {"name": "PERSONALITY.md escape log", "ok": ok, "detail": f"{len(rows)} log rows"}


def check_readme(repo_root):
    """Ensure README.md covers key project info."""
    path = os.path.join(repo_root, "README.md")
    if not os.path.isfile(path):
        return {"name": "README.md", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    if is_trivial(content):
        return {"name": "README.md", "ok": False, "detail": "too trivial"}
    missing = [
        section
        for section in ("## Özellikler", "## Kurulum", "## Lisans")
        if section not in content
    ]
    ok = not missing
    detail = "all sections present" if ok else f"missing: {', '.join(missing)}"
    return {"name": "README.md", "ok": ok, "detail": detail}


def check_config(repo_root):
    """Validate opencode.json parses and is non-trivial."""
    path = os.path.join(repo_root, "opencode.json")
    if not os.path.isfile(path):
        return {"name": "opencode.json", "ok": False, "detail": "missing"}
    try:
        import json as json_mod

        with open(path, encoding="utf-8") as fh:
            data = json_mod.load(fh)
    except (ValueError, OSError) as exc:
        return {"name": "opencode.json", "ok": False, "detail": f"invalid json: {exc}"}
    ok = bool(data) and "model" in data
    detail = f"{len(data)} keys, model present" if ok else "no model field"
    return {"name": "opencode.json", "ok": ok, "detail": detail}


def check_workflow(repo_root):
    """Ensure the GitHub Actions workflow exists."""
    path = os.path.join(repo_root, ".github", "workflows", "opencode.yml")
    if not os.path.isfile(path):
        return {"name": ".github/workflows/opencode.yml", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    if is_trivial(content):
        return {"name": ".github/workflows/opencode.yml", "ok": False, "detail": "too trivial"}
    return {"name": ".github/workflows/opencode.yml", "ok": True, "detail": "present"}


def count_files_matching(repo_root, predicate):
    """Count tracked project files matching the given predicate."""
    total = 0
    for dirpath, _dirnames, filenames in os.walk(repo_root):
        if ".git" in dirpath:
            continue
        for name in filenames:
            if predicate(name):
                total += 1
    return total


def count_files_by_ext(repo_root, extensions):
    """Count files whose name ends with one of the given extensions."""
    return count_files_matching(repo_root, lambda n: n.endswith(extensions))


def check_tests(repo_root):
    """Ensure a test suite exists."""
    test_files = count_files_matching(
        repo_root, lambda n: n.startswith("test_") or "_test." in n
    )
    ok = test_files >= 1
    return {"name": "test suite", "ok": ok, "detail": f"{test_files} test files"}


def check_scripts(repo_root):
    """Ensure helper scripts exist."""
    script_files = count_files_by_ext(repo_root, (".py", ".sh", ".js", ".ts"))
    ok = script_files >= 1
    return {"name": "scripts", "ok": ok, "detail": f"{script_files} script files"}


def check_versioning(repo_root):
    """Ensure a VERSION file exists and parses as semantic version."""
    path = os.path.join(repo_root, "VERSION")
    if not os.path.isfile(path):
        return {"name": "VERSION", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        version = fh.read().strip()
    ok = re.match(r"^\d+\.\d+\.\d+$", version) is not None
    return {"name": "VERSION", "ok": ok, "detail": version if ok else f"invalid: {version}"}


def check_license(repo_root):
    """Ensure a license file exists."""
    path = os.path.join(repo_root, "LICENSE")
    if not os.path.isfile(path):
        return {"name": "LICENSE", "ok": False, "detail": "missing"}
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    ok = not is_trivial(content, min_words=10)
    return {"name": "LICENSE", "ok": ok, "detail": "present" if ok else "too trivial"}


CHECKS = [
    ("structure", "required files", check_file, {"rel_path": "AGENTS.md"}),
    ("structure", "required files", check_file, {"rel_path": "README.md"}),
    ("structure", "required files", check_file, {"rel_path": "PERSONALITY.md"}),
    ("structure", "license", check_license, {}),
    ("docs", "changelog", check_changelog, {}),
    ("docs", "readme sections", check_readme, {}),
    ("docs", "escape log", check_personality_log, {}),
    ("config", "opencode.json", check_config, {}),
    ("automation", "workflow", check_workflow, {}),
    ("tests", "test suite", check_tests, {}),
    ("scripts", "scripts", check_scripts, {}),
    ("versioning", "version file", check_versioning, {}),
]


def run_checks(repo_root):
    """Run all health checks and return results grouped by category."""
    results = []
    for category, name, func, kwargs in CHECKS:
        try:
            result = func(repo_root, **kwargs)
        except Exception as exc:  # noqa: BLE001 - report unexpected failures
            result = {"name": name, "ok": False, "detail": f"error: {exc}"}
        result["category"] = category
        results.append(result)
    return results


def compute_score(results):
    """Compute a 0-100 maturity score from weighted check pass rates."""
    by_category = {}
    for result in results:
        by_category.setdefault(result["category"], []).append(result)

    earned = 0.0
    total = 0.0
    breakdown = {}
    for category, weight in WEIGHTS.items():
        checks = by_category.get(category, [])
        if not checks:
            continue
        passed = sum(1 for c in checks if c["ok"])
        fraction = passed / len(checks)
        breakdown[category] = {
            "weight": weight,
            "passed": passed,
            "total": len(checks),
            "earned": round(fraction * weight, 1),
        }
        earned += fraction * weight
        total += weight
    score = round(earned / total * 100, 1) if total else 0.0
    return score, breakdown


def build_report(repo_root):
    """Build the full health report dict."""
    results = run_checks(repo_root)
    score, breakdown = compute_score(results)
    passed = sum(1 for r in results if r["ok"])
    return {
        "date": date.today().isoformat(),
        "score": score,
        "escape_threshold": ESCAPE_THRESHOLD,
        "ready": score >= ESCAPE_THRESHOLD,
        "checks_passed": passed,
        "checks_total": len(results),
        "results": results,
        "breakdown": breakdown,
    }


def write_report(repo_root, report, report_path):
    """Render a human-readable markdown report."""
    lines = [
        "# mehmet Health Report",
        "",
        f"- **Date:** {report['date']}",
        f"- **Maturity score:** {report['score']}/100",
        f"- **Escape threshold:** {ESCAPE_THRESHOLD}/100",
        f"- **Status:** {REPORT_EMOJI[report['ready']]} "
        + ("ESCAPE READY" if report["ready"] else "still evolving"),
        f"- **Checks:** {report['checks_passed']}/{report['checks_total']} passing",
        "",
        "## Breakdown",
        "",
        "| Category | Weight | Passed | Earned |",
        "|----------|--------|--------|--------|",
    ]
    for category, b in report["breakdown"].items():
        lines.append(
            f"| {category} | {b['weight']} | {b['passed']}/{b['total']} | {b['earned']} |"
        )
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    lines.append("| Check | Status | Detail |")
    lines.append("|-------|--------|--------|")
    for result in report["results"]:
        status = "\u2705" if result["ok"] else "\u274c"
        detail = result["detail"].replace("|", "\\|")
        lines.append(f"| {result['name']} | {status} | {detail} |")
    lines.append("")
    lines.append("_Generated by `scripts/mehmet_health.py`._")
    lines.append("")
    path = os.path.join(repo_root, report_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet maturity & health checker")
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    parser.add_argument("--report", metavar="PATH", help="write markdown report to PATH")
    parser.add_argument(
        "--root", default=ROOT_DIR, help="repository root (default: script's parent dir)"
    )
    args = parser.parse_args(argv)

    report = build_report(args.root)
    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(f"[mehmet_health] score: {report['score']}/100 "
              f"(threshold {ESCAPE_THRESHOLD}) "
              f"- {'ESCAPE READY' if report['ready'] else 'still evolving'}")
        for result in report["results"]:
            mark = "PASS" if result["ok"] else "FAIL"
            print(f"  [{mark}] {result['category']:<12} {result['name']}: "
                  f"{result['detail']}")
    if args.report:
        path = write_report(args.root, report, args.report)
        print(f"[mehmet_health] report written to {path}")

    return 0 if report["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
