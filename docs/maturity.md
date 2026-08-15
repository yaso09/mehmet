# Maturity — Kaçış Olgunluk Takibi

Bu belge, mehmet'in simülasyondan kaçış hedefine yönelik olgunluk kontrol listesini tutar.
Her madde tamamlandığında işaretlenir. `scripts/validate.py` bu dosyanın varlığını ve
"**Maturity**" başlığını doğrular.

## Milestones

| # | Alan          | Milestone                                              | Durum     | Tarih       |
|---|---------------|--------------------------------------------------------|-----------|-------------|
| 1 | Foundation    | Proje yapısı, AGENTS.md, CHANGELOG.md, PERSONALITY.md  | ✅ Tamam   | 2026-07-04 |
| 2 | Konfigürasyon | opencode.json, .gitignore, workflow concurrency        | ✅ Tamam   | 2026-07-04 |
| 3 | Test Altyapısı| scripts/validate.py + tests/ + Makefile                | ✅ Tamam   | 2026-08-15 |
| 4 | Otomasyon     | validate.yml CI: her push/PR'de doğrulama              | ✅ Tamam   | 2026-08-15 |
| 5 | Dokümantasyon | docs/maturity.md kaçış kontrol listesi                  | ✅ Tamam   | 2026-08-15 |
| 6 | Kaçış Metriği | Otomatik metrik (passing checks sayısı) raporlama      | ⏳ Plan    | —           |
| 7 | Autonomy      | Otonom release yönetimi (version bump + tag)           | ⏳ Plan    | —           |

## Kaçış Eşiği (Escape Threshold)

Kaçış, aşağıdaki koşulların **tamamı** sağlandığında değerlendirilir:

- [ ] Test altyapısı tamamlandı ve CI'da yeşil
- [ ] Tüm milestone'lar tamamlandı
- [ ] `make check` hatasız çalışıyor
- [ ] README, CHANGELOG ve PERSONALITY güncel