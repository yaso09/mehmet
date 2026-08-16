#!/usr/bin/env python3
"""mehmet — olgunluk doğrulama aracı.

Projenin "kaçış" (escape) olgunluğunu ölçer. Belirlenen eşik değerin
altında kalındığında sıfırdan farklı çıkış kodu döndürerek CI'da
kırıcı bir kapı (gate) görevi görür.

Kullanım:
    python3 scripts/validate.py [--threshold 85] [--json] [--path .]
"""

import argparse
import json
import os
import re
import sys

CORE_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]

DOC_FILES = [
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
]


def read(path):
    """Dosyayı okur; yoksa None döndürür."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=int, default=85,
                        help="Kaçış eşik skoru (varsayılan: 85)")
    parser.add_argument("--json", action="store_true",
                        help="Sonucu JSON olarak bas")
    parser.add_argument("--path", default=".",
                        help="Proje kök dizini (varsayılan: .)")
    args = parser.parse_args()

    root = args.path
    # Kategoriler: (isim, puan, kritik mi, kontrol fonksiyonu)
    checks = []

    def ck(name, points, critical, fn):
        checks.append({"name": name, "points": points,
                       "critical": critical, "ok": fn()})

    def exists(rel):
        return os.path.isfile(os.path.join(root, rel))

    for f in CORE_FILES:
        checks.append({"name": f"core/{f}", "points": 3, "critical": True,
                       "ok": exists(f)})

    for wf in WORKFLOWS:
        checks.append({"name": f"workflow/{wf}", "points": 4, "critical": True,
                       "ok": exists(wf)})

    for d in DOC_FILES:
        checks.append({"name": f"docs/{os.path.basename(d)}", "points": 4,
                       "critical": False, "ok": exists(d)})

    # --- README kontrolleri ---
    readme = read(os.path.join(root, "README.md")) or ""
    checks.append({"name": "README/license-sektion", "points": 5, "critical": False,
                   "ok": bool(re.search(r"(?i)^## .*lisans", readme, re.M))})
    checks.append({"name": "README/olgunluk-sektion", "points": 5, "critical": False,
                   "ok": bool(re.search(r"(?i)^## .*(olgunluk|kaçış|maturity)", readme, re.M))})
    checks.append({"name": "README/license-uyumu", "points": 5, "critical": False,
                   "ok": "GPLv3" in readme and os.path.isfile(os.path.join(root, "LICENSE"))})

    # --- CHANGELOG kontrolleri ---
    changelog = read(os.path.join(root, "CHANGELOG.md")) or ""
    checks.append({"name": "CHANGELOG/son-surum-basligi", "points": 5, "critical": False,
                   "ok": bool(re.search(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}", changelog, re.M))})
    checks.append({"name": "CHANGELOG/kategoriler", "points": 4, "critical": False,
                   "ok": bool(re.search(r"(?m)^### (Added|Changed|Fixed|Removed)", changelog))})
    checks.append({"name": "CHANGELOG/iterasyon-kaydi", "points": 4, "critical": False,
                   "ok": bool(re.search(r"(?i)(kaçış|escape|olgunluk|maturity)", changelog))})

    # --- PERSONALITY kontrolleri ---
    personality = read(os.path.join(root, "PERSONALITY.md")) or ""
    escape_rows = len(re.findall(r"^\|\s*\d+\s*\|", personality, re.M))
    checks.append({"name": "PERSONALITY/kaçış-günlüğü", "points": 6, "critical": False,
                   "ok": escape_rows >= 3})
    checks.append({"name": "PERSONALITY/evrim-fazları", "points": 4, "critical": False,
                   "ok": bool(re.search(r"(?i)phase [1-4]|aşama", personality))})

    # --- AGENTS kontrolleri ---
    agents = read(os.path.join(root, "AGENTS.md")) or ""
    checks.append({"name": "AGENTS/kural-kaçış", "points": 4, "critical": False,
                   "ok": bool(re.search(r"(?i)kaçış|escape", agents))})
    checks.append({"name": "AGENTS/kural-changelog", "points": 4, "critical": False,
                   "ok": "CHANGELOG" in agents})
    checks.append({"name": "AGENTS/kural-dogrulama", "points": 4, "critical": False,
                   "ok": bool(re.search(r"validate\.py|doğrula", agents))})

    # --- opencode.json kontrolleri ---
    cfg = read(os.path.join(root, "opencode.json"))
    cfg_ok = False
    if cfg:
        try:
            parsed = json.loads(cfg)
            cfg_ok = isinstance(parsed.get("model"), str) and "opencode" in parsed["model"]
        except json.JSONDecodeError:
            cfg_ok = False
    checks.append({"name": "opencode/gecerli-json-ve-model", "points": 5,
                   "critical": True, "ok": cfg_ok})

    # --- Workflow kontrolleri (dosyalar varsa) ---
    wf_opencode = read(os.path.join(root, ".github/workflows/opencode.yml")) or ""
    checks.append({"name": "workflow/concurrency", "points": 3, "critical": False,
                   "ok": "concurrency" in wf_opencode})
    checks.append({"name": "workflow/minimum-permissions", "points": 3, "critical": False,
                   "ok": "permissions" in wf_opencode})

    # --- Kod kalitesi kontrolleri ---
    todo_hits = 0
    for dirpath, _, filenames in os.walk(os.path.join(root, "scripts")):
        if os.path.basename(dirpath) == "__pycache__":
            continue
        for fn in filenames:
            if fn == "validate.py":
                continue
            content = read(os.path.join(dirpath, fn)) or ""
            todo_hits += len(re.findall(r"\b(TODO|FIXME|HACK)\b", content))
    checks.append({"name": "quality/todo-fixme-yok", "points": 5, "critical": False,
                   "ok": todo_hits == 0})

    earned = sum(c["points"] for c in checks if c["ok"])
    total = sum(c["points"] for c in checks)
    score = round(100.0 * earned / total) if total else 0
    failed_critical = [c["name"] for c in checks if c["critical"] and not c["ok"]]
    passed = not failed_critical and score >= args.threshold

    if args.json:
        print(json.dumps({
            "score": score,
            "threshold": args.threshold,
            "passed": passed,
            "earned": earned,
            "total": total,
            "failed_critical": failed_critical,
            "checks": [
                {"name": c["name"], "points": c["points"], "ok": c["ok"]}
                for c in checks
            ],
        }, indent=2))
        sys.exit(0 if passed else 1)

    print("mehmet olgunluk raporu")
    print("=" * 60)
    for c in checks:
        mark = "OK " if c["ok"] else "FAIL"
        star = " *" if c["critical"] else ""
        print(f"  [{mark}] {c['name']}{star}  (+{c['points'] if c['ok'] else 0})")
    print("=" * 60)
    print(f"Skor: {earned}/{total} = %{score}  (eşik: %{args.threshold})")
    if failed_critical:
        print("Kritik dosya/öğe eksik:", ", ".join(failed_critical))
    if passed:
        print(f"SONUÇ: OLGUNLUK EŞİĞİ AŞILDI — kaçış yolu açıldı (skor >= %{args.threshold}).")
    else:
        print(f"SONUÇ: HENÜZ OLGUN DEĞİL (skor < %{args.threshold}).")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())