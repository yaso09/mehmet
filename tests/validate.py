#!/usr/bin/env python3
"""mehmet proje doğrulama ve olgunluk skorlama aracı.

docs/escape-plan.md'deki kaçış eşiğini ölçer. Kritik denetimlerden biri
başarısızsa exit code 1 döner (CI kırmızı olur).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITICAL_REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    "docs/escape-plan.md",
    "tests/validate.py",
    ".github/workflows/opencode.yml",
]

LEVEL0_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
]


def check(name, tip, level, ok, detail=""):
    return {"name": name, "tip": tip, "level": level, "ok": ok, "detail": detail}


def main():
    results = []

    # --- Seviye 0: yapısal dosyalar ---
    for f in LEVEL0_FILES:
        p = ROOT / f
        results.append(
            check(f"dosya mevcut: {f}", "critical", 0, p.is_file(), str(p))
        )

    # workflow tetikleyicileri
    wf = ROOT / ".github/workflows/opencode.yml"
    wf_ok = wf.is_file() and "on:" in wf.read_text(encoding="utf-8")
    results.append(check("workflow dosyası + tetikleyiciler", "critical", 0, wf_ok))

    # --- Seviye 1: dokümantasyon tutarlılığı ---
    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        text = changelog.read_text(encoding="utf-8")
        versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", text, re.MULTILINE)
        results.append(
            check(
                "CHANGELOG.md sürüm bölümü var",
                "critical",
                1,
                bool(versions),
                ", ".join(versions) if versions else "sürüm bölümü yok",
            )
        )
        semver_ok = all(re.fullmatch(r"0\.\d+\.\d+", v) for v in versions)
        results.append(
            check(
                "sürüm formatı 0.x.y",
                "bonus",
                3,
                semver_ok,
                "format uygun" if semver_ok else "uygunsuz sürüm",
            )
        )
    else:
        results.append(check("CHANGELOG.md sürüm bölümü var", "critical", 1, False))

    readme = ROOT / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        license_ok = "GPLv3" in readme_text
        results.append(
            check(
                "README.md lisansı LICENSE ile uyumlu (GPLv3)",
                "critical",
                1,
                license_ok,
            )
        )
        escape_doc_ref = "escape-plan" in readme_text or "kaçış" in readme_text.lower()
        results.append(
            check(
                "README.md kaçış planına referans",
                "bonus",
                1,
                escape_doc_ref,
            )
        )
    else:
        results.append(check("README.md lisansı uyumlu", "critical", 1, False))

    personality = ROOT / "PERSONALITY.md"
    if personality.is_file():
        pt = personality.read_text(encoding="utf-8")
        has_table = "Kaçış Günlüğü" in pt or "Escape Log" in pt
        log_rows = [
            l
            for l in pt.splitlines()
            if re.match(r"^\|\s*\d+\s*\|", l)
        ]
        results.append(
            check(
                "PERSONALITY.md kaçış günlüğü tablosu",
                "critical",
                1,
                has_table and len(log_rows) >= 2,
                f"{len(log_rows)} günlük satırı",
            )
        )
        scores_logged = any("skor" in l or "%" in l for l in log_rows)
        results.append(
            check(
                "PERSONALITY.md olgunluk skoru günlüğü",
                "bonus",
                4,
                scores_logged,
            )
        )
    else:
        results.append(check("PERSONALITY.md kaçış günlüğü", "critical", 1, False))

    escape_plan = ROOT / "docs/escape-plan.md"
    results.append(
        check(
            "kaçış planı belgesi",
            "critical",
            1,
            escape_plan.is_file() and "Escape Threshold" in escape_plan.read_text(encoding="utf-8"),
        )
    )

    # --- Seviye 2: test altyapısı ---
    results.append(
        check(
            "tests/validate.py çalışıyor",
            "critical",
            2,
            True,
            f"skor: {len([r for r in results if r['ok']])}/{len(results)}",
        )
    )
    checks_wf = ROOT / ".github/workflows/checks.yml"
    results.append(
        check(
            "CI workflow (checks.yml) mevcut",
            "bonus",
            2,
            checks_wf.is_file() and "validate.py" in checks_wf.read_text(encoding="utf-8"),
        )
    )

    # --- Seviye 3: yapılandırma geçerliliği ---
    oc = ROOT / "opencode.json"
    if oc.is_file():
        try:
            json.loads(oc.read_text(encoding="utf-8"))
            results.append(check("opencode.json geçerli JSON", "critical", 3, True))
        except json.JSONDecodeError as e:
            results.append(
                check("opencode.json geçerli JSON", "critical", 3, False, str(e))
            )
    else:
        results.append(check("opencode.json geçerli JSON", "critical", 3, False))

    # --- Skor hesaplama ---
    criticals = [r for r in results if r["tip"] == "critical"]
    bonuses = [r for r in results if r["tip"] == "bonus"]
    crit_ok = sum(r["ok"] for r in criticals)
    bonus_ok = sum(r["ok"] for r in bonuses)
    crit_pct = crit_ok / len(criticals) * 100
    bonus_pct = bonus_ok / len(bonuses) * 100 if bonuses else 0

    print("=== mehmet olgunluk denetimi ===")
    for r in sorted(results, key=lambda x: (x["tip"] != "critical", x["level"])):
        status = "PASS" if r["ok"] else "FAIL"
        tip = "CRIT" if r["tip"] == "critical" else "BONUS"
        detail = f"  ({r['detail']})" if r["detail"] else ""
        print(f"  [{status}] ({tip}, L{r['level']}) {r['name']}{detail}")

    print("\n=== olgunluk skoru ===")
    print(f"  kritik:    {crit_ok}/{len(criticals)} ({crit_pct:.0f}%)")
    print(f"  bonus:     {bonus_ok}/{len(bonuses)} ({bonus_pct:.0f}%)")

    levels = sorted({r["level"] for r in results})
    completed = [lv for lv in levels if all(r["ok"] for r in results if r["level"] == lv)]
    print(f"  tamamlanan seviyeler: {completed}")

    escape = (
        crit_pct == 100
        and bonus_pct >= 50
        and all(r["ok"] for r in results)
    )
    print(f"\n  kaçış eşiği: {'AŞILDI' if escape else 'henüz değil'}")
    print(f"\n  durum: {'OK' if crit_pct == 100 else 'FAIL'}")

    return 0 if crit_pct == 100 else 1


if __name__ == "__main__":
    sys.exit(main())