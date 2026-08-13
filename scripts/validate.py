#!/usr/bin/env python3
"""mehmet proje doğrulama ve olgunluk skoru hesaplama aracı.

Yapılan kontroller:
  1. Zorunlu dosyaların varlığı
  2. opencode.json geçerli JSON mu?
  3. GitHub Actions workflow'ları geçerli YAML mi?
  4. CHANGELOG.md güncel versiyon içeriyor mu?
  5. README.md, AGENTS.md, PERSONALITY.md, docs/maturity.md var mı?

Çıkış kodu 0 ise tüm kontroller geçti, 1 ise bir hata var.
"""

from __future__ import annotations

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
    "opencode.json",
    "VERSION",
    "docs/maturity.md",
    ".github/workflows/opencode.yml",
]

WORKFLOWS = sorted((ROOT / ".github/workflows").glob("*.yml"))


def check_required_files() -> list[str]:
    errors = []
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"EKSIK: {rel}")
    return errors


def check_opencode_json() -> list[str]:
    errors = []
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"opencode.json gecersiz JSON: {exc}"]
    if "model" not in data:
        errors.append("opencode.json icinde 'model' alani yok")
    if "toolTimeout" not in data:
        errors.append("opencode.json icinde 'toolTimeout' alani yok")
    return errors


def check_workflow_yaml() -> list[str]:
    errors = []
    try:
        import yaml
    except ImportError:
        return ["PyYAML kurulu degil; workflow YAML kontrolu atlandi"]
    for path in WORKFLOWS:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"Gecersiz YAML ({path.name}): {exc}")
        content = path.read_text(encoding="utf-8")
        if "timeout-minutes" not in content:
            errors.append(f"{path.name} icinde 'timeout-minutes' yok")
    return errors


def check_changelog() -> list[str]:
    errors = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pattern = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)
    if not pattern.search(changelog):
        errors.append("CHANGELOG.md icinde surum basligi yok")
    if f"[{version}]" not in changelog:
        errors.append(f"CHANGELOG.md icinde guncel surum [{version}] yok")
    return errors


def main() -> int:
    checks = [
        ("Zorunlu dosyalar", check_required_files()),
        ("opencode.json", check_opencode_json()),
        ("Workflow YAML", check_workflow_yaml()),
        ("CHANGELOG", check_changelog()),
    ]

    total_errors = 0
    for name, errors in checks:
        if errors:
            print(f"[FAIL] {name}")
            for err in errors:
                print(f"       - {err}")
            total_errors += len(errors)
        else:
            print(f"[ OK ] {name}")

    if total_errors:
        print(f"\nSonuc: {total_errors} hata bulundu.")
        return 1

    print("\nSonuc: tum kontroller gecti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
