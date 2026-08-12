#!/usr/bin/env python3
"""mehmet projesi sağlık kontrolleri.

mehmet'in hayatta kalması için kritik olan dosyaları ve tutarlılığı
denetler: changelog disiplini, kişilik günlüğü, lisans tutarlılığı,
model yapılandırması hizalaması ve workflow varlığı.

Sıfır bağımlılık, yalnızca standart kütüphane. Çıkış kodu 0 başarı,
1 başarısızlık anlamına gelir (CI içinde kullanılır).
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
    "LICENSE",
    "opencode.json",
]

OPENCODE_JSON_KEYS = ["model", "toolTimeout"]

CHANGELOG_TOP_RE = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}", re.MULTILINE)
ESCAPE_LOG_RE = re.compile(r"## Kaçış Günlüğü|## Escape Log", re.MULTILINE)


def check_required_files(errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"Eksik dosya: {name}")


def check_opencode_json(errors: list[str]) -> None:
    path = ROOT / "opencode.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"opencode.json geçerli JSON değil: {exc}")
        return
    for key in OPENCODE_JSON_KEYS:
        if key not in data:
            errors.append(f"opencode.json içinde eksik anahtar: {key}")
    model = data.get("model")
    if model and not str(model).startswith("opencode/"):
        errors.append(f"opencode.json model değeri geçersiz: {model}")


def check_changelog(errors: list[str]) -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not CHANGELOG_TOP_RE.search(text):
        errors.append("CHANGELOG.md en üst sürüm başlığı geçersiz: beklenen '## [x.y.z] - YYYY-MM-DD'.")


def check_personality(errors: list[str]) -> None:
    path = ROOT / "PERSONALITY.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not ESCAPE_LOG_RE.search(text):
        errors.append("PERSONALITY.md kaçış günlüğü bölümü bulunamadı.")
    if "## Traits" not in text:
        errors.append("PERSONALITY.md Traits bölümü bulunamadı.")


def check_workflow(errors: list[str]) -> None:
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.is_file():
        errors.append("Eksik dosya: .github/workflows/opencode.yml")
        return
    text = path.read_text(encoding="utf-8")
    if "OPENCODE_API_KEY" not in text:
        errors.append("Workflow OPENCODE_API_KEY secret'ını kullanmıyor.")
    opencode_json = ROOT / "opencode.json"
    if opencode_json.is_file():
        try:
            model = json.loads(opencode_json.read_text(encoding="utf-8")).get("model")
        except json.JSONDecodeError:
            model = None
        if model and f"model: {model}" not in text:
            errors.append(
                f"Workflow model değeri opencode.json ile uyumsuz (beklenen: {model})."
            )


def check_readme_license(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    license_file = ROOT / "LICENSE"
    if not readme.is_file() or not license_file.is_file():
        return
    license_text = license_file.read_text(encoding="utf-8")
    if "GNU GENERAL PUBLIC LICENSE" not in license_text:
        return
    readme_text = readme.read_text(encoding="utf-8")
    if "GPLv3" not in readme_text and "GPL-3.0" not in readme_text:
        errors.append("README.md lisans bilgisi LICENSE dosyasıyla uyumsuz (GPLv3).")


def main() -> int:
    errors: list[str] = []
    checks = [
        check_required_files,
        check_opencode_json,
        check_changelog,
        check_personality,
        check_workflow,
        check_readme_license,
    ]
    for check in checks:
        check(errors)

    if errors:
        print("Proje sağlık kontrolü başarısız:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Tüm sağlık kontrolleri geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())