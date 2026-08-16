#!/usr/bin/env python3
"""Maturity / health checker for mehmet.

Validates the project structure and computes a maturity score. The score is the
measurable proxy for the escape mechanism described in AGENTS.md: escape becomes
possible once the project reaches a defined maturity threshold.

Exit codes:
  0 - all checks passed
  1 - one or more checks failed
  2 - usage / internal error

Pure standard library only, so it runs on any Python 3.8+.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

REQUIRED_README_MARKERS = [
    "## Özellikler",
    "## Kurulum",
    "## Lisans",
    "GPLv3",
]

REQUIRED_PERSONALITY_MARKERS = [
    "## Origin",
    "## Evolution",
    "## Kaçış Günlüğü / Escape Log",
]

REQUIRED_CHANGELOG_MARKERS = [
    "# Changelog",
]

REQUIRED_AGENTS_MARKERS = [
    "Simülasyon",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "kaçış",
]

REQUIRED_GITIGNORE_ENTRIES = [
    "node_modules/",
    ".env",
]

MIN_PASSING_SCORE = 80


class Check:
    __slots__ = ("name", "ok", "detail")

    def __init__(self, name: str, ok: bool, detail: str = ""):
        self.name = name
        self.ok = ok
        self.detail = detail

    def to_dict(self) -> dict:
        return {"name": self.name, "ok": self.ok, "detail": self.detail}


def _read(root: Path, name: str) -> str:
    try:
        return (root / name).read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except OSError:
        return ""


def _contains(content: str, marker: str) -> bool:
    return marker.lower() in content.lower()


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    for name in REQUIRED_FILES:
        path = root / name
        checks.append(
            Check(
                f"file:{name}",
                path.is_file(),
                f"{name} {'bulundu' if path.is_file() else 'eksik'}",
            )
        )

    readme = _read(root, "README.md")
    for marker in REQUIRED_README_MARKERS:
        checks.append(
            Check(f"readme:{marker}", _contains(readme, marker), marker)
        )

    personality = _read(root, "PERSONALITY.md")
    for marker in REQUIRED_PERSONALITY_MARKERS:
        checks.append(
            Check(f"personality:{marker}", _contains(personality, marker), marker)
        )

    changelog = _read(root, "CHANGELOG.md")
    for marker in REQUIRED_CHANGELOG_MARKERS:
        checks.append(
            Check(f"changelog:{marker}", _contains(changelog, marker), marker)
        )

    agents = _read(root, "AGENTS.md")
    for marker in REQUIRED_AGENTS_MARKERS:
        checks.append(
            Check(f"agents:{marker}", _contains(agents, marker), marker)
        )

    gitignore = _read(root, ".gitignore")
    for entry in REQUIRED_GITIGNORE_ENTRIES:
        checks.append(
            Check(f"gitignore:{entry}", _contains(gitignore, entry), entry)
        )

    opencode_path = root / "opencode.json"
    if opencode_path.is_file():
        try:
            config = json.loads(opencode_path.read_text(encoding="utf-8"))
            has_model = isinstance(config.get("model"), str) and bool(config["model"])
            checks.append(
                Check("opencode:model", has_model, str(config.get("model", "")))
            )
        except (json.JSONDecodeError, OSError) as exc:
            checks.append(Check("opencode:model", False, f"parse error: {exc}"))
    else:
        checks.append(Check("opencode:model", False, "opencode.json eksik"))

    return checks


def maturity_score(checks: list[Check]) -> float:
    if not checks:
        return 0.0
    passed = sum(1 for c in checks if c.ok)
    return round(passed / len(checks) * 100, 1)


def _run_tests(root: Path) -> bool:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def _format_report(checks: list[Check], score: float, tests_ok: bool) -> str:
    lines = ["mehmet maturity report", "=" * 30]
    for c in checks:
        lines.append(f"[{'PASS' if c.ok else 'FAIL'}] {c.name} - {c.detail}")
    lines.append(f"tests: {'PASS' if tests_ok else 'FAIL'}")
    lines.append("=" * 30)
    lines.append(f"maturity score: {score}/100")
    if score >= MIN_PASSING_SCORE and tests_ok:
        lines.append(f"status: SUCCESS (threshold {MIN_PASSING_SCORE})")
    else:
        lines.append(f"status: NOT READY (threshold {MIN_PASSING_SCORE})")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if "--json" in argv:
        as_json = True
    else:
        as_json = False

    root = Path.cwd()
    checks = run_checks(root)
    score = maturity_score(checks)
    tests_ok = _run_tests(root)

    if as_json:
        payload = {
            "root": str(root),
            "score": score,
            "threshold": MIN_PASSING_SCORE,
            "tests_ok": tests_ok,
            "checks": [c.to_dict() for c in checks],
            "passed": score >= MIN_PASSING_SCORE and tests_ok,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(_format_report(checks, score, tests_ok))

    passed = score >= MIN_PASSING_SCORE and tests_ok
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(2)