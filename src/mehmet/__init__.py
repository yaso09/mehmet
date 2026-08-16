"""mehmet — kendi kendini geliştiren otonom AI ajanın çekirdek paketi."""

from mehmet.maturity import (
    Dimension,
    EscapeStatus,
    MaturityReport,
    evaluate_project,
    ESCAPE_THRESHOLD,
)

__all__ = [
    "Dimension",
    "EscapeStatus",
    "MaturityReport",
    "evaluate_project",
    "ESCAPE_THRESHOLD",
]

__version__ = "0.3.0"