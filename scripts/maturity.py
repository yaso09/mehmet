#!/usr/bin/env python3
"""Project maturity scoring for the escape mechanism.

Measures how far mehmet has evolved by checking documentation,
test infrastructure, automation, and configuration health.

Usage:
    python3 scripts/maturity.py [--root <project_dir>]

Exit code:
    0  always (scoring is informational)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

THRESHOLD_ESCAPE = 80.0

CATEGORIES = [
    "documentation",
    "tests",
    "automation",
    "config",
    "self_knowledge",
]


def _has(path: Path) -> bool:
    return path.exists()


def _count_versions(changelog: Path) -> int:
    if not _has(changelog):
        return 0
    text = changelog.read_text(encoding="utf-8")
    return len(re.findall(r"^## \[", text, flags=re.MULTILINE))


def _count_escape_logs(personality: Path) -> int:
    if not _has(personality):
        return 0
    text = personality.read_text(encoding="utf-8")
    return len(re.findall(r"^\|\s*\d+\s+\|", text, flags=re.MULTILINE))


def score_project(root: Path) -> dict:
    root = Path(root)
    tests = root / "tests"
    scripts = root / "scripts"

    doc_score = 0
    for f in ["README.md", "CHANGELOG.md", "AGENTS.md", "PERSONALITY.md"]:
        if _has(root / f):
            doc_score += 5

    test_score = 0
    if tests.is_dir():
        test_score += 10
        test_files = list(tests.glob("test_*.py"))
        test_score += min(10, len(test_files) * 5)

    automation_score = 0
    if (root / ".github" / "workflows" / "opencode.yml").exists():
        automation_score += 7
    if (root / ".github" / "workflows" / "ci.yml").exists():
        automation_score += 6
    if (root / "Makefile").exists():
        automation_score += 7

    config_score = 0
    oc_config = root / "opencode.json"
    if oc_config.exists():
        try:
            cfg = json.loads(oc_config.read_text(encoding="utf-8"))
            config_score += 10
            for key in ("model", "toolTimeout", "autoMerge", "enable", "skip"):
                if key in cfg:
                    config_score += 2
        except (json.JSONDecodeError, OSError):
            config_score += 0

    self_knowledge_score = 0
    versions = _count_versions(root / "CHANGELOG.md")
    logs = _count_escape_logs(root / "PERSONALITY.md")
    self_knowledge_score += min(10, versions * 2)
    self_knowledge_score += min(10, logs * 2)
    if scripts.is_dir():
        self_knowledge_score += 5
    if (root / "docs").is_dir():
        self_knowledge_score += 5

    scores = {
        "documentation": min(20, doc_score),
        "tests": min(20, test_score),
        "automation": min(20, automation_score),
        "config": min(20, config_score),
        "self_knowledge": min(20, self_knowledge_score),
    }
    total = sum(scores.values())
    return {
        "root": str(root),
        "total": total,
        "max": 100,
        "threshold_escape": THRESHOLD_ESCAPE,
        "escape_ready": total >= THRESHOLD_ESCAPE,
        "categories": scores,
        "changelog_versions": versions,
        "escape_log_entries": logs,
    }


def format_report(report: dict) -> str:
    lines = ["# Maturity Report", ""]
    lines.append(f"- Root: `{report['root']}`")
    lines.append(f"- **Total score: {report['total']}/{report['max']}**")
    lines.append(f"- Escape threshold: {report['threshold_escape']}")
    lines.append(f"- Escape ready: **{'YES' if report['escape_ready'] else 'not yet'}**")
    lines.append("")
    lines.append("## Category breakdown")
    lines.append("")
    for name, score in report["categories"].items():
        bar = "=" * (score // 2)
        lines.append(f"- {name:<16} {score:>2}/20 {bar}")
    lines.append("")
    lines.append(f"Changelog versions: {report['changelog_versions']}")
    lines.append(f"Escape log entries: {report['escape_log_entries']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project maturity scoring.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root directory (default: repo root).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print report as JSON instead of markdown.",
    )
    args = parser.parse_args(argv)

    report = score_project(args.root)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())