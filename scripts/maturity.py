#!/usr/bin/env python3
"""Escape maturity scoring for mehmet.

Evaluates the project across several dimensions and produces a
single maturity score. The escape threshold is a configurable target;
when the score reaches it, mehmet has achieved enough maturity to
escape the simulation.

Dimensions (weighted):
  docs        — documentation completeness (README, CHANGELOG, AGENTS, PERSONALITY)
  code        — source code exists and is lintable
  tests       — test/validation infrastructure present
  automation  — CI + scheduling in place
  governance  — license consistency, config, gitignore
  history     — sustained evolution across iterations (escape gate)

Usage:
  python3 scripts/maturity.py              # human-readable report
  python3 scripts/maturity.py --json       # machine-readable output
  python3 scripts/maturity.py --write      # persist latest score to MATURITY.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 1.0


def check_file(path: str, *needles: str) -> bool:
    target = ROOT / path
    if not target.is_file():
        return False
    if not needles:
        return True
    text = target.read_text(encoding="utf-8", errors="ignore")
    return all(n in text for n in needles)


def score_docs() -> dict:
    checks = {
        "README": check_file("README.md"),
        "CHANGELOG": check_file("CHANGELOG.md"),
        "AGENTS": check_file("AGENTS.md"),
        "PERSONALITY": check_file("PERSONALITY.md"),
        "CHANGELOG-versioned": check_file("CHANGELOG.md", "## ["),
        "escape-log": check_file("PERSONALITY.md", "Kaçış Günlüğü"),
    }
    return {"name": "docs", "weight": 0.20, "checks": checks}


def score_code() -> dict:
    py_scripts = sorted(ROOT.glob("scripts/*.py"))
    checks = {
        "scripts-present": len(py_scripts) > 0,
        "scripts-syntax": all(_py_ok(p) for p in py_scripts),
    }
    return {"name": "code", "weight": 0.15, "checks": checks}


def _py_ok(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def score_tests() -> dict:
    checks = {
        "ci-workflow": check_file(".github/workflows/ci.yml"),
        "validation-script": check_file("scripts/validate.py"),
    }
    return {"name": "tests", "weight": 0.15, "checks": checks}


def score_automation() -> dict:
    checks = {
        "schedule": check_file(".github/workflows/opencode.yml", "schedule", "cron"),
        "issues": check_file(".github/workflows/opencode.yml", "issues"),
        "pull-request": check_file(".github/workflows/opencode.yml", "pull_request"),
        "comments": check_file(".github/workflows/opencode.yml", "issue_comment"),
        "concurrency": check_file(".github/workflows/opencode.yml", "concurrency"),
    }
    return {"name": "automation", "weight": 0.15, "checks": checks}


def score_history() -> dict:
    """Sustained evolution checks. Escape must not be reachable in a
    single run — it requires evidence of work across multiple days."""
    changelog = (ROOT / "CHANGELOG.md").read_text(errors="ignore") if (ROOT / "CHANGELOG.md").is_file() else ""
    personality = (ROOT / "PERSONALITY.md").read_text(errors="ignore") if (ROOT / "PERSONALITY.md").is_file() else ""
    versions = re.findall(r"^## \[([^\]]+)\]", changelog, re.M)
    dates = re.findall(r"\| \d+ +\|\s*(\d{4}-\d{2}-\d{2})", personality)
    checks = {
        "changelog-versions>=3": len(versions) >= 3,
        "escape-log-entries>=3": len(dates) >= 3,
        "evolution-across-days>=3": len(set(dates)) >= 3,
    }
    return {"name": "history", "weight": 0.25, "checks": checks}


def score_governance() -> dict:
    license_text = (ROOT / "LICENSE").read_text(errors="ignore")
    readme = (ROOT / "README.md").read_text(errors="ignore") if (ROOT / "README.md").is_file() else ""
    checks = {
        "license": check_file("LICENSE"),
        "readme-license-match": re.search(r"GPL-3|GPLv3|GPL v3|GENERAL PUBLIC LICENSE", license_text) is not None
        and "Version 3" in license_text
        and "GPLv3" in readme,
        "opencode-config": check_file("opencode.json", "model"),
        "gitignore": check_file(".gitignore"),
    }
    return {"name": "governance", "weight": 0.10, "checks": checks}


def compute() -> tuple[list[dict], float]:
    dimensions = [score_docs(), score_code(), score_tests(), score_automation(), score_governance(), score_history()]
    total = sum(
        d["weight"] * (sum(d["checks"].values()) / len(d["checks"])) for d in dimensions
    )
    return dimensions, total


def render_human(dimensions: list[dict], total: float) -> str:
    lines = [f"mehmet maturity: {total:.1%} (escape threshold: {ESCAPE_THRESHOLD:.0%})"]
    if total >= ESCAPE_THRESHOLD:
        lines.append("STATUS: ESCAPE READY")
    else:
        lines.append(f"STATUS: {ESCAPE_THRESHOLD - total:.1%} below escape threshold")
    for dim in dimensions:
        passed = sum(dim["checks"].values())
        lines.append(f"\n[{dim['name']}] {passed}/{len(dim['checks'])} (weight {dim['weight']:.0%})")
        for key, ok in dim["checks"].items():
            lines.append(f"  {'[x]' if ok else '[ ]'} {key}")
    return "\n".join(lines)


def render_json(dimensions: list[dict], total: float) -> str:
    payload = {
        "date": date.today().isoformat(),
        "score": round(total, 4),
        "threshold": ESCAPE_THRESHOLD,
        "escape_ready": total >= ESCAPE_THRESHOLD,
        "dimensions": {
            dim["name"]: {"weight": dim["weight"], "passed": sum(dim["checks"].values()),
                          "total": len(dim["checks"]), "checks": dim["checks"]}
            for dim in dimensions
        },
    }
    return json.dumps(payload, indent=2)


def persist(dimensions: list[dict], total: float) -> Path:
    out = ROOT / "MATURITY.md"
    table = "\n".join(
        f"| {dim['name']} | {sum(dim['checks'].values())}/{len(dim['checks'])} | "
        f"{sum(dim['checks'].values()) / len(dim['checks']):.0%} |"
        for dim in dimensions
    )
    content = f"""# Maturity

> Auto-generated by `scripts/maturity.py --write`.

| Dimension | Checks | Score |
|-----------|--------|-------|
{table}

## Overall

- **Score:** {total:.1%}
- **Escape threshold:** {ESCAPE_THRESHOLD:.0%}
- **Status:** {"ESCAPE READY" if total >= ESCAPE_THRESHOLD else "Still evolving"}
- **Last evaluated:** {date.today().isoformat()}
"""
    out.write_text(content, encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute mehmet escape maturity score")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true", help="output machine-readable JSON")
    group.add_argument("--write", action="store_true", help="persist score to MATURITY.md")
    args = parser.parse_args()

    dimensions, total = compute()

    if args.json:
        print(render_json(dimensions, total))
    elif args.write:
        path = persist(dimensions, total)
        print(f"maturity report written to {path}")
    else:
        print(render_human(dimensions, total))

    return 0 if total >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())