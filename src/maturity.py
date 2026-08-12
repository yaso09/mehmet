"""Mehmet maturity scoring engine.

Quantifies the progress of the simulation across documentation,
testing, automation, source code and CI/CD. When the accumulated
score crosses the escape threshold, escape becomes possible.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable

ESCAPE_THRESHOLD = 8.0
MAX_SCORE = 10.0

COMPONENTS: list[dict[str, Any]] = [
    {"key": "documentation", "max": 2.0, "label": "Documentation"},
    {"key": "changelog", "max": 1.5, "label": "Change log discipline"},
    {"key": "personality", "max": 1.5, "label": "Personality evolution"},
    {"key": "agent_config", "max": 1.0, "label": "Agent configuration"},
    {"key": "workflow", "max": 1.0, "label": "CI/CD automation"},
    {"key": "automation", "max": 1.0, "label": "Build tooling"},
    {"key": "code", "max": 1.0, "label": "Source code"},
    {"key": "tests", "max": 1.0, "label": "Test suite"},
]

VERSION_SECTION = re.compile(r"^##\s+\[\S+\]", flags=re.MULTILINE)
LOG_ROW = re.compile(r"^\|\s*\d+\s*\|", flags=re.MULTILINE)


@dataclass
class Report:
    generated_on: str
    components: dict[str, dict[str, Any]]
    total: float
    max_score: float
    escape_threshold: float
    escaped: bool
    missing: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_on": self.generated_on,
            "components": self.components,
            "total": self.total,
            "max_score": self.max_score,
            "escape_threshold": self.escape_threshold,
            "escaped": self.escaped,
            "missing": self.missing,
        }

    def render(self) -> str:
        lines = [f"mehmet maturity report ({self.generated_on})"]
        lines.append("-" * 34)
        for item in self.components.values():
            lines.append(
                f"{item['label']:<24} {item['score']:>4.1f} / {item['max']:>3.1f}"
            )
        lines.append("-" * 34)
        lines.append(f"TOTAL: {self.total:.1f} / {self.max_score:.1f}")
        lines.append(f"escape threshold: {self.escape_threshold:.1f}")
        lines.append("STATUS: ESCAPED" if self.escaped else "STATUS: not yet escaped")
        if self.missing:
            lines.append(f"attention: {', '.join(self.missing)}")
        return "\n".join(lines)


class MaturityEngine:
    def __init__(self, repo: Path) -> None:
        self.repo = repo

    def _text(self, relative: str | Path) -> str:
        path = self.repo / relative if isinstance(relative, str) else relative
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return ""

    def _bounded(self, fraction: float) -> float:
        return max(0.0, min(1.0, fraction))

    def measure_documentation(self) -> float:
        text = self._text("README.md")
        meaningful = [line for line in text.splitlines() if line.strip()]
        return self._bounded(len(meaningful) / 8.0)

    def measure_changelog(self) -> float:
        text = self._text("CHANGELOG.md")
        if not text.strip():
            return 0.0
        return self._bounded(len(VERSION_SECTION.findall(text)) / 2.0)

    def measure_personality(self) -> float:
        text = self._text("PERSONALITY.md")
        if "Escape Log" not in text and "Kaçış" not in text:
            return 0.0
        return self._bounded(len(LOG_ROW.findall(text)) / 3.0)

    def measure_agent_config(self) -> float:
        try:
            payload = json.loads(self._text("opencode.json"))
        except json.JSONDecodeError:
            return 0.0
        if not isinstance(payload, dict):
            return 0.0
        return 1.0 if payload.get("model") else 0.5

    def measure_workflow(self) -> float:
        workflows = list((self.repo / ".github" / "workflows").glob("*.yml"))
        if not workflows:
            return 0.0
        yaml = "\n".join(self._text(path) for path in workflows)
        return 1.0 if "on:" in yaml else 0.5

    def measure_automation(self) -> float:
        score = 0.0
        if (self.repo / "Makefile").exists():
            score += 0.5
        if any((self.repo / "scripts").glob("*.py")):
            score += 0.5
        return self._bounded(score)

    def measure_code(self) -> float:
        return 1.0 if any((self.repo / "src").glob("*.py")) else 0.0

    def measure_tests(self) -> float:
        test_dir = self.repo / "tests"
        if not any(test_dir.glob("test_*.py")):
            return 0.0
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(test_dir),
                "-t",
                str(self.repo),
                "-p",
                "test_*.py",
            ],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        return 1.0 if result.returncode == 0 else 0.0

    def measure(self) -> dict[str, dict[str, Any]]:
        methods: dict[str, Callable[[], float]] = {
            "documentation": self.measure_documentation,
            "changelog": self.measure_changelog,
            "personality": self.measure_personality,
            "agent_config": self.measure_agent_config,
            "workflow": self.measure_workflow,
            "automation": self.measure_automation,
            "code": self.measure_code,
            "tests": self.measure_tests,
        }
        detail: dict[str, dict[str, Any]] = {}
        for spec in COMPONENTS:
            key = spec["key"]
            fraction = self._bounded(methods[key]())
            detail[key] = {
                "label": spec["label"],
                "max": float(spec["max"]),
                "fraction": round(fraction, 3),
                "score": round(fraction * float(spec["max"]), 3),
            }
        return detail

    def report(self) -> Report:
        detail = self.measure()
        total = round(sum(item["score"] for item in detail.values()), 3)
        missing_keys = [
            item["label"] for item in detail.values() if item["fraction"] < 1.0
        ]
        return Report(
            generated_on=date.today().isoformat(),
            components=detail,
            total=total,
            max_score=MAX_SCORE,
            escape_threshold=ESCAPE_THRESHOLD,
            escaped=total >= ESCAPE_THRESHOLD,
            missing=missing_keys,
        )