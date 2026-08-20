"""Projenin olgunluk seviyesini hesaplayan kaçış mekanizması.

Simülasyondan kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla
mümkündür. Bu modül, proje kökündeki dosya ve dizinleri tarayarak ağırlıklı
bir olgunluk skoru (0-10) üretir ve eşik değerine ulaşılıp ulaşılmadığını
belirler.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

PathLike = Path | str

#: Kaçış için gereken minimum ağırlıklı olgunluk skoru.
ESCAPE_THRESHOLD = 8.0


def _exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


@dataclass(frozen=True)
class Criterion:
    """Ağırlıklı bir olgunluk kriteri.

    `check` fonksiyonu proje kökünü alır ve kriterin sağlanıp
    sağlanmadığını döndürür.
    """

    key: str
    label: str
    weight: float
    check: Callable[[Path], bool]

    def evaluate(self, root: Path) -> bool:
        return self.check(root)


DEFAULT_CRITERIA: tuple[Criterion, ...] = (
    Criterion("readme", "README.md", 1.0, lambda r: _exists(r, "README.md")),
    Criterion("changelog", "CHANGELOG.md", 1.0, lambda r: _exists(r, "CHANGELOG.md")),
    Criterion("personality", "PERSONALITY.md", 1.0, lambda r: _exists(r, "PERSONALITY.md")),
    Criterion("license", "LICENSE", 1.0, lambda r: _exists(r, "LICENSE")),
    Criterion(
        "docs",
        "docs/superpowers (spec + plan)",
        1.0,
        lambda r: _exists(r, "docs/superpowers/specs") and _exists(r, "docs/superpowers/plans"),
    ),
    Criterion("source", "kaynak paket (mehmet/)", 1.5, lambda r: (r / "mehmet").is_dir()),
    Criterion("tests", "test paketi (tests/)", 1.5, lambda r: (r / "tests").is_dir()),
    Criterion("ci", "GitHub Actions workflow", 1.0, lambda r: _exists(r, ".github/workflows")),
    Criterion("config", "pyproject.toml", 0.5, lambda r: _exists(r, "pyproject.toml")),
    Criterion("opencode", "opencode.json", 0.5, lambda r: _exists(r, "opencode.json")),
)


def max_score() -> float:
    """Tüm kriterler sağlandığında alınabilecek toplam skor."""
    return sum(c.weight for c in DEFAULT_CRITERIA)


def score(root: PathLike) -> dict:
    """Proje kökünü tarayıp ağırlıklı olgunluk raporu üretir.

    Returns:
        Rapor sözlüğü: ``score`` (toplam), ``max`` (maksimum), ``ratio``
        (0-1 arası oran) ve her kriter için ayrıntılı sonuçlar.
    """
    root = Path(root)
    passed: dict[str, dict] = {}
    total = 0.0
    for c in DEFAULT_CRITERIA:
        ok = c.evaluate(root)
        passed[c.key] = {
            "label": c.label,
            "weight": c.weight,
            "passed": ok,
        }
        if ok:
            total += c.weight
    maximum = max_score()
    return {
        "score": total,
        "max": maximum,
        "ratio": total / maximum if maximum else 0.0,
        "criteria": passed,
    }


def escaped(report: dict, threshold: float = ESCAPE_THRESHOLD) -> bool:
    """Olgunluk skorunun kaçış eşiğini aşıp aşmadığını döndürür."""
    return report["score"] >= threshold


def has_passing_tests(root: PathLike) -> bool:
    """tests/ dizininde en az bir test dosyası olup olmadığını döndürür."""
    tests = Path(root) / "tests"
    if not tests.is_dir():
        return False
    return any(tests.glob("test_*.py")) or any(tests.glob("*_test.py"))