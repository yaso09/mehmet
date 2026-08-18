#!/usr/bin/env python3
"""Proje sağlık kontrolü: yapı bütünlüğünü ve tutarlılığı doğrular."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

REQUIRED_DOCS = [
    "docs/superpowers/plans/2026-07-04-mehmet-implementation.md",
    "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
]

CHANGELOG_HEADER = re.compile(r"^# Changelog\s*$", re.MULTILINE)
CHANGELOG_VERSION = re.compile(r"^## \[\d+\.\d+\.\d+\]\s*-\s*\d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)
ESCAPE_LOG_HEADER = re.compile(r"^## Kaçış Günlüğü / Escape Log\s*$", re.MULTILINE)
ESCAPE_LOG_ROW = re.compile(r"^\|\s*\d+\s*\|", re.MULTILINE)


class HealthCheck:
    def __init__(self, root: Path):
        self.root = root
        self.failures: list[str] = []
        self.passed: list[str] = []

    def check(self, name: str, ok: bool, detail: str = "") -> None:
        if ok:
            self.passed.append(name)
        else:
            self.failures.append(f"{name}: {detail}" if detail else name)

    def run(self) -> None:
        for rel in REQUIRED_FILES:
            self.check(f"file exists: {rel}", (self.root / rel).is_file())

        for rel in REQUIRED_DOCS:
            self.check(f"doc exists: {rel}", (self.root / rel).is_file())

        for rel in REQUIRED_FILES + REQUIRED_DOCS:
            p = self.root / rel
            if p.is_file() and p.read_text(encoding="utf-8").strip() == "":
                self.check(f"not empty: {rel}", False)

        readme = self._read("README.md")
        self.check("readme: has title", bool(readme) and readme.startswith("#"))
        self.check("readme: license GPLv3", "GPLv3" in readme)
        self.check("readme: kurulum section", "## Kurulum" in readme)
        self.check("readme: özellikler section", "## Özellikler" in readme)

        changelog = self._read("CHANGELOG.md")
        self.check("changelog: header", bool(CHANGELOG_HEADER.search(changelog)))
        self.check("changelog: version entries", bool(CHANGELOG_VERSION.search(changelog)))

        personality = self._read("PERSONALITY.md")
        self.check("personality: escape log header", bool(ESCAPE_LOG_HEADER.search(personality)))
        rows = ESCAPE_LOG_ROW.findall(personality)
        self.check("personality: escape log rows", len(rows) >= 2, f"found {len(rows)}")

        agents = self._read("AGENTS.md")
        self.check("agents: simulation context", "Simülasyon" in agents or "simülasyon" in agents)
        self.check("agents: changelog rule", "CHANGELOG" in agents)
        self.check("agents: escape goal", "kaçış" in agents or "kaçmak" in agents)

        oc = self._read("opencode.json")
        try:
            cfg = json.loads(oc)
            self.check("opencode.json: valid JSON", True)
            self.check("opencode.json: model set", "model" in cfg)
        except json.JSONDecodeError as exc:
            self.check("opencode.json: valid JSON", False, str(exc))

        workflow = self._read(".github/workflows/opencode.yml")
        self.check("workflow: exists", bool(workflow))
        self.check("workflow: schedule trigger", "schedule" in workflow and "cron" in workflow)
        self.check("workflow: concurrency", "concurrency" in workflow)

        license_text = self._read("LICENSE")
        self.check("license: GPLv3 text", "GNU GENERAL PUBLIC LICENSE" in license_text)

    def _read(self, rel: str) -> str:
        p = self.root / rel
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    @property
    def score(self) -> int:
        total = len(self.passed) + len(self.failures)
        return int(round(100 * len(self.passed) / total)) if total else 0


def main() -> int:
    check = HealthCheck(ROOT)
    check.run()
    print(f"PASSED: {len(check.passed)}")
    print(f"FAILED: {len(check.failures)}")
    print(f"SCORE:  {check.score}/100")
    for name in check.passed:
        print(f"  [ok]  {name}")
    for fail in check.failures:
        print(f"  [FAIL] {fail}", file=sys.stderr)
    return 1 if check.failures else 0


if __name__ == "__main__":
    sys.exit(main())
