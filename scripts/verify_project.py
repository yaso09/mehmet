#!/usr/bin/env python3
"""Proje bütünlüğünü doğrulayan otomasyon aracı.

AGENTS.md kurallarının ve proje dosyalarının geçerli olduğunu kontrol eder:
- Zorunlu dosyaların varlığı
- opencode.json geçerliliği ve şema uyumu
- Workflow YAML'lerinin sözdizimi
- CHANGELOG.md formatı
- PERSONALITY.md kaçış günlüğünün varlığı
"""

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

REQUIRED_SECTIONS = {
    "AGENTS.md": ["# Simülasyon Bağlamı", "## Kurallar"],
    "PERSONALITY.md": ["## Kaçış Günlüğü", "## Evolution"],
    "README.md": ["# mehmet", "## Lisans"],
}

CHANGELOG_VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$")

failures = []
warnings = []


def check(cond, message, fatal=True):
    if not cond:
        (failures if fatal else warnings).append(message)


def verify_required_files():
    for name in REQUIRED_FILES:
        check((ROOT / name).exists(), f"[dosya] eksik: {name}")


def verify_sections():
    for name, sections in REQUIRED_SECTIONS.items():
        path = ROOT / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for section in sections:
            check(section in content, f"[içerik] {name} içinde '{section}' bulunamadı")


def verify_opencode_json():
    path = ROOT / "opencode.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        failures.append(f"[json] opencode.json geçersiz: {e}")
        return
    check(isinstance(data, dict), "[json] opencode.json bir nesne olmalı")
    if isinstance(data, dict):
        check("model" in data, "[json] opencode.json 'model' alanı eksik")
        if "model" in data:
            check(
                isinstance(data["model"], str) and data["model"].startswith("opencode/"),
                "[json] 'model' alanı 'opencode/...' ile başlamalı",
            )


def verify_workflows():
    workflow_dir = ROOT / ".github" / "workflows"
    if not workflow_dir.exists():
        warnings.append("[workflow] .github/workflows dizini bulunamadı")
        return
    try:
        import yaml
    except ImportError:
        warnings.append("[workflow] PyYAML yüklü değil, YAML doğrulaması atlandı")
        return
    for yml in sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            failures.append(f"[yaml] {yml.name} geçersiz: {e}")
            continue
        check(isinstance(data, dict) and "jobs" in data, f"[yaml] {yml.name} 'jobs' içermeli")


def verify_changelog():
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    versions = [line for line in content.splitlines() if CHANGELOG_VERSION_RE.match(line)]
    check(len(versions) >= 1, "[changelog] en az bir sürüm girişi olmalı")
    check(content.strip().endswith("- Initial project setup") or "## [0.1.0]" in content,
          "[changelog] 0.1.0 ilk sürüm kaydı olmalı")
    for line in versions:
        date = CHANGELOG_VERSION_RE.match(line).group(2)
        check(bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date)), f"[changelog] geçersiz tarih: {line}")


def verify_escape_log():
    path = ROOT / "PERSONALITY.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    header_index = next(
        (i for i, l in enumerate(lines) if l.strip().startswith("## Kaçış Günlüğü")), None
    )
    if header_index is None:
        failures.append("[kaçış] '## Kaçış Günlüğü' bölümü yok")
        return
    table_rows = [l for l in lines[header_index:] if l.strip().startswith("|") and not l.strip().startswith("|---")]
    entries = [r for r in table_rows if "Iterasyon" not in r and "İterasyon" not in r and re.search(r"\d+\s*\|\s*\d{4}-\d{2}-\d{2}", r)]
    check(len(entries) >= 1, "[kaçış] kaçış günlüğünde en az bir iterasyon girişi olmalı")


def main():
    verify_required_files()
    verify_sections()
    verify_opencode_json()
    verify_workflows()
    verify_changelog()
    verify_escape_log()

    print(f"[sonuç] {len(failures)} hata, {len(warnings)} uyarı")
    for w in warnings:
        print(f"  UYARI: {w}")
    for f in failures:
        print(f"  HATA: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())