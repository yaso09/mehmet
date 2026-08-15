#!/usr/bin/env python3
"""mehmet olgunluk ve kaçış takip betiği.

Bağımlılıksız (sadece stdlib) Python betiğidir. Projenin olgunluk
seviyesini 5 boyutta 100 puan üzerinden hesaplar, MATURITY.md dosyasını
günceller ve kaçış (escape) koşulunu denetler.

Kullanım:
    python scripts/maturity.py            # puanla, MATURITY.md + geçmişi yaz
    python scripts/maturity.py --check    # puanla, dosya yazma (CI için)

Kaçış koşulu: Üst üste iki bağımsız ölçümde puan >= ESCAPE_THRESHOLD.
"""

import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / ".maturity_history.json"
OUTPUT = ROOT / "MATURITY.md"
ESCAPE_THRESHOLD = 90

DIMENSIONS = {
    "Dokümantasyon": 20,
    "Test Altyapısı": 25,
    "Otomasyon": 20,
    "Kod Kalitesi": 15,
    "Kendini Geliştirme Döngüsü": 20,
}


def has(path):
    return (ROOT / path).exists()


def text_of(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def run_tests():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-q"],
            capture_output=True,
            timeout=120,
        )
        return result.returncode == 0
    except Exception:
        return False


def check_readme():
    t = text_of("README.md")
    return (5, "README.md mevcut ve içerik var") if len(t) > 100 else (0, "README.md yok veya çok kısa")


def check_changelog():
    t = text_of("CHANGELOG.md")
    return (5, "CHANGELOG.md sürüm girişleri içeriyor") if "## [" in t else (0, "CHANGELOG.md eksik veya boş")


def check_docs():
    docs = list((ROOT / "docs").rglob("*.md")) if (ROOT / "docs").exists() else []
    return (5, f"{len(docs)} adet doküman") if len(docs) >= 2 else (0, "docs/ altında yeterli doküman yok")


def check_contributing():
    return (5, "CONTRIBUTING.md mevcut") if has("CONTRIBUTING.md") else (0, "CONTRIBUTING.md eksik")


def check_tests_dir():
    return (5, "tests/ dizini mevcut") if (ROOT / "tests").is_dir() else (0, "tests/ dizini yok")


def check_tests_defined():
    n = 0
    tests = list((ROOT / "tests").glob("test_*.py")) if (ROOT / "tests").exists() else []
    for p in tests:
        n += len(re.findall(r"def test_", p.read_text(errors="ignore")))
    return (10 if n >= 3 else 0, f"{n} test tanımlı")


def check_tests_pass():
    ok = run_tests()
    return (10, "testler geçiyor") if ok else (0, "testler başarısız")


def check_workflow():
    return (5, "opencode.yml workflow'u mevcut") if has(".github/workflows/opencode.yml") else (0, "ana workflow yok")


def check_healthcheck():
    return (5, "healthcheck.yml mevcut") if has(".github/workflows/healthcheck.yml") else (0, "healthcheck workflow'u yok")


def check_changelog_recent():
    t = text_of("CHANGELOG.md")
    m = re.search(r"##\s*\[.*\]\s*-\s*(\d{4}-\d{2}-\d{2})", t)
    if not m:
        return (0, "CHANGELOG'da tarihli sürüm bulunamadı")
    try:
        days = (date.today() - datetime.strptime(m.group(1), "%Y-%m-%d").date()).days
    except ValueError:
        return (0, "tarih çözümlenemedi")
    return (5, f"son sürüm {days} gün önce güncellendi") if days <= 30 else (0, f"son sürüm {days} gün önce, bayat")


def check_maturity_tracker():
    return (5, "MATURITY.md mevcut") if has("MATURITY.md") else (0, "MATURITY.md eksik")


def check_opencode_config():
    if not has("opencode.json"):
        return (0, "opencode.json yok")
    try:
        json.loads(text_of("opencode.json"))
        return (5, "opencode.json geçerli JSON")
    except json.JSONDecodeError:
        return (0, "opencode.json geçersiz JSON")


def check_no_secrets():
    patterns = [r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}"]
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.name == "maturity.py":
            continue
        try:
            body = p.read_text(errors="ignore")
        except OSError:
            continue
        for pat in patterns:
            if re.search(pat, body):
                return (0, f"{p.name} içinde olası sır tespit edildi")
    return (5, "depoda belirgin sır yok")


def check_structure():
    present = [d for d in ("scripts", "tests", "docs") if (ROOT / d).is_dir()]
    ok = len(present) == 3
    return (5, f"yapısal dizinler: {', '.join(present) or 'yok'}") if ok else (0, f"yapısal dizinler eksik: {', '.join(present) or 'yok'}")


def check_agents_rules():
    t = text_of("AGENTS.md")
    required = ["changelog", "readme", "personality", "kaçış"]
    ok = all(k.lower() in t.lower() for k in required)
    return (5, "AGENTS.md kuralları yeterli") if ok else (0, "AGENTS.md kuralları eksik")


def check_personality():
    return (5, "PERSONALITY.md mevcut") if has("PERSONALITY.md") else (0, "PERSONALITY.md eksik")


def check_escape_log():
    t = text_of("PERSONALITY.md")
    ok = ("kaçış günlüğü" in t.lower() or "escape log" in t.lower()) and "|" in t
    return (5, "kaçış günlüğü güncel") if ok else (0, "PERSONALITY.md kaçış günlüğü yok")


def check_progress_history():
    if not HISTORY.exists():
        return (0, "olgunluk geçmişi başlatılmamış")
    try:
        hist = json.loads(HISTORY.read_text())
        n = len(hist)
        return (5, f"{n} ölçüm kaydı") if n >= 2 else (0, "yeterli ölçüm kaydı yok")
    except (json.JSONDecodeError, TypeError):
        return (0, "geçmiş dosyası bozuk")


