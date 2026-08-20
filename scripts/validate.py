#!/usr/bin/env python3
"""Repo bütünlük doğrulayıcısı.

JSON/YAML dosyalarını ayrıştırır, kritik dosyaların varlığını kontrol eder
ve CHANGELOG.md sürümünün VERSION dosyasıyla uyumlu olduğunu doğrular.

Kullanım:
    python3 scripts/validate.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
VERSION_FILE = ROOT / "VERSION"
VERSION_RE = re.compile(r"^##\s+\[([0-9]+\.[0-9]+\.[0-9]+)\]\s+-\s+(\d{4}-\d{2}-\d{2})")

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "VERSION",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
    "opencode.json",
]

README_REFERENCES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "docs/MATURITY.md",
    "scripts/validate.py",
]

failures = []
successes = []


def fail(message):
    failures.append(message)


def ok(message):
    successes.append(message)


def check_json(path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        ok(f"JSON OK: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"JSON HATA: {path.relative_to(ROOT)} — {exc}")


def check_yaml(path):
    try:
        import yaml

        yaml.safe_load(path.read_text(encoding="utf-8"))
        ok(f"YAML OK: {path.relative_to(ROOT)}")
    except ImportError:
        ok(f"YAML (atlandı, PyYAML yok): {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"YAML HATA: {path.relative_to(ROOT)} — {exc}")


def check_required_files():
    for name in REQUIRED_FILES:
        if (ROOT / name).exists():
            ok(f"DOSYA OK: {name}")
        else:
            fail(f"DOSYA EKSİK: {name}")


def check_version_consistency():
    if not CHANGELOG.exists():
        fail("CHANGELOG.md yok")
        return

    match = None
    for line in CHANGELOG.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            break
    if match is None:
        fail("CHANGELOG.md'de geçerli bir sürüm başlığı bulunamadı")
        return

    changelog_version = match.group(1)
    ok(f"CHANGELOG sürümü: {changelog_version}")

    if not VERSION_FILE.exists():
        fail("VERSION dosyası yok")
        return

    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if version == changelog_version:
        ok(f"VERSION uyumlu: {version}")
    else:
        fail(f"VERSION uyumsuz: dosya '{version}', CHANGELOG '{changelog_version}'")


def check_readme_references():
    if not (ROOT / "README.md").exists():
        fail("README.md yok")
        return
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for ref in README_REFERENCES:
        if ref in readme:
            ok(f"README referansı: {ref}")
        else:
            fail(f"README'de referans eksik: {ref}")


def main():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix == ".json":
            check_json(path)
        elif path.suffix in (".yaml", ".yml"):
            check_yaml(path)

    check_required_files()
    check_version_consistency()
    check_readme_references()

    print(f"\n[validate] {len(successes)} başarılı, {len(failures)} hata\n")
    for s in successes:
        print(f"  ✔ {s}")
    for f in failures:
        print(f"  ✘ {f}")

    if failures:
        sys.exit(1)
    print("\n[validate] TÜM KONTROLLER BAŞARILI")


if __name__ == "__main__":
    main()