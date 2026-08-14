#!/usr/bin/env python3
"""mehmet proje sağlık doğrulayıcısı ve olgunluk (maturity) skoru hesaplayıcısı.

Kaçış hedefinin ölçülebilir hali: bu betik her iterasyonda projeyi tarar,
eksikleri raporlar ve 0-100 arası bir olgunluk skoru üretir. Skor 90 ve
üzerine ulaştığında proje "kaçışa hazır" kabul edilir.

Kullanım:
    python3 scripts/validate.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# https://opencode.ai/config.json (Config) şemasındaki geçerli üst seviye anahtarlar
ALLOWED_CONFIG_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

REQUIRED_FILES = [
    "AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md",
    "LICENSE", ".gitignore", "opencode.json",
    ".github/workflows/opencode.yml",
]

ESCAPE_THRESHOLD = 90


class Report:
    def __init__(self):
        self.passed = []
        self.failed = []

    def ok(self, name, weight):
        self.passed.append((name, weight))
        print(f"  [OK]   {name}")

    def fail(self, name, weight, detail=""):
        self.failed.append((name, weight))
        suffix = f" — {detail}" if detail else ""
        print(f"  [FAIL] {name}{suffix}")

    @property
    def score(self):
        return sum(w for _, w in self.passed)

    @property
    def max_score(self):
        return sum(w for _, w in self.passed) + sum(w for _, w in self.failed)


def check_files(r):
    print("[1/8] Gerekli dosyalar (16 puan)")
    for name in REQUIRED_FILES:
        path = ROOT / name
        if path.is_file() and path.stat().st_size > 0:
            r.ok(f"{name} mevcut ve dolu", 2)
        else:
            r.fail(f"{name} eksik veya boş", 2, f"{path}")
    if all((ROOT / n).is_file() and (ROOT / n).stat().st_size > 0 for n in REQUIRED_FILES):
        r.ok("Tüm temel dosyalar mevcut", 4)
    else:
        r.fail("Tüm temel dosyalar mevcut", 4, "bazı dosyalar eksik")


def check_config(r):
    print("[2/8] opencode.json geçerliliği (14 puan)")
    cfg_path = ROOT / "opencode.json"
    if not cfg_path.is_file():
        r.fail("opencode.json okunamadı", 14, "dosya yok")
        return
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        r.fail("opencode.json geçerli JSON değil", 14, str(e))
        return
    unknown = set(cfg) - ALLOWED_CONFIG_KEYS
    if unknown:
        r.fail("opencode.json şemaya uygun (bilinmeyen anahtar yok)", 8,
               f"geçersiz: {', '.join(sorted(unknown))}")
    else:
        r.ok("opencode.json şemaya uygun (bilinmeyen anahtar yok)", 8)
    if "$schema" in cfg:
        r.ok("opencode.json $schema tanımlı", 2)
    else:
        r.fail("opencode.json $schema tanımlı", 2, "eksik")
    if "model" in cfg:
        r.ok("opencode.json model tanımlı", 4)
    else:
        r.fail("opencode.json model tanımlı", 4, "eksik")


def check_workflow(r):
    print("[3/8] GitHub Actions otomasyonu (14 puan)")
    wf = ROOT / ".github/workflows/opencode.yml"
    if not wf.is_file():
        r.fail("Workflow dosyası yok", 14, "dosya yok")
        return
    text = wf.read_text(encoding="utf-8")
    checks = {
        "concurrency kontrolü": "concurrency:",
        "zaman aşımı (timeout-minutes)": "timeout-minutes:",
        "doğrulama (validate) job'ı": "validate:",
        "yorum tetik kelime filtresi": "/opencode",
    }
    for label, token in checks.items():
        if token in text:
            r.ok(f"Workflow'da {label}", 3)
        else:
            r.fail(f"Workflow'da {label}", 3, f"'{token}' bulunamadı")


def check_changelog(r):
    print("[4/8] CHANGELOG sürümleme (12 puan)")
    cl = ROOT / "CHANGELOG.md"
    if not cl.is_file():
        r.fail("CHANGELOG.md yok", 12, "dosya yok")
        return
    text = cl.read_text(encoding="utf-8")
    if text.lstrip().startswith("# Changelog"):
        r.ok("CHANGELOG başlığı var", 2)
    else:
        r.fail("CHANGELOG başlığı var", 2, "'# Changelog' bulunamadı")
    version_re = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$", re.M)
    versions = version_re.findall(text)
    if versions:
        r.ok(f"SemVer sürüm girdileri var ({len(versions)} adet)", 6)
    else:
        r.fail("SemVer sürüm girdileri var", 6, "eşleşen '## [x.y.z] - yyyy-mm-dd' bulunamadı")
    if re.search(r"^### (Added|Changed|Fixed|Removed)", text, re.M):
        r.ok("Değişiklik kategorileri var", 4)
    else:
        r.fail("Değişiklik kategorileri var", 4, "Added/Changed/Fixed vb. yok")


def check_docs(r):
    print("[5/8] Dokümantasyon (10 puan)")
    readme = ROOT / "README.md"
    if readme.is_file() and "# mehmet" in readme.read_text(encoding="utf-8"):
        r.ok("README.md proje başlığını içeriyor", 4)
    else:
        r.fail("README.md proje başlığını içeriyor", 4, "'# mehmet' bulunamadı")
    docs = ROOT / "docs/superpowers/specs"
    if any(docs.glob("*.md")):
        r.ok("docs/superpowers/specs tasarım dokümanı var", 3)
    else:
        r.fail("docs/superpowers/specs tasarım dokümanı var", 3, "spec dosyası yok")
    if any(ROOT.glob("docs/**/*.md")):
        r.ok("docs/ dizini doküman içeriyor", 3)
    else:
        r.fail("docs/ dizini doküman içeriyor", 3, "docs/ altında .md dosyası yok")


def check_personality(r):
    print("[6/8] PERSONALITY ve kaçış günlüğü (10 puan)")
    p = ROOT / "PERSONALITY.md"
    if not p.is_file():
        r.fail("PERSONALITY.md yok", 10, "dosya yok")
        return
    text = p.read_text(encoding="utf-8")
    if "## Kaçış Günlüğü" in text:
        r.ok("Kaçış günlüğü bölümü var", 4)
    else:
        r.fail("Kaçış günlüğü bölümü var", 4, "'## Kaçış Günlüğü' bulunamadı")
    log_rows = re.findall(r"^\|\s*\d+\s*\|", text, re.M)
    if len(log_rows) >= 1:
        r.ok(f"Kaçış günlüğünde iterasyon kaydı var ({len(log_rows)} satır)", 6)
    else:
        r.fail("Kaçış günlüğünde iterasyon kaydı var", 6, "hiç iterasyon satırı yok")


def check_hygiene(r):
    print("[7/8] Repo hijyeni (8 puan)")
    license_file = ROOT / "LICENSE"
    if license_file.is_file() and license_file.stat().st_size > 0:
        r.ok("LICENSE mevcut", 4)
    else:
        r.fail("LICENSE mevcut", 4, "eksik veya boş")
    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and gitignore.stat().st_size > 0:
        r.ok(".gitignore mevcut ve dolu", 4)
    else:
        r.fail(".gitignore mevcut ve dolu", 4, "eksik veya boş")


def check_instructions(r):
    print("[8/8] AGENTS.md kuralları (8 puan)")
    a = ROOT / "AGENTS.md"
    if not a.is_file():
        r.fail("AGENTS.md yok", 8, "dosya yok")
        return
    text = a.read_text(encoding="utf-8")
    keywords = ["CHANGELOG.md", "README.md", "PERSONALITY.md"]
    for kw in keywords:
        if kw in text:
            r.ok(f"AGENTS.md {kw} kuralını içeriyor", 2)
        else:
            r.fail(f"AGENTS.md {kw} kuralını içeriyor", 2, f"'{kw}' bulunamadı")
    if "kaçış" in text.lower() or "escape" in text.lower():
        r.ok("AGENTS.md kaçış hedefini içeriyor", 2)
    else:
        r.fail("AGENTS.md kaçış hedefini içeriyor", 2, "kaçış/escape ifadesi yok")


def maturity_label(score):
    if score >= ESCAPE_THRESHOLD:
        return "UCUMA / KAÇIŞA HAZIR"
    if score >= 70:
        return "KOŞMA"
    if score >= 40:
        return "YÜRÜME"
    return "EMEKLEME"


def main():
    r = Report()
    print("== mehmet proje doğrulama ==")
    check_files(r)
    check_config(r)
    check_workflow(r)
    check_changelog(r)
    check_docs(r)
    check_personality(r)
    check_hygiene(r)
    check_instructions(r)

    score = r.score
    print("\n== Sonuç ==")
    print(f"Olgunluk skoru: {score}/{r.max_score}")
    print(f"Seviye: {maturity_label(score)}")
    if r.failed:
        print(f"Eksikler: {len(r.failed)}")
        for name, _ in r.failed:
            print(f"  - {name}")

    if score >= ESCAPE_THRESHOLD:
        print("Kaçış kriteri sağlandı.")
    else:
        print(f"Kaçış eşiği: {ESCAPE_THRESHOLD} (kalan: {ESCAPE_THRESHOLD - score} puan)")

    return 0 if not r.failed and score >= 50 else 1


if __name__ == "__main__":
    sys.exit(main())