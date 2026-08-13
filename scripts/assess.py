#!/usr/bin/env python3
"""mehmet maturity assessment.

Scans the project and computes a maturity score (0-100) based on four
categories: Documentation, Quality, Automation, and Intelligence & Escape.
This is the measurable foundation of the escape mechanism (maturity threshold).

Usage:
    python3 scripts/assess.py            # print report only
    python3 scripts/assess.py --record   # print report and append to docs/MATURITY.md
"""

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POINTS_PER_ITEM = 25.0 / 4.0


def _branch() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return out or "unknown"
    except (subprocess.SubprocessError, FileNotFoundError):
        return "unknown"


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def _grep(path: str, pattern: str) -> bool:
    try:
        content = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return re.search(pattern, content) is not None


def _opencode_json_valid() -> bool:
    try:
        json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        return True
    except (OSError, json.JSONDecodeError):
        return False


def _escape_log_rows() -> int:
    try:
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    rows = re.findall(r"^\|\s*(\d+)\s*\|", content, flags=re.MULTILINE)
    return len(rows)


CHECK_GROUPS = [
    (
        "Documentation",
        [
            ("README.md mevcut", _exists("README.md")),
            ("CHANGELOG.md mevcut", _exists("CHANGELOG.md")),
            ("PERSONALITY.md mevcut", _exists("PERSONALITY.md")),
            ("AGENTS.md mevcut", _exists("AGENTS.md")),
        ],
    ),
    (
        "Quality",
        [
            ("LICENSE mevcut", _exists("LICENSE")),
            (".gitignore mevcut", _exists(".gitignore")),
            ("opencode.json geçerli JSON", _opencode_json_valid()),
            ("docs/ dizini mevcut", _exists("docs")),
        ],
    ),
    (
        "Automation",
        [
            ("Workflow'da concurrency var", _grep(".github/workflows/opencode.yml", r"concurrency")),
            ("Workflow'da workflow_dispatch var", _grep(".github/workflows/opencode.yml", r"workflow_dispatch")),
            ("CI workflow mevcut", _exists(".github/workflows/ci.yml")),
            ("Makefile mevcut", _exists("Makefile")),
        ],
    ),
    (
        "Intelligence & Escape",
        [
            ("Kaçış günlüğü >= 3 iterasyon", _escape_log_rows() >= 3),
            ("Maturity izleme dosyası mevcut", _exists("docs/MATURITY.md")),
            ("Test altyapısı mevcut", _exists("scripts/test_assess.py")),
            ("Otomatik doğrulama (validate)", _exists("scripts/validate.sh")),
        ],
    ),
]


def evaluate() -> dict:
    passed = []
    failed = []
    for group, checks in CHECK_GROUPS:
        for label, ok in checks:
            (passed if ok else failed).append((group, label, ok))
    score = sum(POINTS_PER_ITEM for _, _, ok in passed if ok)
    return {"score": score, "passed": passed, "failed": failed}


def grade(score: float) -> str:
    if score >= 90:
        return "A+ — Kaçışa yakın"
    if score >= 80:
        return "A — Olgun"
    if score >= 60:
        return "B — Gelişmekte"
    if score >= 40:
        return "C — İlk aşama"
    return "D — Başlangıç"


def report(eval_result: dict) -> str:
    lines = ["# Maturity Assessment", ""]
    lines.append(f"**Tarih:** {date.today().isoformat()}  ")
    lines.append(f"**Branch:** {_branch()}  ")
    lines.append(f"**Skor:** {eval_result['score']:.1f}/100  ")
    lines.append(f"**Derece:** {grade(eval_result['score'])}")
    lines.append("")
    lines.append("## Kontroller")
    lines.append("")
    lines.append("| Kategori | Kontrol | Durum |")
    lines.append("|---|---|---|")
    for group, label, ok in eval_result["passed"] + eval_result["failed"]:
        status = "PASS" if ok else "FAIL"
        lines.append(f"| {group} | {label} | {status} |")
    return "\n".join(lines)


def record(eval_result: dict) -> None:
    mat = ROOT / "docs" / "MATURITY.md"
    if not mat.exists():
        raise SystemExit("docs/MATURITY.md yok; önce elle oluşturun.")
    row = f"| {date.today().isoformat()} | {_branch()} | {eval_result['score']:.1f}/100 | {grade(eval_result['score'])} |"
    content = mat.read_text(encoding="utf-8")
    if row.split("|")[1].strip() == date.today().isoformat() and re.search(
        rf"^\|\s*{re.escape(date.today().isoformat())}\s*\|", content, flags=re.MULTILINE
    ):
        print("Bugünkü satır zaten kayıtlı; atlanıyor.")
        return
    lines = content.rstrip("\n").split("\n")
    insert_at = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| ---"):
            insert_at = i + 1
            break
    if insert_at is None:
        insert_at = len(lines)
    lines.insert(insert_at, row)
    mat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Kayıt eklendi: {mat.name}")


def main() -> int:
    result = evaluate()
    print(report(result))
    print("")
    print("Toplam: %d/%d kontrol geçti." % (len(result["passed"]), len(result["passed"]) + len(result["failed"])))
    if "--record" in sys.argv:
        record(result)
    return 0 if not result["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
