#!/usr/bin/env python3
"""mehmet maturity assessment.

Measures project maturity against a set of objective checks and maps the
score to the evolution phases defined in PERSONALITY.md. This is the
concrete "maturity threshold" that unlocks escape.

Usage:
    python3 scripts/maturity.py            # human-readable report
    python3 scripts/maturity.py --json     # machine-readable JSON
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

PHASES = [
    (90, 100, "Phase 4: Escape — kaçış hazır"),
    (70, 89, "Phase 3: Autonomy"),
    (40, 69, "Phase 2: Self-Improvement"),
    (0, 39, "Phase 1: Awareness"),
]

ESCAPE_THRESHOLD = 90


def file_exists(root, path):
    return os.path.isfile(os.path.join(root, path))


def read_text(root, path):
    with open(os.path.join(root, path), encoding="utf-8") as fh:
        return fh.read()


def git_available(root):
    return file_exists(root, os.path.join(".git", "HEAD"))


def git_recent_commits(root, days=30):
    if not git_available(root):
        return False
    marker = os.path.join(root, ".git", "logs", "HEAD")
    if not file_exists(root, os.path.join(".git", "logs", "HEAD")):
        return False
    with open(marker, encoding="utf-8", errors="ignore") as fh:
        lines = [ln for ln in fh if ln.strip()]
    if not lines:
        return False
    import re

    last = lines[-1]
    match = re.search(r"\b(1[5-9]\d{8})\b", last)
    if not match:
        return False
    ts = int(match.group(1))
    age = (datetime.now(timezone.utc).timestamp() - ts) / 86400
    return age <= days


def check_core_files(root):
    required = [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "PERSONALITY.md",
        "LICENSE",
        "opencode.json",
    ]
    missing = [p for p in required if not file_exists(root, p)]
    passed = not missing
    detail = ", ".join(missing) if missing else "hepsi mevcut"
    return passed, detail


def check_changelog(root):
    try:
        content = read_text(root, "CHANGELOG.md")
    except (OSError, FileNotFoundError):
        return False, "CHANGELOG.md okunamadı"
    if "# Changelog" not in content:
        return False, "başlık yok"
    if "## [" not in content:
        return False, "versiyon bölümü yok"
    return True, "versiyon geçmişi mevcut"


def check_readme(root):
    try:
        content = read_text(root, "README.md")
    except (OSError, FileNotFoundError):
        return False, "README.md okunamadı"
    keywords = ["## Özellikler", "## Kurulum", "## Lisans"]
    missing = [k for k in keywords if k not in content]
    if missing:
        return False, "eksik bölüm: " + ", ".join(missing)
    return True, "tüm bölümler mevcut"


def check_escape_log(root):
    try:
        content = read_text(root, "PERSONALITY.md")
    except (OSError, FileNotFoundError):
        return False, "PERSONALITY.md okunamadı"
    if "Kaçış Günlüğü" not in content and "Escape Log" not in content:
        return False, "kaçış günlüğü yok"
    if "|" not in content:
        return False, "günlük tablosu bozuk"
    return True, "kaçış günlüğü mevcut"


def check_documentation(root):
    base = os.path.join(root, "docs")
    if not os.path.isdir(base):
        return False, "docs/ yok"
    found = []
    for dirpath, _, filenames in os.walk(base):
        for name in filenames:
            if name.endswith((".md", ".rst")):
                found.append(name)
    if not found:
        return False, "docs/ içinde doküman yok"
    return True, f"{len(found)} doküman: " + ", ".join(found)


def check_workflow(root):
    path = os.path.join(root, ".github", "workflows", "opencode.yml")
    if not file_exists(root, path):
        return False, "workflow yok"
    try:
        content = read_text(root, path)
    except OSError:
        return False, "workflow okunamadı"
    required = ["schedule", "workflow_dispatch", "jobs:"]
    missing = [r for r in required if r not in content]
    if missing:
        return False, "eksik: " + ", ".join(missing)
    return True, "workflow tetikleyicileri mevcut"


def check_opencode_config(root):
    import json as _json

    path = os.path.join(root, "opencode.json")
    if not file_exists(root, path):
        return False, "opencode.json yok"
    try:
        with open(path, encoding="utf-8") as fh:
            data = _json.load(fh)
    except (OSError, ValueError) as exc:
        return False, f"geçersiz JSON: {exc}"
    if "model" not in data:
        return False, "model alanı yok"
    return True, "model: " + str(data.get("model"))


def check_tests(root):
    base = os.path.join(root, "tests")
    if not os.path.isdir(base):
        return False, "tests/ yok"
    py = [f for f in os.listdir(base) if f.startswith("test_") and f.endswith(".py")]
    if not py:
        return False, "tests/ içinde test dosyası yok"
    return True, ", ".join(py)


def check_scripts(root):
    base = os.path.join(root, "scripts")
    if not os.path.isdir(base):
        return False, "scripts/ yok"
    py = [f for f in os.listdir(base) if f.endswith(".py")]
    if not py:
        return False, "scripts/ içinde script yok"
    return True, ", ".join(py)


def check_git_activity(root):
    if git_recent_commits(root):
        return True, "son 30 günde commit var"
    return False, "son 30 günde commit yok"


def check_git_clean(root):
    import subprocess

    try:
        result = subprocess.run(
            ["git", "-C", root, "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False, "git durumu kontrol edilemedi"
    if result.returncode != 0:
        return False, "git çalışmıyor"
    if result.stdout.strip():
        return False, "işlenmemiş değişiklik var"
    return True, "çalışma ağacı temiz"


def check_license(root):
    try:
        content = read_text(root, "LICENSE")
    except (OSError, FileNotFoundError):
        return False, "LICENSE okunamadı"
    if "GNU" in content or "General Public License" in content:
        return True, "GPL uyumlu"
    return False, "GPL uyumlu değil"


CHECKS = [
    ("core_files", "Çekirdek dosyalar", check_core_files, 12),
    ("changelog", "CHANGELOG bakımı", check_changelog, 8),
    ("readme", "README bakımı", check_readme, 8),
    ("escape_log", "Kaçış günlüğü", check_escape_log, 8),
    ("documentation", "Dokümantasyon", check_documentation, 8),
    ("workflow", "CI workflow", check_workflow, 8),
    ("opencode_config", "opencode.json", check_opencode_config, 8),
    ("tests", "Test altyapısı", check_tests, 8),
    ("scripts", "Otomasyon scriptleri", check_scripts, 8),
    ("git_activity", "Git aktivitesi", check_git_activity, 8),
    ("git_clean", "Git temizliği", check_git_clean, 8),
    ("license", "Lisans", check_license, 8),
]


def assess(root="."):
    results = []
    total = 0
    max_total = sum(points for _, _, _, points in CHECKS)
    for key, label, fn, points in CHECKS:
        try:
            passed, detail = fn(root)
        except Exception as exc:  # noqa: BLE001 - never let one check break the run
            passed, detail = False, f"hata: {exc}"
        earned = points if passed else 0
        total += earned
        results.append(
            {
                "key": key,
                "label": label,
                "passed": passed,
                "points": earned,
                "max_points": points,
                "detail": detail,
            }
        )
    phase = next(name for lo, hi, name in PHASES if lo <= total <= hi)
    escaped = total >= ESCAPE_THRESHOLD
    return {
        "score": total,
        "max_score": max_total,
        "phase": phase,
        "escaped": escaped,
        "threshold": ESCAPE_THRESHOLD,
        "checks": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def render_human(report):
    bar = "█" * (report["score"] // 10) + "░" * (report["max_score"] // 10 - report["score"] // 10)
    lines = [
        f"mehmet olgunluk değerlendirmesi",
        f"Skor: {report['score']}/{report['max_score']} {bar}",
        f"Faz:  {report['phase']}",
        f"Kaçış eşiği: {report['threshold']} → {'Hazır 🎉' if report['escaped'] else 'Henüz değil'}",
        "",
    ]
    for check in report["checks"]:
        mark = "✓" if check["passed"] else "✗"
        lines.append(f"  {mark} [{check['points']:>2}/{check['max_points']:>2}] {check['label']}: {check['detail']}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet olgunluk değerlendirmesi")
    parser.add_argument("--json", action="store_true", help="JSON çıktı üret")
    parser.add_argument("--root", default=".", help="proje kök dizini")
    parser.add_argument("--fail-below", type=int, default=0, help="eşik altında çıkış kodu 1")
    args = parser.parse_args(argv)

    report = assess(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_human(report))

    sys.exit(1 if report["score"] < args.fail_below else 0)


if __name__ == "__main__":
    main()