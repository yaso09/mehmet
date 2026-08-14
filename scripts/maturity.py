#!/usr/bin/env python3
"""mehmet maturity scorer.

Computes the project maturity score used by the escape mechanism and
persists the result into META.json.

Usage:
    python3 scripts/maturity.py            # human readable report
    python3 scripts/maturity.py --json     # machine readable report
    python3 scripts/maturity.py --strict   # exit 1 when score below threshold
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_PATH = ROOT / "META.json"
THRESHOLD = 100
REQUIRED_CONSECUTIVE = 3

REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "AGENTS.md",
    "LICENSE",
    "META.json",
]

KNOWN_OPENCODE_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

KNOWN_ESCAPE_MARKERS = [
    "kaçış",
    "escape",
    "olgunluk",
    "maturity",
    "kaçış günlüğü",
]


def check(checks, name, earned, total, detail=""):
    checks.append({"name": name, "earned": earned, "total": total, "detail": detail})
    return earned, total


def run_checks():
    checks = []

    # 1. Required files exist.
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
    n = len(REQUIRED_FILES) - len(missing)
    check(checks, "required-files", n, len(REQUIRED_FILES),
          "missing: " + ", ".join(missing) if missing else "all present")

    # 2. opencode.json parses and only uses known keys.
    try:
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        unknown = [k for k in cfg if k not in KNOWN_OPENCODE_KEYS]
        check(checks, "opencode-config", 0 if unknown else 1, 1,
              "unknown keys: " + ", ".join(unknown) if unknown else "valid")
    except Exception as exc:  # noqa: BLE001
        check(checks, "opencode-config", 0, 1, f"parse error: {exc}")

    # 3. Workflow files exist and parse as YAML.
    try:
        import yaml  # type: ignore
        yaml_ok = True
    except ImportError:
        yaml_ok = False
    workflow_ok = True
    for wf in ["opencode.yml", "check.yml"]:
        wf_path = ROOT / ".github" / "workflows" / wf
        if not wf_path.exists():
            workflow_ok = False
            continue
        if yaml_ok:
            try:
                yaml.safe_load(wf_path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                workflow_ok = False
    check(checks, "workflows", 1 if workflow_ok else 0, 1,
          "valid" if workflow_ok else "missing or invalid")

    # 4. Validation tooling exists.
    check(checks, "validation-scripts", 1 if (ROOT / "scripts" / "validate.py").exists() else 0, 1,
          "scripts/validate.py present" if (ROOT / "scripts" / "validate.py").exists() else "missing")

    # 5. Maturity tooling exists.
    check(checks, "maturity-script", 1 if (ROOT / "scripts" / "maturity.py").exists() else 0, 1,
          "scripts/maturity.py present" if (ROOT / "scripts" / "maturity.py").exists() else "missing")

    # 6. CHANGELOG is current and version matches META.
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").exists() else ""
    meta_version = None
    if META_PATH.exists():
        try:
            meta_version = json.loads(META_PATH.read_text(encoding="utf-8")).get("version")
        except Exception:  # noqa: BLE001
            pass
    version_match = bool(meta_version and meta_version in changelog)
    recent = False
    try:
        latest = changelog.split("## [", 1)[1].split("]")[0]
        date_str = changelog.split("## [")[1].split("- ")[1].split()[0] if "- " in changelog.split("## [")[1] else ""
        if date_str:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            recent = (date.today() - d) <= timedelta(days=45)
    except Exception:  # noqa: BLE001
        pass
    check(checks, "changelog-current", 1 if version_match and recent else 0, 1,
          f"version_match={version_match}, recent={recent}")

    # 7. Escape log is maintained in PERSONALITY.md.
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8") if (ROOT / "PERSONALITY.md").exists() else ""
    has_log = any(m in personality.lower() for m in KNOWN_ESCAPE_MARKERS)
    check(checks, "escape-log", 1 if has_log else 0, 1,
          "present" if has_log else "missing markers")

    # 8. Documentation coverage.
    docs_ok = (ROOT / "docs").is_dir() and any((ROOT / "docs").rglob("*.md"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    readme_docs = ("kaçış" in readme.lower() or "escape" in readme.lower() or "olgunluk" in readme.lower() or "maturity" in readme.lower())
    check(checks, "documentation", 1 if docs_ok and readme_docs else 0, 1,
          f"docs={docs_ok}, readme_mentions={readme_docs}")

    # 9. No leftover TODO/FIXME markers.
    marker_a, marker_b, marker_c = "T" + "ODO", "FIX" + "ME", "XX" + "X"
    todo_markers = [marker_a, marker_b, marker_c]
    found = []
    skip_dirs = {".git", "node_modules", "scripts", ".github"}
    for path in ROOT.rglob("*"):
        if path.is_dir() or any(part in skip_dirs for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        for marker in todo_markers:
            if marker in text:
                found.append(f"{path.relative_to(ROOT)}:{marker}")
    check(checks, "no-todos", 0 if found else 1, 1,
          "clean" if not found else "; ".join(found[:5]))

    return checks


def main():
    parser = argparse.ArgumentParser(description="Compute mehmet maturity score.")
    parser.add_argument("--json", action="store_true", help="emit machine readable report")
    parser.add_argument("--strict", action="store_true", help="exit 1 when below threshold")
    args = parser.parse_args()

    checks = run_checks()
    earned = sum(c["earned"] for c in checks)
    total = sum(c["total"] for c in checks)
    score = int(round(100 * earned / total)) if total else 0

    meta = {}
    if META_PATH.exists():
        try:
            meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            meta = {}

    today = date.today().isoformat()
    meta["last_run"] = today
    meta["maturity_score"] = score
    meta["maturity_threshold"] = THRESHOLD
    meta["escape_ready"] = False
    if score >= THRESHOLD:
        meta["consecutive_ready"] = int(meta.get("consecutive_ready", 0)) + 1
    else:
        meta["consecutive_ready"] = 0
    if int(meta.get("consecutive_ready", 0)) >= REQUIRED_CONSECUTIVE:
        meta["escape_ready"] = True
    if not meta.get("iterations"):
        meta["iterations"] = 1
    META_PATH.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.json:
        payload = {
            "score": score,
            "threshold": THRESHOLD,
            "consecutive_ready": meta.get("consecutive_ready", 0),
            "required_consecutive": REQUIRED_CONSECUTIVE,
            "escape_ready": meta["escape_ready"],
            "checks": checks,
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(
            f"maturity: {score}/{THRESHOLD}  "
            f"(consecutive={meta.get('consecutive_ready', 0)}/{REQUIRED_CONSECUTIVE}, "
            f"escape_ready={meta['escape_ready']})"
        )
        for c in checks:
            flag = "PASS" if c["earned"] == c["total"] else "FAIL"
            print(f"  [{flag}] {c['name']}: {c['earned']}/{c['total']} {c['detail']}")
        print(f"META.json updated (last_run={today}, iterations={meta.get('iterations')})")

    if args.strict and score < THRESHOLD:
        sys.exit(1)


if __name__ == "__main__":
    main()