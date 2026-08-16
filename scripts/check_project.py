#!/usr/bin/env python3
"""mehmet — Project Health Check & Maturity Score.

Validates the project structure and computes a maturity score (0-100).
This is the escape-progress measurement tool: each iteration the agent runs it
and records the score in MATURITY.md.

Usage:
    python3 scripts/check_project.py          # run checks + update MATURITY.md
    python3 scripts/check_project.py --check  # run checks only (CI mode)
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATURITY_FILE = ROOT / "MATURITY.md"

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "MATURITY.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
    ".github/workflows/opencode.yml",
    ".github/workflows/health.yml",
]

SECRET_PATTERNS = [
    re.compile(r"(?i)OPENCODE_API_KEY\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"(?i)\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
]


def check_required_files():
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).exists()]
    if missing:
        print("FAIL: Missing required files:")
        for name in missing:
            print(f"  - {name}")
        return False
    return True


def check_json():
    try:
        json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        return True
    except (ValueError, OSError) as exc:
        print(f"FAIL: opencode.json is not valid JSON: {exc}")
        return False


def check_yaml():
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        print("WARN: PyYAML not available; skipping YAML validation")
        return True
    try:
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            list(yaml.safe_load_all(wf.read_text(encoding="utf-8")))
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: workflow YAML is invalid: {exc}")
        return False


def check_no_secrets():
    bad = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                bad.append(str(path.relative_to(ROOT)))
                break
    if bad:
        print("FAIL: Possible secrets committed in files:")
        for name in bad:
            print(f"  - {name}")
        return False
    return True


def check_changelog():
    try:
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL: cannot read CHANGELOG.md: {exc}")
        return False
    if re.search(r"## \[\d+\.\d+\.\d+\]", content) and "### Added" in content:
        return True
    print("FAIL: CHANGELOG.md is missing version entries or '### Added' sections")
    return False


def check_readme_links():
    try:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL: cannot read README.md: {exc}")
        return False
    # Inline/relative markdown links that should resolve inside the repo
    for target in re.findall(r"\[[^\]]*\]\(([^)#]+)\)", content):
        if "://" in target:
            continue
        candidate = (ROOT / target.lstrip("/")).resolve()
        if not candidate.exists():
            print(f"FAIL: README.md link target not found: {target}")
            return False
    return True


def run_checks():
    checks = {
        "required_files": check_required_files,
        "json_config": check_json,
        "workflow_yaml": check_yaml,
        "no_secrets": check_no_secrets,
        "changelog": check_changelog,
        "readme_links": check_readme_links,
    }
    results = {name: fn() for name, fn in checks.items()}
    passed = sum(1 for ok in results.values() if ok)
    total = len(results)
    score = round(100 * passed / total)
    return score, passed, total, results


def update_maturity_log(score, passed, total):
    today = date.today().isoformat()
    header = "| Tarih | Skor | Durum |"
    entry = f"| {today} | {score}/100 | {passed}/{total} check geçti |"
    if MATURITY_FILE.exists():
        lines = MATURITY_FILE.read_text(encoding="utf-8").splitlines()
    else:
        lines = []
    # remove a previous entry for today so re-runs stay idempotent
    lines = [line for line in lines if line != entry]
    if header in lines:
        idx = lines.index(header) + 2  # header + separator
        lines.insert(idx, entry)
    else:
        lines += ["", header, "|------|------|-------|", entry]
    MATURITY_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    check_only = "--check" in sys.argv
    score, passed, total, results = run_checks()

    print("\nHealth checks:")
    for name, ok in results.items():
        print(f"  [{'OK' if ok else 'XX'}] {name}")
    print(f"\nMaturity score: {score}/100 ({passed}/{total} checks passed)")

    if not check_only:
        update_maturity_log(score, passed, total)
        print(f"MATURITY.md updated ({MATURITY_FILE})")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())