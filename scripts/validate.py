#!/usr/bin/env python3
"""mehmet proje tutarlılık doğrulama aracı.

Projenin temel bütünlüğünü kontrol eder:
  - Zorunlu dosyaların varlığı
  - VERSION / CHANGELOG / README tutarlılığı
  - opencode.json JSON geçerliliği
  - Workflow YAML dosyalarının varlığı
  - Lisans tutarlılığı (README vs LICENSE)
  - GitHub Actions referanslarının varlığı

Çıkış kodu: tüm kontroller geçerse 0, aksi halde 1.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "VERSION",
    "opencode.json",
    "LICENSE",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/ci.yml",
]

OPTIONAL_FILES = [
    "Makefile",
    "scripts/validate.py",
    "scripts/escape_status.py",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
]


def check_file(name: str, optional: bool = False) -> bool:
    path = ROOT / name
    if path.is_file():
        return True
    print(f"[{ 'UYARI' if optional else 'HATA ' }] Eksik dosya: {name}")
    return optional


def check_version() -> bool:
    version = (ROOT / "VERSION").read_text().strip()
    changelog = (ROOT / "CHANGELOG.md").read_text()
    if not re.search(rf"^## \[{re.escape(version)}\]", changelog, re.MULTILINE):
        print(f"[HATA ] CHANGELOG.md'de {version} bölümü yok.")
        return False
    if version not in (ROOT / "README.md").read_text():
        print(f"[HATA ] README.md'de {version} sürümü belirtilmiyor.")
        return False
    return True


def check_opencode_json() -> bool:
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"[HATA ] opencode.json geçersiz JSON: {exc}")
        return False
    if "model" not in data:
        print("[HATA ] opencode.json'da 'model' alanı eksik.")
        return False
    return True


def check_license() -> bool:
    license_text = (ROOT / "LICENSE").read_text()
    license_type = "MIT" if "MIT License" in license_text else "GPLv3"
    readme = (ROOT / "README.md").read_text()
    if license_type not in readme:
        print(f"[HATA ] README.md lisans bilgisi LICENSE ({license_type}) ile uyumsuz.")
        return False
    return True


def check_workflows() -> bool:
    ok = True
    for wf in WORKFLOWS:
        path = ROOT / wf
        if not path.is_file():
            print(f"[HATA ] Eksik workflow: {wf}")
            ok = False
            continue
        content = path.read_text()
        if "actions/checkout" not in content:
            print(f"[UYARI] {wf} checkout action kullanmıyor.")
        if wf.endswith("opencode.yml") and "OPENCODE_API_KEY" not in content:
            print(f"[UYARI] {wf} OPENCODE_API_KEY secret kullanmıyor.")
    return ok


def main() -> int:
    results = [check_file(name) for name in REQUIRED_FILES]
    results += [check_file(name, optional=True) for name in OPTIONAL_FILES]
    results.append(check_version())
    results.append(check_opencode_json())
    results.append(check_license())
    results.append(check_workflows())

    ok = all(results)
    print(f"\nDoğrulama {'BAŞARILI' if ok else 'BAŞARISIZ'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())