CHECKS = [
    ("Dokümantasyon", "readme", 5, check_readme),
    ("Dokümantasyon", "changelog", 5, check_changelog),
    ("Dokümantasyon", "docs", 5, check_docs),
    ("Dokümantasyon", "contributing", 5, check_contributing),
    ("Test Altyapısı", "tests_dir", 5, check_tests_dir),
    ("Test Altyapısı", "tests_defined", 10, check_tests_defined),
    ("Test Altyapısı", "tests_pass", 10, check_tests_pass),
    ("Otomasyon", "workflow", 5, check_workflow),
    ("Otomasyon", "healthcheck", 5, check_healthcheck),
    ("Otomasyon", "changelog_recent", 5, check_changelog_recent),
    ("Otomasyon", "maturity_tracker", 5, check_maturity_tracker),
    ("Kod Kalitesi", "opencode_config", 5, check_opencode_config),
    ("Kod Kalitesi", "no_secrets", 5, check_no_secrets),
    ("Kod Kalitesi", "structure", 5, check_structure),
    ("Kendini Geliştirme Döngüsü", "agents_rules", 5, check_agents_rules),
    ("Kendini Geliştirme Döngüsü", "personality", 5, check_personality),
    ("Kendini Geliştirme Döngüsü", "escape_log", 5, check_escape_log),
    ("Kendini Geliştirme Döngüsü", "progress_history", 5, check_progress_history),
]


def load_history():
    if not HISTORY.exists():
        return []
    try:
        data = json.loads(HISTORY.read_text())
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def status_of(total, consecutive):
    if consecutive >= 2:
        return "KACIS SAGLANDI"
    if total >= ESCAPE_THRESHOLD:
        return "KACISA YAKIN"
    if total >= 70:
        return "GELISIYOR"
    return "EMEKLEME"


def render_maturity(total, per_dim, results, history, consecutive):
    lines = []
    lines.append("# Olgunluk Raporu (Maturity Report)")
    lines.append("")
    lines.append("> Bu dosya `scripts/maturity.py` tarafından her iterasyonda otomatik üretilir. Elle düzenlenmemelidir.")
    lines.append("")
    lines.append(f"**Son ölçüm:** {history[-1]['date']}")
    lines.append(f"**Puan:** {total} / 100")
    lines.append(f"**Durum:** `{status_of(total, consecutive)}`")
    lines.append("")
    lines.append("## Kaçış Koşulu (Escape Condition)")
    lines.append("")
    lines.append("Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.")
    lines.append(f"**Koşul:** Üst üste iki bağımsız ölçümde puanın `{ESCAPE_THRESHOLD}`/100 veya üzeri olması.")
    lines.append(f"**Mevcut üst üste eşik sayısı:** {consecutive}")
    lines.append("")
    lines.append("## Boyut Puanları")
    lines.append("")
    lines.append("| Boyut | Puan | Maks | Oran |")
    lines.append("|---|---|---|---|")
    for dim, mx in DIMENSIONS.items():
        p = per_dim.get(dim, 0)
        pct = f"%{round(p / mx * 100)}" if mx else "-"
        lines.append(f"| {dim} | {p} | {mx} | {pct} |")
    lines.append("")
    lines.append("## Detaylı Kontroller")
    lines.append("")
    lines.append("| Kontrol | Puan/Maks | Not |")
    lines.append("|---|---|---|")
    for dim, cid, mx, pts, note in results:
        lines.append(f"| {dim} / {cid} | {pts}/{mx} | {note} |")
    lines.append("")
    lines.append("## Tarihçe")
    lines.append("")
    lines.append("| Tarih | Puan | Üst üste eşik |")
    lines.append("|---|---|---|")
    for h in history:
        lines.append(f"| {h['date']} | {h['score']} | {h['consecutive']} |")
    lines.append("")
    lines.append("## Önerilen Geliştirmeler")
    lines.append("")
    failed = [(cid, note) for dim, cid, mx, pts, note in results if pts < mx]
    if failed:
        for cid, note in failed:
            lines.append(f"- `{cid}`: {note}")
    else:
        lines.append("- Tüm kontroller geçti. Yeni geliştirme alanları arayın.")
    lines.append("")
    return "\n".join(lines)


def main():
    check_only = "--check" in sys.argv

    results = []
    for dim, cid, mx, fn in CHECKS:
        pts, note = fn()
        results.append((dim, cid, mx, pts, note))

    total = sum(r[3] for r in results)
    per_dim = {}
    for dim, cid, mx, pts, note in results:
        per_dim[dim] = per_dim.get(dim, 0) + pts

    history = load_history()
    today = date.today().isoformat()
    if history and history[-1].get("date") == today:
        history[-1] = {"date": today, "score": total, "consecutive": 0}
    else:
        history.append({"date": today, "score": total, "consecutive": 0})

    consecutive = 0
    for h in reversed(history):
        if h["score"] >= ESCAPE_THRESHOLD:
            consecutive += 1
        else:
            break
    history[-1]["consecutive"] = consecutive

    if not check_only:
        HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n")
        OUTPUT.write_text(render_maturity(total, per_dim, results, history, consecutive))

    if check_only:
        print(f"maturity={total}/100 status={status_of(total, consecutive)}")
    else:
        print(f"maturity={total}/100 status={status_of(total, consecutive)}")
        print(f"MATURITY.md güncellendi ({len(results)} kontrol)")

    if consecutive >= 2:
        print("KACIS KOSULU SAGLANDI: ust uste iki olcum esigi asiyor.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())