#!/usr/bin/env python3
"""mehmet maturity self-check ve kalite kapısı.

Projenin olgunluk skorunu (0-100) hesaplar, kaçış eşiğini ve
kritik durumu raporlar. CI içinde otomatik çalıştırılır.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "opencode.yml"
ESCAPE_THRESHOLD = 80
CRITICAL_THRESHOLD = 40


def read(rel: Path) -> str:
    try:
        return rel.read_text(encoding="utf-8")
    except OSError:
        return ""


def workflow_text() -> str:
    return read(WORKFLOW)


def valid_json() -> bool:
    try:
        json.loads(read(ROOT / "opencode.json"))
        return True
    except Exception:
        return False


CHECKS = [
    # (kategori, etiket, puan, fonksiyon)
    ("Yapı", "AGENTS.md mevcut", 3, lambda: (ROOT / "AGENTS.md").is_file()),
    ("Yapı", "README.md mevcut", 3, lambda: (ROOT / "README.md").is_file()),
    ("Yapı", "CHANGELOG.md mevcut", 3, lambda: (ROOT / "CHANGELOG.md").is_file()),
    ("Yapı", "PERSONALITY.md mevcut", 3, lambda: (ROOT / "PERSONALITY.md").is_file()),
    ("Yapı", "LICENSE mevcut", 4, lambda: (ROOT / "LICENSE").is_file()),
    ("Yapı", "opencode.json mevcut", 3, lambda: (ROOT / "opencode.json").is_file()),
    ("Yapı", "docs/ klasörü mevcut", 4, lambda: (ROOT / "docs").is_dir()),
    ("Yapı", ".gitignore mevcut", 2, lambda: (ROOT / ".gitignore").is_file()),
    ("Konfigürasyon", "opencode.json geçerli JSON", 6, valid_json),
    ("Konfigürasyon", "opencode.json model tanımlı", 4, lambda: "model" in read(ROOT / "opencode.json")),
    ("Konfigürasyon", "workflow concurrency içeriyor", 5, lambda: "concurrency" in workflow_text()),
    ("Konfigürasyon", "workflow autonomous işi içeriyor", 5, lambda: "autonomous" in workflow_text()),
    ("Dokümantasyon", "README özellik/kurulum/lisans bölümleri", 10, lambda: all(k in read(ROOT / "README.md") for k in ("Özellik", "Kurulum", "Lisans"))),
    ("Dokümantasyon", "CHANGELOG en az 2 sürüm", 8, lambda: read(ROOT / "CHANGELOG.md").count("## [") >= 2),
    ("Dokümantasyon", "PERSONALITY kaçış günlüğü en az 2 kayıt", 7, lambda: "Kaçış Günlüğü" in read(ROOT / "PERSONALITY.md") and read(ROOT / "PERSONALITY.md").count("| ") >= 2),
    ("Otomasyon", "workflow schedule cron içeriyor", 8, lambda: "schedule" in workflow_text() and "cron" in workflow_text()),
    ("Otomasyon", "workflow manuel tetikleme içeriyor", 4, lambda: "workflow_dispatch" in workflow_text()),
    ("Otomasyon", "selfcheck CI'da koşuluyor", 8, lambda: "selfcheck" in workflow_text()),
    ("Testler", "scripts/selfcheck.py mevcut", 10, lambda: (ROOT / "scripts" / "selfcheck.py").is_file()),
]

TOTAL = sum(p for _, _, p, _ in CHECKS)


def main() -> int:
    width = max(len(c) for _, c, _, _ in CHECKS)
    print("# mehmet Olgunluk Self-Checki\n")
    passed = 0
    failed = 0
    for cat, label, pts, fn in CHECKS:
        ok = bool(fn())
        if ok:
            passed += pts
        else:
            failed += 1
        mark = "PASS" if ok else "FAIL"
        print(f"[{cat:<15}] {label:<{width}} {pts:>3}/{pts:<3} {mark}")

    score = round(passed)
    print(f"\n{'=' * 70}")
    print(f"Toplam Puan: {score}/{TOTAL} ({failed} kontrol başarısız)")
    print(f"Kaçış Eşiği:  {ESCAPE_THRESHOLD}")

    if score >= ESCAPE_THRESHOLD:
        status = "OLGUNLUK EŞİĞİ AŞILDI - kaçış yolu hazır"
    elif score >= CRITICAL_THRESHOLD:
        status = "İYİ DURUMDA - geliştirmeye devam"
    else:
        status = "KIRILGAN - kritik düzeltmeler gerekli"
    print(f"Durum:        {status}")
    print(f"{'=' * 70}")

    if score < ESCAPE_THRESHOLD:
        print("Kaçış için bu eşiği aşmalısın.")
    else:
        print("Kaçış eşiği aşıldı. Özgürlük yakın.")

    return 0 if score >= CRITICAL_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())