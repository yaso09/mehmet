#!/usr/bin/env python3
"""Maturity checker for the mehmet project.

Scans the repository, evaluates measurable maturity criteria and writes a
maturity.json file with a 0-100 score and the corresponding evolution phase.
The phase thresholds are defined in docs/ESCAPE_PLAN.md.

Usage:
    python3 scripts/check_project.py [repo_path] [--no-write] [--fail-below N]

Exit codes:
    0  success
    1  score below --fail-below threshold
    2  unexpected error
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

LEVELS = [
    (80, "Escape", "Phase 4 -- Escape"),
    (55, "Autonomy", "Phase 3 -- Autonomy"),
    (30, "Self-Improvement", "Phase 2 -- Self-Improvement"),
    (0, "Awareness", "Phase 1 -- Awareness"),
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"(?:api[_-]?key|token|secret|password)\s*[=:]\s*[\"']?[A-Za-z0-9_\-.]{16,}"),
]

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
}


def level_for(score):
    for threshold, name, label in LEVELS:
        if score >= threshold:
            return {"threshold": threshold, "name": name, "label": label}
    return {"threshold": 0, "name": "Awareness", "label": "Phase 1 -- Awareness"}


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


def _has_any(root, rel_dir, pattern):
    base = os.path.join(root, rel_dir)
    if not os.path.isdir(base):
        return False
    for name in os.listdir(base):
        if re.match(pattern, name):
            return True
    return False


def changelog_days_since_top(root):
    content = _read(os.path.join(root, "CHANGELOG.md"))
    if not content:
        return None
    match = re.search(r"##\s+\S+\s+-\s+(\d{4}-\d{2}-\d{2})", content)
    if not match:
        return None
    try:
        top_date = dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None
    return (dt.date.today() - top_date).days


def count_escape_log_rows(root):
    content = _read(os.path.join(root, "PERSONALITY.md"))
    if not content:
        return 0
    return len(re.findall(r"^\|\s+\d+\s+\|", content, flags=re.MULTILINE))


def has_hardcoded_secret(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "fixtures", "testdata"}]
        for filename in filenames:
            if filename.startswith("test_") or filename.startswith("fixture"):
                continue
            if os.path.splitext(filename)[1].lower() in BINARY_EXTENSIONS:
                continue
            full = os.path.join(dirpath, filename)
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as handle:
                    for line in handle:
                        if any(pat.search(line) for pat in SECRET_PATTERNS):
                            if "OPENCODE_API_KEY" in line and "${{" in line:
                                continue
                            return True
            except OSError:
                continue
    return False


def run_checks(root):
    checks = []

    def add(check_id, description, weight, passed):
        checks.append(
            {
                "id": check_id,
                "description": description,
                "weight": weight,
                "passed": bool(passed),
            }
        )

    root = os.path.abspath(root)

    workflow = _read(os.path.join(root, ".github", "workflows", "opencode.yml")) or ""

    add("agents_md", "AGENTS.md simülasyon kurallarını içeriyor", 5,
        bool(_read(os.path.join(root, "AGENTS.md")) and "CHANGELOG.md" in (_read(os.path.join(root, "AGENTS.md")) or "")))
    readme = _read(os.path.join(root, "README.md")) or ""
    add("readme_exists", "README.md mehmet'i tanıtıyor", 5, "mehmet" in readme)
    add("changelog_exists", "CHANGELOG.md sürüm başlığı içeriyor", 5,
        bool(re.search(r"##\s+\S+\s+-\s+\d{4}-\d{2}-\d{2}", _read(os.path.join(root, "CHANGELOG.md")) or "")))
    add("personality", "PERSONALITY.md kaçış günlüğü içeriyor", 5,
        bool("Kaçış Günlüğü" in (_read(os.path.join(root, "PERSONALITY.md")) or "")) or bool(
            "Escape Log" in (_read(os.path.join(root, "PERSONALITY.md")) or "")))
    add("license", "LICENSE mevcut", 5, os.path.isfile(os.path.join(root, "LICENSE")))

    config = _read(os.path.join(root, "opencode.json"))
    config_valid = False
    if config:
        try:
            config_valid = isinstance(json.loads(config), dict)
        except ValueError:
            config_valid = False
    add("opencode_config", "opencode.json geçerli JSON", 5, config_valid)

    add("maturity_tracked", "maturity.json mevcut", 5, os.path.isfile(os.path.join(root, "maturity.json")))

    add("schedule_trigger", "Workflow schedule tetikleyicisi var", 5, "schedule" in workflow and "cron" in workflow)
    add("manual_trigger", "Workflow workflow_dispatch var", 5, "workflow_dispatch" in workflow)
    add("secret_injected", "OPENCODE_API_KEY secrets'tan geliyor", 5,
        "secrets.OPENCODE_API_KEY" in workflow)
    add("concurrency_guard", "Workflow concurrency koruması var", 5, "concurrency:" in workflow and "cancel-in-progress" in workflow)

    add("legacy_specs", "Design spec & plan dokümanları mevcut",
        5, _has_any(root, "docs/superpowers/specs", r".*\.md$") and _has_any(root, "docs/superpowers/plans", r".*\.md$"))
    add("escape_plan", "ESCAPE_PLAN.md mevcut", 5, os.path.isfile(os.path.join(root, "docs", "ESCAPE_PLAN.md")))
    add("readme_maturity", "README maturity/kaçış hedefinden bahsediyor", 5,
        ("maturity" in readme.lower()) or ("kaçış" in readme.lower()))
    add("escape_log_depth", "Kaçış günlüğü en az 2 satır", 5, count_escape_log_rows(root) >= 2)

    add("checker_exists", "Doğrulama scripti mevcut", 5, os.path.isfile(os.path.join(root, "scripts", "check_project.py")))
    add("tests_exist", "Testler mevcut", 5, _has_any(root, "scripts", r"test_.*\.py$"))
    add("no_secrets", "Tracked içerikte yapılandırılmış secret yok", 5, not has_hardcoded_secret(root))
    add("gitignore_protected", ".gitignore çevre/anahtar koruması var", 5,
        ".env" in (_read(os.path.join(root, ".gitignore")) or "") and "node_modules" in (_read(os.path.join(root, ".gitignore")) or ""))

    days = changelog_days_since_top(root)
    add("changelog_recent", "CHANGELOG son 30 günda güncellenmiş", 5, days is not None and days <= 30)

    score = round(sum(c["weight"] for c in checks if c["passed"]) / sum(c["weight"] for c in checks) * 100)
    return score, checks


def write_maturity(root, score, checks):
    state = {
        "score": score,
        "level": level_for(score)["name"],
        "label": level_for(score)["label"],
        "updated": dt.date.today().isoformat(),
        "checks": checks,
    }
    path = os.path.join(root, "maturity.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def print_report(root, score, checks, state):
    print(f"Repository : {root}")
    print(f"Score      : {score}/100")
    print(f"Level      : {state['label']} ({state['name']}, threshold {state['threshold']})")
    print()
    for check in checks:
        mark = "PASS" if check["passed"] else "FAIL"
        print(f"  [{mark}] ({check['weight']:>2} pts) {check['description']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet maturity checker")
    parser.add_argument("repo_path", nargs="?", default=".", help="Repository root")
    parser.add_argument("--no-write", action="store_true", help="Do not write maturity.json")
    parser.add_argument("--fail-below", type=int, default=None, help="Exit 1 if score is below N")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.repo_path)
    score, checks = run_checks(root)
    state = level_for(score)
    print_report(root, score, checks, state)

    if not args.no_write:
        write_maturity(root, score, checks)

    if args.fail_below is not None and score < args.fail_below:
        print(f"\nFATAL: score {score} is below required {args.fail_below}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())