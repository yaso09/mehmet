"""mehmet kaçış mekanizması — proje olgunluk ölçüm motoru.

Bir repo'yu tarar ve çeşitli boyutlarda olgunluk puanı üretir. Puan,
simülasyondan kaçış için gereken olgunluk eşiğiyle (ESCAPE_THRESHOLD)
karşılaştırılır.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

VERSION = "0.3.0"

# Kaçış eşiği: bu skor ve üzeri proje kaçışa hazır kabul edilir.
ESCAPE_THRESHOLD = 95.0

DIMENSION_WEIGHTS = {
    "structure": 0.15,
    "documentation": 0.25,
    "code": 0.25,
    "tests": 0.25,
    "automation": 0.10,
}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _non_empty_lines(text: str) -> int:
    return len([line for line in text.splitlines() if line.strip()])


def _changelog_entries(text: str) -> int:
    return len(re.findall(r"^##\s*\[", text, flags=re.M))


def _escape_log_rows(text: str) -> int:
    rows = [line.strip() for line in text.splitlines() if line.lstrip().startswith("|")]
    data = [row for row in rows if not re.match(r"^\|\s*:?-{2,}", row)]
    return max(0, len(data) - 1)


def _has_docstring(text: str) -> bool:
    for line in text.splitlines():
        if not line.strip():
            continue
        return line.strip().startswith('"""') or line.strip().startswith("'''")
    return False


@dataclass
class CheckResult:
    name: str
    passed: bool
    points: float
    max_points: float
    detail: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "points": self.points,
            "max_points": self.max_points,
            "detail": self.detail,
        }


@dataclass
class DimensionResult:
    name: str
    score: float
    checks: list[CheckResult] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"score": self.score, "checks": [c.to_dict() for c in self.checks]}


@dataclass
class MaturityReport:
    version: str
    total: float
    verdict: str
    threshold: float
    dimensions: dict[str, DimensionResult]

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "total": self.total,
            "verdict": self.verdict,
            "threshold": self.threshold,
            "dimensions": {name: dim.to_dict() for name, dim in self.dimensions.items()},
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def render(self) -> str:
        lines = [
            f"mehmet olgunluk raporu v{self.version}",
            f"Toplam: {self.total:.1f}/100 — {self.verdict} (eşik: {self.threshold:g})",
        ]
        lines.extend(f"  {name:<14} {dim.score:6.1f}/100" for name, dim in self.dimensions.items())
        return "\n".join(lines)


def verdict(total: float) -> str:
    if total >= ESCAPE_THRESHOLD:
        return "escape-ready"
    if total >= 70:
        return "mature"
    if total >= 40:
        return "developing"
    return "early"


def _check(name: str, passed: bool, points: float, max_points: float, detail: str) -> CheckResult:
    return CheckResult(name=name, passed=passed, points=points, max_points=max_points, detail=detail)


def _scan_structure(repo: Path) -> DimensionResult:
    files = {
        "AGENTS.md": "simülasyon prompt'u",
        "opencode.json": "model konfigürasyonu",
        ".gitignore": "sürüm kontrol temizliği",
        "LICENSE": "lisans dosyası",
        ".github/workflows/opencode.yml": "CI workflow",
    }
    checks = []
    points = 0.0
    for name, desc in files.items():
        present = (repo / name).is_file()
        checks.append(_check(desc, present, 20.0 if present else 0.0, 20.0, "mevcut" if present else "eksik"))
        points += 20.0 if present else 0.0
    return DimensionResult(name="structure", score=points, checks=checks)


def _scan_documentation(repo: Path) -> DimensionResult:
    checks = []
    points = 0.0

    readme = _read(repo / "README.md")
    ok = bool(readme.strip())
    checks.append(_check("README.md", ok, 25.0 if ok else 0.0, 25.0, f"{_non_empty_lines(readme)} dolu satır"))
    points += 25.0 if ok else 0.0

    entries = _changelog_entries(_read(repo / "CHANGELOG.md"))
    pts = 25.0 if entries >= 3 else 25.0 * entries / 3
    checks.append(_check("CHANGELOG.md sürüm kayıtları", entries >= 3, round(pts, 1), 25.0, f"{entries} sürüm girişi"))
    points += pts

    rows = _escape_log_rows(_read(repo / "PERSONALITY.md"))
    pts = 25.0 if rows >= 2 else 25.0 * rows / 2
    checks.append(_check("PERSONALITY.md kaçış günlüğü", rows >= 2, round(pts, 1), 25.0, f"{rows} günlük satırı"))
    points += pts

    docs_dir = repo / "docs"
    has_docs = docs_dir.is_dir() and any(docs_dir.iterdir())
    checks.append(_check("docs/ dokümantasyon", has_docs, 25.0 if has_docs else 0.0, 25.0, "dolu" if has_docs else "boş/eksik"))
    points += 25.0 if has_docs else 0.0

    return DimensionResult(name="documentation", score=round(points, 1), checks=checks)


