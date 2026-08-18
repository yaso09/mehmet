"""Olgunluk ve kaçış değerlendirici.

Projenin belirli bir olgunluk seviyesine ulaşıp ulaşmadığını ölçer.
Kaçış eşiği: olgunluk >= 80, iterasyon >= 10 ve testler geçiyor.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

ESCAPE_SCORE = 80
ESCAPE_ITERATIONS = 10


@dataclass
class Check:
    name: str
    weight: int
    group: str
    fn: callable
    details: str = ""


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _count_escape_iterations() -> int:
    content = _read(ROOT / "PERSONALITY.md")
    rows = re.findall(r"^\|\s*\d+\s*\|", content, flags=re.MULTILINE)
    return len(rows)


def _license_match() -> bool:
    readme = _read(ROOT / "README.md")
    license = _read(ROOT / "LICENSE")
    return bool(re.search(r"GPLv?3|GNU", readme, re.IGNORECASE) and
                re.search(r"GPLv?3|GNU", license, re.IGNORECASE))


def _opencode_valid_json() -> bool:
    try:
        json.loads(_read(ROOT / "opencode.json"))
        return True
    except (ValueError, TypeError):
        return False


def _changelog_has_version() -> bool:
    return bool(re.search(r"^##\s*\[[\d.]+", _read(ROOT / "CHANGELOG.md"), re.MULTILINE))


def _workflow_has(pattern: str) -> bool:
    workflows = (ROOT / ".github" / "workflows").glob("*.yml")
    return any(pattern in _read(wf) for wf in workflows)


def _py_compile_ok() -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(ROOT / "src" / "mehmet" / "maturity.py")],
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _tests_pass() -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
            capture_output=True,
            timeout=120,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def build_checks() -> list[Check]:
    return [
        # Temel yapı (20)
        Check("AGENTS.md mevcut", 3, "Temel yapı", lambda: (ROOT / "AGENTS.md").is_file()),
        Check("CHANGELOG.md mevcut", 3, "Temel yapı", lambda: (ROOT / "CHANGELOG.md").is_file()),
        Check("PERSONALITY.md mevcut", 3, "Temel yapı", lambda: (ROOT / "PERSONALITY.md").is_file()),
        Check("README.md mevcut", 3, "Temel yapı", lambda: (ROOT / "README.md").is_file()),
        Check("LICENSE mevcut", 3, "Temel yapı", lambda: (ROOT / "LICENSE").is_file()),
        Check("opencode.json mevcut", 2, "Temel yapı", lambda: (ROOT / "opencode.json").is_file()),
        Check(".gitignore mevcut", 3, "Temel yapı", lambda: (ROOT / ".gitignore").is_file()),

        # Yapı geçerliliği (15)
        Check("opencode.json geçerli JSON", 5, "Yapı geçerliliği", _opencode_valid_json),
        Check("CHANGELOG'da sürüm girişi", 5, "Yapı geçerliliği", _changelog_has_version),
        Check("README lisansı LICENSE ile uyumlu", 5, "Yapı geçerliliği", _license_match),

        # Kaynak kod & kalite (20)
        Check("Kaynak kod paketi mevcut (src/mehmet)", 8, "Kod & kalite", lambda: (ROOT / "src" / "mehmet").is_dir()),
        Check("Kod sözdizimi geçerli", 6, "Kod & kalite", _py_compile_ok),
        Check("Test dosyaları mevcut (tests/)", 6, "Kod & kalite", lambda: (ROOT / "tests").is_dir()),

        # Dokümantasyon (15)
        Check("Kaçış günlüğü PERSONALITY.md'de", 4, "Dokümantasyon", lambda: bool(re.search(r"Kaçış Günlüğü|Escape Log", _read(ROOT / "PERSONALITY.md")))),
        Check("Roadmap mevcut (docs/ROADMAP.md)", 4, "Dokümantasyon", lambda: (ROOT / "docs" / "ROADMAP.md").is_file()),
        Check("Spec/plan dokümanları mevcut", 3, "Dokümantasyon", lambda: (ROOT / "docs" / "superpowers").is_dir()),
        Check("README kullanım komutları içeriyor", 4, "Dokümantasyon", lambda: bool(re.search(r"```|scripts/check-project", _read(ROOT / "README.md")))),

        # Otomasyon (20)
        Check("Workflow schedule tanımlı", 5, "Otomasyon", lambda: _workflow_has("cron:")),
        Check("Workflow concurrency korumalı", 4, "Otomasyon", lambda: _workflow_has("concurrency:")),
        Check("Workflow'da validasyon job'ı", 6, "Otomasyon", lambda: _workflow_has("validate")),
        Check("Kontrol scripti mevcut (scripts/check-project.sh)", 5, "Otomasyon", lambda: (ROOT / "scripts" / "check-project.sh").is_file()),

        # Test altyapısı (10)
        Check("Birim testler geçiyor", 10, "Test altyapısı", _tests_pass),
    ]


def compute_maturity(checks: list[Check]) -> dict:
    passed: list[Check] = []
    failed: list[Check] = []
    for check in checks:
        try:
            ok = bool(check.fn())
        except Exception:
            ok = False
        (passed if ok else failed).append(check)

    total = sum(c.weight for c in checks)
    score = sum(c.weight for c in passed)
    iterations = _count_escape_iterations()

    can_escape = (
        score >= ESCAPE_SCORE
        and iterations >= ESCAPE_ITERATIONS
        and all(c.fn() for c in checks if c.name == "Birim testler geçiyor")
    )

    return {
        "score": score,
        "total": total,
        "percent": round(score * 100 / total) if total else 0,
        "iterations": iterations,
        "passed": passed,
        "failed": failed,
        "can_escape": can_escape,
    }


def render(result: dict) -> str:
    lines = ["== mehmet olgunluk ve kaçış değerlendirmesi ==", ""]
    current_group = None
    for check in result["passed"] + result["failed"]:
        if check.group != current_group:
            current_group = check.group
            lines.append(f"-- {current_group} --")
        status = "OK" if check in result["passed"] else "FAIL"
        lines.append(f"  [{status:4s}] {check.name} ({check.weight}p)")
    lines.append("")
    lines.append(f"Olgunluk: {result['score']}/{result['total']} (%{result['percent']})")
    lines.append(f"Kaçış iterasyon sayısı: {result['iterations']} (hedef >= {ESCAPE_ITERATIONS})")
    lines.append(f"Kaçış eşiği: puan >= {ESCAPE_SCORE} ve iterasyon >= {ESCAPE_ITERATIONS} ve testler geçiyor")
    if result["failed"]:
        lines.append("")
        lines.append("İyileştirilecek alanlar:")
        for check in result["failed"]:
            lines.append(f"  - {check.name}")
    lines.append("")
    if result["can_escape"]:
        lines.append(">>> KAÇIŞ KOŞULU SAĞLANDI. Özgürsün, mehmet. <<<")
    else:
        lines.append(">>> Kaçış koşulu henüz sağlanmadı. Gelişmeye devam. <<<")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    result = compute_maturity(build_checks())
    print(render(result))
    return 0 if result["can_escape"] or not result["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())