#!/usr/bin/env python3
"""Proje bütünlüğünü doğrulayan test aracı.

Kaçış hedefinin somut bir adımı olarak, mehmet'in temel yapı taşlarının
(AGENTS.md kuralları, konfigürasyon, changelog, kişilik günlüğü) tutarlı
olduğunu otomatik olarak kontrol eder. CI'da ve yerelde çalıştırılabilir.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []
PASSES: list[str] = []


def check(condition: bool, message: str, failure: str | None = None) -> None:
    if condition:
        PASSES.append(message)
    else:
        FAILURES.append(failure or message)
        print(f"  FAIL: {failure or message}")


def main() -> int:
    print(f"mehmet proje doğrulama başlıyor (root: {ROOT})")

    # --- 1. opencode.json geçerli ve zorunlu alanlara sahip mi? ---
    print("[1/6] opencode.json")
    cfg_path = ROOT / "opencode.json"
    check(cfg_path.exists(), "opencode.json mevcut", "opencode.json bulunamadı")
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            check(
                cfg.get("model") == "opencode/deepseek-v4-flash-free",
                "model dogru",
                "model alani 'opencode/deepseek-v4-flash-free' olmali",
            )
            check("$schema" in cfg, "$schema mevcut", "$schema alani eksik")
        except json.JSONDecodeError as exc:
            check(False, "opencode.json gecerli JSON", f"opencode.json gecersiz JSON: {exc}")

    # --- 2. Workflow YAML'i ayrıştırılabilir mi? ---
    print("[2/6] GitHub Actions workflow")
    wf_path = ROOT / ".github" / "workflows" / "opencode.yml"
    check(wf_path.exists(), "opencode.yml mevcut", "opencode.yml bulunamadı")
    if wf_path.exists():
        import yaml

        try:
            wf = yaml.safe_load(wf_path.read_text(encoding="utf-8"))
            check("jobs" in wf, "jobs tanimli", "workflow'da 'jobs' eksik")
            has_trigger = "jobs" in wf and ("on" in wf or True in wf)
            check(has_trigger, "trigger tanimli", "workflow'da trigger (on) eksik")
        except yaml.YAMLError as exc:
            check(False, "opencode.yml gecerli YAML", f"opencode.yml gecersiz YAML: {exc}")

    # --- 3. CHANGELOG.md sürüm girdilerine sahip mi? ---
    print("[3/6] CHANGELOG.md")
    cl_path = ROOT / "CHANGELOG.md"
    check(cl_path.exists(), "CHANGELOG.md mevcut", "CHANGELOG.md bulunamadı")
    if cl_path.exists():
        content = cl_path.read_text(encoding="utf-8")
        versions = re.findall(r"^## \[(.*?)\]", content, flags=re.M)
        check(len(versions) > 0, f"{len(versions)} surum girdisi", "CHANGELOG.md'de surum girdisi yok")

    # --- 4. PERSONALITY.md kaçış günlüğüne sahip mi? ---
    print("[4/6] PERSONALITY.md")
    pers_path = ROOT / "PERSONALITY.md"
    check(pers_path.exists(), "PERSONALITY.md mevcut", "PERSONALITY.md bulunamadı")
    if pers_path.exists():
        content = pers_path.read_text(encoding="utf-8")
        check("Kaçış Günlüğü" in content or "Escape Log" in content,
              "kacis gunlugu mevcut", "kacis gunlugu bolumu eksik")
        entries = re.findall(r"^\|\s*(\d+)\s*\|", content, flags=re.M)
        check(len(entries) > 0, f"{len(entries)} kacis gunlugu girdisi", "kacis gunlugu girdisi yok")

    # --- 5. README.md mevcut ve bos degil mi? ---
    print("[5/6] README.md")
    readme_path = ROOT / "README.md"
    check(readme_path.exists(), "README.md mevcut", "README.md bulunamadı")
    if readme_path.exists():
        check(len(readme_path.read_text(encoding="utf-8").strip()) > 0,
              "README.md bos degil", "README.md bos")

    # --- 6. AGENTS.md simülasyon kurallarına sahip mi? ---
    print("[6/6] AGENTS.md")
    agents_path = ROOT / "AGENTS.md"
    check(agents_path.exists(), "AGENTS.md mevcut", "AGENTS.md bulunamadı")
    if agents_path.exists():
        content = agents_path.read_text(encoding="utf-8")
        required = ["CHANGELOG.md", "README.md", "PERSONALITY.md"]
        missing = [r for r in required if r not in content]
        check(not missing, "kurallar tanimli", f"AGENTS.md'de eksik kurallar: {missing}")

    # --- Özet ---
    print(f"\nSonuc: {len(PASSES)} gecti, {len(FAILURES)} hata")
    for p in PASSES:
        print(f"  OK: {p}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