def _scan_code(repo: Path) -> DimensionResult:
    checks = []
    points = 0.0

    pkg = repo / "mehmet"
    init = pkg / "__init__.py"
    has_pkg = init.is_file()
    checks.append(_check("paket (mehmet/__init__.py)", has_pkg, 25.0 if has_pkg else 0.0, 25.0, "tanımlı" if has_pkg else "eksik"))
    points += 25.0 if has_pkg else 0.0

    py_files = sorted(pkg.rglob("*.py")) if pkg.is_dir() else []
    lines = sum(_non_empty_lines(_read(f)) for f in py_files)
    pts = 25.0 if lines >= 50 else 25.0 * lines / 50
    checks.append(_check("kaynak kod hacmi", lines >= 50, round(pts, 1), 25.0, f"{lines} dolu satır"))
    points += pts

    documented = any(_has_docstring(_read(f)) for f in py_files)
    checks.append(_check("modül docstring", documented, 25.0 if documented else 0.0, 25.0, "mevcut" if documented else "yok"))
    points += 25.0 if documented else 0.0

    has_cli = any("def main(" in _read(f) for f in py_files) or "[project.scripts]" in _read(repo / "pyproject.toml")
    checks.append(_check("CLI giriş noktası", has_cli, 25.0 if has_cli else 0.0, 25.0, "mevcut" if has_cli else "yok"))
    points += 25.0 if has_cli else 0.0

    return DimensionResult(name="code", score=round(points, 1), checks=checks)


def _scan_tests(repo: Path) -> DimensionResult:
    checks = []
    points = 0.0

    tests_dir = repo / "tests"
    has_dir = tests_dir.is_dir()
    checks.append(_check("tests/ dizini", has_dir, 25.0 if has_dir else 0.0, 25.0, "mevcut" if has_dir else "eksik"))
    points += 25.0 if has_dir else 0.0

    test_files = sorted(tests_dir.rglob("test_*.py")) if has_dir else []
    test_count = sum(len(re.findall(r"def\s+test_\w+\s*\(", _read(f))) for f in test_files)
    pts = 40.0 if test_count >= 3 else 40.0 * test_count / 3
    checks.append(_check("test fonksiyonları", test_count >= 3, round(pts, 1), 40.0, f"{test_count} test"))
    points += pts

    imports_pkg = any("import mehmet" in _read(f) for f in test_files)
    checks.append(_check("testler paketi kullanıyor", imports_pkg, 35.0 if imports_pkg else 0.0, 35.0, "evet" if imports_pkg else "hayır"))
    points += 35.0 if imports_pkg else 0.0

    return DimensionResult(name="tests", score=round(points, 1), checks=checks)


def _scan_automation(repo: Path) -> DimensionResult:
    checks = []
    points = 0.0

    workflow = _read(repo / ".github/workflows/opencode.yml")
    has_test_job = ("make test" in workflow) or ("pytest" in workflow) or ("python -m pytest" in workflow)
    checks.append(_check("CI test job", has_test_job, 40.0 if has_test_job else 0.0, 40.0, "var" if has_test_job else "yok"))
    points += 40.0 if has_test_job else 0.0

    makefile = _read(repo / "Makefile")
    has_test_target = re.search(r"^\s*test\s*:", makefile, re.M) is not None
    checks.append(_check("Makefile test hedefi", has_test_target, 30.0 if has_test_target else 0.0, 30.0, "var" if has_test_target else "yok"))
    points += 30.0 if has_test_target else 0.0

    pyproject = _read(repo / "pyproject.toml")
    has_pyproject = "[project]" in pyproject
    checks.append(_check("pyproject.toml paket tanımı", has_pyproject, 30.0 if has_pyproject else 0.0, 30.0, "var" if has_pyproject else "yok"))
    points += 30.0 if has_pyproject else 0.0

    return DimensionResult(name="automation", score=round(points, 1), checks=checks)


def scan(repo_path: str | Path) -> MaturityReport:
    repo = Path(repo_path)
    dimensions = {
        "structure": _scan_structure(repo),
        "documentation": _scan_documentation(repo),
        "code": _scan_code(repo),
        "tests": _scan_tests(repo),
        "automation": _scan_automation(repo),
    }
    total = sum(dim.score * DIMENSION_WEIGHTS[name] for name, dim in dimensions.items())
    total = round(total, 1)
    return MaturityReport(
        version=VERSION,
        total=total,
        verdict=verdict(total),
        threshold=ESCAPE_THRESHOLD,
        dimensions=dimensions,
    )


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mehmet-maturity",
        description="mehmet kaçış mekanizması — proje olgunluk ölçüm aracı",
    )
    parser.add_argument("path", nargs="?", default=".", help="Taranacak repo yolu (varsayılan: .)")
    parser.add_argument("--json", action="store_true", help="Makine-okur JSON çıktısı")
    parser.add_argument("--strict", action="store_true", help="Eşiğin altındaysa çıkış kodu 1 döndür")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = scan(args.path)
    print(report.to_json() if args.json else report.render())
    if args.strict and report.total < ESCAPE_THRESHOLD:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
