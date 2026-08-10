#!/usr/bin/env python3
"""mehmet proje doğrulayıcısı.

Proje yapısını, sürüm günlüğünü ve güvenlik saflığını kontrol eder.
Her çalıştırmada sonuçları yazdırır; herhangi bir kontrol başarısızsa
çıkış kodu 1 döner (CI gate).
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MARKER_PATTERNS = [re.compile(r"\bTODO\b"), re.compile(r"\bFIXME\b")]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"(?:OPENCODE_API_KEY|ANTHROPIC_API_KEY|OPENAI_API_KEY|REPLICATE_API"
               r"_TOKEN|GITHUB_TOKEN|BOT_PASSWORD)\s*=\s*[^\s]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
VERSION_HEADER = re.compile(r"^## \[\d+\.\d+\.\d+\]")


def required_file(rel: str, min_size: int = 0):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    if p.stat().st_size <= min_size:
        return False, f"boş dosya: {rel}"
    return True, f"mevcut: {rel} ({p.stat().st_size} byte)"


def valid_json(rel: str):
    p = ROOT / rel
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, f"eksik dosya: {rel}"
    except ValueError as exc:
        return False, f"geçersiz JSON {rel}: {exc}"
    return True, f"geçerli JSON: {rel}"


def contains(rel: str, needle: str):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    return needle in p.read_text(encoding="utf-8"), f"aranan {needle!r} içinde {rel}"


def regex_in(rel: str, pattern: str, flags: int = re.MULTILINE):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    return bool(re.search(pattern, p.read_text(encoding="utf-8"), flags)), f"regex /{pattern}/ içinde {rel}"


def parse_iso(s: str):
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def changelog_recent(rel: str = "CHANGELOG.md", max_age_days: int = 60):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ["):
            m = re.search(r"-\s*(\d{4}-\d{2}-\d{2})", line)
            if m:
                d = parse_iso(m.group(1))
                if d and (date.today() - d).days <= max_age_days:
                    return True, f"en güncel sürüm: {m.group(1)}"
    return False, f"{rel} içinde son {max_age_days} gün içinde güncel sürüm yok"


def escape_log_recent(rel: str = "PERSONALITY.md", max_age_days: int = 45):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    meetings = [d for d in (parse_iso(m) for m in
                            re.findall(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|",
                                       p.read_text(encoding="utf-8"))) if d]
    if not meetings:
        return False, "kaçış günlüğünde tarihli satır yok"
    newest = max(meetings)
    if (date.today() - newest).days > max_age_days:
        return False, f"kaçış günlüğü güncel değil (son: {newest.isoformat()})"
    return True, f"kaçış günlüğü güncel (son: {newest.isoformat()})"


def maturity_report_recent(rel: str = "MATURITY.md", max_age_days: int = 30):
    p = ROOT / rel
    if not p.is_file():
        return False, f"eksik dosya: {rel}"
    m = re.search(r"Üretim tarihi:\s*(\d{4}-\d{2}-\d{2})", p.read_text(encoding="utf-8"))
    if not m:
        return False, f"{rel} içinde Üretim tarihi bulunamadı"
    d = parse_iso(m.group(1))
    if d is None or (date.today() - d).days > max_age_days:
        return False, f"olgunluk raporu güncel değil (üretim: {m.group(1)})"
    return True, f"olgunluk raporu güncel (üretim: {m.group(1)})"


def scan_free_of(patterns, label, root: str = "."):
    hits = []
    base = (ROOT / root) if root != "." else ROOT

    def walk(directory: Path):
        for p in sorted(directory.iterdir()):
            if p.name.startswith("."):
                continue
            if p.is_dir():
                walk(p)
            elif p.suffix in {"", ".md", ".py", ".yml", ".yaml", ".json", ".txt", ".sh", ".toml", ".cfg", ".log"}:
                try:
                    for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                        for rx in patterns:
                            if rx.search(line):
                                hits.append(f"{p.relative_to(ROOT)}:{i}")
                                break
                except OSError:
                    continue

    walk(base)
    if hits:
        return False, f"{label} bulundu: " + ", ".join(sorted(set(hits)))
    return True, f"{label} yok"


CHECKS = [
    ("AGENTS.md mevcut", lambda: required_file("AGENTS.md", 10)),
    ("README.md mevcut", lambda: required_file("README.md", 10)),
    ("LICENSE mevcut", lambda: required_file("LICENSE", 1000)),
    ("opencode.json geçerli JSON", lambda: valid_json("opencode.json")),
    ("CHANGELOG.md mevcut", lambda: required_file("CHANGELOG.md", 10)),
    ("PERSONALITY.md mevcut", lambda: required_file("PERSONALITY.md", 10)),
    ("CHANGELOG sürüm başlıkları var", lambda: regex_in("CHANGELOG.md", r"^## \[\d+\.\d+\.\d+\]")),
    ("CHANGELOG güncel", lambda: changelog_recent("CHANGELOG.md")),
    ("Kaçış günlüğü güncel", lambda: escape_log_recent("PERSONALITY.md")),
    (".github/workflows/opencode.yml mevcut", lambda: required_file(".github/workflows/opencode.yml", 50)),
    (".github/workflows/ci.yml mevcut", lambda: required_file(".github/workflows/ci.yml", 50)),
    ("Makefile mevcut", lambda: required_file("Makefile", 10)),
    ("Doğrulama betikleri mevcut", lambda: required_file("scripts/validate.py", 50)),
    ("Olgunluk raporu güncel", lambda: maturity_report_recent("MATURITY.md")),
    ("Test dosyaları mevcut", lambda: (any(ROOT.joinpath("tests").glob("test_*.py")), "tests/test_*.py mevcut")),
    ("README Kurulum bölümü var", lambda: contains("README.md", "## Kurulum")),
    ("Script ve testlerde TODO/FIXME yok", lambda: scan_free_of(MARKER_PATTERNS, "TODO/FIXME", "tests")),
    ("Kaynaklarda sır yok", lambda: scan_free_of(SECRET_PATTERNS, "sır")),
]


def run():
    return [(label, check()) for label, check in CHECKS]


def main():
    results = run()
    fails = 0
    width = max(len(label) for label, _ in results) + 2
    for label, (ok, msg) in results:
        status = "PASS" if ok else "FAIL"
        fails += 0 if ok else 1
        print(f"[{status}] {label:<{width}} {msg}")
    print(f"\nSonuç: {len(results) - fails}/{len(results)} kontrol geçti")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()