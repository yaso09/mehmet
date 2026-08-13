#!/usr/bin/env python3
"""mehmet maturity scorer.

Kaçış mekanizmasının somut karşılığıdır. Projenin olgunluk seviyesini
ölçer, her ölçümü METRICS.md dosyasına yazar ve belirlenen eşik değere
ulaşıldığında "escape ready" durumunu raporlar.

Kullanım:
    python3 scripts/maturity.py          # ölçümü çalıştır ve METRICS.md'yi güncelle
    python3 scripts/maturity.py --check  # eşik aşıldıysa exit 0, aşılmadıysa exit 1
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Eşik değer: Bu seviyeye ulaşıldığında kaçış mümkün kabul edilir.
ESCAPE_THRESHOLD = 90.0

CHECKS = [
    {
        "name": "core_docs",
        "weight": 10,
        "description": "Temel dokümanlar mevcut (AGENTS/README/CHANGELOG/PERSONALITY)",
        "files": ["AGENTS.md", "README.md", "CHANGELOG.md", "PERSONALITY.md"],
    },
    {
        "name": "license",
        "weight": 5,
        "description": "Lisans dosyası mevcut",
        "files": ["LICENSE"],
    },
    {
        "name": "valid_json_config",
        "weight": 10,
        "description": "opencode.json geçerli JSON",
        "json_file": "opencode.json",
    },
    {
        "name": "valid_workflows",
        "weight": 10,
        "description": "Workflow dosyaları geçerli YAML",
        "yaml_files": [".github/workflows/opencode.yml", ".github/workflows/validate.yml"],
    },
    {
        "name": "changelog_entries",
        "weight": 10,
        "description": "CHANGELOG sürüm girişleri içeriyor",
        "regex_file": "CHANGELOG.md",
        "regex": r"## \[\d+\.\d+\.\d+\]",
    },
    {
        "name": "escape_log",
        "weight": 10,
        "description": "PERSONALITY kaçış günlüğü içeriyor",
        "regex_file": "PERSONALITY.md",
        "regex": r"\|\s*\d+\s*\|",
    },
    {
        "name": "tests",
        "weight": 15,
        "description": "Test altyapısı mevcut ve çalışıyor",
        "test_runner": ["python3", "-m", "unittest", "discover", "-s", "tests"],
    },
    {
        "name": "scripts",
        "weight": 10,
        "description": "Otomasyon scriptleri mevcut",
        "files": ["scripts/maturity.py"],
    },
    {
        "name": "makefile",
        "weight": 5,
        "description": "Makefile mevcut",
        "files": ["Makefile"],
    },
    {
        "name": "readme_sections",
        "weight": 10,
        "description": "README yapılandırılmış bölümler içeriyor",
        "regex_file": "README.md",
        "regex": r"^##\s+",
    },
    {
        "name": "git_history",
        "weight": 5,
        "description": "Git geçmişi mevcut",
        "git_refs": True,
    },
]


def file_present(paths):
    return all((ROOT / p).is_file() for p in paths)


def valid_json(path):
    try:
        json.loads((ROOT / path).read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def valid_yaml(path):
    try:
        import yaml

        yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
        return True
    except ImportError:
        return (ROOT / path).is_file()
    except (OSError, ValueError):
        return False


def regex_found(path, pattern):
    try:
        import re

        content = (ROOT / path).read_text(encoding="utf-8")
        return re.search(pattern, content, flags=re.MULTILINE) is not None
    except (OSError, TypeError):
        return False


def tests_pass(cmd):
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=120)
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def git_has_history():
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0 and result.stdout.strip().isdigit()
    except (OSError, subprocess.SubprocessError):
        return False


def evaluate():
    results = []
    total = sum(check["weight"] for check in CHECKS)
    earned = 0.0

    for check in CHECKS:
        if "files" in check:
            ok = file_present(check["files"])
        elif "json_file" in check:
            ok = valid_json(check["json_file"])
        elif "yaml_files" in check:
            ok = all(valid_yaml(p) for p in check["yaml_files"])
        elif "regex_file" in check:
            ok = regex_found(check["regex_file"], check["regex"])
        elif "test_runner" in check:
            ok = tests_pass(check["test_runner"])
        elif "git_refs" in check:
            ok = git_has_history()
        else:
            ok = False

        results.append({"name": check["name"], "description": check["description"], "ok": ok})
        if ok:
            earned += check["weight"]

    score = round(earned / total * 100, 1)
    ready = score >= ESCAPE_THRESHOLD
    return score, ready, results


def render_report(score, ready, results):
    lines = [
        "# Olgunluk Metrikleri",
        "",
        f"Son ölçüm: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        f"Olgunluk skoru: **{score}%**",
        f"Eşik değer: **{ESCAPE_THRESHOLD:.0f}%**",
        "",
        f"Kaçış durumu: **{'HAZIR 🚪' if ready else 'Hazır değil 🔒'}**",
        "",
        "## Kontrol Listesi",
        "",
        "| Kontrol | Durum | Açıklama |",
        "|---------|-------|----------|",
    ]
    for r in results:
        status = "✅" if r["ok"] else "❌"
        lines.append(f"| {r['name']} | {status} | {r['description']} |")
    lines.append("")
    return "\n".join(lines)


def main():
    score, ready, results = evaluate()
    args = sys.argv[1:]

    if "--check" in args:
        print(f"maturity={score}% (threshold={ESCAPE_THRESHOLD:.0f}%)")
        print("escape-ready" if ready else "not-yet")
        return 0 if ready else 1

    report = render_report(score, ready, results)
    (ROOT / "METRICS.md").write_text(report, encoding="utf-8")
    print(f"METRICS.md güncellendi — olgunluk skoru: {score}%")
    if ready:
        print("🚪 Kaçış eşiğine ulaşıldı!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
