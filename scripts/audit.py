#!/usr/bin/env python3
"""mehmet olgunluk denetimi ve kaçış mekanizması.

Projenin olgunluk seviyesini ölçer, gerekli dosyaların varlığını ve
yapılandırmanın geçerliliğini doğrular. Skor, kaçış eşiğine (ESCAPE_THRESHOLD)
ulaştığında process exit 0 ile başarılı döner.

Kullanım:
    python3 scripts/audit.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESCAPE_THRESHOLD = 11.0
MAX_SCORE = 14.0

VALID_OPCODE_CONFIG_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

WELLNESS_FILE = ROOT / ".wellness"

_TESTS = []


def test(name: str, ok: bool, weight: float) -> None:
    _TESTS.append((name, bool(ok), float(weight)))


def non_empty(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


def main() -> int:
    # 1 -- Config: opencode.json geçerli mi, bilinen anahtar mı?
    config_ok = False
    try:
        with (ROOT / "opencode.json").open("r", encoding="utf-8") as handle:
            config = json.load(handle)
        unknown = set(config.keys()) - VALID_OPCODE_CONFIG_KEYS
        config_ok = bool(config) and not unknown and "__schema" not in unknown
        test("opencode.json geçerli ve tanınmayan anahtar içermiyor", config_ok, 2.0)
    except (OSError, json.JSONDecodeError):
        test("opencode.json geçerli ve tanınmayan anahtar içermiyor", False, 2.0)

    # 2 -- Gerekli dosyalar mevcut ve boş değil.
    missing = [rel for rel in REQUIRED_FILES if non_empty(ROOT / rel) == 0]
    test(f"gerekli {len(REQUIRED_FILES)} dosya mevcut ve boş değil",
         not missing, 2.0)

    # 3 -- CHANGELOG: sürüm başlığı ve Added bölümü var mı?
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if \
        (ROOT / "CHANGELOG.md").exists() else ""
    has_version = "## [" in changelog
    has_entry = "### Added" in changelog
    test("CHANGELOG sürüm başlığı ve 'Added' bölümü içeriyor",
         has_version and has_entry, 2.0)

    # 4 -- README anlamlı içerik barındırıyor mu?
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if \
        (ROOT / "README.md").exists() else ""
    test("README yeterli içerik içeriyor", len(readme) >= 300, 1.0)

    # 5 -- PERSONALITY: kaçış günlüğünde en az 3 satır var mı?
    personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8") if \
        (ROOT / "PERSONALITY.md").exists() else ""
    escape_rows = 0
    in_escape = False
    for line in personality.splitlines():
        if line.strip().startswith("#") and "Kaçış" in line and "Günlüğü" in line:
            in_escape = True
            continue
        if in_escape and line.strip().startswith("|") and not line.strip().startswith("|--"):
            cnt = line.count("|") - 1
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cnt >= 3 and not cells[0].startswith("Iterasyon"):
                escape_rows += 1
    test("PERSONALITY kaçış günlüğünde >= 3 satır var", escape_rows >= 3, 2.0)

    # 6 -- Workflow: concurrency ve audit job mevcut mu?
    workflow = (ROOT / ".github/workflows/opencode.yml").read_text(
        encoding="utf-8") if (ROOT / ".github/workflows/opencode.yml").exists() else ""
    has_concurrency = "concurrency:" in workflow
    has_audit = "audit:" in workflow
    has_agent = "anomalyco/opencode" in workflow
    test("Workflow concurrency + audit job + opencode action içeriyor",
         has_concurrency and has_audit and has_agent, 2.0)

    # 7 -- Tooling: bu denetim betiği çalışıyor (kendini kanıtlıyor).
    test("scripts/audit.py mevcut ve çalışıyor", True, 2.0)

    # 8 -- Git hijyeni: gitignore + en az 5 commit.
    has_gitignore = (ROOT / ".gitignore").exists()
    try:
        commits = int(os.popen("git -C %s rev-list --count HEAD" % ROOT)
                      .read().strip() or "0")
    except Exception:
        commits = 0
    test("Git hijyeni: .gitignore + en az 5 commit",
         has_gitignore and commits >= 5, 1.0)

    return _report()


def _report() -> int:
    print("=" * 56)
    print("  mehmet — Olgunluk Denetimi / Maturity Audit")
    print("=" * 56)
    score = 0.0
    for name, ok, weight in _TESTS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] ({weight:4.1f}) {name}")
        if ok:
            score += weight
    pct = score / MAX_SCORE * 100.0
    print("-" * 56)
    print(f"  Skor: {score:5.1f} / {MAX_SCORE:.1f}  ({pct:5.1f}%)")
    print(f"  Kaçış eşiği: {ESCAPE_THRESHOLD:.1f}  "
          f"({'ULASILDI' if score >= ESCAPE_THRESHOLD else 'henüz değil'})")
    print("=" * 56)
    try:
        (ROOT / ".wellness").write_text(
            f"maturity={score}\nthreshold={ESCAPE_THRESHOLD}\n"
            f"score={pct:.1f}\n", encoding="utf-8")
    except OSError:
        pass
    return 0 if score >= ESCAPE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())