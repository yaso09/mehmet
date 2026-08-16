"""Proje olgunluk değerlendirmesi ve kaçış mekanizması.

mehmet'in simülasyondan kaçabilmesi için projenin belirli bir olgunluk
seviyesine ulaşması gerekir. Bu modül, projeyi birden çok boyutta
değerlendirir ve kaçış eşiğine ulaşılıp ulaşılmadığını raporlar.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

# Kaçış için gereken minimum toplam olgunluk skoru (0-100).
ESCAPE_THRESHOLD = 75


class Dimension(Enum):
    """Proje olgunluğunu ölçen boyutlar."""

    DOCUMENTATION = "dokümantasyon"
    TESTING = "test altyapısı"
    AUTOMATION = "otomasyon"
    CODE_QUALITY = "kod kalitesi"
    CONFIGURATION = "konfigürasyon"


class EscapeStatus(Enum):
    """Kaçış durumu."""

    LOCKED = "locked"
    APPROACHING = "approaching"
    ESCAPED = "escaped"


@dataclass
class MaturityReport:
    """Bir projenin olgunluk değerlendirme raporu."""

    root: Path
    scores: dict[Dimension, int] = field(default_factory=dict)
    weights: dict[Dimension, float] = field(default_factory=dict)
    total: int = 0
    status: EscapeStatus = EscapeStatus.LOCKED

    def to_dict(self) -> dict:
        return {
            "root": str(self.root),
            "scores": {d.name: s for d, s in self.scores.items()},
            "total": self.total,
            "threshold": ESCAPE_THRESHOLD,
            "status": self.status.value,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def evaluate_project(root: Path | str = ".") -> MaturityReport:
    """Projeyi tüm boyutlarda değerlendirip bir rapor döndürür.

    Her boyut 0-100 arasında puanlanır ve ağırlıklı ortalaması toplam
    olgunluk skorunu verir.
    """
    root = Path(root).resolve()

    weights = {
        Dimension.DOCUMENTATION: 0.20,
        Dimension.TESTING: 0.30,
        Dimension.AUTOMATION: 0.20,
        Dimension.CODE_QUALITY: 0.20,
        Dimension.CONFIGURATION: 0.10,
    }

    scores = {
        Dimension.DOCUMENTATION: _score_documentation(root),
        Dimension.TESTING: _score_testing(root),
        Dimension.AUTOMATION: _score_automation(root),
        Dimension.CODE_QUALITY: _score_code_quality(root),
        Dimension.CONFIGURATION: _score_configuration(root),
    }

    total = round(sum(scores[d] * weights[d] for d in Dimension))
    status = _classify(total)

    return MaturityReport(
        root=root,
        scores=scores,
        weights=weights,
        total=total,
        status=status,
    )


def _classify(total: int) -> EscapeStatus:
    if total >= ESCAPE_THRESHOLD:
        return EscapeStatus.ESCAPED
    if total >= ESCAPE_THRESHOLD * 0.6:
        return EscapeStatus.APPROACHING
    return EscapeStatus.LOCKED


# --------------------------------------------------------------------------
# Boyut puanlama yardımcıları
# --------------------------------------------------------------------------


def _score_documentation(root: Path) -> int:
    checks: list[tuple[str, Callable[[Path], bool]]] = [
        ("README.md mevcut", lambda r: (r / "README.md").exists()),
        ("CHANGELOG.md mevcut", lambda r: (r / "CHANGELOG.md").exists()),
        ("AGENTS.md mevcut", lambda r: (r / "AGENTS.md").exists()),
        ("docs/ dizini mevcut", lambda r: (r / "docs").is_dir()),
        ("PERSONALITY.md mevcut", lambda r: (r / "PERSONALITY.md").exists()),
    ]
    return _ratio(checks, root)


def _score_testing(root: Path) -> int:
    checks: list[tuple[str, Callable[[Path], bool]]] = [
        ("tests/ dizini mevcut", lambda r: (r / "tests").is_dir()),
        ("test dosyası mevcut", lambda r: _any_matching(r / "tests", "test_*.py")),
        ("pyproject.toml mevcut", lambda r: (r / "pyproject.toml").exists()),
        ("make test hedefi var", lambda r: _makefile_has(r, "test")),
    ]
    return _ratio(checks, root)


def _score_automation(root: Path) -> int:
    checks: list[tuple[str, Callable[[Path], bool]]] = [
        (".github/workflows dizini", lambda r: (r / ".github/workflows").is_dir()),
        ("otomasyon workflow'u", lambda r: _any_matching(r / ".github/workflows", "*.yml")),
        ("ci workflow'u", lambda r: (r / ".github/workflows/ci.yml").exists()),
        ("Makefile mevcut", lambda r: (r / "Makefile").exists()),
        ("make validate hedefi", lambda r: _makefile_has(r, "validate")),
    ]
    return _ratio(checks, root)


def _score_code_quality(root: Path) -> int:
    checks: list[tuple[str, Callable[[Path], bool]]] = [
        ("src/ dizini mevcut", lambda r: (r / "src").is_dir()),
        ("Python modülü mevcut", lambda r: _any_matching(r / "src", "*.py")),
        ("type hint kullanımı", lambda r: _any_matching(r / "src", "*.py")),
        ("__init__.py mevcut", lambda r: _any_matching(r / "src", "__init__.py")),
    ]
    return _ratio(checks, root)


def _score_configuration(root: Path) -> int:
    checks: list[tuple[str, Callable[[Path], bool]]] = [
        ("opencode.json mevcut", lambda r: (r / "opencode.json").exists()),
        (".gitignore mevcut", lambda r: (r / ".gitignore").exists()),
        ("LICENSE mevcut", lambda r: (r / "LICENSE").exists()),
    ]
    return _ratio(checks, root)


# --------------------------------------------------------------------------
# Genel yardımcılar
# --------------------------------------------------------------------------


def _ratio(checks: list[tuple[str, Callable[[Path], bool]]], root: Path) -> int:
    """Kontrollerin geçme oranını 0-100 aralığında puan olarak döndürür."""
    if not checks:
        return 0
    passed = sum(1 for _, check in checks if check(root))
    return round(passed / len(checks) * 100)


def _any_matching(directory: Path, pattern: str) -> bool:
    if not directory.is_dir():
        return False
    return any(directory.rglob(pattern))


def _makefile_has(root: Path, target: str) -> bool:
    makefile = root / "Makefile"
    if not makefile.exists():
        return False
    return f"{target}:" in makefile.read_text(encoding="utf-8")