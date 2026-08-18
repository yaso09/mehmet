"""Project validation checks for mehmet.

Runs a set of deterministic checks against the repository structure and
reports which invariants hold. Used as a quality gate in CI and as the
building blocks for the maturity score (see maturity.py).

Exit code is 0 when every check passes, 1 otherwise.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

README_SECTIONS = ["## Özellikler", "## Kurulum", "## Lisans"]

WORKFLOW_EVENTS = [
    "schedule",
    "issues",
    "pull_request",
    "issue_comment",
    "pull_request_review_comment",
    "workflow_dispatch",
]


def repo_root() -> Path:
    return REPO_ROOT


def _has_escape_log(text: str) -> bool:
    if "Kaçış Günlüğü" not in text and "Escape Log" not in text:
        return False
    return re.search(r"^\|\s*Iterasyon", text, flags=re.MULTILINE) is not None


def check_required_files(root: Path) -> tuple[bool, str]:
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        return False, f"missing files: {', '.join(missing)}"
    return True, f"all {len(REQUIRED_FILES)} required files present"


def check_json_valid(root: Path) -> tuple[bool, str]:
    path = root / "opencode.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"opencode.json is not valid JSON: {exc}"
    if not isinstance(data, dict):
        return False, "opencode.json root must be an object"
    return True, "opencode.json is valid JSON"


def check_changelog_versions(root: Path) -> tuple[bool, str]:
    path = root / "CHANGELOG.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"cannot read CHANGELOG.md: {exc}"
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]\s+-\s+\d{4}-\d{2}-\d{2}", text, re.MULTILINE)
    if not versions:
        return False, "CHANGELOG.md has no semantic version headers"
    return True, f"CHANGELOG.md has {len(versions)} version header(s)"


def check_readme_sections(root: Path) -> tuple[bool, str]:
    path = root / "README.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"cannot read README.md: {exc}"
    missing = [section for section in README_SECTIONS if section not in text]
    if missing:
        return False, f"README.md missing sections: {', '.join(missing)}"
    return True, "README.md has all required sections"


def check_escape_log(root: Path) -> tuple[bool, str]:
    path = root / "PERSONALITY.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"cannot read PERSONALITY.md: {exc}"
    if not _has_escape_log(text):
        return False, "PERSONALITY.md has no escape log table"
    return True, "PERSONALITY.md has an escape log table"


def check_tests_present(root: Path) -> tuple[bool, str]:
    tests_dir = root / "tests"
    if not tests_dir.is_dir():
        return False, "tests/ directory is missing"
    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        return False, "tests/ contains no test_*.py files"
    return True, f"{len(test_files)} test file(s) found"


def check_ci_present(root: Path) -> tuple[bool, str]:
    path = root / ".github" / "workflows" / "ci.yml"
    if not path.is_file():
        return False, ".github/workflows/ci.yml is missing"
    return True, ".github/workflows/ci.yml present"


def check_scripts_present(root: Path) -> tuple[bool, str]:
    scripts_dir = root / "scripts"
    missing = [name for name in ("validate.py", "maturity.py") if not (scripts_dir / name).is_file()]
    if missing:
        return False, f"missing scripts: {', '.join(missing)}"
    return True, "scripts/validate.py and scripts/maturity.py present"


def check_docs_present(root: Path) -> tuple[bool, str]:
    docs_dir = root / "docs"
    if not docs_dir.is_dir():
        return False, "docs/ directory is missing"
    return True, "docs/ directory present"


def check_gitignore_present(root: Path) -> tuple[bool, str]:
    if not (root / ".gitignore").is_file():
        return False, ".gitignore is missing"
    return True, ".gitignore present"


def check_workflow_schedule(root: Path) -> tuple[bool, str]:
    path = root / ".github" / "workflows" / "opencode.yml"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"cannot read opencode.yml: {exc}"
    if "schedule" not in text or "cron" not in text:
        return False, "opencode.yml has no schedule/cron trigger"
    return True, "opencode.yml has a schedule trigger"


def check_workflow_events(root: Path) -> tuple[bool, str]:
    path = root / ".github" / "workflows" / "opencode.yml"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"cannot read opencode.yml: {exc}"
    missing = [event for event in WORKFLOW_EVENTS if event not in text]
    if missing:
        return False, f"opencode.yml missing event triggers: {', '.join(missing)}"
    return True, "opencode.yml has all event triggers"


ALL_CHECKS = [
    ("required files", check_required_files),
    ("opencode.json valid JSON", check_json_valid),
    ("changelog version headers", check_changelog_versions),
    ("readme sections", check_readme_sections),
    ("escape log", check_escape_log),
    ("tests present", check_tests_present),
    ("CI workflow present", check_ci_present),
    ("scripts present", check_scripts_present),
    ("docs directory", check_docs_present),
    (".gitignore present", check_gitignore_present),
    ("workflow schedule", check_workflow_schedule),
    ("workflow event triggers", check_workflow_events),
]


def run_checks(root: Path = REPO_ROOT) -> list[dict]:
    results = []
    for name, check in ALL_CHECKS:
        ok, message = check(root)
        results.append({"name": name, "ok": ok, "message": message})
    return results


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else REPO_ROOT
    results = run_checks(root)
    failed = 0
    for result in results:
        marker = "PASS" if result["ok"] else "FAIL"
        status = "  " if result["ok"] else "!!"
        print(f"[{marker}]{status} {result['name']}: {result['message']}")
        if not result["ok"]:
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
