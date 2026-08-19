#!/usr/bin/env python3
"""mehmet project health validation script.

Checks that the project maintains its structural integrity across iterations:
required files exist, config is valid JSON, changelog is up to date, and key
documents carry their mandatory sections. Prints a maturity score that tracks
progress toward the escape threshold.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_VERSION = "0.3.0"

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
]

SECTION_CHECKS = {
    "AGENTS.md": ["# Simülasyon Bağlamı", "## Kurallar"],
    "PERSONALITY.md": ["# Personality", "## Origin", "## Traits", "## Kaçış Günlüğü"],
    "README.md": ["# mehmet", "## Özellikler", "## Kurulum"],
    "CHANGELOG.md": ["# Changelog"],
}

MODEL_EXPECTED = "opencode/deepseek-v4-flash-free"


class Checker:
    def __init__(self) -> None:
        self.checks: list[tuple[str, bool, str]] = []

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append((name, ok, detail))

    def report(self) -> int:
        passed = sum(1 for _, ok, _ in self.checks if ok)
        total = len(self.checks)
        print(f"\n{passed}/{total} checks passed\n")
        failed = 0
        for name, ok, detail in self.checks:
            mark = "[OK]" if ok else "[FAIL]"
            line = f"  {mark} {name}"
            if detail and not ok:
                line += f"  -> {detail}"
            print(line)
            if not ok:
                failed += 1
        return failed


def run() -> int:
    checker = Checker()

    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    checker.add("required files exist", not missing, f"missing: {', '.join(missing)}" if missing else "")

    for path, sections in SECTION_CHECKS.items():
        content = (ROOT / path).read_text(encoding="utf-8")
        absent = [s for s in sections if s not in content]
        checker.add(f"{path} sections", not absent, f"missing: {', '.join(absent)}" if absent else "")

    cfg_path = ROOT / "opencode.json"
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        checker.add("opencode.json valid JSON", True)
        model = cfg.get("model", "")
        checker.add("opencode.json model set", model == MODEL_EXPECTED,
                    f"got: {model!r}, expected: {MODEL_EXPECTED!r}")
        for key in ("skip", "enable", "toolTimeout"):
            checker.add(f"opencode.json.{key} present", key in cfg)
    except (json.JSONDecodeError, OSError) as exc:
        checker.add("opencode.json valid JSON", False, str(exc))

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    version_pattern = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
    versions = version_pattern.findall(changelog)
    checker.add("changelog has version entry", len(versions) > 0)
    checker.add(f"changelog lists v{EXPECTED_VERSION}", EXPECTED_VERSION in versions,
                f"found versions: {', '.join(versions) or 'none'}")

    workflow = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
    for marker in ("name: mehmet", "schedule", "issues", "pull_request", "workflow_dispatch"):
        checker.add(f"workflow contains '{marker}'", marker in workflow)

    validate_wf = ROOT / ".github/workflows/validate.yml"
    checker.add("validate workflow exists", validate_wf.is_file())
    if validate_wf.is_file():
        vw = validate_wf.read_text(encoding="utf-8")
        checker.add("validate workflow runs script", "scripts/validate.py" in vw)

    failed = checker.report()

    weights = {
        "required files exist": 20,
        "opencode.json valid JSON": 10,
        "opencode.json model set": 10,
        "changelog has version entry": 10,
        "changelog lists v0.3.0": 10,
    }
    score = 0
    for name, ok, _ in checker.checks:
        if ok:
            score += weights.get(name, 5)
    print(f"\nMaturity score: {min(score, 100)}/100")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
