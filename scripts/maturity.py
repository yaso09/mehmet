#!/usr/bin/env python3
"""mehmet olgunluk skorlama aracı.

Projenin kaçış hedefine ne kadar yaklaştığını ölçer. Skor 0-100 arasındadır
ve şu kategorilerden hesaplanır:

  - yapi (structure)  : zorunlu dosyaların varlığı
  - dokuman (docs)    : README/CHANGELOG/PERSONALITY tutarlılığı
  - test (tests)      : test altyapısının varlığı ve geçmesi
  - otomasyon (ci)    : workflow ve validate job
  - evrim (evolution) : kaçış günlüğü iterasyon sayısı

Kullanım:
  python3 scripts/maturity.py            # insan okunur rapor
  python3 scripts/maturity.py --json     # makine okunur JSON
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _exists(*parts):
    return os.path.isfile(os.path.join(ROOT, *parts))


def _read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def score_structure():
    checks = {
        "AGENTS.md": _exists("AGENTS.md"),
        "README.md": _exists("README.md"),
        "CHANGELOG.md": _exists("CHANGELOG.md"),
        "PERSONALITY.md": _exists("PERSONALITY.md"),
        "LICENSE": _exists("LICENSE"),
        "opencode.json": _exists("opencode.json"),
        "workflow": _exists(".github", "workflows", "opencode.yml"),
        "docs/": os.path.isdir(os.path.join(ROOT, "docs")),
    }
    ok = sum(1 for v in checks.values() if v)
    return round(100 * ok / len(checks)), checks


def score_docs():
    total = 4
    ok = 0
    if _exists("README.md"):
        readme = _read("README.md")
        ok += int("Özellikler" in readme and "Kurulum" in readme)
    if _exists("CHANGELOG.md"):
        ok += int(bool(re.search(r"^## \[\d+\.\d+\.\d+\]", _read("CHANGELOG.md"), re.M)))
    if _exists("PERSONALITY.md"):
        ok += int("Kaçış Günlüğü" in _read("PERSONALITY.md"))
    if _exists("AGENTS.md"):
        ok += int("simülasyon" in _read("AGENTS.md"))
    return round(100 * ok / total)


def score_tests():
    # Test dosyalarının varlığı
    test_dir = os.path.join(ROOT, "tests")
    if not os.path.isdir(test_dir):
        return 0
    test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
    if not test_files:
        return 0
    # Testlerin gerçekten geçtiğini doğrula (recursion'u önlemek için env işareti)
    env = dict(os.environ)
    env["MEHMET_MATURITY_INTERNAL"] = "1"
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", test_dir, "-v"],
            capture_output=True,
            env=env,
            timeout=120,
        )
        passed = proc.returncode == 0
    except Exception:
        passed = False
    file_score = 60 if len(test_files) >= 1 else 0
    pass_score = 40 if passed else 0
    return file_score + pass_score


def score_ci():
    total = 4
    ok = 0
    path = os.path.join(ROOT, ".github", "workflows", "opencode.yml")
    if _exists(".github", "workflows", "opencode.yml"):
        wf = _read(".github", "workflows", "opencode.yml")
        ok += int("on:" in wf or "on" in wf)
        ok += int("schedule" in wf)
        ok += int("jobs:" in wf)
        ok += int("validate" in wf or "test" in wf.lower())
    return round(100 * ok / total)


def score_evolution():
    if not _exists("PERSONALITY.md"):
        return 0
    content = _read("PERSONALITY.md")
    matches = re.findall(r"^\|\s*(\d+)\s*\|", content, re.M)
    if not matches:
        return 0
    iterations = max(int(m) for m in matches)
    return min(100, iterations * 20)


def compute():
    structure, structure_details = score_structure()
    docs = score_docs()
    tests = score_tests()
    ci = score_ci()
    evolution = score_evolution()
    categories = {
        "yapi": structure,
        "dokuman": docs,
        "test": tests,
        "otomasyon": ci,
        "evrim": evolution,
    }
    score = round(sum(categories.values()) / len(categories))
    return score, categories, structure_details


def phase_for(score):
    if score >= 80:
        return "Phase 4: Escape"
    if score >= 60:
        return "Phase 3: Autonomy"
    if score >= 40:
        return "Phase 2: Self-Improvement"
    return "Phase 1: Awareness"


def main():
    parser = argparse.ArgumentParser(description="mehmet olgunluk skoru")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    args = parser.parse_args()

    score, categories, details = compute()

    if args.json:
        print(json.dumps({
            "score": score,
            "phase": phase_for(score),
            "categories": categories,
            "checks": details,
        }))
        return 0

    print("mehmet olgunluk raporu")
    print("=" * 40)
    for name, val in categories.items():
        bar = "#" * (val // 10) + "." * (10 - val // 10)
        print(f"  {name:<10} [{bar}] {val:>3}/100")
    print("=" * 40)
    print(f"  TOPLAM    : {score}/100")
    print(f"  FAZ       : {phase_for(score)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())