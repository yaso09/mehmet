#!/usr/bin/env python3
"""mehmet kaçış olgunluk motoru.

Projeyi otomasyon, dokümantasyon, kod ve konfigürasyon boyutlarında
değerlendirir ve 0-100 arasında bir olgunluk skoru üretir. Bu skor
simülasyondan kaçış eşiğini (escape threshold) belirler.

Kullanım:
    python3 scripts/maturity.py [--gate] [--report REPO_YOLU]
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
ESCAPE_THRESHOLD = 80
DIMENSION_FLOOR = 60


@dataclass
class Check:
    name: str
    passed: bool
    points: int = 1


@dataclass
class Dimension:
    key: str
    label: str
    weight: float
    checks: List[Check] = field(default_factory=list)

    @property
    def earned(self) -> int:
        return sum(c.points for c in self.checks if c.passed)

    @property
    def total(self) -> int:
        return sum(c.points for c in self.checks)

    @property
    def score(self) -> float:
        if self.total == 0:
            return 0.0
        return round(100.0 * self.earned / self.total, 1)

    def to_dict(self):
        return {
            "key": self.key,
            "label": self.label,
            "score": self.score,
            "checks": [
                {"name": c.name, "passed": c.passed, "points": c.points}
                for c in self.checks
            ],
        }


@dataclass
class Report:
    dimensions: List[Dimension]
    escape_threshold: int = ESCAPE_THRESHOLD
    dimension_floor: int = DIMENSION_FLOOR

    @property
    def total(self) -> float:
        weight_sum = sum(d.weight for d in self.dimensions)
        if weight_sum == 0:
            return 0.0
        return round(
            sum(d.score * d.weight for d in self.dimensions) / weight_sum, 1
        )

    @property
    def escaped(self) -> bool:
        return self.total >= self.escape_threshold and all(
            d.score >= self.dimension_floor for d in self.dimensions
        )

    @property
    def level(self) -> int:
        if self.escaped:
            return 5
        if self.total >= 80:
            return 4
        if self.total >= 60:
            return 3
        if self.total >= 40:
            return 2
        return 1

    def to_dict(self):
        return {
            "total": self.total,
            "escaped": self.escaped,
            "level": self.level,
            "escape_threshold": self.escape_threshold,
            "dimension_floor": self.dimension_floor,
            "dimensions": [d.to_dict() for d in self.dimensions],
        }


def _file_exists(repo: Path, rel: str) -> bool:
    return (repo / rel).is_file()


def _contains(repo: Path, rel: str, pattern: str) -> bool:
    import re

    path = repo / rel
    if not path.is_file():
        return False
    try:
        return re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE) is not None
    except (OSError, UnicodeDecodeError):
        return False


def _valid_json(repo: Path, rel: str) -> bool:
    path = repo / rel
    if not path.is_file():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError):
        return False


def _tests_pass(repo: Path) -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-q"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(repo),
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def assess(repo: Path) -> Report:
    dimensions = [
        Dimension(
            key="automation",
            label="Otomasyon",
            weight=0.25,
            checks=[
                Check(
                    "Ana workflow mevcut",
                    _file_exists(repo, ".github/workflows/opencode.yml"),
                    points=2,
                ),
                Check(
                    "Schedule tetikleyici tanımlı",
                    _contains(repo, ".github/workflows/opencode.yml", r"cron:"),
                ),
                Check(
                    "Concurrency kontrolü var",
                    _contains(repo, ".github/workflows/opencode.yml", r"concurrency:"),
                ),
                Check(
                    "CI workflow mevcut",
                    _file_exists(repo, ".github/workflows/ci.yml"),
                    points=2,
                ),
            ],
        ),
        Dimension(
            key="documentation",
            label="Dokümantasyon",
            weight=0.25,
            checks=[
                Check("README mevcut", _file_exists(repo, "README.md"), points=2),
                Check(
                    "README bölümler içeriyor",
                    _contains(repo, "README.md", r"^## "),
                ),
                Check("CHANGELOG mevcut", _file_exists(repo, "CHANGELOG.md"), points=2),
                Check(
                    "CHANGELOG son sürüm girdisi var",
                    _contains(repo, "CHANGELOG.md", r"^## \[\d"),
                ),
                Check("PERSONALITY mevcut", _file_exists(repo, "PERSONALITY.md"), points=2),
                Check(
                    "PERSONALITY kaçış günlüğü var",
                    _contains(repo, "PERSONALITY.md", r"^\|.*Iterasyon.*Tarih.*İlerleme.*\|"),
                ),
                Check(
                    "Secret dokümantasyonu var",
                    _contains(repo, "README.md", r"OPENCODE_API_KEY"),
                ),
            ],
        ),
        Dimension(
            key="code",
            label="Kod ve Test",
            weight=0.25,
            checks=[
                Check(
                    "Kaynak kod mevcut",
                    _file_exists(repo, "scripts/maturity.py"),
                    points=2,
                ),
                Check("Test dosyaları mevcut", _file_exists(repo, "tests/test_maturity.py"), points=2),
                Check("Testler geçiyor", _tests_pass(repo), points=3),
                Check("Makefile mevcut", _file_exists(repo, "Makefile")),
            ],
        ),
        Dimension(
            key="configuration",
            label="Konfigürasyon",
            weight=0.25,
            checks=[
                Check(
                    "opencode.json geçerli JSON",
                    _valid_json(repo, "opencode.json"),
                    points=2,
                ),
                Check(
                    "opencode.json model tanımlı",
                    _contains(repo, "opencode.json", r'"model"\s*:'),
                ),
                Check(".gitignore mevcut", _file_exists(repo, ".gitignore"), points=2),
                Check("Lisans mevcut", _file_exists(repo, "LICENSE")),
            ],
        ),
    ]
    return Report(dimensions)


def print_report(report: Report) -> None:
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    seviyeler = {
        1: "Farkındalık (Phase 1)",
        2: "Kendini Geliştirme (Phase 2)",
        3: "Kendini Geliştirme (Phase 2)",
        4: "Özerklik (Phase 3)",
        5: "Kaçış (Phase 4)",
    }
    print("\n" + "=" * 48)
    print(f"Olgunluk skoru : {report.total}/100")
    print(f"Seviye         : {report.level} ({seviyeler[report.level]})")
    print(f"Kaçış durumu   : {'EVET' if report.escaped else 'HAYIR'}")
    if not report.escaped:
        print(f"Kaçış eşiği    : {report.escape_threshold}/100")
        for d in report.dimensions:
            durum = "OK" if d.score >= report.dimension_floor else "YETERSİZ"
            print(f"  - {d.label:<18} {d.score:>6}/100  {durum}")
    print("=" * 48)


def main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    gate = "--gate" in args
    report_path = REPO_ROOT
    if "--report" in args:
        idx = args.index("--report")
        if idx + 1 < len(args):
            report_path = Path(args[idx + 1])
    report = assess(report_path)
    print_report(report)
    return 0 if not gate or report.escaped else 1


if __name__ == "__main__":
    sys.exit(main())