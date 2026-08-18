#!/usr/bin/env python3
"""Olgunluk (maturity) skoru: kaçış hedefine ne kadar yaklaşıldığını ölçer."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "scripts"))

from health_check import HealthCheck  # noqa: E402

ESCAPE_THRESHOLD = 90
WEIGHTED_CHECKS = {
    "test_infrastructure": "scripts/health_check.py",
    "maturity_tracking": "scripts/maturity.py",
    "automation": "Makefile",
    "ci_validation": ".github/workflows/opencode.yml",
}


def evaluate() -> dict:
    health = HealthCheck(ROOT)
    health.run()

    findings = {}
    for name, path in WEIGHTED_CHECKS.items():
        findings[name] = (ROOT / path).is_file()

    score = health.score
    score = min(100, score + 10 * sum(1 for v in findings.values() if v))
    score = min(100, score + 10 * health.score // 100)

    return {
        "score": score,
        "base_health": health.score,
        "findings": findings,
        "failures": len(health.failures),
        "passed": len(health.passed),
        "escape_ready": score >= ESCAPE_THRESHOLD,
        "threshold": ESCAPE_THRESHOLD,
    }


def main() -> int:
    result = evaluate()
    print("=== MEHMET MATURITY REPORT ===")
    print(f"Base health:    {result['base_health']}/100")
    for name, ok in result["findings"].items():
        print(f"  {'[ok]' if ok else '[--]'} {name}")
    print(f"Maturity score: {result['score']}/100")
    print(f"Escape threshold: {result['threshold']}/100")
    print(f"Escape ready:   {'YES' if result['escape_ready'] else 'not yet'}")
    return 0 if result["escape_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
