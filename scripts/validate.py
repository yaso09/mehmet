#!/usr/bin/env python3
"""Proje sağlık doğrulayıcısı ve olgunluk (maturity) hesaplayıcısı.

Sıfır-bağımlılık (yalnızca Python standart kütüphanesi) bir araçtır. Projenin
AGENTS.md kurallarına uyup uymadığını kontrol eder ve kaçış mekanizması için
olgunluk skoru üretir.

Kullanım:
    python3 scripts/validate.py            # tüm kontrolleri çalıştır
    python3 scripts/validate.py --maturity # yalnızca olgunluk skorunu yazdır
    python3 scripts/validate.py --json     # makine-okunur çıktı
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

# opencode config şemasındaki geçerli üst-düzey anahtarlar
# (https://opencode.ai/config.json'den alınmıştır).
VALID_CONFIG_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills", "references",
    "reference", "watcher", "snapshot", "plugin", "share", "autoshare",
    "autoupdate", "disabled_providers", "enabled_providers", "model",
    "small_model", "default_agent", "subagent_depth", "username", "mode",
    "agent", "provider", "mcp", "formatter", "lsp", "instructions", "layout",
    "permission", "tools", "attachment", "enterprise", "tool_output",
    "compaction", "experimental",
}

VERSION_HEADER_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\] - (?P<day>\d{4}-\d{2}-\d{2})$",
    re.MULTILINE,
)
WORKFLOW_MARKERS = [
    "name: mehmet",
    "cron:",
    "jobs:",
    "autonomous:",
    "comment:",
]


class Checker:
    def __init__(self) -> None:
        self.results: list[tuple[bool, str]] = []

    def ok(self, msg: str) -> None:
        self.results.append((True, msg))

    def fail(self, msg: str) -> None:
        self.results.append((False, msg))

    def check(self, cond: bool, ok_msg: str, fail_msg: str) -> None:
        self.ok(ok_msg) if cond else self.fail(fail_msg)

    def report(self) -> None:
        for passed, msg in self.results:
            status = "OK " if passed else "FAIL"
            print(f"[{status}] {msg}")
        passed_count = sum(1 for passed, _ in self.results if passed)
        print(f"\n{passed_count}/{len(self.results)} kontrol geçti.")


def check_required_files(checker: Checker) -> None:
    for rel in REQUIRED_FILES:
        checker.check(
            (ROOT / rel).is_file(),
            f"Gerekli dosya mevcut: {rel}",
            f"Gerekli dosya eksik: {rel}",
        )


def check_opencode_config(checker: Checker) -> None:
    path = ROOT / "opencode.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        checker.fail(f"opencode.json geçersiz: {exc}")
        return
    if not isinstance(data, dict):
        checker.fail("opencode.json bir nesne (object) olmalı.")
        return
    checker.ok("opencode.json geçerli JSON.")

    unknown = sorted(set(data) - VALID_CONFIG_KEYS)
    checker.check(
        not unknown,
        "opencode.json'da bilinmeyen anahtar yok.",
        f"opencode.json'da bilinmeyen anahtarlar: {', '.join(unknown)}",
    )
    checker.check(
        data.get("$schema") == "https://opencode.ai/config.json",
        "opencode.json $schema doğru.",
        "opencode.json $schema yanlış veya eksik.",
    )
    checker.check(
        isinstance(data.get("model"), str) and "/" in data["model"],
        f"opencode.json model tanımlı: {data.get('model')}",
        "opencode.json model eksik veya geçersiz.",
    )


def check_license(checker: Checker) -> None:
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").is_file() else ""
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    checker.check(
        "GNU GENERAL PUBLIC LICENSE" in lic and "Version 3" in lic,
        "LICENSE GPLv3.",
        "LICENSE GPLv3 değil.",
    )
    checker.check(
        "GPLv3" in readme,
        "README.md lisans bilgisi GPLv3 ile uyumlu.",
        "README.md lisans bilgisi GPLv3 ile uyumlu değil.",
    )


def check_changelog(checker: Checker) -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        checker.fail("CHANGELOG.md eksik.")
        return
    content = path.read_text(encoding="utf-8")
    headers = VERSION_HEADER_RE.findall(content)
    checker.check(
        len(headers) >= 1,
        "CHANGELOG.md'de en az bir sürüm girişi var.",
        "CHANGELOG.md'de sürüm girişi yok.",
    )
    versions = [v for v, _ in headers]
    checker.check(
        len(versions) == len(set(versions)),
        "CHANGELOG.md'de yinelenen sürüm yok.",
        "CHANGELOG.md'de yinelenen sürüm var.",
    )
    todays = date.today().isoformat()
    latest_date = headers[0][1] if headers else ""
    checker.check(
        latest_date <= todays,
        f"En son sürüm tarihi ({latest_date}) bugünden eski.",
        f"En son sürüm tarihi ({latest_date}) gelecekte.",
    )
    for _, day in headers:
        checker.check(
            _is_valid_date(day),
            f"CHANGELOG tarih biçimi geçerli: {day}",
            f"CHANGELOG tarih biçimi geçersiz: {day}",
        )


def check_personality(checker: Checker) -> None:
    path = ROOT / "PERSONALITY.md"
    if not path.is_file():
        checker.fail("PERSONALITY.md eksik.")
        return
    content = path.read_text(encoding="utf-8")
    checker.check(
        "Kaçış Günlüğü" in content and "Escape Log" in content,
        "PERSONALITY.md kaçış günlüğü tablosunu içeriyor.",
        "PERSONALITY.md kaçış günlüğü tablosunu içermiyor.",
    )
    checker.check(
        "Phase 4: Escape" in content or "Escape" in content,
        "PERSONALITY.md evrim aşamaları tanımlı.",
        "PERSONALITY.md evrim aşamaları tanımsız.",
    )
    rows = []
    for line in content.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|", line)
        if m:
            rows.append(int(m.group(1)))
    checker.check(
        len(rows) >= 1,
        f"Kaçış günlüğünde {len(rows)} iterasyon kaydı var.",
        "Kaçış günlüğünde iterasyon kaydı yok.",
    )
    last = 0
    for it in rows:
        if it <= last:
            checker.fail("Kaçış günlüğü iterasyon numaraları artan sırada değil.")
            return
        last = it


def check_workflow(checker: Checker) -> None:
    path = ROOT / ".github/workflows/opencode.yml"
    if not path.is_file():
        checker.fail("opencode.yml eksik.")
        return
    content = path.read_text(encoding="utf-8")
    for marker in WORKFLOW_MARKERS:
        checker.check(
            marker in content,
            f"Workflow {marker!r} içeriyor.",
            f"Workflow {marker!r} içermiyor.",
        )


def check_validate_self(checker: Checker) -> None:
    path = ROOT / "scripts/validate.py"
    checker.check(
        path.is_file(),
        "scripts/validate.py mevcut.",
        "scripts/validate.py eksik.",
    )


def _is_valid_date(day: str) -> bool:
    try:
        datetime.strptime(day, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def maturity_score(checker: Checker) -> tuple[int, int]:
    """Olgunluk skorunu verir: (geçen, toplam)."""
    passed = sum(1 for ok_, _ in checker.results if ok_)
    total = len(checker.results)
    return passed, total


def run_all() -> Checker:
    checker = Checker()
    check_required_files(checker)
    check_opencode_config(checker)
    check_license(checker)
    check_changelog(checker)
    check_personality(checker)
    check_workflow(checker)
    check_validate_self(checker)
    return checker


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet projesi sağlık doğrulayıcısı")
    parser.add_argument("--maturity", action="store_true", help="yalnızca olgunluk skorunu yazdır")
    parser.add_argument("--json", action="store_true", help="makine-okunur JSON çıktısı")
    args = parser.parse_args()

    checker = run_all()
    passed, total = maturity_score(checker)

    if args.json:
        payload = {
            "passed": passed,
            "total": total,
            "checks": [
                {"ok": ok_, "message": msg} for ok_, msg in checker.results
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif args.maturity:
        print(f"maturity: {passed}/{total}")
    else:
        checker.report()
        pct = (passed / total * 100.0) if total else 100.0
        print(f"olgunluk: %{pct:.1f} ({passed}/{total})")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())