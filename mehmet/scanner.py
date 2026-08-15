"""Proje tarama ve geliştirme fırsatı tespiti."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "venv",
}

TODO_PATTERNS = ("TODO", "FIXME", "XXX", "HACK")

TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}


@dataclass(frozen=True)
class Improvement:
    """Tespit edilen bir geliştirme fırsatı."""

    area: str
    suggestion: str


@dataclass
class ScanResult:
    """Bir projenin tarama sonucu."""

    root: Path
    files: list[Path] = field(default_factory=list)
    python_files: list[Path] = field(default_factory=list)
    test_files: list[Path] = field(default_factory=list)
    todo_count: int = 0
    improvements: list[Improvement] = field(default_factory=list)

    @property
    def has_tests(self) -> bool:
        return bool(self.test_files)

    @property
    def has_source(self) -> bool:
        return bool(self.python_files)

    def opportunities(self) -> list[Improvement]:
        return list(self.improvements)


def _walk(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        files.append(path)
    return files


def _count_todos(root: Path, files: list[Path]) -> int:
    total = 0
    for path in files:
        if path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        total += sum(text.count(marker) for marker in TODO_PATTERNS)
    return total


def scan(root: Path) -> ScanResult:
    """Projeyi tarar ve geliştirme fırsatlarını tespit eder."""
    root = Path(root).resolve()
    files = _walk(root)
    python_files = [f for f in files if f.suffix == ".py"]
    test_files = [f for f in python_files if "test" in f.name.lower()]
    result = ScanResult(
        root=root,
        files=files,
        python_files=python_files,
        test_files=test_files,
        todo_count=_count_todos(root, files),
    )

    if not result.has_source:
        result.improvements.append(
            Improvement("source_code", "Gerçek kaynak kod bulunmuyor; bir çekirdek paket oluştur.")
        )
    if not (root / "README.md").is_file():
        result.improvements.append(
            Improvement("documentation", "README.md eksik; oluştur ve güncel tut.")
        )
    if not (root / "CHANGELOG.md").is_file():
        result.improvements.append(
            Improvement("changelog", "CHANGELOG.md eksik; her değişikliği kaydet.")
        )
    if not (root / ".github" / "workflows").is_dir():
        result.improvements.append(
            Improvement("automation", "CI workflow eksik; testleri otomatik çalıştır.")
        )
    if not result.has_tests:
        result.improvements.append(
            Improvement("tests", "Test dosyası bulunmuyor; pytest testleri ekle.")
        )
    if result.todo_count:
        result.improvements.append(
            Improvement(
                "cleanup",
                f"{result.todo_count} TODO/FIXME işareti bulundu; çöz ya da belgele.",
            )
        )
    return result