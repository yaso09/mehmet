"""Proje olgunluk skoru: kaçış mekanizmasının ölçülebilir kısmı.

Skorlar oransaldır (binary değil); böylece her iterasyonda kaydedilen
ilerleme metrikte görünür ve kaçış eşiğine doğru anlamlı bir yol kalır.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ESCAPE_THRESHOLD = 80.0
MAX_SCORE = 100.0


def _proportional(value: int, target: int, points: float) -> float:
    return points * min(1.0, value / target) if target else 0.0


@dataclass(frozen=True)
class Category:
    name: str
    score: float
    max_score: float
    checks: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ratio(self) -> float:
        return self.score / self.max_score if self.max_score else 0.0


@dataclass(frozen=True)
class Report:
    total: float
    threshold: float
    escaped: bool
    categories: tuple[Category, ...]

    @property
    def remaining(self) -> float:
        return max(0.0, round(self.threshold - self.total, 1))


def _walk(path: Path) -> list[Path]:
    try:
        return [p for p in path.rglob("*") if p.is_file()]
    except OSError:
        return []


def _py_files(path: Path) -> list[Path]:
    return [p for p in _walk(path) if p.suffix == ".py" and "__pycache__" not in str(p)]


def _lines(files: list[Path]) -> int:
    total = 0
    for p in files:
        try:
            total += len(p.read_text(errors="ignore").splitlines())
        except OSError:
            pass
    return total


def _function_count(files: list[Path]) -> int:
    count = 0
    for p in files:
        for line in p.read_text(errors="ignore").splitlines():
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                count += 1
    return count


def score_code(path: Path) -> Category:
    checks = []
    score = 0.0
    max_score = 30.0
    package = path / "mehmet"
    source = _py_files(package)
    n_files = len(source)
    n_lines = _lines(source)
    n_syms = _function_count(source)

    pts = _proportional(n_files, 5, 10.0)
    score += pts
    checks.append(f"kaynak dosya ({n_files}/5)")

    pts = _proportional(n_lines, 400, 10.0)
    score += pts
    checks.append(f"kod satırı ({n_lines}/400)")

    pts = _proportional(n_syms, 12, 10.0)
    score += pts
    checks.append(f"fonksiyon/sınıf ({n_syms}/12)")

    if (package / "__init__.py").is_file():
        checks.append("paket yapısı")
    if (path / "pyproject.toml").is_file():
        checks.append("paketleme yapılandırması")
    return Category("kod", round(min(score, max_score), 1), max_score, tuple(checks))


def score_test(path: Path) -> Category:
    checks = []
    score = 0.0
    max_score = 25.0
    tests = [p for p in _py_files(path / "tests")]
    n_files = len(tests)
    n_tests = _function_count(tests)

    score += _proportional(n_files, 3, 10.0)
    checks.append(f"test dosyası ({n_files}/3)")

    score += _proportional(n_tests, 15, 10.0)
    checks.append(f"test fonksiyonu ({n_tests}/15)")

    configured = (path / "pyproject.toml").is_file() or (path / "pytest.ini").is_file()
    if configured:
        score += 5.0
        checks.append("test yapılandırması")
    return Category("test", round(min(score, max_score), 1), max_score, tuple(checks))


def score_docs(path: Path) -> Category:
    checks = []
    score = 0.0
    max_score = 20.0

    readme = path / "README.md"
    readme_lines = _lines([readme]) if readme.is_file() else 0
    score += _proportional(readme_lines, 30, 8.0)
    checks.append(f"README ({readme_lines}/30 satır)")

    changelog = path / "CHANGELOG.md"
    versions = 0
    if changelog.is_file():
        versions = sum(1 for line in changelog.read_text(errors="ignore").splitlines()
                       if line.startswith("## ["))
    score += _proportional(versions, 5, 6.0)
    checks.append(f"CHANGELOG sürümleri ({versions}/5)")

    if (path / "LICENSE").is_file():
        score += 3.0
        checks.append("LICENSE")

    for name, pts in (("AGENTS.md", 1.5), ("PERSONALITY.md", 1.5)):
        if (path / name).is_file():
            score += pts
            checks.append(name)
    return Category("dokumantasyon", round(min(score, max_score), 1), max_score, tuple(checks))


def score_automation(path: Path) -> Category:
    checks = []
    score = 0.0
    max_score = 15.0
    workflows = [p for p in _walk(path / ".github" / "workflows") if p.suffix == ".yml"]

    score += _proportional(len(workflows), 3, 6.0)
    checks.append(f"CI workflow ({len(workflows)}/3)")

    ci = path / ".github" / "workflows" / "ci.yml"
    if ci.is_file():
        content = ci.read_text(errors="ignore")
        if "pytest" in content and "ruff" in content:
            score += 4.0
            checks.append("CI lint + test")
        elif "pytest" in content:
            score += 2.0
            checks.append("CI test")

    if (path / ".gitignore").is_file():
        score += 3.0
        checks.append(".gitignore")

    if ci.is_file() and "mehmet" in ci.read_text(errors="ignore"):
        score += 2.0
        checks.append("olgunluk doğrulama işi")
    return Category("otomasyon", round(min(score, max_score), 1), max_score, tuple(checks))


def score_governance(path: Path) -> Category:
    checks = []
    score = 0.0
    max_score = 10.0
    changelog = path / "CHANGELOG.md"
    versions = 0
    if changelog.is_file():
        versions = sum(1 for line in changelog.read_text(errors="ignore").splitlines()
                       if line.startswith("## ["))
    score += _proportional(versions, 4, 6.0)
    checks.append(f"versionsal geçmiş ({versions}/4)")

    if (path / "AGENTS.md").is_file():
        score += 4.0
        checks.append("ajan yönergesi")
    return Category("yönetişim", round(min(score, max_score), 1), max_score, tuple(checks))


def assess(path: str | Path = ".") -> Report:
    root = Path(path).resolve()
    categories = (
        score_code(root),
        score_test(root),
        score_docs(root),
        score_automation(root),
        score_governance(root),
    )
    total = round(sum(c.score for c in categories), 1)
    return Report(total, ESCAPE_THRESHOLD, total >= ESCAPE_THRESHOLD, categories)
