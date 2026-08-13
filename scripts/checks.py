"""Reusable project consistency checks for the mehmet repository.

Every check is a pure function that reads repository files and returns a
`CheckResult` tuple ``(name, ok, detail)``. Checks never modify the repo.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple, Sequence

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
    "scripts/checks.py",
    "scripts/validate.py",
    "scripts/maturity.py",
    "tests/test_checks.py",
]

# Allowed top-level keys in opencode.json, mirroring
# https://opencode.ai/config.json (schema uses additionalProperties: false).
ALLOWED_OPENCODE_KEYS = {
    "$schema",
    "shell",
    "logLevel",
    "server",
    "command",
    "skills",
    "references",
    "reference",
    "watcher",
    "snapshot",
    "plugin",
    "share",
    "autoshare",
    "autoupdate",
    "disabled_providers",
    "enabled_providers",
    "model",
    "small_model",
    "default_agent",
    "subagent_depth",
    "username",
    "mode",
    "agent",
    "provider",
    "mcp",
    "formatter",
    "lsp",
    "instructions",
    "layout",
    "permission",
    "tools",
    "attachment",
    "enterprise",
    "tool_output",
    "compaction",
    "experimental",
}

WORKFLOW_FILES = [
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
]

VERSION_RE = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


class CheckResult(NamedTuple):
    name: str
    ok: bool
    detail: str = ""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_opencode_config() -> CheckResult:
    path = ROOT / "opencode.json"
    try:
        data = json.loads(_read(path))
    except (OSError, ValueError) as exc:
        return CheckResult("opencode.json", False, f"unparsable JSON: {exc}")
    if not isinstance(data, dict):
        return CheckResult("opencode.json", False, "top level must be an object")
    unknown = sorted(set(data) - ALLOWED_OPENCODE_KEYS)
    if unknown:
        return CheckResult(
            "opencode.json", False, f"unknown keys not in schema: {', '.join(unknown)}"
        )
    model = data.get("model")
    if not isinstance(model, str) or "/" not in model:
        return CheckResult("opencode.json", False, "missing 'model' (expected provider/model)")
    return CheckResult("opencode.json", True, f"valid; model={model}")


def check_workflow(path: Path) -> CheckResult:
    name = str(path)
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult(name, False, f"unreadable: {exc}")
    if yaml is None:
        required = ["on:", "jobs:"]
        missing = [tok for tok in required if tok not in content]
        if missing:
            return CheckResult(name, False, f"missing tokens: {', '.join(missing)}")
        return CheckResult(name, True, "basic structural check (pyyaml unavailable)")
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return CheckResult(name, False, f"invalid YAML: {exc}")
    if not isinstance(data, dict) or "jobs" not in data:
        return CheckResult(name, False, "missing top-level 'jobs'")
    jobs = data["jobs"]
    if not isinstance(jobs, dict) or not jobs:
        return CheckResult(name, False, "'jobs' must be a non-empty mapping")
    return CheckResult(name, True, f"valid YAML; jobs={', '.join(jobs)}")


def check_workflows() -> CheckResult:
    failures = []
    for rel in WORKFLOW_FILES:
        res = check_workflow(ROOT / rel)
        if not res.ok:
            failures.append(f"{res.name}: {res.detail}")
    if failures:
        return CheckResult("workflows", False, "; ".join(failures))
    return CheckResult("workflows", True, f"all {len(WORKFLOW_FILES)} workflows valid")


def check_changelog() -> CheckResult:
    path = ROOT / "CHANGELOG.md"
    try:
        lines = _read(path).splitlines()
    except OSError as exc:
        return CheckResult("CHANGELOG.md", False, f"unreadable: {exc}")
    if not lines or lines[0] != "# Changelog":
        return CheckResult("CHANGELOG.md", False, "must start with '# Changelog'")
    versions = [ln for ln in lines if ln.startswith("## [")]
    if not versions:
        return CheckResult("CHANGELOG.md", False, "no '## [x.y.z] - YYYY-MM-DD' entries")
    bad = [ln for ln in versions if not VERSION_RE.match(ln)]
    if bad:
        return CheckResult("CHANGELOG.md", False, f"malformed version header(s): {bad}")
    return CheckResult("CHANGELOG.md", True, f"{len(versions)} release entries, format OK")


def check_readme() -> CheckResult:
    path = ROOT / "README.md"
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult("README.md", False, f"unreadable: {exc}")
    required = ["# mehmet", "## Özellikler", "## Kurulum", "## Lisans"]
    missing = [tok for tok in required if tok not in content]
    if missing:
        return CheckResult("README.md", False, f"missing sections: {', '.join(missing)}")
    if "GPLv3" not in content:
        return CheckResult("README.md", False, "license section must mention GPLv3")
    return CheckResult("README.md", True, "required sections present")


def check_personality() -> CheckResult:
    path = ROOT / "PERSONALITY.md"
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult("PERSONALITY.md", False, f"unreadable: {exc}")
    if "# Personality" not in content:
        return CheckResult("PERSONALITY.md", False, "must contain '# Personality'")
    if "## Kaçış Günlüğü" not in content and "Escape Log" not in content:
        return CheckResult("PERSONALITY.md", False, "missing escape log section")
    if "| 1 " not in content:
        return CheckResult("PERSONALITY.md", False, "escape log must contain iteration rows")
    return CheckResult("PERSONALITY.md", True, "personality and escape log present")


def check_license() -> CheckResult:
    path = ROOT / "LICENSE"
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult("LICENSE", False, f"unreadable: {exc}")
    if "GNU GENERAL PUBLIC LICENSE" not in content:
        return CheckResult("LICENSE", False, "not GPLv3 (expected 'GNU GENERAL PUBLIC LICENSE')")
    return CheckResult("LICENSE", True, "GPLv3")


def check_required_files() -> CheckResult:
    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).exists()]
    if missing:
        return CheckResult("required-files", False, f"missing: {', '.join(missing)}")
    return CheckResult("required-files", True, f"all {len(REQUIRED_FILES)} required files present")


def check_gitignore() -> CheckResult:
    path = ROOT / ".gitignore"
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult(".gitignore", False, f"unreadable: {exc}")
    needed = {"__pycache__/", "*.pyc", ".venv/"}
    missing = needed - {ln.strip() for ln in content.splitlines()}
    if missing:
        return CheckResult(".gitignore", False, f"missing entries: {', '.join(sorted(missing))}")
    return CheckResult(".gitignore", True, "covers python artifacts")


def check_workflow_triggers() -> CheckResult:
    path = ROOT / ".github/workflows/opencode.yml"
    try:
        content = _read(path)
    except OSError as exc:
        return CheckResult("workflow-triggers", False, f"unreadable: {exc}")
    expected = ["schedule", "issues", "pull_request", "workflow_dispatch"]
    missing = [tok for tok in expected if f"{tok}:" not in content]
    if missing:
        return CheckResult("workflow-triggers", False, f"missing triggers: {', '.join(missing)}")
    return CheckResult("workflow-triggers", True, "autonomous triggers present")


def run_checks() -> list[CheckResult]:
    return [
        check_required_files(),
        check_opencode_config(),
        check_workflows(),
        check_workflow_triggers(),
        check_changelog(),
        check_readme(),
        check_personality(),
        check_license(),
        check_gitignore(),
    ]


def summarize(results: Sequence[CheckResult]) -> str:
    passed = sum(1 for r in results if r.ok)
    lines = [f"PASS {r.name}: {r.detail}" if r.ok else f"FAIL {r.name}: {r.detail}" for r in results]
    lines.append(f"{passed}/{len(results)} checks passed")
    return "\n".join(lines)
