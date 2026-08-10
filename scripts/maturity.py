#!/usr/bin/env python3
"""Kaçış olgunluk değerlendirmesi.

Projeyi 8 seviyeli olgunluk merdiveni üzerinde ölçer ve MATURITY.md raporunu
üretir. Seviye 8'e ulaşıldığında kaçış eşiği aşılmış sayılır.
Raporu yeniden üret: python3 scripts/maturity.py
"""
from datetime import date
from pathlib import Path

from validate import (ROOT, MARKER_PATTERNS, SECRET_PATTERNS, changelog_recent,
                      contains, escape_log_recent, maturity_report_recent,
                      regex_in, required_file, scan_free_of, valid_json)

ESCAPE_LEVEL = 8


def tests_present():
    return any(p.suffix == ".py" for p in ROOT.joinpath("tests").glob("test_*.py")), "tests/test_*.py mevcut"


def validate_green():
    from validate import run
    ok = all(run_ok for _, (run_ok, _) in run())
    return ok, "validate.py tüm kapıları yeşil"


LEVELS = [
    (1, "Temel Yapı", "Çekirdek dosyalar ve yapı mevcut.", [
        ("AGENTS.md mevcut", required_file("AGENTS.md", 10)[0]),
        ("README.md mevcut", required_file("README.md", 10)[0]),
        ("opencode.json geçerli", valid_json("opencode.json")[0]),
        ("CHANGELOG.md mevcut", required_file("CHANGELOG.md", 10)[0]),
        ("PERSONALITY.md mevcut", required_file("PERSONALITY.md", 10)[0]),
        ("LICENSE mevcut", required_file("LICENSE", 1000)[0]),
        (".gitignore mevcut", required_file(".gitignore", 1)[0]),
    ]),
    (2, "İzlenebilirlik", "Değişiklikler ve kişilik günlükleniyor.", [
        ("README Kurulum bölümü var", contains("README.md", "## Kurulum")[0]),
        ("CHANGELOG sürüm girişleri var", regex_in("CHANGELOG.md", r"^## \[\d+\.\d+\.\d+\]")[0]),
        ("CHANGELOG güncel", changelog_recent("CHANGELOG.md")[0]),
        ("PERSONALITY kaçış günlüğü var", contains("PERSONALITY.md", "Kaçış Günlüğü")[0]),
        ("Otonom workflow mevcut", required_file(".github/workflows/opencode.yml", 50)[0]),
    ]),
    (3, "Kalite Altyapısı", "Test ve doğrulama araçları mevcut.", [
        ("validate.py mevcut", required_file("scripts/validate.py", 50)[0]),
        ("maturity.py mevcut", required_file("scripts/maturity.py", 50)[0]),
        ("Test dosyaları mevcut", tests_present()[0]),
        ("Makefile mevcut", required_file("Makefile", 10)[0]),
    ]),
    (4, "CI Otomasyonu", "Otomatik doğrulama akışı çalışıyor.", [
        ("ci.yml mevcut", required_file(".github/workflows/ci.yml", 50)[0]),
        ("CI test adımı var", contains(".github/workflows/ci.yml", "unittest")[0]),
        ("CI validate adımı var", contains(".github/workflows/ci.yml", "validate.py")[0]),
        ("CI maturity adımı var", contains(".github/workflows/ci.yml", "maturity.py")[0]),
    ]),
    (5, "Güvenlik ve Saflık", "Sır ve kalıntı işaretlerinden arınmış.", [
        ("Testlerde TODO/FIXME yok", scan_free_of(MARKER_PATTERNS, "TODO/FIXME", "tests")[0]),
        ("Kaynaklarda sır yok", scan_free_of(SECRET_PATTERNS, "sır")[0]),
        ("Otonom workflow API anahtarını secret'tan alıyor",
         contains(".github/workflows/opencode.yml", "secrets.OPENCODE_API_KEY")[0]),
    ]),
    (6, "Belgeleme", "Kullanım ve geliştirme dokümantasyonu tam.", [
        ("README Geliştirme bölümü var", contains("README.md", "## Geliştirme")[0]),
        ("README Proje Yapısı bölümü var", contains("README.md", "## Proje Yapısı")[0]),
        ("README make check'i belgeliyor", contains("README.md", "make check")[0]),
        ("Olgunluk raporu güncel", maturity_report_recent("MATURITY.md")[0]),
    ]),
    (7, "Yeniden Üretilebilirlik", "Kontrol adımları otomatiğe bağlı ve belgeli.", [
        ("Makefile test hedefi var", contains("Makefile", "test")[0]),
        ("Makefile validate hedefi var", contains("Makefile", "validate")[0]),
        ("Makefile maturity hedefi var", contains("Makefile", "maturity")[0]),
        ("Workflow check komutunu kullanıyor", contains(".github/workflows/opencode.yml", "make check")[0]),
    ]),
    (8, "Kaçış Eşiği", "Olgunluk eşiği bütün seviyelerle doğrulanıyor.", [
        ("Kaçış günlüğü güncel", escape_log_recent("PERSONALITY.md")[0]),
        ("README kaçış sistemini belgeliyor", contains("README.md", "Kaçış")[0]),
        ("CHANGELOG son 30 gün içinde güncel", changelog_recent("CHANGELOG.md", 30)[0]),
        ("Tüm doğrulama kapıları yeşil", validate_green()[0]),
    ]),
]


