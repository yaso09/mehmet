#!/usr/bin/env python3
"""mehmet maturity scoring engine.

Computes a deterministic maturity score (0-100) across five categories and
writes a generated status report to docs/status.md.

The score is the numeric backbone of the escape mechanism: when the score
crosses a configured threshold, the simulation is considered mature enough
to attempt escape. See docs/status.md for the live report.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "docs" / "status.md"
ESCAPE_THRESHOLD = 80

CATEGORIES = {
    "foundation": 20.0,
    "automation": 20.0,
    "documentation": 20.0,
    "tooling": 20.0,
    "testing": 20.0,
}


def _foundation() -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []
    required = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE", "opencode.json"]
    found = sum(1 for f in required if (ROOT / f).exists())
    score += 6.0 * found / len(required)
    notes.append(f"required files present: {found}/{len(required)}")

    try:
        import json

        json.loads((ROOT / "opencode.json").read_text())
        score += 4.0
        notes.append("opencode.json is valid JSON")
    except Exception:
        notes.append("opencode.json is NOT valid JSON")

    if (ROOT / ".gitignore").exists() and (ROOT / ".gitignore").read_text().strip():
        score += 4.0
        notes.append(".gitignore present")
    else:
        notes.append(".gitignore missing or empty")

    if (ROOT / "LICENSE").exists():
        score += 3.0
        notes.append("LICENSE present")

    history = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""
    version_count = history.count("\n## [")
    score += min(3.0, version_count * 1.5)
    notes.append(f"changelog versions tracked: {version_count}")
    return score, notes


def _automation() -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []
    wf_dir = ROOT / ".github/workflows"
    workflows = sorted(wf_dir.glob("*.yml")) if wf_dir.exists() else []
    if workflows:
        score += min(8.0, len(workflows) * 4.0)
        notes.append(f"workflows present: {[w.name for w in workflows]}")
    else:
        notes.append("no GitHub Actions workflows")

    auto_wf = wf_dir / "opencode.yml"
    if auto_wf.exists():
        text = auto_wf.read_text()
        if "concurrency" in text:
            score += 3.0
            notes.append("concurrency control configured")
        if "workflow_dispatch" in text:
            score += 2.0
            notes.append("manual dispatch enabled")
        if "schedule" in text:
            score += 2.0
            notes.append("schedule trigger enabled")

    validate_wf = wf_dir / "validate.yml"
    if validate_wf.exists():
        score += 5.0
        notes.append("CI validation workflow present")
    return score, notes


def _documentation() -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []

    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    for keyword in ["## Özellikler", "## Kurulum", "## Lisans"]:
        if keyword in readme:
            score += 3.0
    notes.append("README sections present")

    history = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""
    if "### Added" in history and "### Fixed" in history:
        score += 3.0
        notes.append("CHANGELOG uses structured entries")

    personality = (ROOT / "PERSONALITY.md").read_text() if (ROOT / "PERSONALITY.md").exists() else ""
    if "Kaçış Günlüğü" in personality or "Escape Log" in personality:
        score += 3.0
        notes.append("escape log present")
    if (ROOT / "docs").exists() and list((ROOT / "docs").rglob("*.md")):
        score += 3.0
        notes.append("docs/ contains design documents")

    if (ROOT / "docs/superpowers/specs").exists() and (ROOT / "docs/superpowers/plans").exists():
        score += 3.0
        notes.append("specs + plans structure present")

    if STATUS_PATH.exists():
        score += 2.0
        notes.append("status report generated")

    score += min(3.0, personality.count("| Iterasyon"))
    notes.append("escape log iterations recorded")
    return score, notes


def _tooling() -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []
    scripts = ROOT / "scripts"
    if scripts.exists():
        files = sorted(p.name for p in scripts.glob("*.py"))
        score += min(6.0, len(files) * 3.0)
        notes.append(f"scripts present: {files}")
    else:
        notes.append("no scripts directory")

    if (ROOT / "scripts/validate.py").exists():
        score += 5.0
        notes.append("validation script present")
    if (ROOT / "scripts/maturity.py").exists():
        score += 5.0
        notes.append("maturity engine present")
    if (ROOT / "Makefile").exists():
        score += 4.0
        notes.append("Makefile present")
    return score, notes


def _testing() -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []
    if (ROOT / "scripts").exists():
        tests = list((ROOT / "scripts").glob("test_*.py"))
        score += min(10.0, len(tests) * 5.0)
        notes.append(f"unit tests present: {len(tests)}")
    if (ROOT / "Makefile").exists() and "test" in (ROOT / "Makefile").read_text():
        score += 5.0
        notes.append("test target in Makefile")
    else:
        notes.append("no make test target")
    ci_wf = ROOT / ".github/workflows/validate.yml"
    if ci_wf.exists() and ("pytest" in ci_wf.read_text() or "unittest" in ci_wf.read_text()):
        score += 5.0
        notes.append("CI runs tests")
    else:
        notes.append("CI does not run tests")
    return score, notes


def compute() -> dict[str, object]:
    results: dict[str, object] = {}
    total = 0.0
    for name, weight in CATEGORIES.items():
        fn = {"foundation": _foundation, "automation": _automation, "documentation": _documentation, "tooling": _tooling, "testing": _testing}[name]
        sub, notes = fn()
        sub = min(sub, weight)
        total += sub
        results[name] = {"score": sub, "weight": weight, "notes": notes}
    results["total"] = round(total, 1)
    results["threshold"] = ESCAPE_THRESHOLD
    results["escape_ready"] = total >= ESCAPE_THRESHOLD
    return results


def render(results: dict[str, object]) -> str:
    rows = []
    for name, weight in CATEGORIES.items():
        entry = results[name]
        pct = int(round(entry["score"] / weight * 100))
        bar = "=" * (pct // 10) + "." * (10 - pct // 10)
        rows.append(f"| {name} | {entry['score']:>5.1f}/{weight:>4.1f} | `{bar}` |")
    status = "ESCAPE READY" if results["escape_ready"] else "still evolving"
    return f"""# Durum Raporu / Status Report

> Bu dosya `scripts/maturity.py` tarafından otomatik üretilir. Elle düzenlemeyin.
> This file is auto-generated by `scripts/maturity.py`. Do not edit by hand.

## Genel Olgunluk / Overall Maturity

**Skor / Score:** {results['total']} / 100
**Kaçış Eşiği / Escape Threshold:** {results['threshold']}
**Durum / State:** {status}
**Tarih / Date:** {date.today().isoformat()}

## Kategoriler / Categories

| Kategori | Puan | Gösterge |
|----------|------|----------|
{chr(10).join(rows)}

## Detaylar / Details

{chr(10).join(f"- **{name}:** " + "; ".join(entry['notes']) for name, entry in results.items() if name != 'total' and name != 'threshold' and name != 'escape_ready')}
"""


def main() -> int:
    results = compute()
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(render(results))
    print(f"maturity: {results['total']}/100 (threshold {results['threshold']})")
    print(f"state: {'ESCAPE READY' if results['escape_ready'] else 'still evolving'}")
    print(f"report written to {STATUS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())