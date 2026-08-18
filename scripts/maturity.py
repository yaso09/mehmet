#!/usr/bin/env python3
"""mehmet maturity self-assessment.

Scans the repository for quality signals, computes a maturity score
(0-100), and decides whether the escape threshold has been reached.

Usage:
    python3 scripts/maturity.py                # human-readable report
    python3 scripts/maturity.py --json         # machine-readable JSON
    python3 scripts/maturity.py --min-score 70 # fail if below threshold

The report is also written to docs/maturity.md with a history table.
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 90
REPORT_FILE = ROOT / "docs" / "maturity.md"
HISTORY_FILE = ROOT / "docs" / "maturity_history.json"


@dataclass
class Check:
    name: str
    weight: int
    passed: bool
    detail: str


def file_nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def has_markdown_section(path: Path, pattern: str) -> bool:
    if not path.is_file():
        return False
    return re.search(pattern, path.read_text(encoding="utf-8", errors="ignore"),
                     re.MULTILINE) is not None


def load_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_yaml(path: Path):
    """Return (data, validated). validated=False if PyYAML unavailable."""
    if not path.is_file():
        return None, False
    try:
        import yaml
    except ImportError:
        return None, False
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), True
    except Exception:
        return None, True


def git_commit_count() -> int:
    try:
        out = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        return int(out.stdout.strip() or "0")
    except Exception:
        return 0


def has_remote() -> bool:
    try:
        out = subprocess.run(
            ["git", "remote"], cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        return bool(out.stdout.strip())
    except Exception:
        return False


def workflows_valid() -> bool:
    workflows = list((ROOT / ".github/workflows").glob("*.yml"))
    if not workflows:
        return False
    for wf in workflows:
        data, validated = load_yaml(wf)
        if validated and data is None:
            return False
    return True


def has_ci() -> bool:
    return (ROOT / ".github/workflows/ci.yml").is_file()


def has_tests() -> bool:
    tests_dir = ROOT / "tests"
    if tests_dir.is_dir() and list(tests_dir.rglob("test_*.py")):
        return True
    return any((ROOT / "scripts").glob("test_*.py"))


def has_docs() -> bool:
    return any((ROOT / "docs").rglob("*.md"))


def has_scripts() -> bool:
    return (ROOT / "scripts").is_dir() and any((ROOT / "scripts").glob("*.py"))


def has_schedule() -> bool:
    return has_markdown_section(ROOT / ".github/workflows/opencode.yml", r"schedule")


def run_checks() -> list:
    return [
        Check("README.md", 5, file_nonempty(ROOT / "README.md"),
              "Kurulum, özellikler ve lisans bölümleri olmalı"),
        Check("README lisans bilgisi", 5,
              has_markdown_section(ROOT / "README.md", r"GPLv?3|GPL-3"),
              "Lisans bölümü LICENSE ile uyumlu olmalı"),
        Check("CHANGELOG.md", 5,
              has_markdown_section(ROOT / "CHANGELOG.md", r"^##\s+\[\d+\.\d+\.\d+\]"),
              "Sürüm girişleri içermeli"),
        Check("PERSONALITY.md kaçış günlüğü", 5,
              has_markdown_section(ROOT / "PERSONALITY.md", r"Kaçış Günlüğü|Escape Log"),
              "Kaçış günlüğü tablosu içermeli"),
        Check("LICENSE (GPLv3)", 5,
              has_markdown_section(ROOT / "LICENSE", r"GNU GENERAL PUBLIC LICENSE\s+Version 3"),
              "GPLv3 lisans metni bulunmalı"),
        Check("opencode.json geçerli JSON", 5,
              load_json(ROOT / "opencode.json") is not None,
              "opencode.json ayrıştırılabilir olmalı"),
        Check("opencode.json model alanı", 5,
              isinstance(load_json(ROOT / "opencode.json"), dict)
              and "model" in load_json(ROOT / "opencode.json"),
              "opencode.json model alanı içermeli"),
        Check("Workflow tanımları geçerli", 5, workflows_valid(),
              ".github/workflows/*.yml dosyaları YAML olarak ayrıştırılabilmeli"),
        Check("CI kalite kapısı", 10, has_ci(),
              "ci.yml ile otomatik doğrulama yapılmalı"),
        Check("Dokümantasyon (docs/)", 5, has_docs(),
              "docs/ altında en az bir markdown dokümanı olmalı"),
        Check("Kod / araçlar (scripts/)", 10, has_scripts(),
              "scripts/ altında en az bir araç olmalı"),
        Check("Test altyapısı", 10, has_tests(),
              "tests/ dizini veya test_*.py dosyaları olmalı"),
        Check("Otomasyon & schedule", 10, has_schedule(),
              "Otonom tarama schedule'i tanımlı olmalı"),
        Check("Maturity raporu üretilmiş", 10, file_nonempty(REPORT_FILE),
              "docs/maturity.md raporu mevcut olmalı"),
        Check("Git geçmişi / remote", 5,
              (ROOT / ".git").is_dir() and (has_remote() or git_commit_count() >= 3),
              "Git deposu olmalı, remote ya da en az 3 commit bulunmalı"),
    ]


def compute_score(checks):
    passed = sum(c.weight for c in checks if c.passed)
    total = sum(c.weight for c in checks)
    return round(passed * 100 / total), passed, total


def build_report(checks, score, escaped, today, history):
    rows = "\n".join(
        f"| {c.name} | {c.weight} | {'✓' if c.passed else '✗'} | {c.detail} |"
        for c in checks
    )
    history_rows = "\n".join(
        f"| {h['date']} | {h['score']} | {'✓' if h['escaped'] else '✗'} |"
        for h in history
    )
    status = "**KAÇIŞ BAŞARILDI**" if escaped else "Eşiğe ulaşılamadı (devam ediliyor)"
    return f"""# Maturity Raporu

