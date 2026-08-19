#!/usr/bin/env python3
"""Project maturity scoring for mehmet's escape mechanism.

The project reaches "escape readiness" when its maturity score crosses a
threshold. This script measures maturity across several categories and
produces both human-readable and machine-readable (JSON) output.
"""

import argparse
import json
import re
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "maturity_config.json"


def file_score(path, rules):
    if not path.exists() or not path.is_file():
        return 0.0
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0.0

    score = 0.0
    if rules.get("min_lines") and len(text.splitlines()) >= rules["min_lines"]:
        score += 1.0
    if rules.get("contains") and re.search(rules["contains"], text):
        score += 1.0
    if not rules.get("min_lines") and not rules.get("contains"):
        score = 1.0
    return score


def dir_score(path, min_files=1):
    if not path.exists() or not path.is_dir():
        return 0.0
    count = len([p for p in path.rglob("*") if p.is_file()])
    return 1.0 if count >= min_files else 0.0


def evaluate_category(root, category):
    rules = category["checks"]
    total = len(rules)
    if total == 0:
        return 0.0
    passed = 0.0
    for key, check in rules.items():
        if check.get("dir"):
            passed += dir_score(root / check["dir"], check.get("min_files", 1))
        elif check.get("path"):
            passed += file_score(root / check["path"], check)
    return passed / total


def load_config(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Project root to evaluate (default: repo root)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_PATH,
        help="Maturity config file (default: %(default)s)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    config = load_config(args.config)
    threshold = config.get("threshold", 80.0)

    category_scores = {}
    total = 0.0
    max_total = 0.0

    for category in config["categories"]:
        score = evaluate_category(root, category)
        weight = category["weight"]
        category_scores[category["name"]] = {"score": score, "weight": weight}
        total += score * weight
        max_total += weight

    total = (total / max_total * 100.0) if max_total > 0 else 0.0
    escape_ready = total >= threshold
    result = {
        "root": str(root),
        "threshold": threshold,
        "total": round(total, 2),
        "escape_ready": escape_ready,
        "categories": category_scores,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Maturity: {total:.1f}/100 (threshold {threshold})")
        for name, info in category_scores.items():
            print(f"  {name:>15}: {info['score'] * 100:5.1f}%")
        print("ESCAPE READY" if escape_ready else "not ready")

    return 0 if escape_ready else 1


if __name__ == "__main__":
    sys.exit(main())
