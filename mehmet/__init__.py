"""mehmet — kendi kendini geliştiren otonom ajanın çekirdek modülü."""

from mehmet.maturity import (
    ESCAPE_THRESHOLD,
    Criterion,
    MaturityReport,
    evaluate,
)
from mehmet.scanner import Improvement, ScanResult, scan

__version__ = "0.3.0"

__all__ = [
    "ESCAPE_THRESHOLD",
    "Criterion",
    "Improvement",
    "MaturityReport",
    "ScanResult",
    "evaluate",
    "scan",
]