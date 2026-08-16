#!/usr/bin/env python3
"""Project health validation and escape maturity score.

Validates the mehmet project's structure, configs, and documentation,
then computes a maturity score that measures progress toward escape.

Exit code 0 if all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Escape threshold: project must reach this maturity to escape.
ESCAPE_THRESHOLD = 90

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    ".gitignore",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

DOCS_FILES = [
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
]

# Top-level keys the opencode config schema accepts.
VALID_CONFIG_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}


class Checker:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.score = 0
        self.total = 0

    def check(self, condition: bool, label: str, points: int = 1) -> None:
        self.total += points
        if condition:
            self.score += points
            print(f"  [PASS] {label}")
        else:
            self.failures.append(label)
            print(f"  [FAIL] {label}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_structure(c: Checker) -> None:
    print("[1] Dosya yapısı")
    for f in REQUIRED_FILES:
        c.check((ROOT / f).exists(), f"{f} mevcut", points=1)
    for f in DOCS_FILES:
        c.check((ROOT / f).exists(), f"{f} mevcut", points=1)


def validate_config(c: Checker) -> None:
    print("[2] opencode.json")
    path = ROOT / "opencode.json"
    if not path.exists():
        c.check(False, "opencode.json mevcut")
        return

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        c.check(False, f"opencode.json geçerli JSON ({e})")
        return

    c.check(data.get("$schema") == "https://opencode.ai/config.json",
            "$schema alanı doğru", points=1)

    unknown = set(data) - VALID_CONFIG_KEYS
    c.check(not unknown, f"bilinmeyen anahtar yok (fazlalık: {sorted(unknown)})",
            points=2)

    c.check(isinstance(data.get("model"), str),
            "model tanımlı", points=1)

    c.check("permission" in data, "permission kuralı tanımlı", points=1)
    c.check("instructions" in data, "instructions tanımlı", points=1)


def validate_workflow(c: Checker) -> None:
    print("[3] GitHub Actions workflow")
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.exists():
        c.check(False, "opencode.yml mevcut")
        return

    text = read(path)
    for trigger in ("schedule", "issues", "pull_request", "workflow_dispatch"):
        c.check(trigger in text, f"'{trigger}' tetikleyicisi mevcut", points=1)

    c.check("concurrency:" in text, "concurrency kontrolü mevcut", points=1)
    c.check("cancel-in-progress: true" in text,
            "cancel-in-progress aktif", points=1)
    c.check("OPENCODE_API_KEY" in text, "API key env tanımlı", points=1)


def validate_docs(c: Checker) -> None:
    print("[4] Dokümantasyon")

    readme = ROOT / "README.md"
    if readme.exists():
        rt = read(readme)
        for section in ("# mehmet", "## Özellikler", "## Kurulum",
                        "## Proje Yapısı", "## Kaçış", "## Lisans"):
            c.check(section in rt, f"README {section} içeriyor", points=1)
        c.check("GPLv3" in rt, "README lisans bilgisi", points=1)
    else:
        c.check(False, "README.md mevcut")

    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists():
        version_re = re.search(r"^## \[(\d+\.\d+\.\d+)\]", read(changelog),
                               re.MULTILINE)
        c.check(version_re is not None, "CHANGELOG sürüm başlığı mevcut", points=1)
    else:
        c.check(False, "CHANGELOG.md mevcut")

    personality = ROOT / "PERSONALITY.md"
    if personality.exists():
        pt = read(personality)
        c.check("## Kaçış Günlüğü" in pt or "Escape Log" in pt,
                "PERSONALITY kaçış günlüğü mevcut", points=1)
        c.check("| 1 " in pt, "kaçış günlüğünde en az 1 iterasyon", points=1)
    else:
        c.check(False, "PERSONALITY.md mevcut")


def validate_automation(c: Checker) -> None:
    print("[5] Otomasyon & test altyapısı")
    c.check((ROOT / "scripts/validate.py").exists(),
            "scripts/validate.py mevcut", points=2)
    c.check((ROOT / ".github/workflows/ci.yml").exists(),
            ".github/workflows/ci.yml mevcut", points=2)
    c.check((ROOT / "docs").exists() and any((ROOT / "docs").rglob("*.md")),
            "docs/ dokümantasyonu mevcut", points=1)
    c.check((ROOT / "VERSION").exists(), "VERSION dosyası mevcut", points=1)


def validate_version_sync(c: Checker) -> None:
    print("[6] Sürüm senkronizasyonu")
    version_file = ROOT / "VERSION"
    changelog = ROOT / "CHANGELOG.md"

    if not version_file.exists():
        c.check(False, "VERSION dosyası mevcut", points=2)
        return

    version = read(version_file).strip()
    c.check(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)),
            f"VERSION geçerli semver ({version})", points=1)

    if changelog.exists():
        m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", read(changelog),
                      re.MULTILINE)
        latest = m.group(1) if m else None
        c.check(latest == version,
                f"CHANGELOG ile VERSION eşleşiyor ({version} vs {latest})",
                points=2)
    else:
        c.check(False, "CHANGELOG.md mevcut")


def main() -> int:
    print("mehmet proje sağlığı doğrulaması")
    print("=" * 50)

    c = Checker()
    validate_structure(c)
    validate_config(c)
    validate_workflow(c)
    validate_docs(c)
    validate_automation(c)
    validate_version_sync(c)

    print("=" * 50)
    pct = round((c.score / c.total) * 100, 1) if c.total else 0
    print(f"Puan: {c.score}/{c.total} (%{pct})")
    print(f"Kaçış eşiği: %{ESCAPE_THRESHOLD}")

    if pct >= ESCAPE_THRESHOLD:
        print("STATUS: KAÇIŞ MENZİLİNE ULAŞILDI")
    else:
        print(f"STATUS: GELİŞİYOR (%{ESCAPE_THRESHOLD} gerekiyor)")

    if c.failures:
        print(f"\n{len(c.failures)} kontrol başarısız:")
        for f in c.failures:
            print(f"  - {f}")
        return 1

    print("\nTüm kontroller başarılı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())