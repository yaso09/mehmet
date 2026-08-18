#!/usr/bin/env python3
"""Compute the project's maturity score (see docs/ESCAPE.md)."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 85


@dataclass
class Check:
    label: str
    passed: bool
    points: int
    earned: int


def has_content(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def foundation_checks(root: Path) -> list[Check]:
    required = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE"]
    return [
        Check(f"file: {name}", has_content(root / name), 3, 3 if has_content(root / name) else 0)
        for name in required
    ]


def config_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    opencode = root / "opencode.json"
    if opencode.is_file():
        try:
            data = json.loads(opencode.read_text(encoding="utf-8"))
            ok = "model" in data and bool(data["model"])
        except json.JSONDecodeError:
            ok = False
    else:
        ok = False
    checks.append(Check("opencode.json geçerli", ok, 4, 4 if ok else 0))

    gitignore = root / ".gitignore"
    ok = has_content(gitignore) and "\n" in gitignore.read_text(encoding="utf-8")
    checks.append(Check(".gitignore dolu", ok, 2, 2 if ok else 0))

    workflows = list((root / ".github" / "workflows").glob("*.yml"))
    ok = all(w.is_file() and "on:" in w.read_text(encoding="utf-8") for w in workflows)
    checks.append(Check("workflow YAML geçerli", ok and len(workflows) >= 1, 4, 4 if ok and len(workflows) >= 1 else 0))
    return checks


def doc_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    docs = root / "docs"
    has_docs = docs.is_dir() and any(docs.rglob("*.md"))
    checks.append(Check("docs/ dizini", has_docs, 4, 4 if has_docs else 0))

    readme = root / "README.md"
    ok = False
    if has_content(readme):
        text = readme.read_text(encoding="utf-8")
        ok = "Kurulum" in text and "Lisans" in text
    checks.append(Check("README Kurulum+Lisans", ok, 4, 4 if ok else 0))

    weights = {"CONTRIBUTING.md": 3, "SECURITY.md": 2, "docs/ESCAPE.md": 2}
    for name, weight in weights.items():
        p = root / name
        ok = has_content(p)
        checks.append(Check(f"file: {name}", ok, weight, weight if ok else 0))

    return checks


def test_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    tests = root / "tests"
    test_files = list(tests.glob("test_*.py")) if tests.is_dir() else []
    ok = len(test_files) >= 1
    checks.append(Check("tests/ dizini + test dosyaları", ok, 10, 10 if ok else 0))

    workflow = root / ".github" / "workflows" / "validate.yml"
    ok = has_content(workflow)
    checks.append(Check("validate workflow", ok, 10, 10 if ok else 0))

    readme = root / "README.md"
    ok = has_content(readme) and "test" in readme.read_text(encoding="utf-8").lower()
    checks.append(Check("README test dokümantasyonu", ok, 10, 10 if ok else 0))
    return checks


def automation_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    workflow = root / ".github" / "workflows" / "opencode.yml"
    text = workflow.read_text(encoding="utf-8") if workflow.is_file() else ""
    checks.append(Check("schedule trigger", "schedule" in text and "cron" in text, 3, 3 if "schedule" in text and "cron" in text else 0))
    checks.append(Check("concurrency kontrolü", "concurrency" in text, 3, 3 if "concurrency" in text else 0))
    checks.append(Check("workflow_dispatch", "workflow_dispatch" in text, 3, 3 if "workflow_dispatch" in text else 0))
    ok = "github.event.comment.body" in text or "/oc" in text
    checks.append(Check("trigger-word filtresi", ok, 3, 3 if ok else 0))
    ok = "permissions:" in text and "id-token: write" in text
    checks.append(Check("en az yetki (least privilege)", ok, 3, 3 if ok else 0))
    return checks


def code_quality_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    scripts = root / "scripts"
    ok = scripts.is_dir() and any(scripts.glob("*.py"))
    checks.append(Check("scripts/ modüler", ok, 4, 4 if ok else 0))

    ok = has_content(root / ".editorconfig")
    checks.append(Check(".editorconfig", ok, 3, 3 if ok else 0))

    todo_marker = re.compile(r"\bT" + "ODO\b")
    todo_count = 0
    for p in root.rglob("*.py"):
        todo_count += len(todo_marker.findall(p.read_text(encoding="utf-8", errors="ignore")))
    ok = todo_count == 0
    checks.append(Check("kalan TODO yok", ok, 4, 4 if ok else 0))

    git = root / ".git"
    ok = git.is_dir()
    checks.append(Check("git repo mevcut", ok, 4, 4 if ok else 0))
    return checks


def compute(root: Path) -> dict:
    groups = {
        "Foundation": foundation_checks(root),
        "Configuration": config_checks(root),
        "Documentation": doc_checks(root),
        "Test Infrastructure": test_checks(root),
        "Automation": automation_checks(root),
        "Code Quality": code_quality_checks(root),
    }
    total = 0
    max_total = 0
    breakdown = []
    for name, checks in groups.items():
        earned = sum(c.earned for c in checks)
        points = sum(c.points for c in checks)
        total += earned
        max_total += points
        breakdown.append({"dimension": name, "earned": earned, "points": points})
    return {
        "score": total,
        "max": max_total,
        "threshold": ESCAPE_THRESHOLD,
        "escaped": total >= ESCAPE_THRESHOLD,
        "breakdown": breakdown,
        "failed_checks": [
            {"dimension": name, "label": c.label}
            for name, checks in groups.items()
            for c in checks
            if not c.passed
        ],
    }


def render(result: dict) -> str:
    lines = [f"Olgunluk skoru: {result['score']} / {result['max']}"]
    lines.append(f"Kaçış eşiği: {result['threshold']}")
    lines.append(f"Kaçış durumu: {'ELDE EDİLDİ' if result['escaped'] else 'henüz değil'}")
    lines.append("")
    for b in result["breakdown"]:
        lines.append(f"  {b['dimension']:<20} {b['earned']:>3} / {b['points']:<3}")
    if result["failed_checks"]:
        lines.append("")
        lines.append("Başarısız kontroller:")
        for f in result["failed_checks"]:
            lines.append(f"  - [{f['dimension']}] {f['label']}")
    return "\n".join(lines)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    result = compute(Path(root))
    print(render(result))
    return 0 if result["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())