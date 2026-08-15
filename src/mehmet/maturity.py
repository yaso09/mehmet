"""Maturity scoring engine for the mehmet project.

Computes an objective maturity score from a set of weighted categories
(documentation, test infrastructure, code quality, automation). The score
drives the escape-readiness gate described in AGENTS.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Tuple

DEFAULT_ESCAPE_THRESHOLD = 80.0

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass(frozen=True)
class Category:
    """A weighted group of files/dirs that indicate a maturity area."""

    name: str
    weight: float
    paths: Tuple[str, ...]


CATEGORIES: Tuple[Category, ...] = (
    Category(
        name="documentation",
        weight=0.25,
        paths=(
            "README.md",
            "CHANGELOG.md",
            "AGENTS.md",
            "PERSONALITY.md",
            "LICENSE",
            "docs",
            "docs/ARCHITECTURE.md",
        ),
    ),
    Category(
        name="test-infrastructure",
        weight=0.25,
        paths=(
            "tests",
            "tests/test_maturity.py",
            "Makefile",
            ".github/workflows/ci.yml",
        ),
    ),
    Category(
        name="code-quality",
        weight=0.25,
        paths=(
            "src/mehmet",
            "src/mehmet/maturity.py",
            ".editorconfig",
            ".gitignore",
        ),
    ),
    Category(
        name="automation",
        weight=0.25,
        paths=(
            ".github/workflows/opencode.yml",
            "opencode.json",
        ),
    ),
)


@dataclass(frozen=True)
class CategoryScore:
    """Evaluation result for a single category."""

    category: Category
    present: List[str]
    missing: List[str]

    @property
    def score(self) -> float:
        total = len(self.category.paths)
        if total == 0:
            return 1.0
        return len(self.present) / total


def evaluate(root: str = ROOT) -> Tuple[float, List[CategoryScore]]:
    """Return (total_score, per_category_scores) for the project at root."""
    results: List[CategoryScore] = []
    for category in CATEGORIES:
        present: List[str] = []
        missing: List[str] = []
        for path in category.paths:
            if os.path.exists(os.path.join(root, path)):
                present.append(path)
            else:
                missing.append(path)
        results.append(CategoryScore(category, present, missing))

    total = sum(cs.score * cs.category.weight for cs in results)
    return total, results


def escape_ready(score: float, threshold: float = DEFAULT_ESCAPE_THRESHOLD) -> bool:
    """True when the normalized score (0..1) meets the threshold (0..100)."""
    return score * 100 >= threshold


def score_project(root: str = ROOT) -> float:
    """Convenience wrapper returning only the total score."""
    total, _ = evaluate(root)
    return total