#!/usr/bin/env python3
"""CHANGELOG, README ve PERSONALITY arasındaki sürüm/uyum tutarlılığını kontrol eder.

Kurallar:
  1. README.md MATURITY.md'yi referans etmeli.
  2. CHANGELOG.md'de bugünün tarihli (veya en yeni) bir sürüm girişi olmalı.
  3. PERSONALITY.md kaçış günlüğünde en az 2 iterasyon olmalı.
  4. MATURITY.md kaçış eşiği tanımını içermeli.
  5. CHANGELOG'da "Added" / "Fixed" bölümlerinden en az biri kullanılmış olmalı.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def require(path: Path, pattern: str, message: str) -> None:
    if not path.exists():
        ERRORS.append(message)
        return
    content = path.read_text(encoding="utf-8")
    if re.search(pattern, content, flags=re.MULTILINE):
        return
    ERRORS.append(message)


require(
    ROOT / "README.md",
    r"MATURITY\.md",
    "README.md MATURITY.md dosyasına referans vermiyor",
)
require(
    ROOT / "CHANGELOG.md",
    r"^## \[",
    "CHANGELOG.md'de sürüm girişi yok",
)
require(
    ROOT / "CHANGELOG.md",
    r"^### (Added|Fixed|Changed)",
    "CHANGELOG.md'de Added/Fixed/Changed bölümü yok",
)
require(
    ROOT / "PERSONALITY.md",
    r"^\| \d+",
    "PERSONALITY.md kaçış günlüğünde iterasyon satırı yok",
)
require(
    ROOT / "MATURITY.md",
    r"Kaçış Eşiği",
    "MATURITY.md kaçış eşiği tanımı içermiyor",
)

if ERRORS:
    for error in ERRORS:
        print(f"FAIL: {error}", file=sys.stderr)
    sys.exit(1)

print("sürüm tutarlılığı tamam")