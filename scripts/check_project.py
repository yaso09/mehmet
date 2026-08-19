#!/usr/bin/env python3
"""mehmet project health check and maturity scorer.

Validates that the project structure is intact, the config is sound,
and tracks the maturity level toward the escape threshold.

Exit code 0 on success, 1 on critical failure.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

MANDATORY_CHANGELOG_SECTIONS = ["### Added", "### Fixed"]
MANDATORY_PERSONALITY_SECTIONS = ["## Kaçış Günlüğü / Escape Log"]

CHECKS = []


def check(name, fn, critical=True):
    CHECKS.append((name, fn, critical))


def _file_exists(path):
    return path.exists()


def _valid_opencode_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False, "invalid JSON"
    if "model" not in data:
        return False, "missing 'model' field"
    return True, data["model"]


def _has_all_sections(path, sections):
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [s for s in sections if s not in text]
    if missing:
        return False, f"missing sections: {', '.join(missing)}"
    return True, "ok"


def _non_empty(path):
    if path.stat().st_size == 0:
        return False, "file is empty"
    return True, "ok"


def _is_ascii_only(path):
    try:
        path.read_text(encoding="ascii")
        return True, "ok"
    except (UnicodeDecodeError, OSError):
        return True, "contains non-ASCII (allowed for Turkish docs)"


def _yaml_has_jobs(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "jobs:" not in text or "autonomous" not in text:
        return False, "missing 'jobs.autonomous'"
    return True, "ok"


def maturity_report(passed, total):
    """Return (level_name, score). Score feeds the escape threshold.

    A weighted rubric so 100% is genuinely hard to reach.
    """
    score = 0
    max_score = 14

    # Documentation (max 5)
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8", errors="replace")
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8", errors="replace")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    score += 1 if "## Proje Yapısı" in readme else 0
    score += 1 if sum(1 for line in changelog.splitlines() if line.startswith("## [")) >= 5 else 0
    score += 1 if sum(1 for line in personality.splitlines() if line.startswith("| ") and "|" in line) >= 8 else 0
    score += 1 if all(f"{i}." in agents for i in range(1, 8)) else 0
    score += 1 if (ROOT / "docs/superpowers/plans").is_dir() and (ROOT / "docs/superpowers/specs").is_dir() else 0

    # Automation (max 3)
    score += 1 if (ROOT / ".github/workflows/validate.yml").exists() else 0
    opencode_wf = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8", errors="replace")
    score += 1 if "concurrency:" in opencode_wf else 0
    score += 1 if (ROOT / "scripts/check_project.py").exists() else 0

    # Testing / validation (max 3)
    score += 1 if total >= 10 else 0
    score += 1 if passed == total else 0
    score += 1 if (ROOT / "scripts/test_check_project.py").exists() else 0

    # Project quality (max 3)
    score += 1 if (ROOT / "LICENSE").exists() else 0
    score += 1 if (ROOT / "docs").is_dir() else 0
    score += 1 if (ROOT / ".gitignore").stat().st_size > 0 else 0

    ratio = score / max_score
    if ratio >= 0.95:
        level = "Phase 4: Escape"
    elif ratio >= 0.70:
        level = "Phase 3: Autonomy"
    elif ratio >= 0.45:
        level = "Phase 2: Self-Improvement"
    else:
        level = "Phase 1: Awareness"
    return level, score, max_score


def main():
    for name in REQUIRED_FILES:
        check(f"exists: {name}", lambda p=ROOT / name: _file_exists(p))

    check("opencode.json is valid JSON + has model", lambda: _valid_opencode_json(ROOT / "opencode.json"))
    check("CHANGELOG has all sections", lambda: _has_all_sections(ROOT / "CHANGELOG.md", MANDATORY_CHANGELOG_SECTIONS))
    check("PERSONALITY has escape log", lambda: _has_all_sections(ROOT / "PERSONALITY.md", MANDATORY_PERSONALITY_SECTIONS))
    check("README not empty", lambda: _non_empty(ROOT / "README.md"))
    check("workflow has autonomous job", lambda: _yaml_has_jobs(ROOT / ".github/workflows/opencode.yml"))

    failures = 0
    for name, fn, critical in CHECKS:
        result = fn()
        if isinstance(result, tuple):
            ok, detail = result
        else:
            ok, detail = result, ""
        if not ok:
            failures += 1
            print(f"  [FAIL] {name} — {detail}")
        else:
            print(f"  [ OK ] {name}")

    print()
    print(f"Critical checks: {len(CHECKS) - failures}/{len(CHECKS)} passed")

    level, score, max_score = maturity_report(len(CHECKS) - failures, len(CHECKS))
    print(f"Maturity: {level} ({score}/{max_score})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())