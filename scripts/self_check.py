#!/usr/bin/env python3
"""mehmet self-check: proje bütünlüğünü ve kaçış puanını doğrular."""

import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
THRESHOLD_DEFAULT = 80

ERRORS = []


def check(name, condition, hint=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")
    if not condition:
        ERRORS.append(f"{name}: {hint}")


def parse_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        check(f"JSON geçerli: {path.name}", False, str(exc))
        return None


def parse_yaml(path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as exc:
        check(f"YAML geçerli: {path.name}", False, str(exc))
        return None


def check_escape(esc_path):
    if not esc_path.is_file():
        check("ESCAPE: docs/ESCAPE.md mevcut", False, "dosya yok")
        return

    text = esc_path.read_text()

    declared = re.search(r"Maturity Score\):\*{0,2}\s*(\d+)\s*/\s*(\d+)", text)
    threshold_m = re.search(r"Escape Threshold\):\*{0,2}\s*(\d+)", text)

    items = re.findall(r"^- \[( |x)\]\s+(.+?)\((\d+)\)\s*$", text, re.M)
    total = sum(int(p) for _, _, p in items)
    computed = sum(int(p) for mark, _, p in items if mark == "x")

    check("ESCAPE: en az bir madde var", bool(items), "madde bulunamadı")

    if declared:
        declared_score, declared_total = int(declared.group(1)), int(declared.group(2))
        check("ESCAPE: puan toplamı tutarlı", declared_total == total,
              f"bildirilen {declared_total} != hesaplanan {total}")
        check("ESCAPE: mevcut puan tutarlı", declared_score == computed,
              f"bildirilen {declared_score} != hesaplanan {computed}")
    else:
        check("ESCAPE: puan başlığı mevcut", False, "'Maturity Score' satırı yok")

    threshold = int(threshold_m.group(1)) if threshold_m else THRESHOLD_DEFAULT
    print(f"[INFO] Escape puanı: {computed}/{total} (eşik {threshold})")
    if computed >= threshold:
        print("[ESCAPE] EŞİK AŞILDI — kaçış hazır!")
    else:
        print(f"[INFO] Kaçış için kalan: {threshold - computed} puan")


def main():
    print("=== mehmet self-check ===\n")

    required = ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "opencode.json"]
    for name in required:
        check(f"dosya mevcut: {name}", (ROOT / name).is_file(), "eksik")

    cfg = parse_json(ROOT / "opencode.json")
    if cfg:
        check("opencode.json: model tanımlı", isinstance(cfg.get("model"), str), "'model' alanı yok")

    wf = parse_yaml(ROOT / ".github/workflows/opencode.yml")
    if wf:
        check("opencode.yml: jobs tanımlı", isinstance(wf.get("jobs"), dict), "'jobs' yok")
        check("opencode.yml: concurrency var", "concurrency" in wf, "'concurrency' yok")

    ci = parse_yaml(ROOT / ".github/workflows/ci.yml")
    if ci:
        check("ci.yml: jobs tanımlı", isinstance(ci.get("jobs"), dict), "'jobs' yok")

    cl = (ROOT / "CHANGELOG.md").read_text()
    check("CHANGELOG: sürüm başlığı var", re.search(r"^## \[\d+\.\d+\.\d+\]", cl, re.M) is not None,
          "sürüm başlığı yok")
    check("CHANGELOG: en az 2 sürüm", len(re.findall(r"^## \[\d+\.\d+\.\d+\]", cl, re.M)) >= 2,
          "en az 2 sürüm gerekli")

    pers = (ROOT / "PERSONALITY.md").read_text()
    rows = re.findall(r"^\|\s*\d+\s+\|", pers, re.M)
    check("PERSONALITY: kaçış günlüğü >= 3 iterasyon", len(rows) >= 3,
          f"sadece {len(rows)} iterasyon var")

    readme = (ROOT / "README.md").read_text()
    check("README: Özellikler bölümü var", "## Özellikler" in readme, "bölüm yok")

    check_escape(ROOT / "docs/ESCAPE.md")

    print()
    if ERRORS:
        print(f"{len(ERRORS)} kontrol başarısız.")
        sys.exit(1)
    print("Tüm kontroller geçti.")
    sys.exit(0)


if __name__ == "__main__":
    main()