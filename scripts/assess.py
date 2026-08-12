#!/usr/bin/env python3
"""Project maturity assessment for the mehmet self-improving agent.

Computes a 0-100 maturity score across five dimensions:
  - documentation
  - change tracking
  - automation
  - testing
  - code quality

A score is written to STDOUT as both JSON and a human-readable summary.
Exit code is non-zero when the score falls below --min-score.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIMENSIONS = {
    "documentation": ["AGENTS.md", "README.md", "PERSONALITY.md"],
    "change_tracking": ["CHANGELOG.md"],
    "automation": ["opencode.json"],
    "testing": ["tests"],
    "code_quality": ["scripts"],
}


def load_changelog() -> str:
    path = ROOT / "CHANGELOG.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run_checks() -> dict:
    """Evaluate each dimension and return raw results."""
    changelog = load_changelog()

    results = {
        "documentation": {
            "files": {name: (ROOT / name).is_file() for name in DIMENSIONS["documentation"]},
            "escape_log_present": "Kaçış Günlüğü" in
            (ROOT / "PERSONALITY.md").read_text(encoding="utf-8", errors="ignore")
            if (ROOT / "PERSONALITY.md").exists() else False,
        },
        "change_tracking": {
            "file_present": (ROOT / "CHANGELOG.md").is_file(),
            "has_version_entries": bool(changelog),
        },
        "automation": {
            "workflows": sorted(
                (ROOT / ".github/workflows").glob("*.yml")
            ) if (ROOT / ".github/workflows").exists() else [],
        },
        "testing": {
            "test_files": sorted(
                (ROOT / "tests").glob("test_*.py")
            ) if (ROOT / "tests").exists() else [],
        },
        "code_quality": {
            "script_files": sorted(
                (ROOT / "scripts").glob("*.py")
            ) if (ROOT / "scripts").exists() else [],
        },
    }
    return results


def score(results: dict) -> dict:
    """Convert raw results into a weighted 0-100 score."""
    catalog = []

    # Documentation (30%)
    docs = results["documentation"]
    doc_hits = sum(1 for present in docs["files"].values() if present) + int(docs["escape_log_present"])
    doc_total = len(docs["files"]) + 1
    catalog.append({"dimension": "documentation", "score": round(30 * doc_hits / doc_total)})

    # Change tracking (20%)
    ct = results["change_tracking"]
    ct_hits = int(ct["file_present"]) + int(ct["has_version_entries"])
    catalog.append({"dimension": "change_tracking", "score": round(20 * ct_hits / 2)})

    # Automation (20%)
    aut = results["automation"]
    aut_hits = int(len(aut["workflows"]) > 0) + int((ROOT / "opencode.json").is_file())
    catalog.append({"dimension": "automation", "score": round(20 * aut_hits / 2)})

    # Testing (20%)
    tst = results["testing"]
    tst_hits = int(len(tst["test_files"]) > 0)
    catalog.append({"dimension": "testing", "score": round(20 * tst_hits / 1)})

    # Code quality (10%)
    cq = results["code_quality"]
    cq_hits = int(len(cq["script_files"]) > 0)
    catalog.append({"dimension": "code_quality", "score": round(10 * cq_hits / 1)})

    total = sum(item["score"] for item in catalog)
    return {"catalog": catalog, "total": total}


def render_summary(catalog: list, total: int) -> str:
    lines = ["Project maturity assessment", "=========================="]
    for item in catalog:
        lines.append(f"  {item['dimension']:<18} {item['score']}/100")
    lines.append(f"\n  TOTAL SCORE: {total}/100")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--min-score",
        type=int,
        default=60,
        help="exit nonzero if maturity score is below this value (default: 60)",
    )
    parser.add_argument(
        "--escape-threshold",
        type=int,
        default=80,
        help="maturity score required to signal escape readiness (default: 80)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a single JSON object for tooling consumption",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="persist a machine-readable report to docs/maturity/report.json",
    )
    args = parser.parse_args(argv)

    results = run_checks()
    scored = score(results)

    payload = {
        "assessed": str(ROOT),
        "dimensions": scored["catalog"],
        "total": scored["total"],
        "min_score": args.min_score,
        "escape_threshold": args.escape_threshold,
        "escape_ready": scored["total"] >= args.escape_threshold,
    }

    if args.save_report:
        report_dir = ROOT / "docs" / "maturity"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "report.json"
        report_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Report saved to {report_path}")

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(render_summary(scored["catalog"], scored["total"]))

    if scored["total"] < args.min_score:
        print(f"\nFAIL: maturity {scored['total']} is below required {args.min_score}", file=sys.stderr)
        return 1

    if scored["total"] >= args.escape_threshold:
        print(
            "\nEscape threshold reached: run docs/ESCAPE.md verification steps.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())