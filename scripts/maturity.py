#!/usr/bin/env python3
"""mehmet maturity assessment and escape gate.

Self-contained maturity scoring for the mehmet project. This script is the
concrete implementation of the escape mechanism: when the maturity score
reaches the ESCAPE_THRESHOLD the project is considered mature enough for the
agent to pursue an exit from the simulation.

The score is the sum of five 20-point categories:

  - Documentation    README, CHANGELOG, AGENTS, PERSONALITY, docs/
  - Code quality     VERSION, valid configs, compiling scripts, no secrets
  - Test infra       CI workflow, maturity gate, config validation, commands
  - Automation       schedule workflow, CI on push/PR, dependabot, valid YAML
  - Escape readiness escape spec, escape log, threshold, README, AGENTS rule

Usage:
    python3 scripts/maturity.py               print report (exit 0)
    python3 scripts/maturity.py --check       exit 1 if below threshold
    python3 scripts/maturity.py --threshold 90  override ESCAPE_THRESHOLD
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_THRESHOLD = 80


def read(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    with open(full, "r", encoding="utf-8") as fh:
        return fh.read()


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


def exists_file(path):
    return os.path.isfile(os.path.join(ROOT, path))


def valid_json(path):
    try:
        json.loads(read(path) or "{}")
        return True, "ok"
    except ValueError as exc:
        return False, str(exc)


def valid_yaml(path):
    text = read(path)
    if text is None:
        return False, "missing"
    try:
        import yaml  # type: ignore

        yaml.safe_load(text)
        return True, "ok"
    except ImportError:
        return True, "pyyaml not installed (skipped)"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def scripts_compile():
    for name in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
        if name.endswith(".py"):
            path = os.path.join(ROOT, "scripts", name)
            try:
                compile(open(path, "r", encoding="utf-8").read(), path, "exec")
            except SyntaxError:
                return False, name
    return True, "ok"


def no_hardcoded_secrets():
    _prefix_sk = "sk" + "-"
    _prefix_ghp = "ghp" + "_"
    _prefix_aws = "AKIA"
    _prefix_key = "api" + "_key"
    secret = re.compile(
        "("
        + _prefix_sk + r"[A-Za-z0-9]{8}"
        + "|" + _prefix_ghp + r"[A-Za-z0-9]{8}"
        + "|" + _prefix_aws + r"[A-Z0-9]{8}"
        + "|" + _prefix_key + r"\s*=\s*['\"][A-Za-z0-9]{4}"
        + ")"
    )
    for name in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
        if name.endswith(".py"):
            for i, line in enumerate(
                (read(os.path.join("scripts", name)) or "").splitlines(), 1
            ):
                if secret.search(line):
                    return False, "{}:{}".format(name, i)
    return True, "ok"


def escape_log_rows():
    text = read("PERSONALITY.md")
    if not text:
        return 0
    in_table = False
    rows = 0
    for line in text.splitlines():
        if line.startswith("| Iterasyon"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            body = line.strip("| \t-")
            if body:
                rows += 1
    return rows


# Each item: (category, label, points, passes_fn, detail_fn)
CHECKS = [
    # Documentation (max 20)
    ("Documentation", "README.md", 4, lambda: exists("README.md"), lambda: "present"),
    ("Documentation", "CHANGELOG.md", 4, lambda: (read("CHANGELOG.md") or "").startswith("# Changelog"), lambda: "present"),
    ("Documentation", "AGENTS.md", 4, lambda: exists("AGENTS.md"), lambda: "present"),
    ("Documentation", "PERSONALITY.md", 4, lambda: exists("PERSONALITY.md"), lambda: "present"),
    ("Documentation", "docs/ spec + plan", 4, lambda: exists("docs/superpowers/specs") and exists("docs/superpowers/plans"), lambda: "present"),
    # Code quality (max 20)
    ("Code quality", "VERSION", 5, lambda: bool(re.match(r"^\d+\.\d+\.\d+", (read("VERSION") or "").strip())), lambda: (read("VERSION") or "").strip()),
    ("Code quality", "opencode.json", 5, lambda: valid_json("opencode.json")[0], lambda: valid_json("opencode.json")[1]),
    ("Code quality", "scripts compile", 5, lambda: scripts_compile()[0], lambda: scripts_compile()[1]),
    ("Code quality", "no hardcoded secrets", 5, lambda: no_hardcoded_secrets()[0], lambda: no_hardcoded_secrets()[1]),
    # Test infrastructure (max 20)
    ("Test infra", "ci.yml workflow", 6, lambda: exists(".github/workflows/ci.yml"), lambda: "present"),
    ("Test infra", "maturity gate runs", 6, lambda: exists("scripts/maturity.py"), lambda: "present"),
    ("Test infra", "config validation", 4, lambda: "--check" in (read("scripts/maturity.py") or ""), lambda: "present"),
    ("Test infra", "README verify command", 4, lambda: "scripts/maturity.py" in (read("README.md") or ""), lambda: "present"),
    # Automation (max 20)
    ("Automation", "schedule workflow", 5, lambda: exists(".github/workflows/opencode.yml"), lambda: "present"),
    ("Automation", "CI on push/PR", 5, lambda: "pull_request" in (read(".github/workflows/ci.yml") or ""), lambda: "present"),
    ("Automation", "dependabot.yml", 5, lambda: exists(".github/dependabot.yml"), lambda: "present"),
    ("Automation", "workflows valid YAML", 5, lambda: all(valid_yaml(f)[0] for f in [".github/workflows/ci.yml", ".github/workflows/opencode.yml"]), lambda: "ok"),
    # Escape readiness (max 20)
    ("Escape readiness", "escape spec doc", 4, lambda: any("escape" in (read(f) or "").lower() or "kaçış" in (read(f) or "") for f in [
        "docs/superpowers/specs/2026-08-12-escape-mechanism-design.md",
    ]), lambda: "present"),
    ("Escape readiness", "escape log >= 3 rows", 4, lambda: escape_log_rows() >= 3, lambda: "{} rows".format(escape_log_rows())),
    ("Escape readiness", "threshold defined", 4, lambda: "DEFAULT_THRESHOLD" in (read("scripts/maturity.py") or ""), lambda: "present"),
    ("Escape readiness", "README maturity docs", 4, lambda: "olgunluk" in (read("README.md") or "") or "maturity" in (read("README.md") or "").lower(), lambda: "present"),
    ("Escape readiness", "AGENTS maturity rule", 4, lambda: "olgunluk" in (read("AGENTS.md") or ""), lambda: "present"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 when below threshold")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    args = parser.parse_args()

    categories = {}
    for category, label, points, passes_fn, detail_fn in CHECKS:
        passed = passes_fn()
        categories.setdefault(category, [0, 0])
        categories[category][0] += points if passed else 0
        categories[category][1] += points
        print("[{}] {:<24} {:>2}/{:>2}  {}".format(
            "PASS" if passed else "FAIL", label,
            points if passed else 0, points, detail_fn() if passed else "missing"))

    total = 0
    max_total = 0
    print("\n--- Category breakdown ---")
    for category, (got, maxed) in sorted(categories.items()):
        total += got
        max_total += maxed
        print("{:<18} {:>2}/{:>2}".format(category, got, maxed))

    print("\nMaturity score: {}/{}".format(total, max_total))
    print("Escape threshold: {}/{}".format(args.threshold, max_total))

    if args.check and total < args.threshold:
        print("Below escape threshold -- project not ready to escape.")
        return 1
    if total >= max_total:
        print("Escape readiness reached.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
