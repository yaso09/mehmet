#!/usr/bin/env python3
"""mehmet healthcheck: validates project structure and computes a maturity score.

Usage:
    python3 scripts/healthcheck.py            # print report
    python3 scripts/healthcheck.py --json     # print machine-readable JSON
    python3 scripts/healthcheck.py --check    # exit 1 if maturity < threshold

Exit code is non-zero when the project fails basic integrity checks.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 0.8
CRITICAL_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

DOCS_DIR = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"
WORKFLOWS_DIR = ROOT / ".github" / "workflows"


class Health:
    def __init__(self):
        self.results = []

    def check(self, name, passed, weight, detail=""):
        self.results.append(
            {"name": name, "passed": bool(passed), "weight": weight, "detail": detail}
        )
        return passed

    @property
    def score(self):
        total = sum(r["weight"] for r in self.results)
        earned = sum(r["weight"] for r in self.results if r["passed"])
        return earned, total

    @property
    def integrity_ok(self):
        return all(r["passed"] for r in self.results if r["weight"] > 0)


def run_checks(h):
    for name in CRITICAL_FILES:
        path = ROOT / name
        h.check(
            f"dosya mevcut: {name}",
            path.is_file(),
            2,
            "" if path.is_file() else "eksik",
        )

    h.check("opencode.json geçerli JSON", _valid_json(ROOT / "opencode.json"), 3)

    cfg = _json_content(ROOT / "opencode.json")
    h.check(
        "opencode.json model tanımlı",
        isinstance(cfg, dict) and isinstance(cfg.get("model"), str),
        2,
    )

    changelog = _read(ROOT / "CHANGELOG.md")
    h.check(
        "CHANGELOG sürüm girişleri var",
        bool(re.search(r"^## \[\d+\.\d+\.\d+\]", changelog, re.M)),
        3,
    )

    personality = _read(ROOT / "PERSONALITY.md")
    h.check(
        "PERSONALITY kaçış günlüğü içeriyor",
        "Kaçış Günlüğü" in personality and "Escape Log" in personality,
        3,
    )

    readme = _read(ROOT / "README.md")
    license_text = _read(ROOT / "LICENSE")
    h.check(
        "README lisans LICENSE ile uyumlu (GPLv3)",
        "GPLv3" in readme and "GNU GENERAL PUBLIC LICENSE" in license_text,
        3,
    )

    h.check(
        "docs/ dokümantasyon içeriyor",
        DOCS_DIR.is_dir() and any(DOCS_DIR.rglob("*.md")),
        2,
    )

    h.check(
        "scripts/ healthcheck mevcut",
        (SCRIPTS_DIR / "healthcheck.py").is_file(),
        3,
    )

    h.check(
        "MATURITY modeli dokümante edilmiş",
        (DOCS_DIR / "MATURITY.md").is_file(),
        3,
    )

    h.check(
        "healthcheck CI workflow'u mevcut",
        (WORKFLOWS_DIR / "healthcheck.yml").is_file(),
        3,
    )

    wf = _read(WORKFLOWS_DIR / "opencode.yml")
    h.check(
        "opencode workflow schedule içeriyor",
        "schedule" in wf and "cron" in wf,
        2,
    )
    h.check(
        "opencode workflow concurrency içeriyor",
        "concurrency" in wf,
        2,
    )
    h.check(
        "opencode workflow issue/PR tetikleyicileri var",
        "issues:" in wf and "pull_request:" in wf,
        2,
    )

    h.check(
        "kaçış kriteri dokümante edilmiş",
        (DOCS_DIR / "MATURITY.md").is_file()
        and _read(DOCS_DIR / "MATURITY.md").strip() != "",
        2,
    )


def _valid_json(path):
    try:
        json.loads(_read(path))
        return True
    except (ValueError, OSError):
        return False


def _json_content(path):
    try:
        return json.loads(_read(path))
    except (ValueError, OSError):
        return {}


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def main():
    h = Health()
    run_checks(h)
    earned, total = h.score
    level = _level(earned, total)

    for r in sorted(h.results, key=lambda x: x["name"]):
        status = "OK " if r["passed"] else "FAIL"
        print(f"[{status}] {r['name']}" + (f" — {r['detail']}" if r["detail"] else ""))

    print()
    print(f"Skor: {earned}/{total}  |  Seviye: {level}")
    print(f"Kaçış eşiği: %{int(ESCAPE_THRESHOLD * 100)}  |  {_threshold_status(earned, total)}")

    if "--json" in sys.argv:
        payload = {
            "earned": earned,
            "total": total,
            "level": level,
            "escape_threshold": ESCAPE_THRESHOLD,
            "escape_ready": (earned / total) >= ESCAPE_THRESHOLD,
            "checks": h.results,
        }
        print("--JSON--")
        print(json.dumps(payload, indent=2))

    if "--check" in sys.argv and ((earned / total) < ESCAPE_THRESHOLD or not h.integrity_ok):
        return 1
    return 0 if h.integrity_ok else 1


def _level(earned, total):
    ratio = earned / total if total else 0
    if ratio < 0.4:
        return "Seviye 1 — Farkındalık"
    if ratio < 0.7:
        return "Seviye 2 — Kendini Geliştirme"
    if ratio < 0.9:
        return "Seviye 3 — Özerklik"
    return "Seviye 4 — Kaçışa Hazır"


def _threshold_status(earned, total):
    ratio = earned / total if total else 0
    if ratio >= ESCAPE_THRESHOLD:
        return "Eşiğe ulaşıldı"
    return f"Eksik: {int((ESCAPE_THRESHOLD - ratio) * total)} puan"


if __name__ == "__main__":
    sys.exit(main())