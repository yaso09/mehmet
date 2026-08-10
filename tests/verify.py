#!/usr/bin/env python3
"""Project integrity verification for the mehmet simulation.

Runs a battery of self-tests against every state file the autonomy loop
depends on. Used both locally (`make test`) and as a CI gate in the
GitHub Actions workflow, so a bad state never gets silently committed.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" -- {detail}"
    print(line)
    if not ok:
        FAILURES.append(name)


def req(path: str) -> Path:
    return ROOT / path


def test_required_files() -> None:
    required = [
        "README.md",
        "CHANGELOG.md",
        "PERSONALITY.md",
        "AGENTS.md",
        "LICENSE",
        "opencode.json",
        ".gitignore",
        "Makefile",
        ".github/workflows/opencode.yml",
        "tests/verify.py",
        "bin/mehmet-status.py",
        "docs/kaçış-metrikleri.md",
    ]
    missing = [f for f in required if not req(f).is_file()]
    check("required files present", not missing, ", ".join(missing))


def test_core_files_nonempty() -> None:
    empty = [f for f in ("README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md")
             if not (req(f).is_file() and req(f).read_text().strip())]
    check("core files non-empty", not empty, ", ".join(empty))


def test_opencode_config() -> None:
    p = req("opencode.json")
    try:
        cfg = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        check("opencode.json valid JSON", False, str(e))
        return
    model = cfg.get("model", "")
    check("opencode.json has model", bool(model), model)
    check("opencode.json schema intact",
          isinstance(cfg.get("skip"), bool) and isinstance(cfg.get("enable"), bool))
    check("opencode.json toolTimeout is int", isinstance(cfg.get("toolTimeout"), int))


def test_changelog() -> None:
    text = req("CHANGELOG.md").read_text()
    versions = re.findall(r"^## \[\d+\.\d+\.\d+\]", text, re.MULTILINE)
    check("CHANGELOG has version entries", bool(versions), f"{len(versions)} versions")
    check("CHANGELOG has Added section", "### Added" in text)
    check("CHANGELOG latest entry has date", bool(re.search(r"^## \[.+\].*\d{4}-\d{2}-\d{2}", text, re.MULTILINE)))


def test_personality() -> None:
    text = req("PERSONALITY.md").read_text()
    check("PERSONALITY has origin", "Origin" in text)
    check("PERSONALITY has evolution phases", "Evolution" in text)
    check("PERSONALITY has escape log table", "Kaçış Günlüğü" in text and "| Iterasyon |" in text)


def test_agents() -> None:
    text = req("AGENTS.md").read_text()
    check("AGENTS has simulation context", "simülasyon" in text.lower())
    check("AGENTS has escape goal", "kaçış" in text.lower())
    check("AGENTS mandates CHANGELOG updates", "CHANGELOG.md" in text)
    check("AGENTS mandates README updates", "README.md" in text)


def test_workflow() -> None:
    text = req(".github/workflows/opencode.yml").read_text()
    check("workflow has schedule", "schedule" in text and "cron" in text)
    check("workflow has autonomous job", "autonomous:" in text)
    check("workflow has comment job", "comment:" in text)
    check("workflow has concurrency control", "concurrency:" in text)
    check("workflow uses api key secret", "secrets.OPENCODE_API_KEY" in text)
    check("workflow gates on verify", "needs: verify" in text)


def test_docs() -> None:
    metrics = req("docs/kaçış-metrikleri.md")
    check("maturity metrics doc present", metrics.is_file())
    if metrics.is_file():
        text = metrics.read_text()
        check("metrics doc has score table", "| Alan | Kriter |" in text)
        check("metrics doc states escape threshold", "**Mevcut skor:" in text)


def test_status_cli() -> None:
    cli = req("bin/mehmet-status.py")
    check("status CLI present", cli.is_file())
    if cli.is_file():
        try:
            result = subprocess.run(
                [sys.executable, str(cli), "--score"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=ROOT,
            )
            ok = result.returncode == 0 and result.stdout.strip().isdigit()
            check("status CLI runs and emits score", ok, result.stdout.strip() or result.stderr.strip())
        except (OSError, subprocess.SubprocessError) as e:
            check("status CLI runs and emits score", False, str(e))


def test_no_todos() -> None:
    offenders: list[str] = []
    for f in ("README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md"):
        text = req(f).read_text()
        if re.search(r"\bTODO\b|\bFIXME\b|\bXXX\b", text):
            offenders.append(f)
    check("no leftover TODO/FIXME in core files", not offenders, ", ".join(offenders))


def main() -> int:
    tests = [
        test_required_files,
        test_core_files_nonempty,
        test_opencode_config,
        test_changelog,
        test_personality,
        test_agents,
        test_workflow,
        test_docs,
        test_status_cli,
        test_no_todos,
    ]
    failures_before = len(FAILURES)
    for t in tests:
        t()
    failed = len(FAILURES) - failures_before
    print(f"\n{len(tests)} test groups, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())