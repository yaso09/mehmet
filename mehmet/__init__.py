"""mehmet — an autonomous, self-improving AI agent."""

from .escape import (
    CRITERIA,
    ESCAPE_THRESHOLD,
    Criterion,
    CriterionResult,
    EscapeReport,
    format_report,
    scan,
)

__all__ = [
    "CRITERIA",
    "ESCAPE_THRESHOLD",
    "Criterion",
    "CriterionResult",
    "EscapeReport",
    "format_report",
    "scan",
]

__version__ = "0.3.0"
