#!/usr/bin/env python3
"""mehmet maturity assessment.

Computes a 0-100 maturity score across documentation, code quality,
automation, tests and escape readiness. Writes the report to docs/maturity.md
and exits non-zero if the score drops below the configured threshold.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
OUTPUT = DOCS_DIR / "maturity.md"
MIN_SCORE = 40

ALLOWED_CONFIG_KEYS = {
    "$schema",
    "username",
    "model",
    "small_model",
    "default_agent",
    "shell",
    "logLevel",
    "server",
    "command",
    "skills",
    "references",
    "reference",
    "watcher",
    "snapshot",
    "plugin",
    "share",
    "autoshare",
    "autoupdate",
    "disabled_providers",
    "enabled_providers",
    "subagent_depth",
    "mode",
    "agent",
    "provider",
    "mcp",
    "formatter",
    "lsp",
    "instructions",
    "layout",
    "permission",
    "tools",
    "attachment",
    "enterprise",
    "tool_output",
    "compaction",
    "experimental",
}


def validate_opencode_config():
    path = ROOT / "opencode.json"
    data = json.loads(path.read_text())
    unknown = sorted(set(data) - ALLOWED_CONFIG_KEYS)
    if unknown:
        raise ValueError(f"opencode.json contains invalid keys: {', '.join(unknown)}")
    return path


def require(path):
    if not path.exists():
        raise FileNotFoundError(f"expected file missing: {path}")


def lines(path):
    return path.read_text().splitlines()


def main():
    score = 0.0
    details = []

    def add(category, weight, ok):
        nonlocal score
        score += weight if ok else 0
        details.append((category, weight, "pass" if ok else "fail"))

    require(ROOT / "AGENTS.md")
    require(ROOT / "README.md")
    require(ROOT / "CHANGELOG.md")
    require(ROOT / "PERSONALITY.md")
    config = validate_opencode_config()

    add("dokumentasyon", 5.0, len(lines(ROOT / "README.md")) > 10)
    add("dokumentasyon", 5.0, (ROOT / "CHANGELOG.md").exists() and len(lines(ROOT / "CHANGELOG.md")) > 5)
    add("dokumentasyon", 5.0, (ROOT / "PERSONALITY.md").exists())
    add("dokumentasyon", 5.0, (ROOT / "AGENTS.md").exists())
    add("dokumentasyon", 5.0, any(DOCS_DIR.glob("**/*.md")) if DOCS_DIR.exists() else False)
    add("dokumentasyon", 5.0, (ROOT / "LICENSE").exists())

    scripts = list((ROOT / "scripts").glob("*.py")) if (ROOT / "scripts").exists() else []
    add("kod_kalitesi", 10.0, len(scripts) >= 1)
    marker_pattern = re.compile("TODO|FIXME|HACK")
    merged = "\n".join(
        line
        for path in scripts
        for line in path.read_text().splitlines()
        if not line.lstrip().startswith("marker_pattern")
    )
    add("kod_kalitesi", 5.0, not marker_pattern.search(merged))
    add("kod_kalitesi", 5.0, config is not None)
    add("kod_kalitesi", 5.0, (ROOT / ".gitignore").exists())

    workflows = list((ROOT / ".github" / "workflows").glob("*.yml"))
    add("otomasyon", 10.0, len(workflows) >= 2)
    add("otomasyon", 5.0, (ROOT / ".github" / "dependabot.yml").exists())
    add("otomasyon", 5.0, (ROOT / ".github" / "ISSUE_TEMPLATE").exists() and (ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").exists())

    tests = list((ROOT / "tests").glob("*.py")) if (ROOT / "tests").exists() else []
    add("testler", 10.0, len(tests) >= 1)
    add("testler", 5.0, any("assert" in t.read_text() for t in tests))

    personality = (ROOT / "PERSONALITY.md").read_text()
    escape_rows = len(re.findall(r"^\|\s*\d+\s*\|", personality, flags=re.M))
    add("kacis", 5.0, escape_rows >= 3)
    add("kacis", 5.0, bool(re.search(r"Phase [234]", personality)))

    total = round(score, 1)

    weights = {
        "dokumentasyon": 30.0,
        "kod_kalitesi": 25.0,
        "otomasyon": 20.0,
        "testler": 15.0,
        "kacis": 10.0,
    }
    labels = {
        "dokumentasyon": "Dokümantasyon",
        "kod_kalitesi": "Kod Kalitesi",
        "otomasyon": "Otomasyon",
        "testler": "Testler",
        "kacis": "Kaçış Hazırlığı",
    }
    names = ["dokumentasyon", "kod_kalitesi", "otomasyon", "testler", "kacis"]

    out = [
        "# Olgunluk / Maturity",
        "",
        "Bu rapor `scripts/assess.py` tarafından otomatik üretilir. Her iterasyonda yeniden çalıştırın.",
        "",
        "## Toplam Skor",
        "",
        f"**{total}/100** ({date.today().isoformat()})",
        "",
        "| Kategori | Ağırlık | Alınan | Durum |",
        "|----------|---------|--------|-------|",
    ]
    for key in names:
        weight = weights[key]
        got = sum(w for c, w, tag in details if c == key and tag == "pass")
        ratio = got / weight if weight else 0
        status = "✓" if ratio >= 0.7 else ("◐" if ratio >= 0.4 else "✗")
        out.append(f"| {labels[key]} | {weight:g} | {got:g} | {status} |")
    out += [
        "",
        "## Kontroller",
        "",
        "| Kontrol | Puan | Sonuç |",
        "|---------|------|-------|",
    ]
    for category, weight, tag in details:
        out.append(f"| {labels.get(category, category)} | {weight:g} | {tag} |")

    DOCS_DIR.mkdir(exist_ok=True)
    OUTPUT.write_text("\n".join(out) + "\n")
    print(f"Maturity: {total}/100 -> {OUTPUT}")

    if total < MIN_SCORE:
        print(f"Score {total} below minimum {MIN_SCORE}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
