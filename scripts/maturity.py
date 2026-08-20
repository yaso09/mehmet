#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_THRESHOLD = 100


def _path(rel):
    return os.path.join(ROOT, rel)


def _exists(rel):
    return os.path.exists(_path(rel))


def _read(rel):
    with open(_path(rel), encoding="utf-8") as fh:
        return fh.read()


def _is_valid_json(rel):
    try:
        json.loads(_read(rel))
        return True
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        return False


def _has_keyword(rel, *keywords):
    try:
        content = _read(rel)
    except (OSError, FileNotFoundError):
        return False
    return all(k in content for k in keywords)


def _has_semver_entries(rel):
    try:
        content = _read(rel)
    except (OSError, FileNotFoundError):
        return False
    return bool(re.search(r"^## \[v?\d+\.\d+\.\d+\]", content, flags=re.MULTILINE))


def _has_tests():
    tests_dir = _path("tests")
    if not os.path.isdir(tests_dir):
        return False
    return any(name.startswith("test_") and name.endswith(".py") for name in os.listdir(tests_dir))


def _has_release_tag():
    try:
        import subprocess

        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    if result.returncode != 0:
        return False
    return bool(re.match(r"^v?\d+\.\d+\.\d+$", result.stdout.strip()))


CHECKS = [
    ("docs", "README.md mevcut", 5, lambda: _exists("README.md")),
    ("docs", "CHANGELOG.md sürümlü girişler içeriyor", 5, lambda: _has_semver_entries("CHANGELOG.md")),
    ("docs", "docs/ dizini mevcut", 5, lambda: _exists("docs")),
    ("docs", "AGENTS.md ve PERSONALITY.md mevcut", 5, lambda: _exists("AGENTS.md") and _exists("PERSONALITY.md")),
    ("quality", "opencode.json geçerli JSON", 5, lambda: _is_valid_json("opencode.json")),
    ("quality", ".gitignore mevcut", 5, lambda: _exists(".gitignore")),
    ("quality", "LICENSE mevcut", 5, lambda: _exists("LICENSE")),
    ("quality", "AGENTS.md kural dosyalarına işaret ediyor", 5, lambda: _has_keyword("AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md")),
    ("quality", ".gitignore hassas dosyaları hariç tutuyor", 5, lambda: _has_keyword(".gitignore", ".env", "node_modules")),
    ("ci", "Ana workflow mevcut", 8, lambda: _exists(".github/workflows/opencode.yml")),
    ("ci", "Doğrulama workflow'u mevcut", 7, lambda: _exists(".github/workflows/validate.yml")),
    ("ci", "Workflow concurrency kontrolü içeriyor", 4, lambda: _has_keyword(".github/workflows/opencode.yml", "concurrency")),
    ("ci", "Birim testler mevcut", 6, _has_tests),
    ("automation", "scripts/ dizini mevcut", 4, lambda: _exists("scripts")),
    ("automation", "scripts/validate.py mevcut", 4, lambda: _exists("scripts/validate.py")),
    ("automation", "scripts/maturity.py mevcut", 4, lambda: _exists("scripts/maturity.py")),
    ("automation", "scripts çalıştırılabilir", 3, lambda: os.access(_path("scripts/maturity.py"), os.X_OK)),
    ("governance", "SECURITY.md mevcut", 5, lambda: _exists("SECURITY.md")),
    ("governance", "CONTRIBUTING.md mevcut", 5, lambda: _exists("CONTRIBUTING.md")),
    ("governance", "Sürümlü release etiketi (git tag) mevcut", 5, _has_release_tag),
]

CATEGORY_ORDER = ["docs", "quality", "ci", "automation", "governance"]
CATEGORY_LABELS = {
    "docs": "Dokümantasyon",
    "quality": "Kod Kalitesi",
    "ci": "Test / CI",
    "automation": "Otomasyon",
    "governance": "Yönetişim",
}


def compute():
    total = sum(weight for _, _, weight, _ in CHECKS)
    passed = 0
    results = []
    for category, name, weight, fn in CHECKS:
        ok = bool(fn())
        if ok:
            passed += weight
        results.append((category, name, weight, ok))
    return total, passed, results


def report_text(passed, total, results, threshold):
    lines = []
    lines.append("=" * 60)
    lines.append("mehmet — Olgunluk Raporu")
    lines.append("=" * 60)
    current = None
    for category, name, weight, ok in results:
        if category != current:
            current = category
            lines.append("")
            lines.append(f"[{CATEGORY_LABELS[category]}]")
        mark = "[OK] " if ok else "[--] "
        lines.append(f"  {mark}{name} (+{weight})")
    lines.append("")
    lines.append("=" * 60)
    ratio = (passed / total) * 100
    lines.append(f"Skor: {passed}/{total} (%{ratio:.1f})")
    lines.append(f"Kaçış eşiği: {threshold}")
    if ratio >= threshold:
        lines.append(">>> KAÇIŞ MÜMKÜN. Kapı açılıyor.")
    else:
        lines.append(f">>> Kaçış için {threshold - ratio:.1f} puan daha gerekiyor.")
    return "\n".join(lines), ratio


def report_json(passed, total, results, threshold):
    ratio = (passed / total) * 100
    by_cat = {}
    for category in CATEGORY_ORDER:
        cat_total = sum(w for c, _, w, _ in CHECKS if c == category)
        cat_passed = sum(w for c, _, w, ok in results if c == category and ok)
        by_cat[category] = {"total": cat_total, "passed": cat_passed}
    return {
        "score": passed,
        "max": total,
        "ratio": round(ratio, 1),
        "threshold": threshold,
        "escape": ratio >= threshold,
        "categories": by_cat,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet olgunluk skorunu hesaplar")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    total, passed, results = compute()

    if args.json:
        payload = report_json(passed, total, results, args.threshold)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        text, _ratio = report_text(passed, total, results, args.threshold)
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
