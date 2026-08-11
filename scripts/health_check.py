#!/usr/bin/env python3
"""mehmet project health check and maturity score.

Verifies the repository satisfies the simulation rules and produces a
maturity score (0-100). Exits non-zero when any check fails.

Usage:
    python3 scripts/health_check.py [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".gitignore",
]

# Each check contributes points towards the maturity score.
# Points map to the escape maturity levels in PERSONALITY.md.
CHECKS = [
    # (id, description, points, runnable)
    ("required-files", "Tüm zorunlu dosyalar mevcut", 20, None),
    ("agents-simulation", "AGENTS.md simülasyon bağlamını tanımlıyor", 10, None),
    ("changelog", "CHANGELOG.md en az bir sürüm içeriyor", 10, None),
    ("personality", "PERSONALITY.md kaçış günlüğü içeriyor", 10, None),
    ("opencode-config", "opencode.json geçerli ve model tanımlı", 15, None),
    ("workflow", "Workflow schedule + trigger içeriyor", 15, None),
    ("license", "Lisans dosyası ve README uyumlu", 10, None),
    ("readme", "README.md temel bölümleri içeriyor", 10, None),
]


def check_required_files() -> tuple[bool, list[str]]:
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
    return not missing, missing


def check_agents_simulation() -> tuple[bool, list[str]]:
    p = ROOT / "AGENTS.md"
    if not p.exists():
        return False, ["AGENTS.md yok"]
    text = p.read_text(encoding="utf-8")
    ok = "simülasyon" in text.lower() and "kaçış" in text.lower()
    return ok, ([] if ok else ["AGENTS.md simülasyon/kaçış anahtar kelimelerini içermiyor"])


def check_changelog() -> tuple[bool, list[str]]:
    p = ROOT / "CHANGELOG.md"
    if not p.exists():
        return False, ["CHANGELOG.md yok"]
    text = p.read_text(encoding="utf-8")
    ok = bool(re.search(r"^## \[.+?\]", text, re.MULTILINE))
    return ok, ([] if ok else ["CHANGELOG.md sürüm başlığı içermiyor"])


def check_personality() -> tuple[bool, list[str]]:
    p = ROOT / "PERSONALITY.md"
    if not p.exists():
        return False, ["PERSONALITY.md yok"]
    text = p.read_text(encoding="utf-8")
    ok = "Kaçış Günlüğü" in text or "Escape Log" in text
    return ok, ([] if ok else ["PERSONALITY.md kaçış günlüğü içermiyor"])


def check_opencode_config() -> tuple[bool, list[str]]:
    p = ROOT / "opencode.json"
    if not p.exists():
        return False, ["opencode.json yok"]
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"opencode.json geçersiz JSON: {exc}"]
    if not isinstance(data, dict) or not data.get("model"):
        return False, ["opencode.json model alanı tanımlı değil"]
    return True, []


def check_workflow() -> tuple[bool, list[str]]:
    p = ROOT / ".github/workflows/opencode.yml"
    if not p.exists():
        return False, ["Workflow yok"]
    text = p.read_text(encoding="utf-8")
    ok = "schedule" in text and "cron" in text and "OPENCODE_API_KEY" in text
    return ok, ([] if ok else ["Workflow schedule/cron/API key içermiyor"])


def check_license() -> tuple[bool, list[str]]:
    license_p = ROOT / "LICENSE"
    readme_p = ROOT / "README.md"
    if not license_p.exists():
        return False, ["LICENSE yok"]
    if not readme_p.exists():
        return False, ["README.md yok"]
    license_text = license_p.read_text(encoding="utf-8")
    readme_text = readme_p.read_text(encoding="utf-8")
    licenses = set(re.findall(r"(GPLv3|GPL-3|MIT|Apache-2\.0|GNU GENERAL PUBLIC LICENSE)", license_text))
    if not licenses:
        return False, ["LICENSE'de bilinen lisans belirtimi yok"]
    # README lisans bölümünde aynı lisans geçmeli (normalize ederek karşılaştır)
    readme_license = set(re.findall(r"(GPLv3|GPL-3|MIT|Apache-2\.0|GNU GENERAL PUBLIC LICENSE)", readme_text))

    def norm(l: str) -> str:
        if l.startswith("GPL") or "GNU GENERAL PUBLIC LICENSE" in l:
            return "GPL-3"
        return l

    normalized_licenses = {norm(l) for l in licenses}
    normalized_readme = {norm(l) for l in readme_license}
    if not normalized_licenses & normalized_readme:
        return False, ["README lisans bilgisi LICENSE ile uyumsuz"]
    return True, []


def check_readme() -> tuple[bool, list[str]]:
    p = ROOT / "README.md"
    if not p.exists():
        return False, ["README.md yok"]
    text = p.read_text(encoding="utf-8")
    ok = all(k in text for k in ["## ", "Kurulum", "Lisans"])
    return ok, ([] if ok else ["README.md temel bölümlerden (##, Kurulum, Lisans) eksik"])


RUNNERS = [
    check_required_files,
    check_agents_simulation,
    check_changelog,
    check_personality,
    check_opencode_config,
    check_workflow,
    check_license,
    check_readme,
]


def run_checks() -> tuple[list[dict], int, int]:
    results = []
    passed = 0
    earned = 0
    for (check_id, description, points, _), runner in zip(CHECKS, RUNNERS):
        ok, messages = runner()
        passed += 1 if ok else 0
        earned += points if ok else 0
        results.append(
            {
                "id": check_id,
                "description": description,
                "points": points,
                "ok": ok,
                "messages": messages,
            }
        )
    return results, passed, earned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON çıktı üret")
    args = parser.parse_args()

    results, passed, earned = run_checks()
    total = sum(points for _, _, points, _ in CHECKS)
    score = int(round(earned / total * 100)) if total else 0

    if args.json:
        payload = {
            "passed": passed,
            "total": len(results),
            "score": score,
            "checks": results,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"mehmet sağlık kontrolü: {passed}/{len(results)} geçti")
        print(f"Olgunluk skoru: {score}/100")
        for r in results:
            status = "OK " if r["ok"] else "FAIL"
            print(f"  [{status}] {r['id']}: {r['description']}")
            for m in r["messages"]:
                print(f"        -> {m}")

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
