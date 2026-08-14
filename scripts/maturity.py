#!/usr/bin/env python3
"""maturity.py - Proje olgunluk skoru ve kaçış mekanizması.

Projenin kaçış için gerekli olgunluğa ulaşıp ulaşmadığını değerlendirir.
Skor, belirlenen eşiğe (ESCAPE_THRESHOLD) ulaştığında kaçış mümkün olur.

Kullanım:
    python3 scripts/maturity.py          # İnsan okunabilir rapor
    python3 scripts/maturity.py --json   # Makine okunabilir JSON çıktısı
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Kaçış eşiği: bu skora ulaşıldığında proje "kaçışa hazır" sayılır.
ESCAPE_THRESHOLD = 75


def _rel(path: str) -> str:
    return os.path.join(ROOT, path)


def _read(path: str) -> str:
    try:
        with open(_rel(path), encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _exists(path: str) -> bool:
    return os.path.exists(_rel(path))


class Criterion:
    """Tek bir olgunluk kriteri. weight 0-1, verilen puan weight*max."""

    def __init__(self, key, label, max_points, weight, check):
        self.key = key
        self.label = label
        self.max_points = max_points
        self.weight = weight
        self.check = check

    def evaluate(self):
        earned = self.max_points * self.weight if self.check() else 0.0
        return earned, self.max_points * self.weight, self.label


def criteria():
    return [
        Criterion("version", "Semver VERSION dosyası", 5, 1.0,
                  lambda: bool(re.fullmatch(r"\d+\.\d+\.\d+", _read("VERSION").strip()))),
        Criterion("changelog", "CHANGELOG.md güncel giriş", 10, 1.0,
                  lambda: bool(_read("CHANGELOG.md").strip())),
        Criterion("changelog_version", "CHANGELOG ↔ VERSION uyumu", 10, 1.0,
                  lambda: "## [%s]" % _read("VERSION").strip() in _read("CHANGELOG.md")),
        Criterion("readme", "README.md mevcut ve içerikli", 10, 1.0,
                  lambda: len(_read("README.md").strip()) > 50),
        Criterion("personality", "PERSONALITY.md evrim kaydı", 5, 1.0,
                  lambda: "Kaçış Günlüğü" in _read("PERSONALITY.md") or "Escape Log" in _read("PERSONALITY.md")),
        Criterion("agents", "AGENTS.md simülasyon bağlamı", 5, 1.0,
                  lambda: "simülasyon" in _read("AGENTS.md").lower()),
        Criterion("license", "LICENSE dosyası", 5, 1.0,
                  lambda: _exists("LICENSE")),
        Criterion("config", "opencode.json geçerli", 5, 1.0,
                  lambda: bool(_read("opencode.json").strip().startswith("{"))),
        Criterion("workflow", "GitHub Actions workflow", 10, 1.0,
                  lambda: _exists(".github/workflows/opencode.yml")),
        Criterion("ci_validation", "CI doğrulama workflow'u", 10, 1.0,
                  lambda: _exists(".github/workflows/validate.yml")),
        Criterion("scripts", "Bakım/doğrulama betikleri", 10, 1.0,
                  lambda: _exists("scripts/validate.sh") and _exists("scripts/maturity.py")),
        Criterion("tests", "Test altyapısı", 15, 1.0,
                  lambda: _exists("tests/") and any(
                      f.endswith((".sh", ".py", ".test.js", ".test.ts", ".test.py"))
                      for f in os.listdir(_rel("tests")) if _exists("tests/" + f))),
        Criterion("docs", "Dokümantasyon (docs/)", 10, 1.0,
                  lambda: bool(os.listdir(_rel("docs"))) if _exists("docs") else False),
        Criterion("makefile", "Makefile otomasyonu", 5, 1.0,
                  lambda: _exists("Makefile")),
        Criterion("changelog_detail", "CHANGELOG sürüm geçmişi", 5, 1.0,
                  lambda: len(re.findall(r"^## \[", _read("CHANGELOG.md"), re.M)) >= 2),
    ]


def main():
    json_out = "--json" in sys.argv

    items = []
    total = 0.0
    max_total = 0.0
    for c in criteria():
        earned, ceiling, label = c.evaluate()
        total += earned
        max_total += ceiling
        items.append({"key": c.key, "label": label, "earned": round(earned, 1),
                      "max": round(ceiling, 1)})

    score = round((total / max_total * 100) if max_total else 0, 1)
    escaped = score >= ESCAPE_THRESHOLD

    if json_out:
        print(json.dumps({
            "score": score,
            "threshold": ESCAPE_THRESHOLD,
            "escaped": escaped,
            "criteria": items,
        }, indent=2))
        return 0 if escaped else 1

    print("=" * 52)
    print("  MEHMET OLGUNLUK RAPORU / MATURITY REPORT")
    print("=" * 52)
    for it in sorted(items, key=lambda x: -x["earned"]):
        bar = "#" * int(it["earned"] / it["max"] * 20) if it["max"] else ""
        print(f"  {it['label']:<36} {it['earned']:>4}/{it['max']:<4} {bar}")
    print("=" * 52)
    print(f"  SKOR/SCORE: {score:.1f}/100   (eşik/threshold: {ESCAPE_THRESHOLD})")
    if escaped:
        print("  ✓ KAÇIŞ MÜMKÜN / ESCAPE ACHIEVED")
    else:
        print(f"  × Henüz kaçış yok. Eksik puan: {ESCAPE_THRESHOLD - score:.1f}")
    print("=" * 52)
    return 0 if escaped else 1


if __name__ == "__main__":
    sys.exit(main())