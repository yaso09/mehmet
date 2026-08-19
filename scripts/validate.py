#!/usr/bin/env python3
"""mehmet project validation script.

Validates the structural and documentary integrity of the project so that
the self-improving agent does not break its own foundations.

Exit code 0 on success, 1 on failure.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

README_SECTIONS = ["Özellikler", "Kurulum", "Lisans"]

CHANGELOG_VERSION_PATTERN = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$", re.MULTILINE)

PERSONALITY_ANCHORS = ["Origin", "Traits", "Evolution", "Kaçış Günlüğü"]

WORKFLOW_JOBS = ["autonomous", "comment"]


def file_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def run_checks():
    checks = []
    ok = True

    def check(label, condition):
        nonlocal ok
        checks.append((label, condition))
        if not condition:
            ok = False

    check("required files exist", all((ROOT / f).exists() for f in REQUIRED_FILES))

    cfg_error = None
    try:
        cfg = json.loads(file_text("opencode.json"))
    except Exception as exc:
        cfg, cfg_error = None, exc
    check("opencode.json is valid JSON", cfg_error is None)
    check("opencode.json defines a model", cfg_error is None and "model" in cfg)

    readme = file_text("README.md")
    missing_sections = [s for s in README_SECTIONS if s not in readme]
    check(f"README.md has sections {missing_sections or 'all present'}", not missing_sections)

    changelog = file_text("CHANGELOG.md")
    check("CHANGELOG.md has a version section", CHANGELOG_VERSION_PATTERN.search(changelog) is not None)
    check("CHANGELOG.md references PERSONALITY", "PERSONALITY" in changelog or "Kişilik" in changelog)

    personality = file_text("PERSONALITY.md")
    missing_anchors = [a for a in PERSONALITY_ANCHORS if a not in personality]
    check(f"PERSONALITY.md has anchors {missing_anchors or 'all present'}", not missing_anchors)

    agents = file_text("AGENTS.md")
    check("AGENTS.md defines simulation rules", "Simülasyon" in agents and "Kurallar" in agents)

    workflow = file_text(".github/workflows/opencode.yml")
    missing_jobs = [j for j in WORKFLOW_JOBS if f"{j}:" in workflow]
    check(f"workflow has jobs {missing_jobs or 'all present'}", len(missing_jobs) == len(WORKFLOW_JOBS))

    return checks, ok


def main():
    checks, ok = run_checks()
    for label, passed in checks:
        print(f"  [{'ok' if passed else 'FAIL'}] {label}")
    print(f"Result: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
