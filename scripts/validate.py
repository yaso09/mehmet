#!/usr/bin/env python3
"""Proje tutarlılık doğrulama aracı.

Projede olması gereken dosyaları, yapılandırmaları ve dokümantasyon
tutarlılığını kontrol eder. Herhangi bir kontrol başarısız olursa
çıkış kodu 1 döner.
"""

import json
import pathlib
import sys

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

REQUIRED_OPENCODE_FIELDS = ["$schema", "model"]

WORKFLOW_REQUIRED_JOBS = ["autonomous", "comment"]

CHANGELOG_SECTION_HEADER = "## ["
ESCAPE_LOG_HEADER = "## Kaçış Günlüğü / Escape Log"
README_PROJECT_MARKER = "# mehmet"


def check_required_files(root):
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        return False, "eksik dosyalar: " + ", ".join(missing)
    return True, "tüm gerekli dosyalar mevcut"


def check_opencode_json(root):
    path = root / "opencode.json"
    if not path.is_file():
        return False, "opencode.json bulunamadı"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"opencode.json geçersiz JSON: {exc}"
    missing = [field for field in REQUIRED_OPENCODE_FIELDS if field not in data]
    if missing:
        return False, "eksik alanlar: " + ", ".join(missing)
    return True, "opencode.json geçerli ve gerekli alanları içeriyor"


def check_workflow(root):
    path = root / ".github/workflows/opencode.yml"
    if not path.is_file():
        return False, "workflow dosyası bulunamadı"
    text = path.read_text(encoding="utf-8")
    missing = [
        job
        for job in WORKFLOW_REQUIRED_JOBS
        if f"\n  {job}:" not in "\n" + text
    ]
    if missing:
        return False, "eksik job'lar: " + ", ".join(missing)
    return True, "workflow gerekli job'ları içeriyor"


def check_changelog(root):
    path = root / "CHANGELOG.md"
    if not path.is_file():
        return False, "CHANGELOG.md bulunamadı"
    text = path.read_text(encoding="utf-8")
    if CHANGELOG_SECTION_HEADER not in text:
        return False, "CHANGELOG.md'de sürüm bölümü yok"
    return True, "CHANGELOG.md sürüm bölümü içeriyor"


def check_personality(root):
    path = root / "PERSONALITY.md"
    if not path.is_file():
        return False, "PERSONALITY.md bulunamadı"
    text = path.read_text(encoding="utf-8")
    if ESCAPE_LOG_HEADER not in text:
        return False, "PERSONALITY.md'de kaçış günlüğü yok"
    return True, "PERSONALITY.md kaçış günlüğü içeriyor"


def check_readme(root):
    path = root / "README.md"
    if not path.is_file():
        return False, "README.md bulunamadı"
    text = path.read_text(encoding="utf-8")
    if README_PROJECT_MARKER not in text:
        return False, "README.md proje adını içermiyor"
    return True, "README.md proje adını içeriyor"


def run_validation(root):
    checks = [
        ("Gerekli dosyalar", check_required_files),
        ("opencode.json", check_opencode_json),
        ("Workflow job'ları", check_workflow),
        ("CHANGELOG", check_changelog),
        ("PERSONALITY", check_personality),
        ("README", check_readme),
    ]
    results = []
    for name, func in checks:
        ok, message = func(root)
        results.append((name, ok, message))
    return results


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    root = pathlib.Path(argv[0]).resolve() if argv else pathlib.Path.cwd()
    results = run_validation(root)
    failures = 0
    for name, ok, message in results:
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {name}: {message}")
        if not ok:
            failures += 1
    print(f"\n{failures} başarısız kontrol, {len(results) - failures} başarılı")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())