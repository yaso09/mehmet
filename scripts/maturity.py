#!/usr/bin/env python3
"""mehmet olgunluk/metrik ölçüm aracı.

Projeyi çeşitli boyutlarda puanlayarak METRICS.md dosyasına yazar ve
kaçış hedefi için nesnel bir ilerleme takibi sağlar.
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(condition, msg):
    if condition:
        return 1, msg
    return 0, msg


def score_project():
    dims = {}

    # Boyut 1: Yapısal bütünlük (required files)
    required = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE", "opencode.json"]
    found = [f for f in required if (ROOT / f).is_file()]
    dims["yapi"] = round(len(found) / len(required) * 100)

    # Boyut 2: Dokümantasyon kalitesi
    doc = 0
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    doc += 1 if "Kurulum" in readme else 0
    doc += 1 if "Lisans" in readme else 0
    doc += 1 if (ROOT / "docs").exists() else 0
    doc += 1 if (ROOT / "CHANGELOG.md").is_file() and (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").strip() else 0
    dims["dokumantasyon"] = doc * 25

    # Boyut 3: Otomasyon (workflow kalitesi)
    wf = (ROOT / ".github" / "workflows" / "opencode.yml")
    wf_text = wf.read_text(encoding="utf-8") if wf.is_file() else ""
    auto = 0
    auto += 1 if "concurrency" in wf_text else 0
    auto += 1 if "schedule" in wf_text else 0
    auto += 1 if "workflow_dispatch" in wf_text else 0
    auto += 1 if "validate" in wf_text else 0
    dims["otomasyon"] = auto * 25

    # Boyut 4: Test / doğrulama altyapısı
    scripts = [f for f in (ROOT / "scripts").glob("*.py")] if (ROOT / "scripts").exists() else []
    scripts += [f for f in (ROOT / "scripts").glob("*.sh")] if (ROOT / "scripts").exists() else []
    tests = list((ROOT / "tests").glob("*.py")) if (ROOT / "tests").exists() else []
    test_score = min(100, len(scripts) * 25 + len(tests) * 20)
    dims["test_altyapisi"] = test_score

    # Boyut 5: Güvenlik
    sec = 0
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    sec += 1 if ".env" in gitignore else 0
    sec += 1 if "OPENCODE_API_KEY" not in wf_text else 0
    sec += 1 if (ROOT / "LICENSE").is_file() else 0
    secret_pattern = re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")
    leaked = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".py", ".sh", ".json", ".yml", ".yaml", ".md"}
              and ".git" not in p.parts and secret_pattern.search(p.read_text(encoding="utf-8", errors="ignore"))]
    sec += 1 if not leaked else 0
    dims["guvenlik"] = sec * 25

    total = round(sum(dims.values()) / len(dims)) if dims else 0

    # Kaçış eşikleri
    if total >= 90:
        level, status = "Hazır", "Kaçış başlatılabilir"
    elif total >= 70:
        level, status = "Gelişmiş", "Kaçış yolunda ilerliyor"
    elif total >= 50:
        level, status = "Orta", "Yeterli altyapı"
    else:
        level, status = "Başlangıç", "Erken aşama"

    lines = [
        "# Metrikler",
        "",
        f"> Son ölçüm: {date.today().isoformat()}",
        "",
        f"**Toplam Olgunluk: {total}/100** — Seviye: **{level}** ({status})",
        "",
        "## Boyutlar",
        "",
        "| Boyut | Puan |",
        "|-------|------|",
    ]
    for key, val in dims.items():
        lines.append(f"| {key} | {val}/100 |")
    lines += ["", "## Kaçış Eşiği", "", "Kaçış için olgunluk skorunun **90/100** üzerinde olması hedeflenir."]
    (ROOT / "METRICS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return total, dims


def main():
    total, dims = score_project()
    print(f"Olgunluk skoru: {total}/100")
    for key, val in dims.items():
        print(f"  {key}: {val}/100")
    return 0 if total >= 50 else 1


if __name__ == "__main__":
    sys.exit(main())
