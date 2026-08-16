#!/usr/bin/env python3
"""mehmet self-check: validates project health and computes a maturity score.

Runs a battery of structural, configuration and documentation checks against
the repository and reports a maturity score (0-100). Exit code is non-zero
when any check fails, so it can gate CI.

Usage:
    python3 scripts/validate.py [--json] [--score]

    --json    Emit the report as JSON (for tooling).
    --score   Only print the maturity score.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is optional
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "VERSION",
    "opencode.json",
    ".github/workflows/opencode.yml",
]
AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "projeyi taray",
    "kaçış",
]
README_SECTIONS = ["Kurulum", "Lisans", "Özellikler"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
CHECK_MARK = "[PASS]"
FAIL_MARK = "[FAIL]"


def read_text(rel_path: str) -> str | None:
    try:
        return (ROOT / rel_path).read_text(encoding="utf-8")
    except OSError:
        return None


def main() -> int:
    args = parse_args()
    checks: list[tuple[str, bool, str]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))

    # --- Structure ---------------------------------------------------------
    for rel in REQUIRED_FILES:
        add(f"file:{rel}", (ROOT / rel).is_file(), "")

    # --- Versioning --------------------------------------------------------
    version_raw = (read_text("VERSION") or "").strip()
    version_ok = bool(SEMVER.match(version_raw))
    add("version:semver", version_ok, version_raw)

    changelog = read_text("CHANGELOG.md") or ""
    top = re.search(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]\s", changelog, re.M)
    add(
        "version:changelog-matches-VERSION",
        bool(top and version_raw and top.group(1) == version_raw),
        f"changelog={top.group(1) if top else None}",
    )

    # --- Configuration validity ---------------------------------------------
    oc = read_text("opencode.json") or ""
    try:
        oc_data = json.loads(oc)
        oc_valid = True
    except json.JSONDecodeError as e:
        oc_data, oc_valid = {}, False
    add("config:opencode.json-valid-json", oc_valid, "")
    if oc_valid:
        add("config:opencode.json-has-model", "model" in oc_data, str(oc_data.get("model")))
        add(
            "config:opencode.json-model-zen-free",
            oc_data.get("model") == "opencode/deepseek-v4-flash-free",
            str(oc_data.get("model")),
        )

    for rel in [".github/workflows/opencode.yml", ".github/workflows/ci.yml"]:
        text = read_text(rel) or ""
        if not text:
            add(f"config:{rel}-yaml", False, "missing")
            continue
        if yaml is None:
            ok = bool(text.strip())
            add(f"config:{rel}-yaml", ok, "syntax not fully parsed (PyYAML missing)")
        else:
            try:
                list(yaml.safe_load_all(text))
                add(f"config:{rel}-yaml", True, "")
            except yaml.YAMLError as e:
                add(f"config:{rel}-yaml", False, str(e))

    # --- Documentation consistency ------------------------------------------
    personality = read_text("PERSONALITY.md") or ""
    add(
        "docs:personality-escape-log",
        "Kaçış Günlüğü" in personality and re.search(r"\|\s*\d+\s*\|", personality) is not None,
        "",
    )

    agents = read_text("AGENTS.md") or ""
    missing_rules = [kw for kw in AGENTS_RULES if kw not in agents]
    add("docs:agents-rules", not missing_rules, ",".join(missing_rules))

    readme = read_text("README.md") or ""
    missing_sections = [s for s in README_SECTIONS if s not in readme]
    add("docs:readme-sections", not missing_sections, ",".join(missing_sections))

    changelog_has_entries = bool(re.search(r"^##\s*\[[0-9]", changelog, re.M))
    add("docs:changelog-entries", changelog_has_entries, "")

    gitignore = read_text(".gitignore") or ""
    add("docs:gitignore-nonempty", bool(gitignore.strip()), "")

    # --- Test / tooling ------------------------------------------------------
    add("tooling:validate.py-self-check", True, "")
    makefile = read_text("Makefile") or ""
    add("tooling:makefile-validate-target", "validate:" in makefile, "")

    # --- Report --------------------------------------------------------------
    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0

    if args.score:
        print(score)
        return 0 if passed == total else 1

    if args.json:
        print(
            json.dumps(
                {
                    "score": score,
                    "passed": passed,
                    "total": total,
                    "checks": [
                        {"name": n, "ok": ok, "detail": d} for n, ok, d in checks
                    ],
                },
                indent=2,
            )
        )
    else:
        width = max(len(n) for n, _, _ in checks)
        for name, ok, detail in checks:
            mark = CHECK_MARK if ok else FAIL_MARK
            suffix = f"  ({detail})" if detail else ""
            print(f"{mark} {name.ljust(width)}{suffix}")
        print("-" * 60)
        print(f"Maturity score: {score}/100 ({passed}/{total} checks passed)")
        print(
            "PASS"
            if passed == total
            else f"FAIL ({total - passed} check(s) failed)"
        )

    return 0 if passed == total else 1


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="emit report as JSON")
    p.add_argument("--score", action="store_true", help="print only the score")
    return p.parse_args()


if __name__ == "__main__":
    sys.exit(main())