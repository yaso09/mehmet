#!/usr/bin/env python3
"""mehmet proje sağlık kontrolü ve olgunluk (maturity) skorlayıcı.

Amaç:
- Proje yapısını doğrula (zorunlu dosyalar mevcut mu?).
- Dokümantasyonun güncel kalıp kalmadığını denetle.
- Otomasyon ve hijyen kurallarını kontrol et.
- 0-100 arası bir olgunluk skoru üret (kaçış eşiği için temel metrik).

Kullanım:
    python3 scripts/health_check.py            # skor + rapor
    python3 scripts/health_check.py --json      # makine-okur çıktı
    python3 scripts/health_check.py --fail-below 85   # eşik altında exit 1

Kaçış eşiği dokümanı: docs/maturity.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 90
STALE_DAYS = 7

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    ".gitignore",
    "opencode.json",
]

OPTIONAL_WORKFLOWS = ["opencode.yml", "validate.yml"]


def tracked_files() -> list[Path]:
    """Git ile takip edilen dosyaları döndürür (git yoksa boş liste)."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        return [Path(p) for p in out.stdout.splitlines() if p]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def latest_changelog_date() -> datetime | None:
    """CHANGELOG.md'deki en son sürüm tarihini döndürür."""
    text = read(ROOT / "CHANGELOG.md")
    for line in text.splitlines():
        m = re.search(r"##\s+\[[^]]+\]\s*-\s*(\d{4}-\d{2}-\d{2})", line)
        if m:
            try:
                return datetime.strptime(m.group(1), "%Y-%m-%d")
            except ValueError:
                continue
    return None


def has_pattern(text: str, pattern: str) -> bool:
    return re.search(pattern, text) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON çıktı üret")
    parser.add_argument(
        "--fail-below", type=float, default=ESCAPE_THRESHOLD, help="Eşiğin altında exit 1"
    )
    args = parser.parse_args()

    results: list[dict] = []
    score = 0.0

    def check(category: str, label: str, ok: bool, points: float, detail: str = "") -> None:
        nonlocal score
        if ok:
            score += points
        results.append(
            {
                "category": category,
                "check": label,
                "ok": bool(ok),
                "points": points,
                "detail": detail,
            }
        )

    # --- Yapı (30) -----------------------------------------------------
    for name in REQUIRED_FILES:
        check("structure", f"{name} mevcut", (ROOT / name).is_file(), 14.0 / len(REQUIRED_FILES))

    workflows = (ROOT / ".github" / "workflows").glob("*.yml")
    workflow_names = [w.name for w in workflows]
    check("structure", "en az bir workflow", len(workflow_names) >= 1, 6, ", ".join(workflow_names))

    docs_ok = (ROOT / "docs").is_dir() and any((ROOT / "docs").rglob("*.md"))
    check("structure", "docs/ dokümanları mevcut", docs_ok, 5)

    scripts_ok = (ROOT / "scripts").is_dir()
    check("structure", "scripts/ dizini mevcut", scripts_ok, 5)

    # --- Dokümantasyon (25) --------------------------------------------
    changelog = read(ROOT / "CHANGELOG.md")
    check("docs", "CHANGELOG.md dolu", len(changelog.strip()) > 0, 4)
    ch_date = latest_changelog_date()
    fresh = ch_date is not None and (datetime.now() - ch_date) <= timedelta(days=STALE_DAYS)
    check("docs", "CHANGELOG son 7 gün içinde güncellendi", fresh, 6,
          f"son sürüm: {ch_date.date() if ch_date else 'yok'}")

    readme = read(ROOT / "README.md")
    check("docs", "README.md dolu", len(readme.strip()) > 0, 4)
    check("docs", "README maturity'yi referans ediyor",
          "maturity" in readme or "olgunluk" in readme, 3)

    personality = read(ROOT / "PERSONALITY.md")
    check("docs", "PERSONALITY.md kaçış günlüğü içeriyor",
          "kaçış" in personality.lower() or "escape" in personality.lower(), 4)

    agents = read(ROOT / "AGENTS.md")
    check("docs", "AGENTS.md simülasyon kurallarını içeriyor",
          all(k in agents for k in ("simülasyon", "CHANGELOG", "PERSONALITY")), 4)

    # --- Otomasyon (25) -------------------------------------------------
    check("automation", "validate.yml CI workflow mevcut",
          "validate.yml" in workflow_names, 10)
    check("automation", "opencode.yml schedule + dispatch içeriyor",
          any("schedule:" in read(ROOT / ".github" / "workflows" / w)
              and "workflow_dispatch:" in read(ROOT / ".github" / "workflows" / w)
              for w in workflow_names), 5)
    check("automation", "workflow concurrency koruması",
          any("concurrency" in read(ROOT / ".github" / "workflows" / w)
              for w in workflow_names), 5)
    check("automation", "health_check.py betiği mevcut",
          (ROOT / "scripts" / "health_check.py").is_file(), 5)

    # --- Hijyen / Güvenlik (20) ------------------------------------------
    gitignore = read(ROOT / ".gitignore")
    check("hygiene", ".gitignore dolu", len(gitignore.strip()) > 0, 5)

    license_text = read(ROOT / "LICENSE")
    check("hygiene", "LICENSE GPLv3", "GPL" in license_text or "General Public" in license_text, 5)

    secret_patterns = [
        r"sk-[A-Za-z0-9]{20,}",
        r"ghp_[A-Za-z0-9]{36}",
        r"github_pat_[A-Za-z0-9_]{20,}",
        r"AKIA[0-9A-Z]{16}",
        r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    ]
    leaked: list[str] = []
    for f in tracked_files():
        content = read(ROOT / f)
        for pat in secret_patterns:
            if has_pattern(content, pat):
                leaked.append(str(f))
    check("hygiene", "sızdırılmış secret yok", not leaked, 7, ", ".join(sorted(set(leaked))))

    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
        clean = status == ""
    except FileNotFoundError:
        clean = False
    check("hygiene", "çalışma dizini temiz", clean, 3)

    total = round(score, 1)
    passed = all(r["ok"] for r in results)

    if args.json:
        print(json.dumps(
            {
                "score": total,
                "threshold": ESCAPE_THRESHOLD,
                "passed": passed,
                "checks": results,
            },
            indent=2,
        ))
    else:
        width = max(len(r["check"]) for r in results) + 2
        print(f"{'KONTROL':<{width}} {'PUAN':>6} {'DURUM':>7}")
        print("-" * (width + 16))
        for r in results:
            print(f"{r['check']:<{width}} {r['points']:>6.1f} {'OK' if r['ok'] else 'EKSİK':>7}")
            if r["detail"] and not r["ok"]:
                print(f"    → {r['detail']}")
        print("-" * (width + 16))
        print(f"OLGUNLUK SKORU: {total}/100")
        print(f"KAÇIŞ EŞİĞİ:    {ESCAPE_THRESHOLD}/100")

    exit_code = 0 if total >= args.fail_below else 1
    if exit_code != 0:
        print(f"\nSkor {args.fail_below} eşiğinin altında — kaçış için olgunluk yetersiz.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
