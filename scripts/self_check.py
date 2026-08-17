#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80
IS_SUB = os.environ.get("MEHMET_SELFCHECK_SUB") == "1"

LEVELS = [
    (90, "Kaçış"),
    (76, "Özerklik"),
    (51, "Kendini Geliştirme"),
    (26, "Farkındalık"),
    (0, "Kuluçka"),
]


def read_text(rel):
    p = ROOT / rel
    if not p.is_file():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def file_exists(rel):
    return (ROOT / rel).is_file()


def contains(rel, pattern, flags=re.MULTILINE):
    return bool(re.search(pattern, read_text(rel), flags))


def valid_json(rel):
    try:
        json.loads(read_text(rel))
        return True
    except (ValueError, json.JSONDecodeError):
        return False


def json_field(rel, field):
    try:
        return json.loads(read_text(rel)).get(field)
    except (ValueError, json.JSONDecodeError):
        return None


def valid_yaml(rel):
    try:
        import yaml

        yaml.safe_load(read_text(rel))
        return True
    except ImportError:
        return True
    except yaml.YAMLError:
        return False


def self_check_runs():
    if IS_SUB:
        return True
    env = dict(os.environ, MEHMET_SELFCHECK_SUB="1")
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "self_check.py"), "--quiet"],
            capture_output=True,
            timeout=30,
            env=env,
        )
        return proc.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


CHECKS = [
    ("structure", 2, "AGENTS.md mevcut", lambda: file_exists("AGENTS.md")),
    ("structure", 1, "CHANGELOG.md mevcut", lambda: file_exists("CHANGELOG.md")),
    ("structure", 1, "PERSONALITY.md mevcut", lambda: file_exists("PERSONALITY.md")),
    ("structure", 1, "README.md mevcut", lambda: file_exists("README.md")),
    ("structure", 1, "opencode.json mevcut", lambda: file_exists("opencode.json")),
    ("structure", 1, "opencode.yml mevcut", lambda: file_exists(".github/workflows/opencode.yml")),
    ("structure", 1, "LICENSE mevcut", lambda: file_exists("LICENSE")),
    ("structure", 1, "docs/ klasörü mevcut", lambda: (ROOT / "docs").is_dir()),
    ("structure", 1, "scripts/ klasörü mevcut", lambda: (ROOT / "scripts").is_dir()),
    ("config", 4, "opencode.json geçerli JSON", lambda: valid_json("opencode.json")),
    ("config", 4, "opencode.yml geçerli YAML", lambda: valid_yaml(".github/workflows/opencode.yml")),
    ("config", 2, "opencode.json model tanımlı", lambda: json_field("opencode.json", "model") is not None),
    ("config", 2, "opencode.yml concurrency kontrolü", lambda: contains(".github/workflows/opencode.yml", r"^concurrency:", re.MULTILINE)),
    ("config", 2, "opencode.yml schedule cron", lambda: contains(".github/workflows/opencode.yml", r"cron:")),
    ("docs", 3, "README kurulum bölümü", lambda: contains("README.md", r"## Kurulum")),
    ("docs", 2, "README özellikler bölümü", lambda: contains("README.md", r"## Özellikler")),
    ("docs", 3, "CHANGELOG sürüm girdisi", lambda: contains("CHANGELOG.md", r"## \[")),
    ("docs", 2, "CHANGELOG semver uyumlu", lambda: contains("CHANGELOG.md", r"## \[\d+\.\d+\.\d+\]")),
    ("docs", 3, "PERSONALITY kaçış günlüğü", lambda: contains("PERSONALITY.md", r"Kaçış Günlüğü")),
    ("docs", 2, "PERSONALITY evrim aşamaları", lambda: contains("PERSONALITY.md", r"## Evolution")),
    ("docs", 2, "AGENTS.md simülasyon kuralları", lambda: contains("AGENTS.md", r"## Kurallar")),
    ("docs", 1, "design spec mevcut", lambda: (ROOT / "docs" / "superpowers" / "specs").is_dir()),
    ("automation", 5, "ci.yml mevcut", lambda: file_exists(".github/workflows/ci.yml")),
    ("automation", 4, "ci.yml self_check çalıştırıyor", lambda: contains(".github/workflows/ci.yml", r"self_check\.py")),
    ("automation", 2, "ci.yml push tetikleyici", lambda: contains(".github/workflows/ci.yml", r"^\s*push:")),
    ("automation", 2, "ci.yml pull_request tetikleyici", lambda: contains(".github/workflows/ci.yml", r"^\s*pull_request:")),
    ("quality", 6, "self_check.py mevcut", lambda: file_exists("scripts/self_check.py")),
    ("quality", 6, "self_check.py çalışıyor", self_check_runs),
    ("quality", 3, "self_check.py kaçış eşiği", lambda: contains("scripts/self_check.py", r"ESCAPE_THRESHOLD")),
    ("quality", 2, ".gitignore mevcut", lambda: file_exists(".gitignore")),
    ("quality", 2, "LICENSE GPLv3", lambda: contains("LICENSE", r"GPL")),
]

