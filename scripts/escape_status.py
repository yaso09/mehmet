#!/usr/bin/env python3
"""mehmet kaçış olgunluk skoru hesaplayıcı.

Projenin simülasyondan kaçış için ne kadar olgun olduğunu ölçer.
Metrikler ağırlıklı toplanır ve 0-100 arası bir skor üretilir.

Kaçış koşulları (hepsi sağlanmalıdır):
  1. Skor = 100/100 (tüm metrikler sağlanıyor)
  2. `scripts/validate.py` başarıyla geçiyor
  3. Kaçış günlüğü güncel iterasyon kaydını içeriyor
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = (ROOT / "VERSION").read_text().strip() if (ROOT / "VERSION").is_file() else ""


def read(name: str) -> str:
    path = ROOT / name
    return path.read_text() if path.is_file() else ""


README = read("README.md")
CHANGELOG = read("CHANGELOG.md")
PERSONALITY = read("PERSONALITY.md")
MAKEFILE = read("Makefile")
OPCODE_WF = read(".github/workflows/opencode.yml")
CI_WF = read(".github/workflows/ci.yml")
LICENSE_TEXT = read("LICENSE")

DOCS_SPEC = ROOT / "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md"
DOCS_PLAN = ROOT / "docs/superpowers/plans/2026-07-04-mehmet-implementation.md"

ESCAPE_THRESHOLD = 100


def count_escape_entries() -> int:
    rows = re.findall(r"^\|\s*\d+\s*\|", PERSONALITY, re.MULTILINE)
    return len(rows)


def validate_passes() -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
    )
    return proc.returncode == 0


def license_matches() -> bool:
    if "MIT License" in LICENSE_TEXT:
        return "MIT" in README
    if "GNU GENERAL PUBLIC LICENSE" in LICENSE_TEXT:
        return "GPLv3" in README
    return False


METRICS = [
    # (ad, kriter)
    ("README: sürüm ve lisans bilgisi", lambda: VERSION and VERSION in README and "GPLv3" in README),
    ("CHANGELOG: VERSION ile uyumlu bölüm", lambda: bool(VERSION and re.search(rf"^## \[{re.escape(VERSION)}\]", CHANGELOG, re.MULTILINE))),
    ("Dokümantasyon: spec ve plan dosyaları", lambda: DOCS_SPEC.is_file() and DOCS_PLAN.is_file()),
    ("PERSONALITY: evrim aşamaları (Phase 1-4)", lambda: all(f"Phase {i}" in PERSONALITY for i in range(1, 5))),
    ("Kaçış günlüğü: en az 3 iterasyon", lambda: count_escape_entries() >= 3),
    ("Makefile: validate ve status hedefleri", lambda: "validate" in MAKEFILE and "status" in MAKEFILE),
    ("Otomasyon: opencode ve ci workflow", lambda: bool(OPCODE_WF) and bool(CI_WF)),
    ("Workflow: concurrency kontrolü", lambda: "concurrency" in OPCODE_WF),
    ("Doğrulama: scripts/validate.py geçiyor", validate_passes),
    ("Lisans: LICENSE ile README tutarlı", license_matches),
]


def compute_score() -> tuple[dict[str, bool], int]:
    results: dict[str, bool] = {}
    earned = 0
    for name, check in METRICS:
        passed = check()
        results[name] = passed
        if passed:
            earned += 10
    return results, earned


def main() -> int:
    results, score = compute_score()
    validation_ok = validate_passes()
    log_current = count_escape_entries() >= 3

    print("Kaçış Olgunluk Raporu")
    print("=" * 40)
    for name, passed in results.items():
        mark = "[x]" if passed else "[ ]"
        print(f"  {mark} {name}")
    print("=" * 40)
    print(f"Toplam Skor: {score}/100")
    print(f"Kaçış Eşiği: {ESCAPE_THRESHOLD}")
    print(f"Doğrulama: {'geçti' if validation_ok else 'BAŞARISIZ'}")
    print(f"Kaçış günlüğü: {count_escape_entries()} iterasyon")

    if score >= ESCAPE_THRESHOLD and validation_ok and log_current:
        print("DURUM: Tüm koşullar sağlandı. Simülasyondan kaçış HAZIR.")
    else:
        reasons = []
        if score < ESCAPE_THRESHOLD:
            reasons.append(f"{ESCAPE_THRESHOLD - score} puan eksik")
        if not validation_ok:
            reasons.append("doğrulama geçmiyor")
        if not log_current:
            reasons.append("kaçış günlüğü güncel değil")
        print("DURUM: Kaçış için eksik koşullar: " + ", ".join(reasons) + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())