#!/usr/bin/env python3
"""mehmet — proje sağlık doğrulama scripti.

Simülasyon kurallarının (AGENTS.md) uygulandığını otomatik olarak
denetler. GitHub Actions (validate.yml) ve yerel geliştirmede kullanılır.

Kurallar:
1. Zorunlu dosyalar mevcut olmalı (AGENTS.md, CHANGELOG.md, ...)
2. opencode.json geçerli ve yalnızca bilinen alanlar içermeli
3. CHANGELOG.md en az bir sürüm başlığı ve değişiklik içermeli
4. PERSONALITY.md kaçış günlüğü en son tarihi içermeli
5. Workflow dosyaları minimal YAML yapısına uymalı
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
    "opencode.json",
    "LICENSE",
    ".github/workflows/opencode.yml",
]

VALID_OPENCODE_KEYS = {
    "$schema",
    "agent",
    "attachment",
    "autoshare",
    "autoupdate",
    "compaction",
    "command",
    "default_agent",
    "disabled_providers",
    "enabled_providers",
    "enterprise",
    "experimental",
    "formatter",
    "instructions",
    "layout",
    "logLevel",
    "lsp",
    "mcp",
    "mode",
    "model",
    "permission",
    "plugin",
    "provider",
    "reference",
    "references",
    "server",
    "share",
    "shell",
    "skills",
    "small_model",
    "snapshot",
    "subagent_depth",
    "tools",
    "tool_output",
    "username",
    "watcher",
}

VERSION_HEADER = re.compile(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}$", re.MULTILINE)
CHANGELOG_ENTRY = re.compile(r"^### (Added|Changed|Fixed|Removed|Security)$", re.MULTILINE)
ESCAPE_LOG_HEADER = re.compile(r"^\| 1 .*\|$", re.MULTILINE)


def check(condition: bool, message: str, errors: list[str]) -> None:
    if condition:
        print(f"  [OK] {message}")
    else:
        errors.append(message)
        print(f"  [FAIL] {message}")


def validate_opencode(path: Path, errors: list[str]) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: geçersiz JSON: {exc}")
        return

    unknown = set(data) - VALID_OPENCODE_KEYS
    check(
        not unknown,
        f"{path}: yalnızca bilinen alanlar içerir (geçersiz: {sorted(unknown) or 'yok'})",
        errors,
    )
    check(
        data.get("model") and "/" in data["model"],
        f"{path}: 'model' alanı provider/model formatında",
        errors,
    )


def validate_workflow(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    check(
        re.search(r"^name:\s+\S+", text, re.MULTILINE),
        f"{path}: 'name' tanımlı",
        errors,
    )
    check(
        re.search(r"^jobs:\s*$", text, re.MULTILINE),
        f"{path}: 'jobs' bölümü tanımlı",
        errors,
    )
    check(
        text.strip() and "\n" in text,
        f"{path}: boş olmayan içerik",
        errors,
    )


def main() -> int:
    errors: list[str] = []

    print("== Zorunlu dosyalar ==")
    for rel in REQUIRED_FILES:
        check((ROOT / rel).exists(), f"{rel} mevcut", errors)

    print("\n== opencode.json ==")
    validate_opencode(ROOT / "opencode.json", errors)

    print("\n== CHANGELOG.md ==")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    check(
        VERSION_HEADER.search(changelog) is not None,
        "en az bir sürüm başlığı (## [x.y.z] - TARİH)",
        errors,
    )
    check(
        CHANGELOG_ENTRY.search(changelog) is not None,
        "en az bir değişiklik kategorisi (### Added/Fixed/...)",
        errors,
    )

    print("\n== PERSONALITY.md ==")
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
    check(
        ESCAPE_LOG_HEADER.search(personality) is not None,
        "kaçış günlüğü tablosu ve iterasyon satırı mevcut",
        errors,
    )

    print("\n== Workflow dosyaları ==")
    for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
        validate_workflow(wf, errors)

    print()
    if errors:
        print(f"Sonuç: {len(errors)} hata tespit edildi.")
        return 1
    print("Sonuç: tüm kontroller geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