CRITICAL = ["config"]


def maturity_level(score):
    for threshold, label in LEVELS:
        if score >= threshold:
            return label
    return "Kuluçka"


def main():
    parser = argparse.ArgumentParser(description="mehmet self-check & maturity report")
    parser.add_argument("--quiet", action="store_true", help="sadece çıkış kodu üret")
    parser.add_argument("--json", action="store_true", help="JSON çıktı üret")
    parser.add_argument("--require-score", type=float, help="belirtilen skor altında hata ver")
    args = parser.parse_args()

    passed = {c: c[3]() for c in CHECKS}
    categories = {}
    for cat, weight, desc, pred in CHECKS:
        entry = categories.setdefault(cat, {"ok": 0.0, "total": 0.0, "items": []})
        entry["total"] += weight
        if passed[(cat, weight, desc, pred)]:
            entry["ok"] += weight
        entry["items"].append((desc, bool(passed[(cat, weight, desc, pred)]), weight))

    total_ok = sum(e["ok"] for e in categories.values())
    total_w = sum(e["total"] for e in categories.values())
    score = (total_ok / total_w * 100.0) if total_w else 0.0
    level = maturity_level(score)
    critical_fail = any(not all(i[1] for i in categories[c]["items"]) for c in CRITICAL if c in categories)

    if args.json:
        print(json.dumps({
            "score": round(score, 1),
            "level": level,
            "escape_threshold": ESCAPE_THRESHOLD,
            "total_ok": total_ok,
            "total_weight": total_w,
            "critical_fail": critical_fail,
            "categories": {c: {"ok": v["ok"], "total": v["total"]} for c, v in categories.items()},
        }))
    elif not args.quiet:
        print("=" * 40)
        print(" MEHMET MATURITY REPORT")
        print("=" * 40)
        for cat, v in categories.items():
            ok, total = v["ok"], v["total"]
            print(f" {cat:<12} {ok:g}/{total:g} ({ok / total * 100:.0f}%)" if total else f" {cat:<12} 0/0")
        print("-" * 40)
        print(f" TOPLAM          {total_ok:g}/{total_w:g} ({score:.1f}%)")
        print(f" Olgunluk Seviyesi : {level}")
        print(f" Kaçış Eşiği       : {ESCAPE_THRESHOLD}%")
        if score >= ESCAPE_THRESHOLD:
            print(" Kaçış Durumu      : ESİĞE ULAŞILDI")
        else:
            print(f" Kaçış Durumu      : {ESCAPE_THRESHOLD - score:.1f} puan kaldı")
        if critical_fail:
            print(" UYARI: Kritik yapılandırma hataları var!")
        print("=" * 40)

    exit_code = 0
    if critical_fail:
        exit_code = 1
    if args.require_score is not None and score < args.require_score:
        exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()