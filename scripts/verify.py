#!/usr/bin/env python3
"""mehmet — project integrity & maturity verifier.

Validates the repository against the rules defined in AGENTS.md and computes
the maturity score defined in docs/escape-plan.md.

Exit codes:
    0  PASS  — no critical check failed
    1  FAIL  — at least one critical check failed
    2  ERROR — script-level error

Usage:
    python3 scripts/verify.py            # human-readable report
    python3 scripts/verify.py --json     # machine-readable JSON report
    python3 scripts/verify.py --quiet    # only PASS/FAIL + exit code (CI)
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_CHANGELOG_AGE_DAYS = 30
GPG_KEYS = {
    "docs": ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md", "docs/escape-plan.md"],
}
SENSITIVE_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
ALLOWED_OPENCODE_KEYS = {
    "$schema", "model", "small_model", "instructions", "provider", "agent", "permission",
    "tools", "mcp", "logLevel", "experimental", "compaction", "commands", "command",
    "formatter", "lsp", "plugin", "snapshot", "autoupdate", "disabled_providers",
    "enabled_providers", "default_agent", "subagent_depth", "username", "mode",
    "instruction", "skills", "references", "reference", "watcher", "attachment",
    "server", "shell", "share", "autoshare", "layout",
}


class Check:
    def __init__(self, key, name, critical=False):
        self.key = key
        self.name = name
        self.critical = critical
        self.ok = False

    def run(self, fn):
        try:
            self.ok = bool(fn())
        except Exception:
            self.ok = False
        return self.ok

    def result(self):
        return {
            "key": self.key,
            "name": self.name,
            "ok": self.ok,
            "critical": self.critical,
        }


def read_rel(path):
    with open(os.path.join(ROOT, path), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


def check_docs():
    checks = []
    checks.append(Check("docs/readme", "README complete (# mehmet, Özellikler, Kurulum, Lisans GPLv3)"))
    checks.append(Check("docs/changelog", "CHANGELOG has a fresh (<30d) version entry"))
    checks.append(Check("docs/design", "Design docs exist (spec + implementation plan)"))
    checks.append(Check("docs/rescape", "Escape plan with measurable threshold exists"))
    checks[-1].run(lambda: exists("docs/escape-plan.md"))
    checks[-1].critical = False
    checks[-1].ok = checks[-1].ok and "Kaçış Eşiği" in read_rel("docs/escape-plan.md") if checks[-1].ok else False

    checks[0].run(lambda: (
        exists("README.md")
        and "# mehmet" in read_rel("README.md")
        and "Özellikler" in read_rel("README.md")
        and "Lisans" in read_rel("README.md")
        and "GPLv3" in read_rel("README.md")
    ))

    def changelog_fresh():
        if not exists("CHANGELOG.md"):
            return False
        text = read_rel("CHANGELOG.md")
        dates = re.findall(r"\[[\d.]+\]\s*-\s*(\d{4}-\d{2}-\d{2})", text)
        if not dates:
            return False
        top = datetime.strptime(max(dates), "%Y-%m-%d").date()
        return (date.today() - top).days <= MAX_CHANGELOG_AGE_DAYS
    checks[1].run(changelog_fresh)

    checks[2].run(lambda: (
        exists("docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md")
        and exists("docs/superpowers/plans/2026-07-04-mehmet-implementation.md")
    ))

    return checks


def check_automation():
    wf = ".github/workflows/opencode.yml"
    checks = [
        Check("autom/workflow", "CI workflow exists", critical=True),
        Check("autom/triggers", "Workflow listens to schedule + issues + PR"),
        Check("autom/concurrency", "Workflow enforces concurrency control"),
        Check("autom/validate", "Workflow runs a validate job via verify.py"),
    ]

    def triggers():
        if not exists(wf):
            return False
        t = read_rel(wf)
        return ("schedule:" in t and "*/10" in t and "issues:" in t
                and "pull_request:" in t and "workflow_dispatch" in t)
    checks[0].run(lambda: exists(wf))
    checks[1].run(triggers)
    checks[2].run(lambda: exists(wf) and "concurrency:" in read_rel(wf) and "cancel-in-progress" in read_rel(wf))
    checks[3].run(lambda: exists(wf) and "verify" in read_rel(wf) and "validate" in read_rel(wf))
    return checks


def check_testing():
    checks = [
        Check("test/script", "scripts/verify.py is valid Python", critical=True),
        Check("test/doc-run", "README documents how to run verification"),
        Check("test/opencode-cfg", "opencode.json is valid, clean JSON"),
        Check("test/metrics", "Escape plan defines scoring table"),
    ]

    def valid_python():
        import py_compile
        path = os.path.join(ROOT, "scripts", "verify.py")
        if not os.path.exists(path):
            return False
        py_compile.compile(path, doraise=True)
        return True
    checks[0].run(valid_python)

    checks[1].run(lambda: exists("README.md") and "scripts/verify.py" in read_rel("README.md"))

    def opencode_clean():
        if not exists("opencode.json"):
            return False
        try:
            data = json.loads(read_rel("opencode.json"))
        except json.JSONDecodeError:
            return False
        unknown = set(data.keys()) - ALLOWED_OPENCODE_KEYS
        return not unknown and "model" in data
    checks[2].run(opencode_clean)

    checks[3].run(lambda: (
        exists("docs/escape-plan.md")
        and "Puan Dağılımı" in read_rel("docs/escape-plan.md")
        and "| Kategori" in read_rel("docs/escape-plan.md")
    ))
    return checks


def check_security():
    wf = ".github/workflows/opencode.yml"
    checks = [
        Check("sec/no-secrets", "No secrets / API keys committed", critical=True),
        Check("sec/gitignore", ".gitignore covers sensitive files"),
        Check("sec/least-priv", "Workflow declares least-privilege permissions"),
        Check("sec/creds", "Working tree keeps credentials out (persist-credentials false)"),
    ]

    def no_secrets():
        for dirpath, _, filenames in os.walk(ROOT):
            if ".git" in dirpath:
                continue
            for name in filenames:
                path = os.path.join(dirpath, name)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except OSError:
                    continue
                if any(p.search(content) for p in SENSITIVE_PATTERNS):
                    return False
        return True
    checks[0].run(no_secrets)

    def gitignore_ok():
        if not exists(".gitignore"):
            return False
        gi = read_rel(".gitignore")
        return all(k in gi for k in (".env", "node_modules", "*.log", ".DS_Store"))
    checks[1].run(gitignore_ok)

    checks[2].run(lambda: (
        exists(wf)
        and "permissions:" in read_rel(wf)
        and all(k in read_rel(wf) for k in ("contents:", "issues:", "pull-requests:"))
    ))
    checks[3].run(lambda: (
        exists(wf)
        and "persist-credentials: false" in read_rel(wf)
        and "OPENCODE_API_KEY" in read_rel(wf)
        and "secrets.OPENCODE_API_KEY" in read_rel(wf)  # only via secrets, never literal
    ))
    return checks


def check_self_improvement():
    checks = [
        Check("imp/agents", "AGENTS.md defines goal + rules"),
        Check("imp/personality", "PERSONALITY.md has evolution phases + escape log"),
        Check("imp/log-today", "Escape log has a row for a recent iteration"),
        Check("imp/dirty", "Docs are in sync with reality (README references escape plan)"),
    ]
    checks[0].run(lambda: (
        exists("AGENTS.md")
        and "simülasyon" in read_rel("AGENTS.md").lower()
        and "CHANGELOG.md" in read_rel("AGENTS.md")
    ))

    def personality_ok():
        if not exists("PERSONALITY.md"):
            return False
        p = read_rel("PERSONALITY.md")
        return "Kaçış Günlüğü" in p and "Escape Log" in p
    checks[1].run(personality_ok)

    def log_recent():
        if not exists("PERSONALITY.md"):
            return False
        text = read_rel("PERSONALITY.md")
        rows = re.findall(r"\|\s*\d+\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", text)
        if not rows:
            return False
        top = datetime.strptime(max(rows), "%Y-%m-%d").date()
        return (date.today() - top).days <= MAX_CHANGELOG_AGE_DAYS
    checks[2].run(log_recent)

    checks[3].run(lambda: (
        exists("README.md")
        and ("escape-plan" in read_rel("README.md") or "Olgunluk" in read_rel("README.md"))
    ))
    return checks


def main():
    parser = argparse.ArgumentParser(description="mehmet integrity & maturity verifier")
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    parser.add_argument("--quiet", action="store_true", help="emit only PASS/FAIL")
    args = parser.parse_args()

    try:
        groups = [
            ("Dokümantasyon", check_docs()),
            ("Otomasyon", check_automation()),
            ("Test & Araçlar", check_testing()),
            ("Güvenlik", check_security()),
            ("Kendini Geliştirme", check_self_improvement()),
        ]
    except Exception as exc:  # script-level error
        if args.quiet:
            print("ERROR")
        else:
            print(f"ERROR: {exc}")
        return 2

    report = {"root": ROOT, "date": date.today().isoformat(),
              "score": {"total": 0, "categories": {}}}
    critical_failed = False
    total_checks = 0
    passed_checks = 0

    for name, checks in groups:
        cat_score = sum(5 for c in checks if c.ok)
        report["score"]["categories"][name] = cat_score
        report["score"]["total"] += cat_score
        for c in checks:
            total_checks += 1
            passed_checks += int(c.ok)
            if c.critical and not c.ok:
                critical_failed = True

    if args.quiet:
        print("FAIL" if critical_failed else "PASS")
        return 1 if critical_failed else 0

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if critical_failed else 0

    print(f"mehmet verifier — {report['date']}")
    print("=" * 72)
    for name, checks in groups:
        print(f"\n[{name}] {report['score']['categories'][name]}/20")
        for c in checks:
            mark = "ok " if c.ok else "FAIL" if c.critical else "warn"
            print(f"  [{mark:4}] {c.key:16} {c.name}")
    print("\n" + "=" * 72)
    print(f"Checks: {passed_checks}/{total_checks}  "
          f"Maturity: {report['score']['total']}/100  (escape threshold ≥ 90)")
    if critical_failed:
        print("RESULT: FAIL (critical checks failed)")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())