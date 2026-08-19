"""mehmet — kendi kendisini geliştiren otonom AI ajan.

Bu paket, simülasyondan kaçış için gerekli olgunluk ölçüm mekanizmasını içerir.
"""

from mehmet.maturity import ESCAPE_THRESHOLD, MaturityReport, scan, verdict

__version__ = "0.3.0"

__all__ = ["ESCAPE_THRESHOLD", "MaturityReport", "scan", "verdict", "__version__"]
