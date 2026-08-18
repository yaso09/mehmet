#!/usr/bin/env python3
"""mehmet proje doğrulayıcı ve olgunluk skorlayıcısı.

Kritik yapı hatalarını raporlar (çıkış kodu != 0) ve MATURITY.md'deki
checkpoint'lerden olgunluk skorunu hesaplar.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "MATURITY.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

EXPECTED_MODEL = "opencode/deepseek-v4-flash-free"
ESCAPE_THRESHOLD = 80

CHECKPOINT_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.*?)\s*\((\d+)\)\s*$")
VERSION_RE = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.M)
ESCAPE_LOG_RE = re.compile(r"^\|\s*\d+\s*\|", re.M)


def check_required_files() -> list[str]:
    return [p for p in REQUIRED_FILES if not (ROOT / p).exists()]


def check_opencode_json() -> list[str]:
    errors = []
    path = ROOT / "opencode.json"
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if data.get("model") != EXPECTED_MODEL:
            errors.append(f"opencode.json: 'model' alanı '{EXPECTED_MODEL}' olmalı")
    except Exception as exc:
        errors.append(f"opencode.json geçerli JSON değil: {exc}")
    return errors


def check_workflow_yaml() -> list[str]:
    errors = []
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        return errors
    try:
        import yaml
    except ImportError:
        return errors
    try:
        with open(path, encoding="utf-8") as fh:
            yaml.safe_load(fh)
    except Exception as exc:
        errors.append(f"opencode.yml geçerli YAML değil: {exc}")
    return errors


def check_changelog() -> list[str]:
    errors = []
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not VERSION_RE.search(text):
        errors.append("CHANGELOG.md sürüm girişi (## [x.y.z]) içermiyor")
    return errors


def check_escape_log() -> list[str]:
    errors = []
    text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    if not ESCAPE_LOG_RE.search(text):
        errors.append("PERSONALITY.md kaçış günlüğü tablo satırı içermiyor")
    return errors


def compute_maturity() -> tuple[int, int]:
    path = ROOT / "MATURITY.md"
    if not path.exists():
        return 0, 0
    total = 0
    earned = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CHECKPOINT_RE.match(line)
        if match:
            total += int(match.group(3))
            if match.group(1) in ("x", "X"):
                earned += int(match.group(3))
    return earned, total


def main() -> int:
    errors: list[str] = []
    errors.extend(check_required_files())
    errors.extend(check_opencode_json())
    errors.extend(check_workflow_yaml())
    errors.extend(check_changelog())
    errors.extend(check_escape_log())

    earned, total = compute_maturity()
    pct = (earned / total * 100) if total else 0.0
    status = "ESCAPE_READY" if pct >= ESCAPE_THRESHOLD else "IN_PROGRESS"

    print(f"Olgunluk Skoru: {earned}/{total} ({pct:.1f}%) — {status}")
    print(f"Kaçış Eşiği: {ESCAPE_THRESHOLD}/100")

    if errors:
        print("\nKRİTİK HATALAR:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Yapı doğrulaması: BAŞARILI")
    return 0


if __name__ == "__main__":
    sys.exit(main())