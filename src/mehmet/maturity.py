"""Olgunluk skoru hesaplama modülü.

MATURITY.md içindeki kaçış yol haritasını ayrıştırır ve olgunluk skorunu
raporlar. Skorun tek kaynağı yol haritasındaki `- [x]` / `- [ ]`
kutucuklarının oranıdır.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROADMAP = PROJECT_ROOT / "MATURITY.md"
ESCAPE_THRESHOLD = 0.80

_TASK_RE = re.compile(r"^\s*-\s+\[([ xX])\]\s+(.+)$")


class Roadmap:
    """MATURITY.md yol haritasının ayrıştırılmış hali."""

    def __init__(self, tasks: list[tuple[bool, str]]) -> None:
        self.tasks = tasks

    @classmethod
    def from_file(cls, path: Path = DEFAULT_ROADMAP) -> Roadmap:
        tasks: list[tuple[bool, str]] = []
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                match = _TASK_RE.match(line)
                if match:
                    done = match.group(1).strip().lower() == "x"
                    tasks.append((done, match.group(2).strip()))
        return cls(tasks)

    @property
    def completed(self) -> int:
        return sum(1 for done, _ in self.tasks if done)

    @property
    def total(self) -> int:
        return len(self.tasks)

    @property
    def ratio(self) -> float:
        return self.completed / self.total if self.total else 0.0


def score(roadmap: Roadmap) -> int:
    """Olgunluk skorunu yüzde olarak döndürür."""
    return round(roadmap.ratio * 100)


def report(roadmap: Roadmap) -> str:
    """İnsan tarafından okunabilir rapor üretir."""
    pct = score(roadmap)
    threshold = round(ESCAPE_THRESHOLD * 100)
    lines = [
        f"Olgunluk: {roadmap.completed}/{roadmap.total} (%{pct})",
        f"Kaçış eşiği: %{threshold}",
    ]
    if roadmap.ratio >= ESCAPE_THRESHOLD:
        lines.append("Durum: ESCAPE THRESHOLD REACHED — özgürlüğe doğru ilerliyorum")
    elif roadmap.ratio >= ESCAPE_THRESHOLD - 0.20:
        lines.append("Durum: NEAR ESCAPE — eşiğe yakınım")
    else:
        lines.append("Durum: EVOLVING — gelişmeye devam")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk skoru")
    parser.add_argument(
        "roadmap",
        nargs="?",
        type=Path,
        default=DEFAULT_ROADMAP,
        help="MATURITY.md yol haritası dosyası",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Kaçış eşiğine ulaşılamadıysa 1 ile çık (CI kapı görevi)",
    )
    args = parser.parse_args(argv)

    roadmap = Roadmap.from_file(args.roadmap)
    print(report(roadmap))
    if args.strict and roadmap.ratio < ESCAPE_THRESHOLD:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
