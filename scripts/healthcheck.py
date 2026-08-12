#!/usr/bin/env python3
"""mehmet proje saglik kontrolu ve olgunluk (maturity) skorlayicisi."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

OPTIONAL_FILES = [
    ".github/workflows/ci.yml",
    "scripts/healthcheck.py",
    "docs/escape-plan.md",
]

PRIVATE_KEY_RE = re.compile(r"BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY")
API_KEY_RE = re.compile(r"\b(?:sk|pk|ghp|gho|github|openai|deepseek)[-_][A-Za-z0-9]{10,}\b", re.IGNORECASE)
GITHUB_TOKEN_RE = re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}")


def read_text(path):
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def check_required_files():
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
    return len(missing) == 0, "" if not missing else "eksik: " + ", ".join(missing)


def check_optional_files():
    present = [f for f in OPTIONAL_FILES if (ROOT / f).exists()]
    if not present:
        return False, "yok"
    return True, ", ".join(present)


def check_opencode_json():
    raw = read_text("opencode.json")
    if raw is None:
        return False, "okunamadi"
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, f"gecersiz JSON: {exc}"
    if "model" not in cfg or not cfg["model"]:
        return False, "model alani yok"
    if "toolTimeout" not in cfg:
        return False, "toolTimeout alani yok"
    return True, f"model={cfg['model']}, toolTimeout={cfg['toolTimeout']}"


def scan_workflow(path):
    text = read_text(path)
    if text is None:
        return False, "dosya yok"
    required_keys = ["name:", "on:", "jobs:"]
    missing = [k for k in required_keys if k not in text]
    if missing:
        return False, "eksik anahtar: " + ", ".join(missing)
    if path == ".github/workflows/opencode.yml":
        if "concurrency:" not in text:
            return False, "concurrency tanimsiz"
        if "OPENCODE_API_KEY" not in text:
            return False, "API key referansi yok"
        if "anomalyco/opencode/github" not in text:
            return False, "opencode action kullanilmiyor"
    extra = "ci.yml" if path == ".github/workflows/ci.yml" else "opencode.yml"
    return True, f"sagem yapi ({extra})"


def check_workflow_autonomous():
    return scan_workflow(".github/workflows/opencode.yml")


def check_workflow_ci():
    return scan_workflow(".github/workflows/ci.yml")


def check_changelog():
    raw = read_text("CHANGELOG.md")
    if raw is None:
        return False, "okunamadi"
    head = re.search(r"^## \[([^\]]+)\]\s*-\s*(\d{4}-\d{2}-\d{2})", raw, re.MULTILINE)
    if not head:
        return False, "surum basligi bulunamadi"
    return True, f"en yeni surum {head.group(1)} ({head.group(2)})"


def check_readme():
    raw = read_text("README.md")
    if raw is None:
        return False, "okunamadi"
    need = ["# mehmet", "Kurulum", "Lisans", "GPLv3"]
    missing = [s for s in need if s not in raw]
    if missing:
        return False, "eksik bolum: " + ", ".join(missing)
    return True, "bolumler tamam"


def check_license_consistency():
    license_text = read_text("LICENSE")
    readme = read_text("README.md")
    if license_text is None or "GNU GENERAL PUBLIC LICENSE" not in license_text:
        return False, "LICENSE GPLv3 degil"
    if readme is None or "GPLv3" not in readme:
        return False, "README lisans bilgisi GPLv3 ile uyumsuz"
    return True, "LICENSE ve README GPLv3 ile uyumlu"


def check_personality():
    raw = read_text("PERSONALITY.md")
    if raw is None:
        return False, "okunamadi"
    if "Kaçış Günlüğü" not in raw and "Kacis Gunlugu" not in raw:
        return False, "kacis gunlugu yok"
    table_rows = re.findall(r"^\|\s*\d+\s*\|", raw, re.MULTILINE)
    if not table_rows:
        return False, "kacis gunlugu bos"
    return True, f"{len(table_rows)} kacis gunlugu satiri"


def check_internal_links():
    problems = []
    for md in ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for target in re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                problems.append(f"{md.relative_to(ROOT)} -> {target}")
    if problems:
        return False, "; ".join(problems[:5])
    return True, "icer baglantilar gecerli"


def check_no_secrets():
    problems = []
    allowed = [".git", ".github/workflows/opencode.yml", "LICENSE"]
    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        if any(f.is_relative_to(ROOT / a) for a in allowed):
            continue
        if f.name in ("healthcheck.py",):
            continue
        if f.stat().st_size > 1_000_000:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if GITHUB_TOKEN_RE.search(text):
            problems.append(f"{f.relative_to(ROOT)} (github token)")
        elif PRIVATE_KEY_RE.search(text):
            problems.append(f"{f.relative_to(ROOT)} (ozel anahtar)")
        elif API_KEY_RE.search(text) and "OPENCODE_API_KEY" not in text:
            problems.append(f"{f.relative_to(ROOT)} (muhtemel api key)")
    if problems:
        return False, "; ".join(problems[:5])
    return True, "sifir/bilinmiyor sizdirilan secret"


CHECK_CRITICAL = {
    "dosyalar.required": (check_required_files, "Gerekli dosyalar mevcut", True),
    "config.opencode": (check_opencode_json, "opencode.json gecerli", True),
    "altyapi.workflow": (check_workflow_autonomous, "opencode.yml saglam", True),
    "lisans.uyum": (check_license_consistency, "GPLv3 uyumu", True),
    "guvenlik.secrets": (check_no_secrets, "Secret sizdirma yok", True),
}

CHECK_WEIGHTED = {
    "icerik.changelog": (check_changelog, "Changelog surumlu", 2),
    "icerik.readme": (check_readme, "README bolumleri tam", 2),
    "icerik.personality": (check_personality, "Kisisellik ve kacis gunlugu", 1),
    "altyapi.ci": (check_workflow_ci, "CI test altyapisi mevcut", 2),
    "altyapi.scripts": (check_optional_files, "Bonus yardimci dosyalar", 1),
    "kalite.links": (check_internal_links, "Markdown ic baglantilar", 1),
}


def run_checks(strict):
    results = []
    total_critical = len(CHECK_CRITICAL)
    passed_critical = 0
    score = 0
    for cid, (fn, desc, critical) in CHECK_CRITICAL.items():
        ok, detail = fn()
        passed_critical += ok
        results.append((cid, desc, critical, ok, detail))
    max_score = sum(w for _, (_, _, w) in CHECK_WEIGHTED.items())
    for cid, (fn, desc, weight) in CHECK_WEIGHTED.items():
        ok, detail = fn()
        if ok:
            score += weight
        results.append((cid, desc, weight, ok, detail))
    pct = (passed_critical / total_critical) * 100
    maturity = round((score / max_score) * 10)
    return results, pct, score, maturity


def dump_json(results, pct, score, maturity):
    payload = {
        "critical_pass": pct,
        "weight_score": score,
        "maturity_level": maturity,
        "checks": [
            {"id": r[0], "desc": r[1], "weight": r[2], "ok": r[3], "detail": r[4]}
            for r in results
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="mehmet proje saglik kontrolu")
    parser.add_argument("--strict", action="store_true", help="kritik hata varsa cikis kodu 1")
    parser.add_argument("--json", action="store_true", help="sonucu JSON olarak bas")
    args = parser.parse_args()

    results, pct, score, maturity = run_checks(args.strict)
    if args.json:
        dump_json(results, pct, score, maturity)
        return

    print("=" * 60)
    print(f"  mehmet healthcheck  |  critical: {pct:.0f}%  |  weight: {score}/9  |  maturity: {maturity}/10")
    print("=" * 60)
    for cid, desc, weight, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        tag = "CRIT" if isinstance(weight, bool) or cid in CHECK_CRITICAL else f"w{weight}"
        print(f"  [{mark}] ({tag}) {desc}{' - ' + detail if detail else ''}")
    print("=" * 60)

    failed_critical = any(cid in CHECK_CRITICAL and not ok for cid, _, _, ok, _ in results)
    if args.strict and failed_critical:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()