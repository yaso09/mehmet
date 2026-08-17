#!/usr/bin/env python3
"""mehmet self-check & maturity scorer.

Scans the repository, verifies integrity, and computes a maturity score
across five dimensions. Used by .github/workflows/validate.yml and by the
escape mechanism (see docs/escape-criteria.md).

Usage:
  python3 scripts/maturity.py --check   exit non-zero on any failed check
  python3 scripts/maturity.py --score   print score summary
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KNOWN_OPENCODE_KEYS = {
    "$schema", "agent", "attachment", "autoshare", "autoupdate", "command",
    "compaction", "default_agent", "disabled_providers", "enabled_providers",
    "enterprise", "experimental", "formatter", "instructions", "layout",
    "logLevel", "lsp", "mcp", "mode", "model", "permission", "plugin",
    "provider", "reference", "references", "server", "share", "shell",
    "skills", "small_model", "snapshot", "subagent_depth", "tool_output",
    "tools", "username", "watcher",
}

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def read(path):
    if not Path(path).exists():
        return ""
    return Path(path).read_text(encoding="utf-8")


def escape_log_entries():
    content = read(ROOT / "PERSONALITY.md")
    return len(re.findall(r"^\|\s*\d+\s*\|", content, re.MULTILINE))


def changelog_versions():
    content = read(ROOT / "CHANGELOG.md")
    return re.findall(r"^##\s+\[\d+\.\d+\.\d+\]", content, re.MULTILINE)


def workflow_content(name):
    return read(ROOT / ".github" / "workflows" / name)


CHECKS = [
    ("documentation", "README.md mevcut ve yapı/kaçış bölümü içeriyor",
     lambda: "## " in read(ROOT / "README.md") and "escape" in read(ROOT / "README.md")),
    ("documentation", "CHANGELOG.md en az bir sürüm kaydı içeriyor",
     lambda: len(changelog_versions()) >= 1),
    ("documentation", "docs/escape-criteria.md mevcut",
     lambda: (ROOT / "docs" / "escape-criteria.md").exists()),
    ("documentation", "PERSONALITY.md kaçış günlüğü en az 3 kayıt içeriyor",
     lambda: escape_log_entries() >= 3),
    ("documentation", "README.md kaçış/olgunluk mekanizmasına değiniyor",
     lambda: "maturity" in read(ROOT / "README.md")),

    ("code_quality", "scripts/ dizininde en az bir .py dosyası var",
     lambda: len(list((ROOT / "scripts").glob("*.py"))) >= 1 if (ROOT / "scripts").exists() else False),
    ("code_quality", "tüm scripts/*.py dosyaları sözdizimsel olarak geçerli",
     lambda: all(compile(p.read_text(encoding="utf-8"), str(p), "exec") is not None
                 for p in (ROOT / "scripts").glob("*.py"))),
    ("code_quality", "scripts/*.py dosyalarında 120 karakteri aşan satır yok",
     lambda: all(len(line) <= 120
                 for p in (ROOT / "scripts").glob("*.py")
                 for line in p.read_text(encoding="utf-8").splitlines())),
    ("code_quality", "opencode.json geçerli JSON",
     lambda: bool(json.loads(read(ROOT / "opencode.json")))),
    ("code_quality", "opencode.json bilinmeyen anahtar içermiyor",
     lambda: set(json.loads(read(ROOT / "opencode.json"))) <= KNOWN_OPENCODE_KEYS),

    ("test_infrastructure", "validate workflow'u mevcut",
     lambda: (ROOT / ".github" / "workflows" / "validate.yml").exists()),
    ("test_infrastructure", "validate workflow'u timeout içeriyor",
     lambda: "timeout-minutes" in workflow_content("validate.yml")),
    ("test_infrastructure", "opencode workflow job'ları timeout içeriyor",
     lambda: workflow_content("opencode.yml").count("timeout-minutes") >= 2),
    ("test_infrastructure", "opencode workflow'u concurrency korumasına sahip",
     lambda: "concurrency" in workflow_content("opencode.yml")),
    ("test_infrastructure", "workflow YAML dosyaları ayrıştırılabilir",
     lambda: all(yaml.safe_load(workflow_content(f)) is not None for f in ("opencode.yml", "validate.yml"))
     if HAS_YAML else None),

    ("automation", "opencode workflow'u schedule tetikleyicisine sahip",
     lambda: "schedule" in workflow_content("opencode.yml")),
    ("automation", "opencode workflow'u cron */10 tanımlı",
     lambda: "*/10" in workflow_content("opencode.yml")),
    ("automation", "concurrency cancel-in-progress ayarlı",
     lambda: "cancel-in-progress: true" in workflow_content("opencode.yml")),
    ("automation", "comment job'u /oc veya /opencode mention filtresine sahip",
     lambda: "mentions" in workflow_content("opencode.yml") or "/oc" in workflow_content("opencode.yml")),
    ("automation", "opencode workflow'u model girişi tanımlı",
     lambda: "model:" in workflow_content("opencode.yml")),

    ("autonomy", "kaçış günlüğünde en az 3 iterasyon kaydı var",
     lambda: escape_log_entries() >= 3),
    ("autonomy", "tasarım spec dokümanı mevcut",
     lambda: len(list((ROOT / "docs" / "superpowers" / "specs").glob("*.md"))) >= 1),
    ("autonomy", "AGENTS.md kaçış hedefini tanımlıyor",
     lambda: "kaçmak" in read(ROOT / "AGENTS.md")),
    ("autonomy", "README.md geliştirme döngüsünü belgeliyor",
     lambda: "döngü" in read(ROOT / "README.md").lower() or "loop" in read(ROOT / "README.md").lower()),
    ("autonomy", "validate workflow'u schedule ile otomatik çalışıyor",
     lambda: "schedule" in workflow_content("validate.yml")),
]


def run_checks():
    results = []
    for dimension, name, check in CHECKS:
        try:
            result = check()
        except Exception:
            result = False
        results.append((dimension, name, result))
    return results


def score_summary(results):
    dims = {}
    for dimension, name, result in results:
        entry = dims.setdefault(dimension, {"earned": 0, "total": 0})
        if result is not None:
            entry["total"] += 1
            if result:
                entry["earned"] += 1
    total_pts = 0
    lines = []
    for dimension, entry in dims.items():
        pts = 10 * entry["earned"] / entry["total"] if entry["total"] else 0
        total_pts += pts
        lines.append(f"  {dimension:<20} {pts:5.1f}/10")
    level = maturity_level(total_pts)
    return total_pts, lines, level


def maturity_level(total_pts):
    if total_pts >= 45:
        return "Escape Ready"
    if total_pts >= 35:
        return "Mature"
    if total_pts >= 20:
        return "Growing"
    return "Seed"


def main():
    parser = argparse.ArgumentParser(description="mehmet maturity self-check")
    parser.add_argument("--check", action="store_true", help="fail on any failed check")
    parser.add_argument("--score", action="store_true", help="print score summary")
    args = parser.parse_args()

    results = run_checks()
    failures = [r for r in results if r[2] is False]
    skipped = [r for r in results if r[2] is None]
    total_pts, lines, level = score_summary(results)

    for dimension, name, result in results:
        status = "OK " if result is True else ("SKIP" if result is None else "FAIL")
        print(f"[{status}] [{dimension}] {name}")

    print(f"\nMaturity: {total_pts:.1f}/50  Level: {level}")
    for line in lines:
        print(line)
    if skipped:
        print(f"\n{len(skipped)} check(s) skipped (pyyaml kurulu değil):")
        for _, name, _ in skipped:
            print(f"  - {name}")

    if args.score:
        return 0
    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    if not args.check:
        print("\ninfo modunda çalıştırıldı: --check ile hata durumunda çıkış kodu 1 döner")
        return 0
    print("\nTüm kontroller geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
