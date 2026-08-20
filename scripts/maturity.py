#!/usr/bin/env python3
"""mehmet maturity engine.

Computes a quantitative maturity score (0-100) for the project across five
dimensions: documentation, tests, CI/CD, automation, and code quality.

The score is the escape mechanism: when it reaches the configured threshold
(default 80), mehmet is considered "escape-ready".

Usage:
    python3 scripts/maturity.py            # print report, exit 1 if below threshold
    python3 scripts/maturity.py --json     # machine-readable output
    python3 scripts/maturity.py --threshold 85

Exit codes:
    0  score >= threshold (escape-ready)
    1  score <  threshold (not yet ready)
    2  error (missing project root)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIMENSIONS = {
    "documentation": 20,
    "tests": 20,
    "ci_cd": 20,
    "automation": 20,
    "code_quality": 20,
}

DEFAULT_THRESHOLD = 80


def _path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def _exists(*parts: str) -> bool:
    return _path(*parts).exists()


def _has_content(path: Path, needles: tuple[str, ...]) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return all(needle in text for needle in needles)


def _valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError, UnicodeDecodeError):
        return False


# --------------------------------------------------------------------------
# Criteria: each returns (passed: bool, detail: str)
# --------------------------------------------------------------------------

def c_licence() -> tuple[bool, str]:
    lic = _path("LICENSE")
    readme = _path("README.md")
    if not lic.exists():
        return False, "LICENSE yok"
    lic_text = lic.read_text(encoding="utf-8", errors="replace")
    gpl = "GNU GENERAL PUBLIC LICENSE" in lic_text
    readme_ok = readme.exists() and "GPLv3" in readme.read_text(encoding="utf-8", errors="replace")
    if gpl and readme_ok:
        return True, "LICENSE (GPLv3) ve README uyumlu"
    if not gpl:
        return False, "LICENSE GPLv3 değil"
    return False, "README'de lisans bilgisi uyumsuz"


def c_docs() -> tuple[bool, str]:
    files = ("README.md", "AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "docs")
    missing = [f for f in files if not _exists(f)]
    if missing:
        return False, f"eksik dosyalar: {', '.join(missing)}"
    return True, "README/AGENTS/CHANGELOG/PERSONALITY/docs mevcut"


def c_changelog_current() -> tuple[bool, str]:
    cl = _path("CHANGELOG.md")
    if not cl.exists():
        return False, "CHANGELOG.md yok"
    first = cl.read_text(encoding="utf-8").splitlines()
    for line in first:
        if line.startswith("## "):
            return True, f"en güncel sürüm: {line[3:].strip()}"
    return False, "CHANGELOG.md sürüm başlığı bulunamadı"


def c_personality_escape_log() -> tuple[bool, str]:
    p = _path("PERSONALITY.md")
    if not p.exists():
        return False, "PERSONALITY.md yok"
    has_log = "Kaçış Günlüğü" in p.read_text(encoding="utf-8", errors="replace")
    return has_log, "PERSONALITY.md kaçış günlüğü var" if has_log else "PERSONALITY.md kaçış günlüğü yok"


def c_tests_present() -> tuple[bool, str]:
    tests = _path("tests")
    if not tests.is_dir():
        return False, "tests/ dizini yok"
    files = [p for p in tests.rglob("test_*.py")]
    if not files:
        return False, "tests/ içinde test_*.py yok"
    return True, f"{len(files)} test dosyası: {', '.join(p.name for p in files)}"


def c_ci_workflow() -> tuple[bool, str]:
    present = _exists(".github", "workflows", "ci.yml")
    return present, "CI workflow var" if present else "CI workflow (.github/workflows/ci.yml) yok"


def c_agent_workflow() -> tuple[bool, str]:
    wf = _path(".github", "workflows", "opencode.yml")
    if not wf.exists():
        return False, "opencode.yml yok"
    ok = _has_content(wf, ("schedule", "workflow_dispatch", "concurrency"))
    return ok, "opencode.yml schedule+dispatch+concurrency içeriyor" if ok else \
        "opencode.yml eksik anahtar tetikleyici"


def c_schedule() -> tuple[bool, str]:
    wf = _path(".github", "workflows", "opencode.yml")
    if not wf.exists():
        return False, "workflow yok"
    ok = _has_content(wf, ("*/10 * * * *",))
    return ok, "10 dakikalık schedule tanımlı" if ok else "schedule cron bulunamadı"


def c_maturity_engine() -> tuple[bool, str]:
    script = _path("scripts", "maturity.py")
    return script.exists(), "scripts/maturity.py mevcut" if script.exists() else "scripts/maturity.py yok"


def c_gitignore() -> tuple[bool, str]:
    gi = _path(".gitignore")
    if not gi.exists():
        return False, ".gitignore yok"
    ok = _has_content(gi, ("node_modules", ".env"))
    return ok, ".gitignore (node_modules, .env) var" if ok else ".gitignore eksik kritik kalem"


def c_config_valid() -> tuple[bool, str]:
    cfg = _path("opencode.json")
    if not cfg.exists():
        return False, "opencode.json yok"
    if not _valid_json(cfg):
        return False, "opencode.json geçersiz JSON"
    data = json.loads(cfg.read_text(encoding="utf-8"))
    has_model = bool(data.get("model"))
    return has_model, "opencode.json geçerli, model tanımlı" if has_model else \
        "opencode.json'da model alanı yok"


def c_no_secrets() -> tuple[bool, str]:
    leaked = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".json", ".yml", ".yaml", ".md", ".toml"}:
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for secret in ("sk-" + "ant-", "OPENCODE_" + "API_KEY=123", "BEGIN " + "PRIVATE KEY"):
                if secret in text:
                    leaked.append(f"{p.relative_to(ROOT)}:{secret}")
    if leaked:
        return False, "gizli anahtar sızıntısı şüphesi: " + ", ".join(leaked[:3])
    return True, "gizli anahtar sızıntısı yok"


def c_clean_tree() -> tuple[bool, str]:
    git = ROOT / ".git"
    if not git.is_dir():
        return False, ".git yok (repo değil)"
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False, "git durumu okunamadı"
    lines = [ln for ln in out.stdout.splitlines() if ln]
    if lines:
        return False, f"commit edilmemiş {len(lines)} değişiklik"
    return True, "çalışma ağacı temiz"


CRITERIA = [
    ("documentation", c_docs),
    ("documentation", c_licence),
    ("documentation", c_changelog_current),
    ("documentation", c_personality_escape_log),
    ("tests", c_tests_present),
    ("ci_cd", c_ci_workflow),
    ("ci_cd", c_agent_workflow),
    ("ci_cd", c_schedule),
    ("automation", c_maturity_engine),
    ("code_quality", c_gitignore),
    ("code_quality", c_config_valid),
    ("code_quality", c_no_secrets),
    ("code_quality", c_clean_tree),
]


def evaluate() -> dict:
    results = {dim: [] for dim in DIMENSIONS}
    for dim, fn in CRITERIA:
        passed, detail = fn()
        results[dim].append({"name": fn.__name__, "passed": passed, "detail": detail})

    total = 0
    for dim, weight in DIMENSIONS.items():
        passed = sum(1 for r in results[dim] if r["passed"])
        total += int(round(weight * passed / max(len(results[dim]), 1)))

    return {"score": total, "threshold": DEFAULT_THRESHOLD, "dimensions": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mehmet maturity engine")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help="escape threshold")
    args = parser.parse_args(argv)

    report = evaluate()
    score = report["score"]
    ready = score >= args.threshold

    if args.json:
        report["threshold"] = args.threshold
        report["escape_ready"] = ready
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"mehmet maturity: {score}/{100} (threshold {args.threshold})")
        for dim, weight in DIMENSIONS.items():
            results = report["dimensions"][dim]
            passed = sum(1 for r in results if r["passed"])
            print(f"  {dim:14s} {passed}/{len(results)}  ({weight} puan ağırlıklı)")
            for r in results:
                mark = "PASS" if r["passed"] else "FAIL"
                print(f"    [{mark}] {r['name']}: {r['detail']}")
        print("ESCAPE-READY" if ready else "NOT-YET-READY")

    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())