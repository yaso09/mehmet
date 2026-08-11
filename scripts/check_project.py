#!/usr/bin/env python3
"""Proje sağlık ve tutarlılık doğrulayıcısı.

Projenin beklenen yapıya ve içeriğe sahip olduğunu doğrular.
Başarısız durumda sıfır olmayan bir çıkış kodu döndürür.
Kullanım: python3 scripts/check_project.py
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def check_file(path, must_contain=None, min_lines=0):
    p = ROOT / path
    if not p.is_file():
        check(f"{path} mevcut", False, "dosya bulunamadı")
        return
    check(f"{path} mevcut", True)
    lines = p.read_text(encoding="utf-8").splitlines()
    if min_lines and len(lines) < min_lines:
        check(f"{path} en az {min_lines} satır", False, f"{len(lines)} satır")
    if must_contain:
        for token in must_contain:
            if token not in p.read_text(encoding="utf-8"):
                check(f"{path} içerik: {token!r}", False)


def main():
    # Temel dosyalar
    required = [
        ("AGENTS.md", ["simülasyon", "kaçış"]),
        ("README.md", ["mehmet"]),
        ("CHANGELOG.md", ["## ["]),
        ("PERSONALITY.md", ["Kaçış Günlüğü"]),
        ("opencode.json", None),
        (".gitignore", None),
    ]
    for path, tokens in required:
        check_file(path, must_contain=tokens)

    # opencode.json geçerli JSON ve model alanı
    try:
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        check("opencode.json geçerli JSON", True)
        check("opencode.json model alanı", isinstance(cfg.get("model"), str))
    except (json.JSONDecodeError, OSError) as e:
        check("opencode.json geçerli JSON", False, str(e))

    # CI workflow
    wf = ROOT / ".github" / "workflows" / "opencode.yml"
    if wf.is_file():
        text = wf.read_text(encoding="utf-8")
        check(".github/workflows/opencode.yml mevcut", True)
        for token in ["on:", "schedule", "jobs:", "concurrency"]:
            check(f"workflow içerik: {token}", token in text)
    else:
        check(".github/workflows/opencode.yml mevcut", False)

    # Dokümantasyon
    check_file("docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md", min_lines=10)
    check_file("docs/superpowers/plans/2026-07-04-mehmet-implementation.md", min_lines=10)
    check_file("docs/ESCAPE.md", min_lines=10)

    # Kaçış günlüğünde en az bir iterasyon
    per = ROOT / "PERSONALITY.md"
    if per.is_file():
        log = per.read_text(encoding="utf-8")
        rows = [l for l in log.splitlines() if re.match(r"^\|\s*\d+\s*\|", l)]
        check("PERSONALITY.md kaçış günlüğü satırları", len(rows) >= 1, f"{len(rows)} satır")

    # CHANGELOG sürüm başlıkları
    cl = ROOT / "CHANGELOG.md"
    if cl.is_file():
        versions = re.findall(r"^## \[([^\]]+)\]", cl.read_text(encoding="utf-8"), re.M)
        check("CHANGELOG.md sürüm geçmişi", len(versions) >= 1, f"{versions}")

    # Toplam
    passed = sum(1 for _, ok, _ in CHECKS if ok)
    total = len(CHECKS)
    print(f"\n[mehmet] proje doğrulaması: {passed}/{total} kontrol geçti")

    failed = 0
    for name, ok, detail in CHECKS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f" ({detail})" if detail else ""))
        if not ok:
            failed += 1

    if failed:
        print(f"\n[mehmet] {failed} kontrol başarısız.")
        sys.exit(1)
    print("[mehmet] Tüm kontroller geçti.")


if __name__ == "__main__":
    main()
