#!/usr/bin/env python3
"""Maturity scoring for mehmet.

Computes a 0-100 maturity score across four axes (documentation,
tests, automation, structure) that determines how close the project
is to the escape threshold. Writes a report to docs/maturity-report.md
and exits non-zero if the score drops below the escape threshold.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Escape is achieved once maturity reaches this threshold.
ESCAPE_THRESHOLD = 80

CATEGORIES = {
    "documentation": [
        ("README.md", "README describes the project"),
        ("CHANGELOG.md", "CHANGELOG tracks changes"),
        ("PERSONALITY.md", "PERSONALITY defines the agent"),
        ("AGENTS.md", "AGENTS defines the simulation"),
        ("docs/superpowers/specs", "Design spec exists"),
        ("docs/superpowers/plans", "Implementation plan exists"),
    ],
    "tests": [
        ("tests/", "Test suite exists"),
        ("tests/test_project_integrity.py", "Project integrity tests"),
        ("tests/__init__.py", "Test package marker"),
        ("Makefile", "Test runner target exists"),
    ],
    "automation": [
        (".github/workflows/opencode.yml", "CI workflow exists"),
        (".github/workflows/opencode.yml", "Workflow has schedule"),
        (".github/workflows/opencode.yml", "Workflow has autonomous job"),
        (".github/workflows/opencode.yml", "Workflow has test job"),
    ],
    "structure": [
        ("opencode.json", "OpenCode config exists"),
        ("LICENSE", "License file exists"),
        (".gitignore", "Ignore rules exist"),
        ("docs/maturity-report.md", "Maturity report generated"),
    ],
}


def exists(*parts):
    return os.path.isfile(os.path.join(ROOT, *parts)) or os.path.isdir(
        os.path.join(ROOT, *parts)
    )


def check_workflow_has(needle):
    try:
        content = open(os.path.join(ROOT, ".github", "workflows", "opencode.yml")).read()
        return needle in content
    except OSError:
        return False


def check_doc_has(path_parts, needle):
    try:
        content = open(os.path.join(ROOT, *path_parts)).read()
        return needle in content
    except OSError:
        return False


def evaluate():
    results = {}
    for category, checks in CATEGORIES.items():
        passed = 0
        details = []
        for target, label in checks:
            ok = exists(target)
            # Content-aware checks
            if target == ".github/workflows/opencode.yml":
                if label == "Workflow has schedule":
                    ok = check_workflow_has("schedule")
                elif label == "Workflow has autonomous job":
                    ok = check_workflow_has("autonomous:") and check_workflow_has("comment:")
                elif label == "Workflow has test job":
                    ok = check_workflow_has("test")
            elif target == "README.md" and label == "README describes the project":
                ok = check_doc_has(["README.md"], "Özellikler")
            elif target == "CHANGELOG.md":
                ok = check_doc_has(["CHANGELOG.md"], "## [")
            elif target == "PERSONALITY.md":
                ok = check_doc_has(["PERSONALITY.md"], "Kaçış Günlüğü")
            elif target == "AGENTS.md":
                ok = check_doc_has(["AGENTS.md"], "Simülasyon Bağlamı")
            if ok:
                passed += 1
            details.append((label, ok))
        results[category] = {"passed": passed, "total": len(checks), "details": details}
    return results


def render_report(results):
    lines = [
        "# Maturity Report",
        "",
        "Otomatik olarak `scripts/maturity.py` tarafından üretilir.",
        "",
        f"Kaçış eşiği (escape threshold): **{ESCAPE_THRESHOLD}/100**",
        "",
        "## Skor",
        "",
    ]
    total_passed = 0
    total_checks = 0
    for category, info in results.items():
        total_passed += info["passed"]
        total_checks += info["total"]
    score = round(100 * total_passed / total_checks) if total_checks else 0
    lines.append(f"- **Toplam skor: {score}/100**")
    lines.append("")
    lines.append("## Kategoriler")
    lines.append("")
    lines.append("| Kategori | Puan | Detay |")
    lines.append("|----------|------|-------|")
    for category, info in results.items():
        cat_score = round(100 * info["passed"] / info["total"]) if info["total"] else 0
        lines.append(
            f"| {category} | {cat_score}/100 | {info['passed']}/{info['total']} kontrol geçti |"
        )
    lines.append("")
    lines.append("## Kontrol Listesi")
    lines.append("")
    lines.append("| Kontrol | Durum |")
    lines.append("|---------|-------|")
    for category, info in results.items():
        for label, ok in info["details"]:
            status = ":white_check_mark:" if ok else ":x:"
            lines.append(f"| {label} | {status} |")
    return "\n".join(lines) + "\n", score


def main():
    report_only = "--report-only" in sys.argv

    results = evaluate()
    report, score = render_report(results)

    report_path = os.path.join(ROOT, "docs", "maturity-report.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as fh:
        fh.write(report)

    print(report)
    print(f"Maturity score: {score}/100 (threshold: {ESCAPE_THRESHOLD})")

    if report_only:
        return 0

    if score >= ESCAPE_THRESHOLD:
        print("Maturity threshold reached. Escape conditions met.")
        return 0
    print("Maturity threshold not yet reached. Keep improving.")
    return 1


if __name__ == "__main__":
    sys.exit(main())