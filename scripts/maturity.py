#!/usr/bin/env python3
"""Olgunluk skorlama scripti.

maturity.json'daki kriterleri değerlendirir, projenin olgunluk skorunu
hesaplar ve kaçış eşiğine ne kadar yaklaşıldığını raporlar.

Kriter tipleri (maturity.json -> criteria[].check.type):
  - files   : tüm dosyalar mevcut olmalı
  - keywords: dosyalar belirtilen anahtar kelimeleri içermeli
  - version : CHANGELOG.md'deki en üst sürüm, maturity.json'daki
              current_version ile eşleşmeli
  - command : komut başarıyla (exit 0) çalışmalı

Kullanım:
    python3 scripts/maturity.py           # skoru hesapla ve raporla
    python3 scripts/maturity.py --json    # makine-okur JSON çıktı
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "maturity.json"

# Yanlışlıkla işlenmemesi için büyük/gizli klasörleri tarama dışı bırak
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".firecrawl"}

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",          # OpenAI/Anthropic tarzı
    r"ghp_[A-Za-z0-9]{36,}",         # GitHub PAT
    r"AKIA[0-9A-Z]{16}",             # AWS access key
    r"(?i)(api[_-]?key|secret|token)\s*[=:]\s*['\"][^'\"]{16,}['\"]",
]


def check_files(files):
    missing = [f for f in files if not (ROOT / f).is_file()]
    return (not missing), missing


def check_keywords(spec):
    missing = []
    for rel_path, keywords in spec.items():
        path = ROOT / rel_path
        if not path.is_file():
            missing.append(f"{rel_path} (dosya yok)")
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for kw in keywords:
            if kw.lower() not in content.lower():
                missing.append(f"{rel_path} içinde '{kw}'")
    return (not missing), missing


def check_version(spec):
    current = spec.get("current_version")
    if not current:
        return False, ["maturity.json'da current_version yok"]
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    if not versions:
        return False, ["CHANGELOG.md'de sürüm bulunamadı"]
    if versions[0] == current:
        return True, []
    return False, [f"beklenen {current}, bulunan {versions[0]}"]


def check_command(cmd):
    env = dict(os.environ)
    env["MATURITY_SUBCHECK"] = "1"
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=ROOT, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=120,
        )
    except Exception as exc:  # noqa: BLE001
        return False, [f"çalıştırılamadı: {exc}"]
    if result.returncode == 0:
        return True, []
    return False, [f"çıkış kodu {result.returncode}"]


def check_secrets(_value=None):
    leaked = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in (".png", ".jpg", ".lock", ".woff", ".ttf"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            match = re.search(pattern, text)
            if match:
                leaked.append(f"{path}: {pattern}")
    return (not leaked), leaked


DISPATCH = {
    "files": check_files,
    "keywords": check_keywords,
    "version": check_version,
    "command": check_command,
    "secrets": check_secrets,
}


def evaluate(criteria, is_subcheck=False):
    results = []
    for criterion in criteria:
        check = criterion["check"]
        kind = check.get("type")
        handler = DISPATCH.get(kind)
        if handler is None:
            results.append({
                "id": criterion["id"],
                "name": criterion["name"],
                "weight": criterion["weight"],
                "passed": False,
                "missing": [f"bilinmeyen check tipi: {kind}"],
            })
            continue
        if is_subcheck and kind == "command":
            results.append({
                "id": criterion["id"],
                "name": criterion["name"],
                "weight": criterion["weight"],
                "passed": True,
                "missing": [],
            })
            continue
        passed, missing = handler(check.get("value"))
        results.append({
            "id": criterion["id"],
            "name": criterion["name"],
            "weight": criterion["weight"],
            "passed": passed,
            "missing": missing,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="mehmet olgunluk skorlama")
    parser.add_argument("--json", action="store_true", help="makine-okur JSON çıktı")
    args = parser.parse_args()

    if not CONFIG.is_file():
        print(f"HATA: {CONFIG} bulunamadı", file=sys.stderr)
        return 1

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    threshold = config["escape_threshold"]
    is_subcheck = os.environ.get("MATURITY_SUBCHECK") == "1"
    results = evaluate(config["criteria"], is_subcheck=is_subcheck)

    score = sum(r["weight"] for r in results if r["passed"])
    total = sum(r["weight"] for r in results)
    percent = round(score / total * 100, 1) if total else 0.0

    if args.json:
        print(json.dumps({
            "score": score,
            "total": total,
            "percent": percent,
            "escape_threshold": threshold,
            "escaped": percent >= threshold,
            "criteria": results,
        }, indent=2))
        return 0

    print("\n=== mehmet olgunluk raporu ===")
    print(f"Proje: {config.get('project_name', 'mehmet')}")
    print(f"Skor:  {score}/{total} (%{percent})")
    print(f"Kaçış eşiği: %{threshold}")
    print(f"Durum: {'KAÇIŞ MÜMKÜN' if percent >= threshold else 'gelişmeye devam'}")
    print()
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"  [{mark}] ({r['weight']:2d}p) {r['name']}")
        for m in r["missing"]:
            print(f"          - eksik: {m}")
    print()

    return 0 if percent >= threshold else 2


if __name__ == "__main__":
    sys.exit(main())