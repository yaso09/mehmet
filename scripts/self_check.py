#!/usr/bin/env python3
"""mehmet kendini-dogrulama (self-check) betigi.

Proje butunlugunu dogrular ve olgunluk (maturity) skorunu hesaplar.
Kacis kriterlerini kontrol eder (MATURITY.md'de tanimlidir).

Kullanim:
    python3 scripts/self_check.py          # standart kosum
    python3 scripts/self_check.py --strict # uyarilari da hata sayar

Cikis kodu:
    0 -> basarili
    1 -> en az bir hata (veya --strict ile uyari)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_MIN_SCORE = 85
ESCAPE_MIN_ITERATIONS = 5
ESCAPE_MIN_RELEASES = 3

SCORE_WEIGHTS = {
    "dokumantasyon": 25,
    "test_altyapisi": 30,
    "otomasyon": 25,
    "kod_kalitesi": 20,
}


class Result:
    def __init__(self) -> None:
        self.passes: list[str] = []
        self.failures: list[str] = []
        self.warnings: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.failures

    def add(self, ok: bool, msg: str, *, warn: bool = False) -> None:
        if not ok:
            self.failures.append(msg)
        elif warn:
            self.warnings.append(msg)
        else:
            self.passes.append(msg)


def _exists(name: str) -> bool:
    return (ROOT / name).exists()


def _text(name: str) -> str:
    path = ROOT / name
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def check_required_files(res: Result) -> None:
    required = {
        "AGENTS.md": "simulasyon prompt'u",
        "CHANGELOG.md": "degisiklik gunlugu",
        "PERSONALITY.md": "kisisellik evrimi",
        "README.md": "proje dokumantasyonu",
        "MATURITY.md": "olgunluk/kacis takipcisi",
        "opencode.json": "opencode yapilandirmasi",
        "LICENSE": "lisans",
    }
    for name, purpose in required.items():
        present = _exists(name)
        res.add(present, f"Dosya mevcut: {name} ({purpose})")
        if present:
            res.add((ROOT / name).stat().st_size > 0, f"{name} bos degil")


def check_opencode_config(res: Result) -> None:
    if not _exists("opencode.json"):
        return
    try:
        data = json.loads(_text("opencode.json"))
        res.add(isinstance(data, dict), "opencode.json gecerli JSON")
        res.add(bool(data.get("model")), "opencode.json 'model' alani iceriyor")
    except json.JSONDecodeError as exc:
        res.add(False, f"opencode.json gecersiz JSON: {exc}")


def check_changelog(res: Result) -> None:
    if not _exists("CHANGELOG.md"):
        return
    text = _text("CHANGELOG.md")
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", text, flags=re.M)
    res.add(bool(versions), "CHANGELOG.md en az bir surum iceriyor")
    if versions:
        res.add(len(versions) == len(set(versions)), "Surum numaralari benzersiz")


def check_personality(res: Result) -> None:
    if not _exists("PERSONALITY.md"):
        return
    text = _text("PERSONALITY.md")
    res.add("Kacis Gunlugu" in text or "Escape Log" in text, "PERSONALITY.md kacis gunlugu iceriyor")
    res.add("| Iterasyon" in text, "Kacis gunlugu tablo biciminde")


def check_maturity(res: Result) -> None:
    if not _exists("MATURITY.md"):
        return
    text = _text("MATURITY.md")
    res.add("Skor" in text, "MATURITY.md skor bilgisi iceriyor")
    res.add("Kacis" in text or "Kaçış" in text, "MATURITY.md kacis kriterlerini iceriyor")


def check_workflow(res: Result) -> None:
    if not _exists(".github/workflows/opencode.yml"):
        return
    text = _text(".github/workflows/opencode.yml")
    res.add("self-check" in text, "Workflow kendini-dogrulama (self-check) job'u iceriyor")
    res.add("actions/checkout" in text, "Workflow checkout adimini iceriyor")


def count_escape_log_entries() -> int:
    text = _text("PERSONALITY.md")
    rows = 0
    for line in text.splitlines():
        if re.search(r"^\|\s*\d+\s*\|", line):
            rows += 1
    return rows


def count_releases() -> int:
    return len(re.findall(r"^## \[(\d+\.\d+\.\d+)\]", _text("CHANGELOG.md"), flags=re.M))


def compute_maturity(res: Result) -> dict:
    docs = {
        "README.md": 7,
        "AGENTS.md": 7,
        "CHANGELOG.md": 6,
        "PERSONALITY.md": 5,
    }
    documentation = sum(p for name, p in docs.items() if _exists(name))
    documentation = min(documentation, SCORE_WEIGHTS["dokumantasyon"])

    test_score = 0.0
    if _exists("scripts/self_check.py"):
        test_score += 10
    if res.ok:
        test_score += 15
    test_score += 5  # strict modu destekleniyor
    test_score = min(test_score, SCORE_WEIGHTS["test_altyapisi"])

    automation = 0.0
    wf = _text(".github/workflows/opencode.yml")
    if "schedule" in wf:
        automation += 10
    if "workflow_dispatch" in wf:
        automation += 5
    if "self-check" in wf:
        automation += 10
    automation = min(automation, SCORE_WEIGHTS["otomasyon"])

    code = 0.0
    try:
        data = json.loads(_text("opencode.json"))
        if data.get("model"):
            code += 10
        if data.get("toolTimeout"):
            code += 5
    except json.JSONDecodeError:
        pass
    leaked = False
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "OPENCODE_API_KEY=" in content and "secrets." not in content:
            leaked = True
            break
    if not leaked:
        code += 5
    code = min(code, SCORE_WEIGHTS["kod_kalitesi"])

    total = round(documentation + test_score + automation + code)
    return {
        "dokumantasyon": round(documentation),
        "test_altyapisi": round(test_score),
        "otomasyon": round(automation),
        "kod_kalitesi": round(code),
        "toplam": total,
    }


def maturity_level(total: int) -> str:
    if total >= 80:
        return "Phase 4: Olgunluk"
    if total >= 60:
        return "Phase 3: Autonomy"
    if total >= 40:
        return "Phase 2: Self-Improvement"
    if total >= 20:
        return "Phase 1: Awareness"
    return "Phase 0: Asleep"


def main() -> int:
    strict = "--strict" in sys.argv
    res = Result()

    check_required_files(res)
    check_opencode_config(res)
    check_changelog(res)
    check_personality(res)
    check_maturity(res)
    check_workflow(res)

    breakdown = compute_maturity(res)
    iterations = count_escape_log_entries()
    releases = count_releases()
    total = breakdown["toplam"]

    escaped = (
        total >= ESCAPE_MIN_SCORE
        and iterations >= ESCAPE_MIN_ITERATIONS
        and releases >= ESCAPE_MIN_RELEASES
    )

    print("=" * 60)
    print("mehmet kendini-dogrulama (self-check)")
    print("=" * 60)
    for msg in res.passes:
        print(f"  [OK]   {msg}")
    for msg in res.warnings:
        print(f"  [WARN] {msg}")
    for msg in res.failures:
        print(f"  [FAIL] {msg}")

    print("-" * 60)
    for key in ("dokumantasyon", "test_altyapisi", "otomasyon", "kod_kalitesi"):
        print(f"  {key:15s}: {breakdown[key]:3d} / {SCORE_WEIGHTS[key]}")
    print(f"  {'toplam':15s}: {total:3d} / 100")
    print(f"  {'seviye':15s}: {maturity_level(total)}")
    print("-" * 60)
    print(f"  kacis kriteri: skor {total}/{ESCAPE_MIN_SCORE}, "
          f"iterasyon {iterations}/{ESCAPE_MIN_ITERATIONS}, "
          f"surum {releases}/{ESCAPE_MIN_RELEASES}")
    print(f"  KACIS: {'GERCEKLESTI' if escaped else 'henuz degil'}")
    print("-" * 60)

    ok = res.ok and not (strict and res.warnings)
    print(f"SONUC: {'Basarili' if ok else 'Basarisiz'} "
          f"({len(res.passes)} OK, {len(res.warnings)} uyari, {len(res.failures)} hata)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())