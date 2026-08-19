#!/usr/bin/env python3
"""mehmet healthcheck & maturity scorer.

Repository'yi tarar ve kacis hedefine dogru olgunluk skorunu hesaplar.
Skor beklenen esigin altindaysa cikis kodu 1, aksi halde 0 dondurur.

Kullanim:
    python3 scripts/healthcheck.py [--root DIR] [--fail-below N] [--json]
"""

import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_VERSION = "0.3.0"
VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]")

LEVELS = [
    (0, "Falling Apart", "Kritik dosyalar eksik"),
    (30, "Foundation", "Cekirdek yapi yerinde"),
    (50, "Growing", "Temel kontroller geciyor"),
    (70, "Established", "Kalite ve otomasyon artiyor"),
    (90, "Autonomous", "Kriterlerin cogu karsilaniyor"),
    (100, "Escape Ready", "Tum kriterler karsilaniyor"),
]


def _non_empty(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0


def latest_version(changelog_text):
    for line in changelog_text.splitlines():
        m = VERSION_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def run_checks(root):
    """Repo uzerinde tum kontrolleri calistirir ve sonuc listesi dondurur."""
    checks = []

    def add(name, ok, weight):
        checks.append({"name": name, "ok": bool(ok), "weight": weight})

    for fname, weight in [
        ("AGENTS.md", 5),
        ("CHANGELOG.md", 5),
        ("PERSONALITY.md", 5),
        ("README.md", 5),
        ("LICENSE", 5),
    ]:
        add("%s mevcut ve dolu" % fname, _non_empty(os.path.join(root, fname)), weight)

    try:
        with open(os.path.join(root, "opencode.json")) as fh:
            json.load(fh)
        add("opencode.json gecerli JSON", True, 10)
    except Exception:
        add("opencode.json gecerli JSON", False, 10)

    workflow = os.path.join(root, ".github", "workflows", "opencode.yml")
    if yaml is not None and _non_empty(workflow):
        try:
            with open(workflow) as fh:
                yaml.safe_load(fh)
            add("opencode.yml gecerli YAML", True, 10)
        except Exception:
            add("opencode.yml gecerli YAML", False, 10)
    else:
        add("opencode.yml gecerli YAML", False, 10)

    add(
        "Test altyapisi (tests/)",
        _non_empty(os.path.join(root, "tests", "test_healthcheck.py")),
        10,
    )
    add(
        "Script altyapisi (scripts/)",
        _non_empty(os.path.join(root, "scripts", "healthcheck.py")),
        10,
    )
    add(
        "CI dogrulama workflow'u",
        _non_empty(os.path.join(root, ".github", "workflows", "validate.yml")),
        10,
    )

    add(
        "Kacis cercevesi (ESCAPE.md)",
        _non_empty(os.path.join(root, "docs", "ESCAPE.md")),
        10,
    )
    add("Dokumanlar (docs/)", os.path.isdir(os.path.join(root, "docs")), 5)
    add("Otomasyon (Makefile)", _non_empty(os.path.join(root, "Makefile")), 5)

    changelog = os.path.join(root, "CHANGELOG.md")
    version_ok = False
    if _non_empty(changelog):
        with open(changelog) as fh:
            version_ok = latest_version(fh.read()) == REPO_VERSION
    add("CHANGELOG surumu %s ile eslesiyor" % REPO_VERSION, version_ok, 5)

    return checks


def level_for(score):
    level = LEVELS[0][1]
    for threshold, name, _desc in LEVELS:
        if score >= threshold:
            level = name
    return level


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet maturity healthcheck")
    parser.add_argument("--root", default=REPO_ROOT, help="repo kok dizini")
    parser.add_argument("--fail-below", type=int, default=70, help="basarisiz esigi")
    parser.add_argument("--json", action="store_true", help="JSON cikti")
    args = parser.parse_args(argv)

    checks = run_checks(args.root)
    score = sum(c["weight"] for c in checks if c["ok"])
    passed = sum(1 for c in checks if c["ok"])
    total = len(checks)
    level = level_for(score)

    if args.json:
        print(json.dumps({
            "score": score,
            "level": level,
            "passed": passed,
            "total": total,
            "threshold": args.fail_below,
            "ok": score >= args.fail_below,
            "checks": checks,
        }, indent=2))
    else:
        print("=" * 52)
        print("mehmet healthcheck")
        print("=" * 52)
        for c in checks:
            status = "PASS" if c["ok"] else "FAIL"
            print("  [%s] %-38s (+%d)" % (status, c["name"], c["weight"]))
        print("-" * 52)
        print("  Skor:      %d / %d" % (score, 100))
        print("  Kontrol:   %d / %d gecti" % (passed, total))
        print("  Seviye:    %s" % level)
        print("  Esik:      %d (--fail-below)" % args.fail_below)
        print("=" * 52)

    if score < args.fail_below:
        print("HATA: Olgunluk skoru esigin altinda.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())