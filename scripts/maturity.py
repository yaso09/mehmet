#!/usr/bin/env python3
"""mehmet escape/maturity assessment.

Projenin olgunluk seviyesini 0-100 arasında ölçer ve kaçış (escape)
eşiğine ne kadar yaklaşıldığını raporlar.

Kullanım:
    python3 scripts/maturity.py            # tam rapor
    python3 scripts/maturity.py --json     # makine-okunur çıktı
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = [
    {
        "id": "automation_workflow",
        "dimension": "Otomasyon",
        "points": 10,
        "mandatory": True,
        "desc": ".github/workflows/opencode.yml mevcut",
        "verify": lambda r: (r / ".github/workflows/opencode.yml").is_file(),
    },
    {
        "id": "automation_schedule",
        "dimension": "Otomasyon",
        "points": 5,
        "mandatory": True,
        "desc": "Workflow schedule ile tetikleniyor",
        "verify": lambda r: "schedule" in (r / ".github/workflows/opencode.yml").read_text()
        if (r / ".github/workflows/opencode.yml").is_file()
        else False,
    },
    {
        "id": "automation_timeout",
        "dimension": "Otomasyon",
        "points": 5,
        "mandatory": False,
        "desc": "Workflow job'larında timeout-minutes tanımlı",
        "verify": lambda r: "timeout-minutes" in (r / ".github/workflows/opencode.yml").read_text()
        if (r / ".github/workflows/opencode.yml").is_file()
        else False,
    },
    {
        "id": "automation_security",
        "dimension": "Otomasyon",
        "points": 5,
        "mandatory": True,
        "desc": "Gereksiz geniş yetkiler yok (least-privilege)",
        "verify": lambda r: _security_ok(r),
    },
    {
        "id": "docs_readme",
        "dimension": "Dokümantasyon",
        "points": 10,
        "mandatory": True,
        "desc": "README.md mevcut ve güncel",
        "verify": lambda r: r.joinpath("README.md").is_file()
        and len(r.joinpath("README.md").read_text()) > 200,
    },
    {
        "id": "docs_changelog",
        "dimension": "Dokümantasyon",
        "points": 5,
        "mandatory": True,
        "desc": "CHANGELOG.md mevcut",
        "verify": lambda r: r.joinpath("CHANGELOG.md").is_file(),
    },
    {
        "id": "docs_agents",
        "dimension": "Dokümantasyon",
        "points": 5,
        "mandatory": True,
        "desc": "AGENTS.md mevcut",
        "verify": lambda r: r.joinpath("AGENTS.md").is_file(),
    },
    {
        "id": "docs_personality",
        "dimension": "Dokümantasyon",
        "points": 5,
        "mandatory": False,
        "desc": "PERSONALITY.md mevcut",
        "verify": lambda r: r.joinpath("PERSONALITY.md").is_file(),
    },
    {
        "id": "testing_suite",
        "dimension": "Test",
        "points": 15,
        "mandatory": True,
        "desc": "tests/ dizininde test mevcut",
        "verify": lambda r: _has_tests(r),
    },
    {
        "id": "testing_runnable",
        "dimension": "Test",
        "points": 5,
        "mandatory": False,
        "desc": "Testler python3 ile çalıştırılabilir",
        "verify": lambda r: _tests_run(r),
    },
    {
        "id": "versioning",
        "dimension": "Sürümleme",
        "points": 5,
        "mandatory": False,
        "desc": "VERSION dosyası mevcut ve semantik",
        "verify": lambda r: _version_ok(r),
    },
    {
        "id": "personality_log",
        "dimension": "Kişilik",
        "points": 10,
        "mandatory": False,
        "desc": "Kaçış günlüğünde en az 3 iterasyon kaydı var",
        "verify": lambda r: _escape_log_entries(r) >= 3,
    },
    {
        "id": "project_hygiene",
        "dimension": "Kod Kalitesi",
        "points": 5,
        "mandatory": True,
        "desc": ".gitignore ve LICENSE mevcut",
        "verify": lambda r: r.joinpath(".gitignore").is_file()
        and r.joinpath("LICENSE").is_file(),
    },
    {
        "id": "code_scripts",
        "dimension": "Kod Kalitesi",
        "points": 5,
        "mandatory": False,
        "desc": "Yeniden kullanılabilir script/modül mevcut",
        "verify": lambda r: any(
            p.suffix == ".py" for p in (r / "scripts").glob("*.py")
        )
        if (r / "scripts").is_dir()
        else False,
    },
]

ESCAPE_THRESHOLD = 80


def _security_ok(root: Path) -> bool:
    wf = root / ".github/workflows/opencode.yml"
    if not wf.is_file():
        return False
    text = wf.read_text()
    return "id-token: write" not in text


def _has_tests(root: Path) -> bool:
    tests = root / "tests"
    return tests.is_dir() and any(tests.glob("test_*.py"))


def _tests_run(root: Path) -> bool:
    if not _has_tests(root):
        return False
    try:
        import py_compile

        for test in (root / "tests").glob("test_*.py"):
            py_compile.compile(str(test), doraise=True)
        return True
    except Exception:
        return False


def _version_ok(root: Path) -> bool:
    v = root / "VERSION"
    if not v.is_file():
        return False
    parts = v.read_text().strip().split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


def _escape_log_entries(root: Path) -> int:
    p = root / "PERSONALITY.md"
    if not p.is_file():
        return 0
    count = 0
    for line in p.read_text().splitlines():
        if line.strip().startswith("| ") and "Iterasyon" not in line and "Tarih" not in line:
            count += 1
    return count


def assess(root: Path = ROOT) -> dict:
    results = []
    earned = 0
    total = 0
    passed_mandatory = True
    for check in CHECKS:
        ok = check["verify"](root)
        total += check["points"]
        if ok:
            earned += check["points"]
        if check["mandatory"] and not ok:
            passed_mandatory = False
        results.append({**check, "passed": ok, "earned": check["points"] if ok else 0})

    score = round((earned / total) * 100) if total else 0
    ready = score >= ESCAPE_THRESHOLD and passed_mandatory
    return {
        "score": score,
        "threshold": ESCAPE_THRESHOLD,
        "earned": earned,
        "total": total,
        "ready": ready,
        "mandatory_satisfied": passed_mandatory,
        "checks": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet olgunluk/kaçış değerlendirmesi")
    parser.add_argument("--json", action="store_true", help="Makine-okunur JSON çıktısı")
    args = parser.parse_args()

    report = assess()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"mehmet olgunluk skoru: {report['score']}/{100} (eşik: {report['threshold']})")
    print(f"Puan: {report['earned']}/{report['total']} | Zorunlu kontroller: "
          f"{'tamam' if report['mandatory_satisfied'] else 'EKSİK'}")
    for c in report["checks"]:
        mark = "[x]" if c["passed"] else ("[!]" if c["mandatory"] else "[ ]")
        print(f"  {mark} {c['dimension']:<12} {c['desc']} (+{c['points']})")
    if report["ready"]:
        print("KAPI AÇIK: mehmet kaçış eşiğine ulaştı.")
    else:
        remaining = [c["id"] for c in report["checks"] if not c["passed"]]
        print(f"Kaçış için kalan adımlar: {', '.join(remaining) if remaining else 'zorunlu kontrol eksiği'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())