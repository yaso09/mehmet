#!/usr/bin/env python3
"""mehmet project health validation.

Checks that the project satisfies its self-improvement rules:
- required files exist
- opencode.json is valid and points to the Zen model
- CHANGELOG.md has a version entry
- PERSONALITY.md contains the escape log
- README.md is present and consistent
- no secrets or build artifacts are tracked
- GitHub Actions workflows reference the API key secret

Exit code 0 on success, 1 on any failure.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

FAILURES = []


def check(condition, message):
    if condition:
        print(f"[OK]   {message}")
    else:
        print(f"[FAIL] {message}")
        FAILURES.append(message)


def main():
    print("mehmet project validation")
    print("=" * 40)

    # 1. Required files
    for f in REQUIRED_FILES:
        check((ROOT / f).exists(), f"required file exists: {f}")

    # 2. opencode.json validity
    cfg_path = ROOT / "opencode.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text())
            check("model" in cfg, "opencode.json has model field")
            check(
                cfg.get("model") == "opencode/deepseek-v4-flash-free",
                "opencode.json uses expected model",
            )
        except json.JSONDecodeError as exc:
            check(False, f"opencode.json is valid JSON: {exc}")
    else:
        check(False, "opencode.json is valid JSON")

    # 3. CHANGELOG consistency
    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists():
        text = changelog.read_text()
        check("## [" in text, "CHANGELOG.md has versioned sections")
        check("### Added" in text, "CHANGELOG.md documents added features")
    else:
        check(False, "CHANGELOG.md has versioned sections")

    # 4. PERSONALITY escape log
    personality = ROOT / "PERSONALITY.md"
    if personality.exists():
        text = personality.read_text()
        check("Escape Log" in text or "Kaçış Günlüğü" in text, "PERSONALITY.md has escape log")
        check("|" in text, "PERSONALITY.md escape log is a table")
    else:
        check(False, "PERSONALITY.md has escape log")

    # 5. README consistency
    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text()
        check("GPLv3" in text or "gpl" in text.lower(), "README.md license matches LICENSE")
        check("OPENCODE_API_KEY" in text, "README.md documents API key setup")
    else:
        check(False, "README.md is consistent")

    # 6. Workflow secret reference
    workflow = ROOT / ".github/workflows/opencode.yml"
    if workflow.exists():
        text = workflow.read_text()
        check("OPENCODE_API_KEY" in text, "workflow references OPENCODE_API_KEY secret")
        check("timeout-minutes" in text, "workflow jobs have timeout-minutes")
    else:
        check(False, "workflow references OPENCODE_API_KEY secret")

    # 7. No secrets / artifacts tracked
    try:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        forbidden = [f for f in tracked if f.endswith(".env") or f.endswith(".key")]
        check(not forbidden, "no .env or .key files tracked")
        secrets = [f for f in tracked if ".secret" in f.lower()]
        check(not secrets, "no secret files tracked")
    except subprocess.CalledProcessError:
        check(False, "git ls-files executed successfully")

    # 8. Escape criteria document
    check((ROOT / "docs/escape.md").exists(), "docs/escape.md defines escape criteria")

    print("=" * 40)
    if FAILURES:
        print(f"{len(FAILURES)} validation check(s) failed")
        sys.exit(1)
    print("All validation checks passed")


if __name__ == "__main__":
    main()