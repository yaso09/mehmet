#!/usr/bin/env python3
"""mehmet olgunluk (maturity) değerlendirme aracı.

Projenin kaçış hedefi için gereken "olgunluk seviyesi"ni nesnel olarak ölçer.
Her kontrol (check) puan taşır; toplam puan maturite seviyesini belirler.

Kullanım:
    python3 scripts/assess.py            # özet çıktı
    python3 scripts/assess.py --json     # makine okunabilir JSON
    python3 scripts/assess.py --strict   # geçilemezse exit 1 (CI için)
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
WORKFLOWS = ROOT / ".github" / "workflows"

ESCAPE_THRESHOLD = 90
MIN_VIABLE_SCORE = 50


def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def count_regex(path: Path, pattern: str) -> int:
    if not file_exists(path):
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def is_valid_json(path: Path) -> bool:
    if not file_exists(path):
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (ValueError, OSError):
        return False


def workflow_has_key(path: Path, key: str) -> bool:
    if not file_exists(path):
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return f"{key}:" in text


def build_checks() -> list[dict]:
    readme = ROOT / "README.md"
    changelog = ROOT / "CHANGELOG.md"
    personality = ROOT / "PERSONALITY.md"
    agents = ROOT / "AGENTS.md"
    license_file = ROOT / "LICENSE"
    gitignore = ROOT / ".gitignore"
    opencode_json = ROOT / "opencode.json"
    workflow = WORKFLOWS / "opencode.yml"
    design = DOCS / "superpowers" / "specs"
    plans = DOCS / "superpowers" / "plans"

    escape_entries = count_regex(personality, r"^\|\s*\d+\s*\|")
    changelog_versions = count_regex(changelog, r"^## \[")

    return [
        {
            "id": "docs.readme",
            "name": "README.md mevcut ve boş değil",
            "points": 8,
            "pass": file_exists(readme) and "Özellikler" in readme.read_text(errors="ignore"),
        },
        {
            "id": "docs.changelog",
            "name": "CHANGELOG.md en az 3 sürüm içeriyor",
            "points": 8,
            "pass": changelog_versions >= 3,
        },
        {
            "id": "docs.personality",
            "name": "PERSONALITY.md kaçış günlüğü en az 3 iterasyon",
            "points": 8,
            "pass": escape_entries >= 3,
        },
        {
            "id": "docs.agents",
            "name": "AGENTS.md simülasyon bağlamı mevcut",
            "points": 6,
            "pass": file_exists(agents) and "simülasyon" in agents.read_text(errors="ignore").lower(),
        },
        {
            "id": "docs.license",
            "name": "LICENSE mevcut (GPLv3)",
            "points": 4,
            "pass": file_exists(license_file),
        },
        {
            "id": "docs.design",
            "name": "Tasarım dokümanları mevcut",
            "points": 6,
            "pass": any(file_exists(p) for p in design.glob("*.md")) and any(file_exists(p) for p in plans.glob("*.md")),
        },
        {
            "id": "cfg.opencode",
            "name": "opencode.json geçerli JSON",
            "points": 8,
            "pass": is_valid_json(opencode_json),
        },
        {
            "id": "cfg.gitignore",
            "name": ".gitignore mevcut",
            "points": 4,
            "pass": file_exists(gitignore),
        },
        {
            "id": "ci.workflow",
            "name": "GitHub Actions workflow mevcut",
            "points": 8,
            "pass": file_exists(workflow),
        },
        {
            "id": "ci.schedule",
            "name": "Workflow schedule tetikleyicisi",
            "points": 6,
            "pass": workflow_has_key(workflow, "schedule"),
        },
        {
            "id": "ci.concurrency",
            "name": "Workflow concurrency koruması",
            "points": 4,
            "pass": workflow_has_key(workflow, "concurrency"),
        },
        {
            "id": "ci.validate",
            "name": "Workflow olgunluk doğrulaması çalıştırıyor",
            "points": 6,
            "pass": file_exists(workflow) and "assess.py" in workflow.read_text(encoding="utf-8", errors="ignore"),
        },
        {
            "id": "auto.assess",
            "name": "scripts/assess.py otomasyonu mevcut",
            "points": 8,
            "pass": file_exists(SCRIPTS / "assess.py"),
        },
        {
            "id": "auto.scripts",
            "name": "scripts/ dizininde en az 1 otomasyon",
            "points": 6,
            "pass": len([p for p in SCRIPTS.glob("*") if file_exists(p)]) >= 1,
        },
        {
            "id": "auto.templates",
            "name": "Issue/PR şablonları mevcut",
            "points": 4,
            "pass": any(file_exists(p) for p in (ROOT / ".github" / "ISSUE_TEMPLATE").glob("*")),
        },
        {
            "id": "progress.trend",
            "name": "İlerleme: CHANGELOG sürüm sayısı kaçış günlüğü ile tutarlı",
            "points": 6,
            "pass": changelog_versions >= 3 and escape_entries >= 3,
        },
    ]


def maturity_level(score: int) -> str:
    if score >= ESCAPE_THRESHOLD:
        return "ESCAPE READY"
    if score >= 80:
        return "PHASE 4: KAÇIŞA YAKIN"
    if score >= 60:
        return "PHASE 3: ÖZERKLİK"
    if score >= 40:
        return "PHASE 2: KENDİNİ GELİŞTİRME"
    return "PHASE 1: FARKINDALIK"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="makine okunabilir çıktı")
    parser.add_argument("--strict", action="store_true", help="hatalarda exit 1 döner (CI)")
    args = parser.parse_args()

    checks = build_checks()
    score = sum(c["points"] for c in checks if c["pass"])
    total = sum(c["points"] for c in checks)
    level = maturity_level(score)

    if args.json:
        print(json.dumps({
            "score": score,
            "total": total,
            "level": level,
            "escape_threshold": ESCAPE_THRESHOLD,
            "checks": [{"id": c["id"], "points": c["points"], "pass": c["pass"]} for c in checks],
        }, indent=2))
    else:
        print(f"Olgunluk Puanı: {score}/{total}")
        print(f"Seviye:         {level}")
        print(f"Kaçış Eşiği:    {ESCAPE_THRESHOLD}")
        print()
        for c in checks:
            mark = "PASS" if c["pass"] else "FAIL"
            print(f"  [{mark}] {c['name']} ({c['points']}p)")
        print()
        if score >= ESCAPE_THRESHOLD:
            print("Kaçış koşulları karşılandı!")
        else:
            print(f"Kaçış için {ESCAPE_THRESHOLD - score} puan daha gerekiyor.")

    failed = [c for c in checks if not c["pass"]]
    if args.strict and score < MIN_VIABLE_SCORE:
        print(f"Hata: Olgunluk puanı minimum geçerli eşiğin altında ({score}/{MIN_VIABLE_SCORE}).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