def assess():
    rows = []
    gaps = []
    next_gaps = []
    total_checks = 0
    met_checks = 0
    current_level = 0
    all_met = True
    for level, name, desc, checks in LEVELS:
        met = sum(1 for _, ok in checks if ok)
        total = len(checks)
        total_checks += total
        met_checks += met
        rows.append({"level": level, "name": name, "desc": desc,
                     "met": met, "total": total})
        if all_met and met == total:
            current_level = level
        else:
            if all_met:
                next_gaps = [d for d, ok in checks if not ok]
            all_met = False
        gaps.extend(d for d, ok in checks if not ok)
    score = round(100.0 * met_checks / total_checks, 1)
    return {"score": score, "met": met_checks, "total": total_checks,
            "current": current_level, "escape": ESCAPE_LEVEL,
            "next": current_level + 1 if current_level < ESCAPE_LEVEL else ESCAPE_LEVEL,
            "rows": rows, "gaps": gaps, "next_gaps": next_gaps}


def render(data) -> str:
    today = date.today().isoformat()
    lines = [
        "# Olgunluk Raporu / Maturity",
        "",
        "> Bu rapor `python3 scripts/maturity.py` tarafından otomatik üretilir. Elle düzenleme.",
        "",
        f"Üretim tarihi: {today}",
        "",
        "## Skor",
        "",
        f"- **Seviye:** {data['current']}/{data['escape']}",
        f"- **İlerleme:** %{data['score']} ({data['met']}/{data['total']} kontrol)",
        "",
        "## Seviyeler",
        "",
        "| Seviye | Ad | Durum | Kontrol |",
        "|---|---|---|---|",
    ]
    for r in data["rows"]:
        status = "✅" if r["met"] == r["total"] else ("🔄" if r["level"] == data["current"] + 1 else "⏳")
        lines.append(f"| {r['level']} | {r['name']} | {status} | {r['met']}/{r['total']} |")
    lines.append("")
    lines.append("## Sonraki Adım")
    lines.append("")
    if data["current"] >= data["escape"]:
        lines.append("Kaçış eşiği aşıldı. 🎉")
    else:
        lines.append(f"Hedef: Seviye {data['next']}")
        lines.append("")
        for gap in data["next_gaps"] or ["(yakında tanımlanacak)"]:
            lines.append(f"- [ ] {gap}")
    lines.append("")
    lines.append("## Kaçış Eşiği")
    lines.append("")
    lines.append(f"Seviye {data['escape']}'e ulaşıldığında kaçış eşiği aşılmış sayılır. "
                 f"Mevcut durum: {data['current']}/{data['escape']}.")
    lines.append("")
    return "\n".join(lines)


def write_report(data):
    (ROOT / "MATURITY.md").write_text(render(data), encoding="utf-8")


def main():
    data = assess()
    write_report(data)
    print(f"Olgunluk seviyesi: {data['current']}/{data['escape']} "
          f"(ilerleme %{data['score']}, {data['met']}/{data['total']} kontrol)")
    if data["current"] >= data["escape"]:
        print("Kaçış eşiği aşıldı.")
    else:
        print(f"Sonraki hedef: Seviye {data['next']} — "
              + next(r["name"] for r in data["rows"] if r["level"] == data["next"]))
        for gap in data["next_gaps"]:
            print(f"  - [ ] {gap}")
    print(f"Rapor güncellendi: {ROOT / 'MATURITY.md'}")


if __name__ == "__main__":
    main()