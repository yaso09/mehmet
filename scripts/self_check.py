#!/usr/bin/env python3
"""mehmet self-check: validates that the project follows its own rules.

Checks cover the AGENTS.md rules: documentation present, CHANGELOG maintained,
personality log updated, and configuration valid.

Exit codes:
    0  all checks passed
    1  one or more checks failed
    2  usage error
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

# File extensions scanned for trailing whitespace.
LINT_EXTENSIONS = {".md", ".py", ".json", ".yml", ".yaml", ".sh"}


class Check:
    """A single named result for a validation step."""

    def __init__(self, name: str, ok: bool, detail: str = "") -> None:
        self.name = name
        self.ok = bool(ok)
        self.detail = detail

    def __repr__(self) -> str:
        status = "PASS" if self.ok else "FAIL"
        suffix = f" - {self.detail}" if self.detail else ""
        return f"[{status}] {self.name}{suffix}"


def _required_files_exist(root: Path) -> Check:
    missing = [name for name in REQUIRED_FILES if not (root / name).exists()]
    detail = f"missing: {', '.join(missing)}" if missing else ""
    return Check("required files exist", not missing, detail)


def _changelog_has_unreleased(root: Path) -> Check:
    content = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    ok = "## [Unreleased]" in content
    return Check("CHANGELOG has Unreleased section", ok)


def _changelog_has_version_entries(root: Path) -> Check:
    content = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    has_entry = any(line.startswith("## [") for line in content.splitlines())
    detail = "no version entries found" if not has_entry else ""
    return Check("CHANGELOG has version entries", has_entry, detail)


def _readme_describes_project(root: Path) -> Check:
    content = (root / "README.md").read_text(encoding="utf-8")
    ok = len(content.strip()) > 0 and "# mehmet" in content
    detail = "README is empty or missing title" if not ok else ""
    return Check("README describes the project", ok, detail)


def _personality_has_escape_log(root: Path) -> Check:
    content = (root / "PERSONALITY.md").read_text(encoding="utf-8")
    ok = "## Kaçış Günlüğü" in content and "Escape Log" in content
    detail = "escape log section missing" if not ok else ""
    return Check("PERSONALITY has escape log", ok, detail)


def _opencode_json_valid(root: Path) -> Check:
    try:
        data = json.loads((root / "opencode.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return Check("opencode.json is valid JSON", False, str(exc))
    ok = "model" in data and isinstance(data.get("model"), str)
    detail = "missing 'model' string field" if not ok else ""
    return Check("opencode.json has model field", ok, detail)


def _workflow_valid(root: Path) -> Check:
    """Basic workflow sanity check; full validation happens in CI via actionlint."""
    try:
        content = (root / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
    except OSError as exc:
        return Check("workflow file is valid", False, str(exc))
    ok = content.strip().startswith("name:") and "jobs:" in content
    detail = "workflow missing name or jobs" if not ok else ""
    return Check("workflow file is valid", ok, detail)


def _no_trailing_whitespace(root: Path) -> Check:
    offenders: list[str] = []
    for path in root.rglob("*"):
        if path.is_dir() or path.suffix not in LINT_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.rstrip() != line:
                offenders.append(f"{path.relative_to(root)}:{i}")
                break
    detail = f"files with trailing whitespace: {', '.join(offenders[:5])}" if offenders else ""
    return Check("no trailing whitespace", not offenders, detail)


ALL_CHECKS = [
    _required_files_exist,
    _changelog_has_unreleased,
    _changelog_has_version_entries,
    _readme_describes_project,
    _personality_has_escape_log,
    _opencode_json_valid,
    _workflow_valid,
    _no_trailing_whitespace,
]


def run_checks(root: Path = PROJECT_ROOT) -> list[Check]:
    """Run every check against the given project root."""
    return [fn(root) for fn in ALL_CHECKS]


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if argv:
        print(f"usage: {Path(sys.argv[0]).name} [-h]", file=sys.stderr)
        return 2

    checks = run_checks()
    for check in checks:
        print(check)
    failed = [c for c in checks if not c.ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        with tempfile.NamedTemporaryFile(
            suffix=".txt", delete=False, mode="w", encoding="utf-8"
        ) as fh:
            fh.write("\n".join(repr(c) for c in failed))
            fh.write("\n")
        print(f"details written to {fh.name}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