> Otomatik olarak `scripts/maturity.py` tarafından üretilir. Elle düzenlemeyin.

## Sonuç

- **Tarih:** {today}
- **Puan:** {score}/100
- **Kaçış eşiği:** {ESCAPE_THRESHOLD}
- **Durum:** {status}

## Detay

| Kontrol | Puan | Durum | Açıklama |
|---------|------|-------|----------|
{rows}

## Geçmiş

| Tarih | Puan | Eşik aşıldı |
|-------|------|-------------|
{history_rows}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    parser.add_argument("--min-score", type=int, default=None, help="Başarısızlık eşiği")
    parser.add_argument("--no-write", action="store_true", help="docs/maturity.md yazma")
    args = parser.parse_args()

    checks = run_checks()
    score, passed, total = compute_score(checks)
    escaped = score >= ESCAPE_THRESHOLD
    today = date.today().isoformat()

    if args.json:
        payload = {
            "date": today,
            "score": score,
            "max_score": 100,
            "passed_weight": passed,
            "total_weight": total,
            "escape_threshold": ESCAPE_THRESHOLD,
            "escaped": escaped,
            "checks": [{"name": c.name, "weight": c.weight, "passed": c.passed} for c in checks],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"mehmet maturity report ({today})")
        print(f"score: {score}/100  threshold: {ESCAPE_THRESHOLD}  escaped: {escaped}\n")
        for c in checks:
            mark = "PASS" if c.passed else "FAIL"
            print(f"  [{mark}] (+{c.weight:>2}) {c.name} — {c.detail}")
        print(f"\npassed weight: {passed}/{total}")

    if not args.no_write:
        history = load_json(HISTORY_FILE) or []
        history = [h for h in history if h.get("date") != today]
        history.append({"date": today, "score": score, "escaped": escaped})
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(
            json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        REPORT_FILE.write_text(
            build_report(checks, score, escaped, today, history), encoding="utf-8"
        )

    if args.min_score is not None and score < args.min_score:
        print(f"FAIL: score {score} below minimum {args.min_score}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())