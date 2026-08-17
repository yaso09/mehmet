#!/usr/bin/env python3
"""Validation utilities for mehmet's core documents.

Checks that the repository stays consistent:

  * CHANGELOG.md has a valid Keep-a-Changelog style top entry with today's
    date and a version number that matches VERSION.
  * PERSONALITY.md's escape log has an entry for the current iteration.
  * README.md exists.

Exit codes:
    0  everything valid
    1  one or more validation errors
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = REPO_ROOT / "VERSION"
VERSION_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)\s*$")

CHANGELOG_VERSION_RE = re.compile(
    r"^## \[(?P<version>\d+\.\d+\.\d+)\] - (?P<date>\d{4}-\d{2}-\d{2})$"
)
CHANGELOG_SECTION_RE = re.compile(r"^### (Added|Changed|Deprecated|Removed|Fixed|Security)$")

ESCAPE_LOG_HEADER = "## Kaçış Günlüğü / Escape Log"
ESCAPE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")


def read_current_version() -> str | None:
    """Read the version from VERSION file, if it exists."""
    if not VERSION_FILE.exists():
        return None
    match = VERSION_RE.match(VERSION_FILE.read_text(encoding="utf-8"))
    return match.group(0).strip() if match else None


def validate_changelog(today: date | None = None) -> list[str]:
    """Validate CHANGELOG.md structure and the most recent entry."""
    today = today or date.today()
    changelog = REPO_ROOT / "CHANGELOG.md"
    errors: list[str] = []
    if not changelog.exists():
        return ["CHANGELOG.md bulunamadı"]
    lines = changelog.read_text(encoding="utf-8").splitlines()

    version_headers = [ln for ln in lines if CHANGELOG_VERSION_RE.match(ln)]
    if not version_headers:
        errors.append("CHANGELOG.md'de geçerli bir sürüm başlığı yok")
        return errors

    head = CHANGELOG_VERSION_RE.match(version_headers[0])
    assert head is not None
    head_version, head_date = head.group("version"), head.group("date")

    if head_date != today.isoformat():
        errors.append(
            f"En üstteki changelog girişinin tarihi {today.isoformat()} olmalı, "
            f"mevcut: {head_date}"
        )

    current_version = read_current_version()
    if current_version and head_version != current_version:
        errors.append(
            f"Changelog sürümü ({head_version}) VERSION dosyasıyla ({current_version}) uyuşmuyor"
        )

    header_index = lines.index(version_headers[0])
    body = lines[header_index + 1 :]
    has_section = any(CHANGELOG_SECTION_RE.match(ln) for ln in body)
    if not has_section:
        errors.append("En üstteki changelog girişinin altında '### Added' gibi bölüm yok")
    return errors


def validate_escape_log() -> list[str]:
    """Validate that PERSONALITY.md has at least one escape log entry."""
    personality = REPO_ROOT / "PERSONALITY.md"
    errors: list[str] = []
    if not personality.exists():
        return ["PERSONALITY.md bulunamadı"]
    lines = personality.read_text(encoding="utf-8").splitlines()
    in_log = False
    row_count = 0
    for line in lines:
        if line.strip() == ESCAPE_LOG_HEADER:
            in_log = True
            continue
        if in_log:
            if line.startswith("|") and ESCAPE_ROW_RE.match(line):
                row_count += 1
            elif line.startswith("#") or line.startswith("---"):
                break
    if not in_log:
        errors.append("PERSONALITY.md'de kaçış günlüğü bölümü yok")
    elif row_count == 0:
        errors.append("PERSONALITY.md kaçış günlüğünde hiç giriş yok")
    return errors


def validate_all(today: date | None = None) -> list[str]:
    """Run all validators and collect every error."""
    errors: list[str] = []
    if not (REPO_ROOT / "README.md").exists():
        errors.append("README.md bulunamadı")
    errors.extend(validate_changelog(today))
    errors.extend(validate_escape_log())
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="mehmet repo validation")
    parser.add_argument(
        "--today",
        default=date.today().isoformat(),
        help="Bugünün tarihi (YYYY-AA-GG), testlerde aşırı yüklemek için",
    )
    args = parser.parse_args()
    today = date.fromisoformat(args.today)
    errors = validate_all(today)

    if errors:
        for error in errors:
            print(f"[HATA] {error}", file=sys.stderr)
        return 1
    print("Tüm doğrulamalar başarılı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
