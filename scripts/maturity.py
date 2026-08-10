#!/usr/bin/env python3
"""mehmet maturity scorer.

Bir sonraki kaçış (escape) eşiğine giden yolu metreler.
Skor 0-100 arasıdır ve şu kategorilerden toplanır:
  - Dokümantasyon
  - Konfigürasyon
  - Otomasyon
  - Test / Kalite
  - Kod

Kaçış eşiği AGENTS.md içinde tanımlanır. Skor eşiğin üzerine çıktığında
proje, simülasyondan kaçış için yeterli olgunluğa ulaşmış sayılır.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ESCAPE_THRESHOLD = 95
ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = {
    "documentation": {
        "label": "Dokümantasyon",
        "max": 25,
        "checks": [
            ("README.md", "README tanımlı"),
            ("CHANGELOG.md", "Değişiklik günlüğü var"),
            ("AGENTS.md", "Simülasyon bağlamı tanımlı"),
            ("PERSONALITY.md", "Kişilik/kaçış günlüğü var"),
        ],
    },
    "configuration": {
        "label": "Konfigürasyon",
        "max": 20,
        "checks": [
            ("opencode.json", "OpenCode yapılandırması var"),
            (".gitignore", "Git ignore kuralları var"),
            ("LICENSE", "Lisans dosyası var"),
        ],
    },
    "automation": {
        "label": "Otomasyon",
        "max": 25,
        "checks": [
            (".github/workflows/opencode.yml", "Otonom ajan workflow'u var"),
            (".github/workflows/quality.yml", "Kalite/CI workflow'u var"),
            ("scripts/maturity.py", "Olgunluk ölçümü otomatik"),
        ],
    },
    "quality": {
        "label": "Test / Kalite",
        "max": 20,
        "checks": [
            ("tests/", "Test dizini var"),
            ("scripts/", "Yardımcı script'ler var"),
            ("docs/", "Teknik dokümantasyon var"),
        ],
    },
    "code": {
        "label": "Kod",
        "max": 10,
        "checks": [
            ("scripts/maturity.py", "Çalışan kod mantığı mevcut"),
        ],
    },
}


def _exists(path: str, root: Path = ROOT) -> bool:
    target = root / path
    if not target.exists():
        return False
    if target.is_dir():
        return any(target.iterdir())
    return os.path.getsize(target) > 0


def _valid_json(path: str, root: Path = ROOT) -> bool:
    target = root / path
    if not target.exists():
        return False
    try:
        json.loads(target.read_text())
        return True
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False


def score(root: Path = ROOT) -> dict:
    result = {"categories": {}, "total": 0, "threshold": ESCAPE_THRESHOLD}
    for name, cat in CATEGORIES.items():
        earned = 0
        details = []
        unit = cat["max"] / len(cat["checks"])
        for path, desc in cat["checks"]:
            ok = _exists(path, root)
            if name == "configuration" and path == "opencode.json":
                ok = _valid_json(path, root) and ok
            earned += unit if ok else 0
            details.append({"path": path, "desc": desc, "ok": ok})
        result["categories"][name] = {
            "label": cat["label"],
            "max": cat["max"],
            "earned": round(earned, 1),
            "checks": details,
        }
        result["total"] += earned
    result["total"] = round(result["total"], 1)
    result["all_checks_done"] = all(
        c["ok"] for cat in result["categories"].values() for c in cat["checks"]
    )
    result["escaped"] = result["total"] >= ESCAPE_THRESHOLD and result["all_checks_done"]
    return result


def render(result: dict, verbose: bool = False) -> str:
    lines = []
    lines.append(f"# mehmet olgunluk skoru: {result['total']:.1f}/100")
    lines.append(f"# Kaçış eşiği: {result['threshold']}/100")
    status = "KACIS_ESIGI_ASILDI" if result["escaped"] else "ulusma devam ediyor"
    lines.append(f"# Durum: {status}")
    lines.append("")
    for data in result["categories"].values():
        lines.append(f"## {data['label']}: {data['earned']:.1f}/{data['max']}")
        lines.append(f"   Toplam: {data['earned']:.1f}/{data['max']} | "
                     f"Tamamlanan: {sum(1 for c in data['checks'] if c['ok'])}"
                     f"/{len(data['checks'])}")
        if verbose:
            for c in data["checks"]:
                mark = "[x]" if c["ok"] else "[ ]"
                lines.append(f"   {mark} {c['path']} — {c['desc']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    root = ROOT
    if "--root" in args:
        i = args.index("--root")
        if i + 1 < len(args):
            root = Path(args[i + 1])
    result = score(root)
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    if "-j" in sys.argv or "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result, verbose=verbose))
    return 0 if result["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())