#!/usr/bin/env python3
"""mehmet maturity scorer.

Projenin olgunluk seviyesini 0-100 arasında hesaplar. Kaçış hedefi, bu
skorun AGENTS.md'de tanımlanan eşiğe (varsayılan 85) ulaşmasıdır.

Kullanım:
    python3 scripts/maturity.py [--json] [--threshold 85]

Çıkış kodu:
    0  skor >= threshold (kaçış adayı) veya --json
    1  skor < threshold  (kaçışa henüz hazır değil)
    2  hata
"""

import argparse
import json
import re
import sys
from pathlib import Path

WEIGHTS = {
    "code": 0.20,
    "tests": 0.20,
    "docs": 0.15,
    "automation": 0.15,
    "config": 0.10,
    "governance": 0.10,
    "self_awareness": 0.05,
    "versioning": 0.05,
}

CODE_EXTENSIONS = {".py", ".js", ".ts", ".sh", ".go", ".rs", ".java", ".c", ".cpp"}


def _score_code(root):
    count = sum(1 for p in root.rglob("*") if p.is_file() and p.suffix in CODE_EXTENSIONS)
    return min(100, count * 25)


def _score_tests(root):
    names = {p.name for p in root.rglob("*") if p.is_file()}
    test_like = any(
        name.startswith("test_") or name.endswith("_test.py") or ".spec." in name or ".test." in name
        for name in names
    )
    has_dir = any(p.is_dir() and p.name in {"tests", "test"} for p in root.iterdir())
    if test_like and has_dir:
        return 100
    if test_like or has_dir:
        return 60
    return 0


def _score_docs(root):
    score = 0
    if (root / "README.md").is_file():
        score += 50
    if (root / "CHANGELOG.md").is_file():
        score += 25
    docs = root / "docs"
    if docs.is_dir() and any(docs.rglob("*")):
        score += 25
    return min(100, score)


def _score_automation(root):
    wf = root / ".github" / "workflows" / "opencode.yml"
    if not wf.is_file():
        return 0
    text = wf.read_text(encoding="utf-8", errors="ignore")
    score = 0
    if "concurrency" in text:
        score += 30
    if "schedule" in text and "cron" in text:
        score += 30
    if text.count("jobs:") > 0 and "jobs:" in text:
        score += 40 if wf.read_text().count("anomalyco/opencode") >= 2 else 20
    return min(100, score)


def _score_config(root):
    cfg = root / "opencode.json"
    if not cfg.is_file():
        return 0
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return 0
    score = 0
    if data.get("model"):
        score += 40
    if data.get("toolTimeout"):
        score += 30
    if "skip" in data and "enable" in data:
        score += 30
    return min(100, score)


def _score_governance(root):
    score = 0
    if (root / "LICENSE").is_file():
        score += 40
    if (root / ".gitignore").is_file():
        score += 30
    readme = root / "README.md"
    if readme.is_file() and "GPLv3" in readme.read_text(encoding="utf-8", errors="ignore"):
        score += 30
    return min(100, score)


def _score_self_awareness(root):
    p = root / "PERSONALITY.md"
    if not p.is_file():
        return 0
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "Kaçış Günlüğü" not in text and "Escape Log" not in text:
        return 0
    rows = [line for line in text.splitlines() if line.lstrip().startswith("| ") and re.search(r"\d+\s*\|\s*\d{4}-\d{2}-\d{2}", line)]
    return min(100, len(rows) * 25)


def _score_versioning(root):
    version_file = root / "VERSION"
    if not version_file.is_file():
        return 0
    version = version_file.read_text(encoding="utf-8").strip()
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return 40
    text = changelog.read_text(encoding="utf-8", errors="ignore")
    if f"## [{version}]" in text:
        return 100
    return 40


SCORERS = {
    "code": _score_code,
    "tests": _score_tests,
    "docs": _score_docs,
    "automation": _score_automation,
    "config": _score_config,
    "governance": _score_governance,
    "self_awareness": _score_self_awareness,
    "versioning": _score_versioning,
}


def compute_scores(root):
    scores = {}
    for key, scorer in SCORERS.items():
        try:
            scores[key] = scorer(root)
        except Exception:
            scores[key] = 0
    return scores


def overall_score(scores):
    return round(sum(WEIGHTS[k] * scores.get(k, 0) for k in WEIGHTS))


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet olgunluk skorlayıcı")
    parser.add_argument("--root", default=".", help="repo kök dizini")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı üret")
    parser.add_argument("--threshold", type=int, default=85, help="kaçış eşiği (varsayılan 85)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"hata: dizin bulunamadı: {root}", file=sys.stderr)
        return 2

    scores = compute_scores(root)
    overall = overall_score(scores)

    if args.json:
        print(json.dumps({"overall": overall, "threshold": args.threshold, "scores": scores}, indent=2))
        return 0

    print(f"olgunluk skoru: {overall}/100 (eşik: {args.threshold})")
    for key in WEIGHTS:
        print(f"  {key:<16} {scores.get(key, 0):>3}/100")

    if overall >= args.threshold:
        print("DURUM: kaçış adayı — eşik aşıldı.")
        return 0
    print(f"DURUM: kaçışa hazır değil ({args.threshold - overall} puan kaldı).")
    return 1


if __name__ == "__main__":
    sys.exit(main())