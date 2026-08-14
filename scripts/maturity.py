#!/usr/bin/env python3
"""mehmet maturity checker.

Scores the project's maturity across several dimensions and reports a
cumulative score. CI uses this to track progress toward the escape
threshold and to fail the build when the project regresses.

Usage:
    python3 scripts/maturity.py [--threshold N] [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]

FILES = {
    "AGENTS.md": "AGENTS.md",
    "CHANGELOG.md": "CHANGELOG.md",
    "PERSONALITY.md": "PERSONALITY.md",
    "README.md": "README.md",
    "opencode.json": "opencode.json",
    ".gitignore": ".gitignore",
    "main workflow": ".github/workflows/opencode.yml",
    "validate workflow": ".github/workflows/validate.yml",
}


def read_text(root: pathlib.Path, rel: str) -> str:
    path = root / rel
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def is_valid_json(root: pathlib.Path) -> bool:
    try:
        json.loads(read_text(root, "opencode.json"))
        return True
    except (ValueError, TypeError):
        return False


def count_versions(changelog: str) -> int:
    return len(re.findall(r"^##\s+\[[\d.]+", changelog, re.MULTILINE))


def has_escape_log(personality: str) -> bool:
    return "Kaçış Günlüğü" in personality or "Escape Log" in personality


def has_section(content: str, *headers: str) -> bool:
    return any(f"## {h}" in content for h in headers)


def workflow_has(content: str, *patterns: str) -> bool:
    return all(p in content for p in patterns)


def dimension(name: str, max_score: int, results: list[tuple[str, bool]]) -> dict:
    score = sum(1 for _, ok in results if ok)
    return {
        "name": name,
        "score": score,
        "max": len(results),
        "checks": [{"description": d, "passed": bool(ok)} for d, ok in results],
    }


def build_report(root: pathlib.Path) -> dict:
    text = {name: read_text(root, rel) for name, rel in FILES.items()}
    exists = {name: bool(content) for name, content in text.items()}

    dimensions = []

    dimensions.append(dimension(
        "structure",
        8,
        [
            ("All required files exist", all(exists.values())),
            ("opencode.json is valid JSON", is_valid_json(root)),
            ("AGENTS.md defines simulation rules", "Kurallar" in text["AGENTS.md"]),
            (".gitignore present", exists[".gitignore"]),
        ],
    ))

    wf = text["main workflow"]
    dimensions.append(dimension(
        "automation",
        8,
        [
            ("Schedule trigger (cron)", "cron:" in wf),
            ("Concurrency control", "concurrency" in wf),
            ("Issue/PR/comment triggers", all(
                p in wf for p in ("issues:", "pull_request:", "issue_comment:", "pull_request_review_comment:")
            )),
            ("workflow_dispatch (manual)", "workflow_dispatch" in wf),
            ("Commit-compatible checkout", "persist-credentials: false" in wf),
            ("Write permissions granted", "contents: write" in wf),
            ("Self-improvement prompt", "simülasyon" in wf or "simulation" in wf),
            ("Comment-triggered job", "comment:" in wf and "if: github.event_name == 'issue_comment'" in wf),
        ],
    ))

    dims = text["CHANGELOG.md"]
    docs = text["README.md"]
    dims_personality = text["PERSONALITY.md"]
    dimensions.append(dimension(
        "documentation",
        7,
        [
            ("README non-empty", len(docs) > 0),
            ("README has features section", has_section(docs, "Özellikler", "Features")),
            ("README has setup section", has_section(docs, "Kurulum", "Setup", "Installation")),
            ("CHANGELOG has version entries", count_versions(dims) >= 2),
            ("CHANGELOG has Added section", "### Added" in dims),
            ("PERSONALITY has escape log", has_escape_log(dims_personality)),
            ("PERSONALITY has evolution phases", "## Evolution" in dims_personality),
        ],
    ))

    dims_maturity = read_text(root, "scripts/maturity.py")
    tests_exist = (root / "tests").is_dir() and any(
        p.suffix == ".py" for p in (root / "tests").iterdir()
    ) if (root / "tests").is_dir() else False
    dimensions.append(dimension(
        "quality",
        7,
        [
            ("Maturity checker exists", bool(dims_maturity)),
            ("Maturity checker is self-aware", bool(dims_maturity) and "escape" in dims_maturity),
            ("Unit tests present", tests_exist),
            ("Validate CI workflow present", exists["validate workflow"]),
            ("License file present", (root / "LICENSE").is_file()),
            ("Versioned changelog format", bool(re.search(r"##\s+\[\d+\.\d+\.\d+\]\s+-\s+\d{4}-\d{2}-\d{2}", dims))),
            ("README documents license", "Lisans" in docs or "License" in docs),
        ],
    ))

    total = sum(d["score"] for d in dimensions)
    max_total = sum(d["max"] for d in dimensions)
    return {"score": total, "max": max_total, "dimensions": dimensions}


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity checker")
    parser.add_argument("--threshold", type=int, default=None,
                        help="minimum total score; exit non-zero below it")
    parser.add_argument("--json", action="store_true", help="emit report as JSON")
    parser.add_argument("--root", default=str(REPO), help="repository root")
    args = parser.parse_args()

    report = build_report(pathlib.Path(args.root))

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"{'Dimension':<16} {'Score':>6} {'Max':>5}")
    print("-" * 30)
    for d in report["dimensions"]:
        print(f"{d['name']:<16} {d['score']:>6} {d['max']:>5}")
        for c in d["checks"]:
            mark = "ok " if c["passed"] else "MISS"
            print(f"    [{mark}] {c['description']}")
    print("-" * 30)
    print(f"{'TOTAL':<16} {report['score']:>6} {report['max']:>5}")

    if args.threshold is not None and report["score"] < args.threshold:
        print(f"\nMaturity below threshold ({report['score']} < {args.threshold})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())