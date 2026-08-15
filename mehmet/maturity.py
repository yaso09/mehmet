"""mehmet — mehmet projesinin olgunluk (maturity) denetleyicisi.

Simülasyondan kaçış için gereken olgunluk seviyesini ölçülebilir kriterlerle
hesaplar. MATURITY.md'deki framework'ü uygular.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "MATURITY.md",
    ".gitignore",
    "opencode.json",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]

DOCS = [
    "docs/superpowers/specs",
    "docs/superpowers/plans",
]


@dataclass
class Criterion:
    """Tek bir olgunluk kriterinin durumu."""

    name: str
    points: int
    passed: bool
    detail: str = ""

    @property
    def awarded(self) -> int:
        return self.points if self.passed else 0


@dataclass
class MaturityReport:
    """Olgunluk denetiminin sonucu."""

    criteria: list[Criterion] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(c.awarded for c in self.criteria)

    @property
    def max_score(self) -> int:
        return sum(c.points for c in self.criteria)

    def level(self) -> int:
        s = self.score
        if s >= 90:
            return 5
        if s >= 70:
            return 4
        if s >= 50:
            return 3
        if s >= 30:
            return 2
        return 1

    def level_name(self) -> str:
        return {1: "Farkındalık", 2: "Yapı", 3: "Doğrulama", 4: "Otonomi", 5: "Kaçış"}[self.level()]

    def can_escape(self) -> bool:
        return self.score >= 90

    def render(self) -> str:
        lines = [f"mehmet olgunluk raporu", f"Puan: {self.score}/{self.max_score}"]
        lines.append(f"Seviye: {self.level()} ({self.level_name()})")
        lines.append(f"Kaçış koşulu: {'SAĞLANDI' if self.can_escape() else 'sağlanmadı'}")
        lines.append("")
        for c in self.criteria:
            mark = "[x]" if c.passed else "[ ]"
            suffix = f" — {c.detail}" if c.detail else ""
            lines.append(f"{mark} ({c.awarded}/{c.points}) {c.name}{suffix}")
        return "\n".join(lines)


def _has_files(repo: str, files: list[str]) -> bool:
    return all(os.path.isfile(os.path.join(repo, f)) for f in files)


def _has_any_of(repo: str, globs: list[str]) -> bool:
    import glob

    return any(glob.glob(os.path.join(repo, g)) for g in globs)


def _contains(repo: str, path: str, needle: str) -> bool:
    try:
        with open(os.path.join(repo, path), encoding="utf-8") as fh:
            return needle in fh.read()
    except OSError:
        return False


def check(repo: str) -> MaturityReport:
    """Belirtilen repo kökü için olgunluk denetimi yapar."""
    report = MaturityReport()

    # --- 1. Yapı (20 puan) ---
    report.criteria.append(
        Criterion(
            "Gerekli dosyalar mevcut",
            10,
            _has_files(repo, REQUIRED_FILES),
            "eksik: " + ", ".join(f for f in REQUIRED_FILES if not os.path.isfile(os.path.join(repo, f))) or "tamam",
        )
    )
    report.criteria.append(
        Criterion(
            "Doküman tutarlılığı (lisans GPLv3, MATURITY referansı)",
            5,
            _contains(repo, "README.md", "GPLv3")
            and _contains(repo, "AGENTS.md", "PERSONALITY.md"),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            ".gitignore ve lisans dosyası mevcut",
            5,
            _has_files(repo, [".gitignore", "LICENSE"]),
            "",
        )
    )

    # --- 2. Otomasyon (25 puan) ---
    report.criteria.append(
        Criterion(
            "Ana workflow (opencode.yml) mevcut",
            10,
            os.path.isfile(os.path.join(repo, WORKFLOWS[0])),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "Doğrulama workflow'u (validate.yml) mevcut",
            10,
            os.path.isfile(os.path.join(repo, WORKFLOWS[1])),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "Schedule + workflow_dispatch tanımlı",
            5,
            _contains(repo, WORKFLOWS[0], "schedule")
            and _contains(repo, WORKFLOWS[0], "workflow_dispatch"),
            "",
        )
    )

    # --- 3. Test Altyapısı (25 puan) ---
    tests_ok = _has_any_of(repo, ["tests/**/test_*.py", "tests/test_*.py"])
    report.criteria.append(
        Criterion(
            "Otomatik testler mevcut (tests/)",
            15,
            tests_ok,
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "Test kritik modülü kapsıyor (maturity)",
            5,
            _has_any_of(repo, ["tests/**/*maturity*", "tests/**/*check*"]),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "Test komutu dokümante edilmiş",
            5,
            _contains(repo, "README.md", "pytest"),
            "",
        )
    )

    # --- 4. Dokümantasyon (20 puan) ---
    report.criteria.append(
        Criterion(
            "README kurulum/kullanım içeriyor",
            8,
            _contains(repo, "README.md", "Kurulum") and _contains(repo, "README.md", "pytest"),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "CHANGELOG mevcut ve sürüm içeriyor",
            6,
            _contains(repo, "CHANGELOG.md", "## ["),
            "",
        )
    )
    report.criteria.append(
        Criterion(
            "Tasarım/spec dokümanları mevcut",
            6,
            all(_has_any_of(repo, [g]) for g in DOCS),
            "",
        )
    )

    # --- 5. Otonomi (10 puan) ---
    report.criteria.append(
        Criterion(
            "Ajan kendi gelişimini ölçebiliyor (MATURITY.md + paket)",
            10,
            _contains(repo, "MATURITY.md", "python3 -m mehmet.maturity"),
            "",
        )
    )

    return report


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="mehmet olgunluk denetimi")
    parser.add_argument("--repo", default=".", help="Repo kök dizini")
    parser.add_argument("--json", action="store_true", help="JSON çıktı")
    args = parser.parse_args()

    report = check(args.repo)
    if args.json:
        import json

        print(
            json.dumps(
                {
                    "score": report.score,
                    "max": report.max_score,
                    "level": report.level(),
                    "level_name": report.level_name(),
                    "escape": report.can_escape(),
                },
                indent=2,
            )
        )
        return

    print(report.render())
    sys.exit(0 if report.can_escape() else 1)


if __name__ == "__main__":
    main()