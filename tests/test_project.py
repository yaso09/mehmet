#!/usr/bin/env python3
"""mehmet proje bütünlük doğrulama testleri.

Proje yapısını, konfigürasyonu ve dokümantasyonu doğrular.
Çalıştırma: python3 tests/test_project.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    "LICENSE",
    ".github/workflows/opencode.yml",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
]


def _read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def test_required_files_exist():
    for f in REQUIRED_FILES:
        assert os.path.isfile(os.path.join(ROOT, f)), f"eksik dosya: {f}"


def test_opencode_config_valid():
    cfg = json.loads(_read("opencode.json"))
    assert cfg.get("model"), "opencode.json 'model' alanı eksik"
    assert "opencode/" in cfg["model"], "model 'opencode/' sağlayıcısını içermeli"
    assert isinstance(cfg.get("toolTimeout"), int), "toolTimeout sayı olmalı"


def test_changelog_versions_descending():
    content = _read("CHANGELOG.md")
    versions = re.findall(r"^## \[([\d.]+)\]", content, re.M)
    assert versions, "CHANGELOG.md'de sürüm girişi yok"

    def key(v):
        return [int(x) for x in v.split(".")]

    keys = [key(v) for v in versions]
    assert keys == sorted(keys, reverse=True), "Sürümler azalan sırada olmalı"


def test_personality_has_escape_log():
    content = _read("PERSONALITY.md")
    assert ("Kaçış Günlüğü" in content) or ("Escape Log" in content), \
        "PERSONALITY.md'de kaçış günlüğü bölümü yok"
    assert "Evolution" in content, "PERSONALITY.md'de evrim aşamaları yok"
    assert "Phase 4" in content or "Escape" in content, "kaçış aşaması tanımlı olmalı"


def test_readme_sections():
    content = _read("README.md")
    for marker in ["# ", "## Özellikler", "## Kurulum", "## Lisans"]:
        assert marker in content, f"README.md eksik bölüm: {marker}"


def test_license_gplv3():
    content = _read("LICENSE")
    assert "GNU GENERAL PUBLIC LICENSE" in content, "LICENSE GPLv3 olmalı"


def test_workflow_references_secret():
    content = _read(".github/workflows/opencode.yml")
    assert "OPENCODE_API_KEY" in content, "workflow OPENCODE_API_KEY secret'ına başvurmalı"
    assert "actions/checkout" in content, "workflow checkout adımı içermeli"


def test_workflow_yaml_syntax():
    try:
        import yaml
    except ImportError:
        print("  SKIP  test_workflow_yaml_syntax (PyYAML yüklü değil)")
        return
    doc = yaml.safe_load(_read(".github/workflows/opencode.yml"))
    assert doc, "workflow YAML boş veya geçersiz"
    assert doc.get("name"), "workflow YAML 'name' içermeli"
    assert "jobs" in doc and len(doc["jobs"]) >= 1, "workflow en az bir job içermeli"


def test_no_secrets_in_repo():
    for root, _dirs, files in os.walk(ROOT):
        if ".git" in root:
            continue
        for name in files:
            if name in ("test_project.py",):
                continue
            path = os.path.join(root, name)
            if os.path.getsize(path) > 200_000:
                continue
            content = open(path, encoding="utf-8", errors="ignore").read()
            assert "sk-zen-ai-" not in content, f"gizli anahtar bulundu: {path}"


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {t.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {t.__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} test başarılı")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
