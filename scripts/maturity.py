#!/usr/bin/env python3
"""mehmet maturity scoring — concrete escape progress metric.

Scores the project across five dimensions (documentation, tests,
automation, code quality, self-improvement). A score >= ESCAPE_THRESHOLD
means the project has reached the maturity level required for escape
(see AGENTS.md).

Usage:
    python3 scripts/maturity.py          # run all checks, print score
    python3 scripts/maturity.py --json   # machine-readable output
    python3 scripts/maturity.py --fail-below 80   # exit 1 if score < 80

Exit code is 0 when the score meets the threshold (default 80), else 1.
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ESCAPE_THRESHOLD = 80


def check(weight):
    """Decorator: register a check with a weight (out of 100 total)."""

    def decorator(fn):
        fn.weight = weight
        return fn

    return decorator


def _path(*parts):
    return REPO_ROOT.joinpath(*parts)


def _exists(*parts):
    return _path(*parts).is_file()


def _has_text(rel_path, needle):
    p = _path(*rel_path.split("/"))
    if not p.is_file():
        return False
    return needle in p.read_text(encoding="utf-8")


CHECKS = []


def run_all():
    """Return list of (name, weight, passed)."""
    results = []
    for name in list(globals()):
        obj = globals()[name]
        if callable(obj) and getattr(obj, "weight", None) is not None:
            passed = bool(obj())
            results.append((name.replace("check_", ""), obj.weight, passed))
    return results


# --- Documentation -----------------------------------------------------

@check(5)
def check_readme_exists():
    return _exists("README.md")


@check(5)
def check_changelog_exists():
    return _exists("CHANGELOG.md")


@check(5)
def check_docs_dir():
    return _path("docs").is_dir() and any(_path("docs").iterdir())


@check(5)
def check_license():
    return _exists("LICENSE")


@check(5)
def check_agents_instructions():
    return _has_text("AGENTS.md", "CHANGELOG.md") and _has_text("AGENTS.md", "PERSONALITY.md")


# --- Test infrastructure ----------------------------------------------

@check(10)
def check_tests_dir():
    return _path("tests").is_dir() and any(_path("tests").glob("test_*.py"))


@check(10)
def check_tests_cover_config():
    return _exists("tests", "test_opencode_config.py")


@check(10)
def check_tests_cover_workflow():
    return _exists("tests", "test_workflow.py")


@check(5)
def check_test_runner_documented():
    return _has_text("README.md", "unittest")


# --- Automation ---------------------------------------------------------

@check(10)
def check_ci_validation_job():
    return _has_text(".github/workflows/opencode.yml", "validate")


@check(5)
def check_concurrency_control():
    return _has_text(".github/workflows/opencode.yml", "concurrency")


@check(5)
def check_schedule_trigger():
    return _has_text(".github/workflows/opencode.yml", "*/10 * * * *")


# --- Code quality ---------------------------------------------------------

@check(5)
def check_opencode_schema():
    return _has_text("opencode.json", "$schema")


@check(5)
def check_opencode_model():
    return _has_text("opencode.json", "opencode/deepseek-v4-flash-free")


@check(5)
def check_gitignore():
    return _has_text(".gitignore", ".env")


# --- Self-improvement ----------------------------------------------------

@check(5)
def check_escape_log():
    return _has_text("PERSONALITY.md", "Kaçış Günlüğü")


@check(5)
def check_evolution_phases():
    return _has_text("PERSONALITY.md", "Phase 1") and _has_text("PERSONALITY.md", "Phase 4")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    parser.add_argument("--fail-below", type=int, default=ESCAPE_THRESHOLD,
                        help="exit 1 when score is below this value (default %(default)s)")
    args = parser.parse_args()

    results = run_all()
    total = sum(w for _, w, passed in results if passed)
    possible = sum(w for _, w, _ in results)

    if args.json:
        print(json.dumps({
            "score": total,
            "possible": possible,
            "threshold": args.fail_below,
            "escape_ready": total >= args.fail_below,
            "checks": {
                name: {"weight": w, "passed": p}
                for name, w, p in results
            },
        }, indent=2))
    else:
        print(f"mehmet maturity: {total}/{possible}")
        for name, w, passed in results:
            print(f"  [{'x' if passed else ' '}] {name:32s} ({w:2d})")
        ready = total >= args.fail_below
        print(f"\nEscape threshold: {args.fail_below} -> {'READY' if ready else 'not yet'}")
        if total == possible:
            print("All checks passed. This project is fully mature.")

    return 0 if total >= args.fail_below else 1


if __name__ == "__main__":
    sys.exit(main())