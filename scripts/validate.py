#!/usr/bin/env python3
"""Proje yapısını ve konfigürasyon dosyalarını doğrular."""

import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

VERSION_HEADER_PREFIX = "## ["


def checks() -> list[tuple[str, bool]]:
    root = Path(__file__).resolve().parent.parent
    results = []

    for name in REQUIRED_FILES:
        results.append((f"required file: {name}", (root / name).exists()))

    config_path = root / "opencode.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            has_model = isinstance(data.get("model"), str) and bool(data["model"])
            results.append(("opencode.json: model tanımlı", has_model))
            results.append(("opencode.json: geçerli JSON", True))
        except (json.JSONDecodeError, OSError):
            results.append(("opencode.json: geçerli JSON", False))
    else:
        results.append(("opencode.json: geçerli JSON", False))

    workflow = root / ".github/workflows/opencode.yml"
    if workflow.exists():
        text = workflow.read_text(encoding="utf-8")
        results.append(("workflow: name tanımlı", text.strip().startswith("name:")))
        results.append(("workflow: 'on' tetikleyici var", "\non:" in text or "\non :" in text))
        results.append(("workflow: schedule cron var", "cron" in text))
        results.append(("workflow: opencode action kullanılıyor", "anomalyco/opencode/github" in text))
        results.append(("workflow: OPENCODE_API_KEY env var", "OPENCODE_API_KEY" in text))

    changelog = root / "CHANGELOG.md"
    if changelog.exists():
        lines = changelog.read_text(encoding="utf-8").splitlines()
        has_versions = any(line.startswith(VERSION_HEADER_PREFIX) for line in lines)
        results.append(("changelog: sürüm başlıkları var", has_versions))

    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        results.append(("readme: proje adı var", "# mehmet" in text))
        results.append(("readme: kurulum bölümü var", "## Kurulum" in text))
        results.append(("readme: lisans bölümü var", "## Lisans" in text))

    personality = root / "PERSONALITY.md"
    if personality.exists():
        text = personality.read_text(encoding="utf-8")
        results.append(("personality: kaçış günlüğü var", "Kaçış Günlüğü" in text))

    gitignore = root / ".gitignore"
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8")
        results.append((".gitignore: node_modules var", "node_modules" in text))
        results.append((".gitignore: .env var", ".env" in text))

    return results


def main() -> int:
    results = checks()
    failed = 0
    for name, ok in results:
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {name}")
        if not ok:
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} kontrol geçti")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())