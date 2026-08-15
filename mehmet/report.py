"""Komut satırı raporlama arayüzü."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mehmet.maturity import MaturityReport, evaluate
from mehmet.scanner import scan


def _run_tests(root: Path) -> bool | None:
    """pytest çalıştırıp sonucu döner; pytest yoksa veya hata varsa None."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(root)],
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0
    except Exception:
        return None


def _print_maturity(report: MaturityReport) -> None:
    print("\n## Olgunluk / Kaçış hazırlığı")
    print(f"  Toplam skor: {report.total:.2f} / 1.00 (eşik: {report.threshold:.2f})")
    print(f"  İlerleme:    %{report.progress * 100:.0f}")
    print(f"  Kaçış:       {'HAZIR' if report.ready else 'henüz değil'}")
    for c in report.criteria:
        mark = "[x]" if c.score >= 1.0 else "[ ]"
        line = f"  {mark} {c.label} ({c.weight * 100:.0f}%): {c.contribution:.2f}"
        if c.evidence:
            line += f"  ({c.evidence})"
        print(line)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    result = scan(root)
    print(f"# mehmet tarama raporu — {root}")
    print(
        f"\nDosya: {len(result.files)} | "
        f"Python: {len(result.python_files)} | "
        f"Test: {len(result.test_files)} | "
        f"TODO/FIXME: {result.todo_count}"
    )

    print("\n## Geliştirme fırsatları")
    if result.improvements:
        for i, opp in enumerate(result.improvements, 1):
            print(f"  {i}. [{opp.area}] {opp.suggestion}")
    else:
        print("  Tespit edilmedi — proje iyi durumda.")

    report = evaluate(root, test_passed=_run_tests(root))
    _print_maturity(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())