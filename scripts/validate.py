#!/usr/bin/env python3
"""mehmet proje sağlığı doğrulama betiği.

Kaçış hedefinin bir parçası: projenin her iterasyonda tutarlı ve sağlıklı
kalmasını garanti eden otomatik kontroller. Çıkış kodu 0 = sağlıklı.

Kullanım:  python3 scripts/validate.py
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def report(ok, name, detail=""):
    tag = "OK " if ok else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{tag}] {name}{suffix}")
    return ok


def check_yaml(path):
    try:
        import yaml
    except ImportError:
        try:
            import ruamel.yaml as yaml
            yaml = yaml.YAML(typ="safe")
            yaml.load(path.read_text())
            return True
        except Exception:
            return False
    try:
        data = yaml.safe_load(path.read_text())
        return data is not None
    except yaml.YAMLError:
        return False


def check_json(path):
    try:
        json.loads(path.read_text())
        return True
    except (json.JSONDecodeError, OSError):
        return False


def check_no_todo_markers():
    ignore = {".git", "node_modules"}
    pattern = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ignore]
        for name in files:
            p = Path(root) / name
            if p == Path(__file__).resolve():
                continue
            if p.suffix not in {".py", ".yml", ".yaml", ".json", ".sh"}:
                continue
            try:
                for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                    if pattern.search(line):
                        hits.append(f"{p.relative_to(ROOT)}:{i}")
            except OSError:
                continue
    return hits


def main():
    results = []

    config = ROOT / "opencode.json"
    results.append(report(
        check_json(config),
        "opencode.json geçerli JSON",
    ))

    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    results.append(report(
        len(workflows) >= 1,
        "en az bir GitHub Actions workflow var",
        f"{len(workflows)} bulundu",
    ))
    for wf in workflows:
        results.append(report(
            check_yaml(wf),
            f"{wf.name} geçerli YAML",
        ))
        text = wf.read_text()
        results.append(report(
            "on:" in text and "jobs:" in text,
            f"{wf.name} `on` ve `jobs` içeriyor",
        ))

    license_text = (ROOT / "LICENSE").read_text(errors="ignore")
    results.append(report(
        "GNU GENERAL PUBLIC LICENSE" in license_text,
        "LICENSE GPLv3 içeriyor",
    ))

    readme = (ROOT / "README.md").read_text(errors="ignore")
    results.append(report(
        os.path.exists(ROOT / "README.md"),
        "README.md mevcut",
    ))
    results.append(report(
        "GPLv3" in readme,
        "README lisans bilgisi LICENSE ile tutarlı (GPLv3)",
    ))

    changelog = (ROOT / "CHANGELOG.md")
    if changelog.exists():
        text = changelog.read_text(errors="ignore")
        versions = re.findall(r"^## \[([\d.]+)\]", text, re.MULTILINE)
        results.append(report(
            bool(versions),
            "CHANGELOG.md sürüm girişleri içeriyor",
            f"{versions[0] if versions else '-'} (en son)",
        ))
    else:
        results.append(report(False, "CHANGELOG.md mevcut"))

    personality = (ROOT / "PERSONALITY.md")
    if personality.exists():
        text = personality.read_text(errors="ignore")
        results.append(report(
            "Kaçış Günlüğü" in text,
            "PERSONALITY.md kaçış günlüğü içeriyor",
        ))
        results.append(report(
            re.search(r"\|\s*\d+\s*\|", text) is not None,
            "kaçış günlüğü en az bir iterasyon kaydı içeriyor",
        ))
    else:
        results.append(report(False, "PERSONALITY.md mevcut"))

    agents = (ROOT / "AGENTS.md")
    results.append(report(
        agents.exists() and "CHANGELOG.md" in agents.read_text(errors="ignore"),
        "AGENTS.md kuralları CHANGELOG kuralını içeriyor",
    ))

    hits = check_no_todo_markers()
    results.append(report(
        not hits,
        "kodda TODO/FIXME marker yok",
        ", ".join(hits[:5]) if hits else "",
    ))

    passed = sum(1 for r in results if r)
    total = len(results)
    print()
    print(f"Sonuç: {passed}/{total} kontrol geçti")

    score = round(passed / total * 100)
    print(f"Sağlık skoru: %{score}")
    if score >= 90:
        print("Kaçış olgunluğu: YÜKSEK")
    elif score >= 60:
        print("Kaçış olgunluğu: ORTA")
    else:
        print("Kaçış olgunluğu: DÜŞÜK")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
