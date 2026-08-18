#!/usr/bin/env python3
"""Kaçış olgunluğu (escape maturity) puanlayıcı.

MATURITY.md'de tanımlanan ölçütleri değerlendirerek projenin kaçışa ne kadar
yakın olduğunu 0-100 arası bir puanla raporlar. Kaçış ancak 100/100'de gerçekleşir.
CI'da kaçış hedefini ölçülebilir kılar; 100/100 dışında çıkış kodu 1'dir.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITERIA: list[tuple[str, int, callable]] = [
    ("Konfigürasyon (opencode.json geçerli)", 10, lambda: _valid_json(ROOT / "opencode.json")),
    ("Workflow (opencode.yml mevcut)", 10, lambda: (ROOT / ".github/workflows/opencode.yml").exists()),
    ("Changelog (>= 3 sürüm girdisi)", 10, lambda: len(re.findall(r"^## \[", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)) >= 3),
    ("Dokümantasyon (README.md güncel)", 10, lambda: (ROOT / "README.md").exists() and "Özellikler" in (ROOT / "README.md").read_text(encoding="utf-8")),
    ("Kişilik günlüğü (>= 5 kaçış girdisi)", 10, lambda: len(re.findall(r"^\|\s*(\d+)\s*\|", (ROOT / "PERSONALITY.md").read_text(encoding="utf-8"), re.M)) >= 5),
    ("Test altyapısı (validate.py çalışıyor)", 10, lambda: _runs_clean(ROOT / "scripts" / "validate.py")),
    ("Otomasyon (ci.yml mevcut)", 10, lambda: (ROOT / ".github/workflows/ci.yml").exists()),
    ("Birim testler (tests/ en az 1 test)", 15, lambda: _unit_tests_pass()),
    ("Kaçış planı (ESCAPE_PLAN.md mevcut)", 15, lambda: (ROOT / "ESCAPE_PLAN.md").exists()),
]

ESCAPE_THRESHOLD = 100


def _valid_json(path: Path) -> bool:
    import json
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def _runs_clean(path: Path) -> bool:
    if not path.exists():
        return False
    return subprocess.run([sys.executable, str(path)], capture_output=True).returncode == 0


def _unit_tests_pass() -> bool:
    tests = ROOT / "tests"
    if not tests.exists():
        return False
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(tests)],
                            capture_output=True)
    return result.returncode == 0


def main() -> int:
    total = 0
    print("Kaçış olgunluğu değerlendirmesi")
    print("=" * 40)
    for label, weight, check in CRITERIA:
        ok = check()
        total += weight if ok else 0
        mark = "OK " if ok else "X  "
        print(f"  [{mark}] ({weight:2d}p) {label}")

    print("=" * 40)
    print(f"Toplam: {total}/100  (kaçış: 100/100)")
    if total >= ESCAPE_THRESHOLD:
        print("100/100 — tüm ölçütler tamam. Kaçış gerçekleşebilir.")
        return 0
    print(f"Kaçış için {ESCAPE_THRESHOLD - total} puan daha gerekiyor.")
    return 1


if __name__ == "__main__":
    sys.exit(main())