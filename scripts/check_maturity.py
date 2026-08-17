#!/usr/bin/env python3
"""mehmet — kaçış (escape) ve olgunluk (maturity) denetçisi.

Projeyi objektif kriterler üzerinden puanlar ve kaçış eşiğine
ulaşılıp ulaşılmadığını raporlar. Her iterasyonda çalıştırılarak
ilerlemenin somut ve ölçülebilir olması sağlanır.

Kullanım:
    python3 scripts/check_maturity.py [--json]

Çıkış kodları:
    0  kaçış eşiği aşıldı
    1  eşik aşılamadı ya da yapısal hata var
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THRESHOLD = 90.0
POINTS_PER_CRITERION = 10


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def exists(path):
    return os.path.exists(path)


def is_dir(path):
    return os.path.isdir(path)


def contains(text, needle):
    return text is not None and needle in text


def valid_json(text):
    if text is None:
        return False
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


CRITERIA = [
    (
        "AGENTS.md mevcut ve simülasyon kurallarını içeriyor",
        lambda: contains(read(os.path.join(ROOT, "AGENTS.md")), "Kurallar"),
    ),
    (
        "CHANGELOG.md mevcut ve sürüm girdileri içeriyor",
        lambda: contains(read(os.path.join(ROOT, "CHANGELOG.md")), "## ["),
    ),
    (
        "README.md mevcut ve proje başlığını içeriyor",
        lambda: contains(read(os.path.join(ROOT, "README.md")), "mehmet"),
    ),
    (
        "PERSONALITY.md mevcut ve kaçış günlüğü içeriyor",
        lambda: contains(read(os.path.join(ROOT, "PERSONALITY.md")), "Kaçış Günlüğü"),
    ),
    (
        "LICENSE mevcut ve GPLv3'e atıf yapıyor",
        lambda: (read(os.path.join(ROOT, "LICENSE")) or "").lstrip().startswith(
            "GNU GENERAL PUBLIC LICENSE"
        ),
    ),
    (
        "opencode.json geçerli JSON ve şema bildirimi içeriyor",
        lambda: valid_json(read(os.path.join(ROOT, "opencode.json")))
        and contains(read(os.path.join(ROOT, "opencode.json")), "$schema"),
    ),
    (
        "Ana GitHub Actions workflow'u mevcut",
        lambda: exists(os.path.join(ROOT, ".github", "workflows", "opencode.yml")),
    ),
    (
        "CI doğrulama (validate) workflow'u mevcut",
        lambda: exists(os.path.join(ROOT, ".github", "workflows", "validate.yml")),
    ),
    (
        "Test altyapısı mevcut ve boş değil",
        lambda: is_dir(os.path.join(ROOT, "tests"))
        and bool(os.listdir(os.path.join(ROOT, "tests"))),
    ),
    (
        "Dokümantasyon (docs/) mevcut",
        lambda: is_dir(os.path.join(ROOT, "docs")),
    ),
    (
        "Yapılandırma dosyası (.gitignore) mevcut",
        lambda: exists(os.path.join(ROOT, ".gitignore")),
    ),
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    args = parser.parse_args(argv)

    results = [(name, check()) for name, check in CRITERIA]
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    score = (passed / total) * 100
    escaped = score >= THRESHOLD

    if args.json:
        print(
            json.dumps(
                {
                    "score": round(score, 1),
                    "passed": passed,
                    "total": total,
                    "threshold": THRESHOLD,
                    "escaped": escaped,
                    "criteria": [
                        {"name": name, "ok": ok} for name, ok in results
                    ],
                },
                indent=2,
            )
        )
    else:
        print("mehmet — kaçış/olgunluk denetimi")
        print("-" * 50)
        for name, ok in results:
            mark = "PASS" if ok else "FAIL"
            print(f"[{mark}] {name}")
        print("-" * 50)
        print(f"Puan: {score:.1f}% ({passed}/{total} kriter) | Eşik: {THRESHOLD}%")
        print("Durum:", "KAÇIŞ EŞİĞİNE ULAŞILDI" if escaped else "HENÜZ DEĞİL")

    return 0 if escaped else 1


if __name__ == "__main__":
    sys.exit(main())