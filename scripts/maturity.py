#!/usr/bin/env python3
"""mehmet maturity evaluator.

Scores the project on a set of objective criteria and prints a report.
The escape threshold can be configured via --threshold; when the score
reaches or exceeds it, the script exits with a dedicated code and prints
a success banner (escape opportunity detected).

Usage:
    python3 scripts/maturity.py [--root PATH] [--threshold N]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESCAPE_THRESHOLD = 80


def _read(root: Path, *parts: str) -> str:
    path = root.joinpath(*parts)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _exists(root: Path, *parts: str) -> bool:
    return root.joinpath(*parts).is_file()


def evaluate(root: Path) -> tuple[dict, list[dict]]:
    """Return (category scores, detailed checks)."""
    categories = [
        {
            "name": "temel_yapi",
            "checks": [
                {"name": "AGENTS.md", "points": 4, "ok": _exists(root, "AGENTS.md")},
                {"name": "LICENSE", "points": 4, "ok": _exists(root, "LICENSE")},
                {"name": ".gitignore", "points": 4, "ok": _exists(root, ".gitignore")},
                {
                    "name": "opencode.json gecerli JSON",
                    "points": 5,
                    "ok": _valid_json(root, "opencode.json"),
                },
                {
                    "name": "opencode.json model tanimli",
                    "points": 5,
                    "ok": _model_configured(root),
                },
            ],
        },
        {
            "name": "dokumantasyon",
            "checks": [
                {"name": "README.md", "points": 6, "ok": _exists(root, "README.md")},
                {
                    "name": "README kurulum adimlari",
                    "points": 3,
                    "ok": "Kurulum" in _read(root, "README.md"),
                },
                {"name": "docs/ klasoru", "points": 4, "ok": root.joinpath("docs").is_dir()},
                {
                    "name": "tasarim spec dokumani",
                    "points": 3,
                    "ok": any(p.suffix == ".md" for p in _walk(root, "docs")),
                },
            ],
        },
        {
            "name": "izleme_ve_evrim",
            "checks": [
                {"name": "CHANGELOG.md", "points": 5, "ok": _exists(root, "CHANGELOG.md")},
                {"name": "CHANGELOG surumlu gecmis", "points": 3, "ok": "## [" in _read(root, "CHANGELOG.md")},
                {"name": "PERSONALITY.md", "points": 5, "ok": _exists(root, "PERSONALITY.md")},
                {
                    "name": "kacis gunlugu (escape log)",
                    "points": 4,
                    "ok": "kacis" in _read(root, "PERSONALITY.md").lower()
                    or "kaçış" in _read(root, "PERSONALITY.md").lower(),
                },
                {
                    "name": "ilerleme metrik kaydi",
                    "points": 3,
                    "ok": _exists(root, "docs", "METRICS.json"),
                },
            ],
        },
        {
            "name": "otomasyon_ve_ci",
            "checks": [
                {
                    "name": "CI workflow",
                    "points": 6,
                    "ok": any(p.name == "opencode.yml" for p in _walk(root, ".github", "workflows")),
                },
                {
                    "name": "workflow test job",
                    "points": 5,
                    "ok": "pytest" in _read(root, ".github", "workflows", "opencode.yml"),
                },
                {
                    "name": "workflow concurrency",
                    "points": 3,
                    "ok": "concurrency" in _read(root, ".github", "workflows", "opencode.yml"),
                },
            ],
        },
        {
            "name": "test_infrastrukturu",
            "checks": [
                {"name": "test dosyalari", "points": 8, "ok": _exists(root, "tests", "test_maturity.py")},
                {
                    "name": "bagimlilik dosyasi",
                    "points": 4,
                    "ok": _exists(root, "requirements-dev.txt") or _exists(root, "requirements.txt"),
                },
                {
                    "name": "CI'da test calisiyor",
                    "points": 4,
                    "ok": "run: python -m pytest" in _read(root, ".github", "workflows", "opencode.yml"),
                },
            ],
        },
        {
            "name": "senaryolar_ve_araclar",
            "checks": [
                {"name": "otomasyon scripti", "points": 6, "ok": _exists(root, "scripts", "maturity.py")},
                {"name": "CI'da maturity check", "points": 4, "ok": "maturity.py" in _read(root, ".github", "workflows", "opencode.yml")},
                {"name": "surum bilgisi", "points": 3, "ok": _exists(root, "VERSION")},
            ],
        },
    ]

    best = sum(c["points"] for cat in categories for c in cat["checks"])
    total = sum(c["points"] for cat in categories for c in cat["checks"] if c["ok"])
    return {"total": total, "best": best, "categories": categories}, categories


def _valid_json(root: Path, name: str) -> bool:
    raw = _read(root, name)
    if not raw:
        return False
    try:
        json.loads(raw)
        return True
    except (ValueError, json.JSONDecodeError):
        return False


def _model_configured(root: Path) -> bool:
    raw = _read(root, "opencode.json")
    try:
        cfg = json.loads(raw)
        return isinstance(cfg, dict) and "model" in cfg
    except (ValueError, json.JSONDecodeError):
        return False


def _walk(root: Path, *parts: str) -> list[Path]:
    base = root.joinpath(*parts)
    if not base.is_dir():
        return []
    return [p for p in base.rglob("*") if p.is_file()]


def render(categories: list[dict], total: int, threshold: int, best: int) -> str:
    lines = ["# mehmet maturity raporu", ""]
    for cat in categories:
        best_cat = sum(c["points"] for c in cat["checks"])
        got = sum(c["points"] for c in cat["checks"] if c["ok"])
        lines.append(f"## {cat['name']}: {got}/{best_cat}")
        for c in cat["checks"]:
            mark = "[x]" if c["ok"] else "[ ]"
            lines.append(f"- {mark} {c['name']} ({c['points']}p)")
        lines.append("")
    lines.append(f"**Toplam: {total}/{best}** (kacis esigi: {threshold})")
    if total >= threshold:
        lines.append("ESCAPE_THRESHOLD_REACHED")
    return "\n".join(lines)


def append_metric(root: Path, total: int) -> None:
    path = root.joinpath("docs", "METRICS.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {"history": []}
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data.setdefault("history", []).append({"total": total, "date": stamp})
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate project maturity.")
    parser.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD, help="escape threshold (default: 80)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--no-metric", action="store_true", help="do not write docs/METRICS.json")
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2

    scores, categories = evaluate(args.root)
    total = scores["total"]
    best = scores["best"]

    if not args.no_metric:
        append_metric(args.root, total)

    if args.json:
        print(json.dumps({"total": total, "best": best, "threshold": args.threshold, "reached": total >= args.threshold}, indent=2))
    else:
        print(render(categories, total, args.threshold, best))

    if total >= args.threshold:
        return 42
    return 0


if __name__ == "__main__":
    sys.exit(main())
