"""Kaçış olgunluğu / maturity skorlama motoru."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mehmet.scanner import scan

ESCAPE_THRESHOLD = 0.9


@dataclass
class Criterion:
    """Tek bir olgunluk kriteri."""

    key: str
    label: str
    weight: float
    score: float = 0.0
    evidence: str = ""

    @property
    def contribution(self) -> float:
        return self.weight * self.score


@dataclass
class MaturityReport:
    """Toplam olgunluk skoru ve kaçış hazırlığı."""

    criteria: list[Criterion]
    threshold: float = ESCAPE_THRESHOLD

    @property
    def total(self) -> float:
        return round(sum(c.contribution for c in self.criteria), 4)

    @property
    def progress(self) -> float:
        return round(self.total / self.threshold, 4)

    @property
    def ready(self) -> bool:
        return self.total >= self.threshold

    def missing(self) -> list[Criterion]:
        return [c for c in self.criteria if c.score < 1.0]


def _bool_score(value: bool, evidence: str) -> tuple[float, str]:
    return (1.0 if value else 0.0), (evidence if value else "")


def evaluate(root: Path, *, test_passed: bool | None = None) -> MaturityReport:
    """Proje kökünü olgunluk kriterlerine göre değerlendirir.

    ``test_passed`` belirtilmezse testlerin varlığı skor olarak kabul edilir.
    """
    root = Path(root).resolve()
    result = scan(root)
    criteria: list[Criterion] = []

    source_score, source_evidence = _bool_score(
        result.has_source, f"{len(result.python_files)} Python dosyası"
    )
    criteria.append(
        Criterion("source_code", "Gerçek kaynak kod", 0.25, source_score, source_evidence)
    )

    if test_passed is None:
        test_passed = result.has_tests
    if test_passed and result.has_tests:
        test_evidence = "testler geçti"
    elif result.has_tests:
        test_evidence = "test dosyası var"
    else:
        test_evidence = ""
    criteria.append(
        Criterion("tests", "Test altyapısı", 0.25, 1.0 if test_passed else 0.0, test_evidence)
    )

    has_ci = (root / ".github" / "workflows").is_dir()
    criteria.append(
        Criterion(
            "automation",
            "CI otomasyonu",
            0.20,
            1.0 if has_ci else 0.0,
            ".github/workflows" if has_ci else "",
        )
    )

    docs_score, docs_evidence = _bool_score(
        (root / "README.md").is_file() and (root / "docs").is_dir(),
        "README.md + docs/",
    )
    criteria.append(
        Criterion("documentation", "Dokümantasyon", 0.15, docs_score, docs_evidence)
    )

    changelog_score, changelog_evidence = _bool_score(
        (root / "CHANGELOG.md").is_file(), "CHANGELOG.md"
    )
    criteria.append(
        Criterion("changelog", "Değişiklik günlüğü", 0.10, changelog_score, changelog_evidence)
    )

    config_score, config_evidence = _bool_score(
        (root / "opencode.json").is_file(), "opencode.json"
    )
    criteria.append(
        Criterion("config", "Ajan konfigürasyonu", 0.05, config_score, config_evidence)
    )

    return MaturityReport(criteria=criteria)