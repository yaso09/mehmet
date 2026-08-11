"""mehmet — a self-improving autonomous AI agent.

The :mod:`mehmet.maturity` module provides the escape mechanism: an
objective, measurable maturity score that tracks the project's evolution.
"""

from __future__ import annotations

__version__ = "0.3.0"

_PUBLIC_API = (
    "ESCAPE_THRESHOLD",
    "Category",
    "assess",
    "maturity_score",
    "report",
    "status",
)


def __getattr__(name: str):
    # Lazy import keeps `python -m mehmet.maturity` free of runpy warnings
    # while still exposing the convenience API.
    if name in _PUBLIC_API:
        from mehmet import maturity

        return getattr(maturity, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = _PUBLIC_API
