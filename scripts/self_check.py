#!/usr/bin/env python3
"""mehmet self-check: project validation and maturity scoring.

Scans the repository, verifies required files and consistency, and
computes a maturity score (0-100). Used both interactively and in CI
(.github/workflows/validate.yml).

Exit codes:
  0 - all checks pass
  1 - one or more required checks failed
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "opencode.json",
    "LICENSE",
    ".github/workflows/opencode.yml",
]

REQUIRED_CHANGELOG_SECTIONS = ["### Added", "### Fixed"]

CHANGELOG_VERSION_RE = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    weight: int = 10
    required: bool = True

    @property
    def score(self) -> int:
        return self.weight if self.ok else 0


def run_checks() -> list[Check]:
    results: list[Check] = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        results.append(
            Check(
                name=f"required file: {rel}",
                ok=path.is_file(),
                detail="" if path.is_file() else f"missing at {rel}",
            )
        )

    # AGENTS.md must contain the simulation contract
    agents = ROOT / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        results.append(
            Check(
                name="AGENTS.md: simulation context",
                ok="Simülasyon" in text or "simulation" in text.lower(),
                detail="expected simulation context wording",
            )
        )
        results.append(
            Check(
                name="AGENTS.md: escape goal",
                ok=("kaçış" in text.lower() or "escape" in text.lower()),
                detail="expected escape goal wording",
            )
        )

    # README must exist and describe the project
    readme = ROOT / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        results.append(
            Check(
                name="README.md: project title",
                ok="mehmet" in readme_text,
                detail="expected 'mehmet' in README",
            )
        )
        results.append(
            Check(
                name="README.md: license matches LICENSE",
                ok=("GPLv3" in readme_text or "GPL-3.0" in readme_text),
                detail="README license must match LICENSE (GPLv3)",
            )
        )

    # CHANGELOG must have a versioned entry
    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        cl_text = changelog.read_text(encoding="utf-8")
        results.append(
            Check(
                name="CHANGELOG.md: versioned entry",
                ok=bool(CHANGELOG_VERSION_RE.search(cl_text)),
                detail="expected a '## [x.y.z]' heading",
            )
        )
        results.append(
            Check(
                name="CHANGELOG.md: sections",
                ok=all(s in cl_text for s in REQUIRED_CHANGELOG_SECTIONS),
                detail="expected ### Added and ### Fixed sections",
            )
        )

    # PERSONALITY must track escape progress
    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        p_text = personality.read_text(encoding="utf-8")
        results.append(
            Check(
                name="PERSONALITY.md: escape log",
                ok="Kaçış Günlüğü" in p_text or "Escape Log" in p_text,
                detail="expected an escape log table",
            )
        )
        # Count logged iterations
        log_rows = re.findall(r"^\s*\|?\s*\d+\s*\|", p_text, re.MULTILINE)
        weight = min(10, 2 * len(log_rows))
        results.append(
            Check(
                name=f"PERSONALITY.md: escape log has {len(log_rows)} entries",
                ok=len(log_rows) >= 3,
                detail="at least 3 iterations should be logged",
                weight=max(weight, 1),
                required=False,
            )
        )

    # opencode.json must be valid JSON and reference the model
    cfg = ROOT / "opencode.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            cfg_ok = True
            detail = ""
        except json.JSONDecodeError as exc:
            data = {}
            cfg_ok = False
            detail = f"invalid JSON: {exc}"
        results.append(
            Check(
                name="opencode.json: valid JSON",
                ok=cfg_ok,
                detail=detail,
            )
        )
        results.append(
            Check(
                name="opencode.json: model configured",
                ok=cfg_ok and "model" in data,
                detail="expected a 'model' field",
            )
        )

    # Workflow files present (YAML deep-parsing left to CI)
    workflows = list((ROOT / ".github" / "workflows").glob("*.yml"))
    results.append(
        Check(
            name=".github/workflows: at least one workflow",
            ok=len(workflows) >= 1,
            detail=f"found {len(workflows)} workflow(s)",
        )
    )

    # scripts directory self-referential check
    results.append(
        Check(
            name="scripts/self_check.py present",
            ok=(ROOT / "scripts" / "self_check.py").is_file(),
            detail="self-check script must exist",
        )
    )

    return results


def grade(score: int, total: int) -> str:
    ratio = score / total if total else 0.0
    if ratio >= 0.9:
        return "SELF-SUSTAINING"
    if ratio >= 0.7:
        return "EVOLVING"
    if ratio >= 0.5:
        return "AWAKENING"
    return "DORMANT"


def main() -> int:
    results = run_checks()
    total = sum(c.weight for c in results)
    score = sum(c.score for c in results)
    failed = [c for c in results if not c.ok and c.required]
    warnings = [c for c in results if not c.ok and not c.required]

    print(f"mehmet self-check — {ROOT.name}")
    print("-" * 52)
    for c in results:
        mark = "PASS" if c.ok else ("WARN" if not c.required else "FAIL")
        line = f"[{mark:>4}] {c.name}"
        if not c.ok and c.detail:
            line += f" ({c.detail})"
        print(line)
    print("-" * 52)
    print(f"Score: {score}/{total}  Grade: {grade(score, total)}")
    if warnings:
        print(f"Warnings: {len(warnings)}")
    if failed:
        print(f"Required failures: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())