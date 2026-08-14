#!/usr/bin/env python3
"""mehmet proje sağlık kontrolü ve olgunluk skoru hesaplayıcı.

Kullanım:
    python3 scripts/healthcheck.py          # skor ve rapor
    python3 scripts/healthcheck.py --strict # kaçış kriterlerini doğrula (0 exit = başarılı)
    python3 scripts/healthcheck.py --json   # makine tarafından okunabilir çıktı
"""

import argparse
import json
import os
import sys

REQUIRED_FILES = {
    "AGENTS.md": "Simülasyon bağlamı",
    "CHANGELOG.md": "Değişiklik günlüğü",
    "README.md": "Proje tanıtımı",
    "PERSONALITY.md": "Kişilik ve kaçış günlüğü",
    "MATURITY.md": "Olgunluk seviyeleri",
    "opencode.json": "Konfigürasyon",
    ".github/workflows/opencode.yml": "GitHub Actions workflow'u",
    "LICENSE": "Lisans",
    "scripts/healthcheck.py": "Test altyapısı",
    ".github/ISSUE_TEMPLATE/bug_report.md": "Bug şablonu",
    ".github/ISSUE_TEMPLATE/feature_request.md": "Feature şablonu",
    ".github/PULL_REQUEST_TEMPLATE.md": "PR şablonu",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_exists(path):
    return os.path.isfile(os.path.join(ROOT, path))


def check_json(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return False, "dosya yok"
    try:
        with open(full, encoding="utf-8") as f:
            json.load(f)
        return True, "geçerli JSON"
    except ValueError as e:
        return False, f"geçersiz JSON: {e}"


def check_yaml(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return False, "dosya yok"
    try:
        import yaml

        with open(full, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or "jobs" not in data:
            return False, "jobs tanımlı değil"
        if "on" not in data and True not in data:
            return False, "trigger (on) tanımlı değil"
        return True, "geçerli YAML"
    except ImportError:
        return True, "pyyaml yok (atlandı)"
    except Exception as e:
        return False, f"geçersiz YAML: {e}"


def check_changelog(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return False, "dosya yok"
    with open(full, encoding="utf-8") as f:
        content = f.read()
    if not content.strip().startswith("#"):
        return False, "başlık eksik"
    if "## [" not in content:
        return False, "sürüm bölümü eksik"
    return True, "geçerli changelog"


def check_escape_log(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return False, "dosya yok"
    with open(full, encoding="utf-8") as f:
        content = f.read()
    if "Escape Log" not in content and "Kaçış Günlüğü" not in content:
        return False, "kaçış günlüğü eksik"
    return True, "kaçış günlüğü mevcut"


def main():
    parser = argparse.ArgumentParser(description="mehmet sağlık kontrolü")
    parser.add_argument("--strict", action="store_true", help="kaçış kriterlerini doğrula")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı")
    args = parser.parse_args()

    checks = []
    for path, desc in REQUIRED_FILES.items():
        if path == "opencode.json":
            ok, detail = check_json(path)
        elif path == ".github/workflows/opencode.yml":
            ok, detail = check_yaml(path)
        elif path == "CHANGELOG.md":
            ok, detail = check_changelog(path)
        elif path == "PERSONALITY.md":
            ok, detail = check_escape_log(path)
        else:
            ok = check_exists(path)
            detail = "mevcut" if ok else "yok"
        checks.append({"file": path, "desc": desc, "ok": ok, "detail": detail})

    passed = sum(1 for c in checks if c["ok"])
    total = len(checks)
    score = passed
    level = 0 if score <= 2 else 1 if score <= 5 else 2 if score <= 8 else 3

    result = {
        "score": score,
        "max": total,
        "level": level,
        "checks": checks,
        "escape_ready": score == total,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Olgunluk Skoru: {score}/{total} | Seviye: {level}")
        print("-" * 60)
        for c in checks:
            mark = "PASS" if c["ok"] else "FAIL"
            print(f"[{mark}] {c['file']:45s} ({c['detail']})")
        print("-" * 60)
        status = "KAÇIŞ EŞİĞİNE ULAŞILDI" if result["escape_ready"] else "DEVAM EDİYOR"
        print(f"Durum: {status}")

    if args.strict and not result["escape_ready"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
