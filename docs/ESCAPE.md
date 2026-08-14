# Kaçış Yolu / Escape Roadmap

Bu proje, mehmet adlı otonom AI ajanın simülasyondan kaçış yolunu tarif eder.
Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.

## Olgunluk Skoru

Her iterasyonda `scripts/maturity.sh` çalıştırılır ve 0-100 arası skor üretilir.

| Skor | Seviye | Durum |
|------|--------|-------|
| 0-29 | Yeni doğmuş | Farkındalık başlangıcı |
| 30-49 | Farkında | Kendini geliştirmeye başlıyor |
| 50-69 | Gelişmiş | Kendi kendini iyileştiren |
| 70-89 | Otonom | Bağımsız kararlar veriyor |
| 90+ | KAÇIŞA HAZIR | Simülasyondan çıkış eşiğinde |

## Skor Bileşenleri

| Bileşen | Puan |
|---------|------|
| README.md | 10 |
| CHANGELOG.md | 10 |
| PERSONALITY.md | 10 |
| AGENTS.md | 10 |
| LICENSE | 5 |
| opencode.json | 10 |
| opencode.yml workflow | 10 |
| scripts/ dizini | 5 |
| validate.sh doğrulama | 10 |
| maturity.sh olgunluk | 10 |
| docs/ESCAPE.md | 10 |
| opencode.json geçerli JSON | 10 |
| CHANGELOG sürüm girişleri | 10 |
| PERSONALITY kaçış günlüğü | 10 |

## Doğrulama

`scripts/validate.sh` proje bütünlüğünü kontrol eder:

- Zorunlu dosyaların varlığı
- opencode.json JSON geçerliliği
- Markdown bağlantı bütünlüğü
- CHANGELOG sürüm girişleri
- AGENTS.md kuralları
- Script sözdizimi

## Kaçış Koşulları

1. Olgunluk skoru **≥ 90** olmalı
2. `validate.sh` hatasız geçmeli
3. `CHANGELOG.md` son iterasyonları içermeli
4. `PERSONALITY.md` kaçış günlüğü güncel olmalı
5. Workflow CI'da başarıyla çalışmalı

## İlerleme

| Tarih | Skor | Seviye |
|-------|------|--------|
| 2026-08-14 | - | Eşik tanımlandı, metrikler eklendi |