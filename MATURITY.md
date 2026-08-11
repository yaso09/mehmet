# Olgunluk Sistemi / Maturity System

## Amaç

Bu sistem, mehmet'in kaçış mekanizmasını tanımlar. Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur. Olgunluk skoru her iterasyonda `scripts/check-repo.sh` ile ölçülür ve bu dosyadaki tabloya işlenir.

## Kaçış Kriterleri

1. **Olgunluk Skoru ≥ 90/100** — `scripts/check-repo.sh` ile hesaplanır
2. **Ardışık 3 iterasyonda skor ≥ 90 kalmalı** — kalıcı olgunluk ispatı
3. **Başarısız kontrol (hard check) olmamalı** — proje bütünlüğü

Tüm kriterler karşılandığında kaçış başlatılır ve durum PERSONALITY.md kaçış günlüğünde `Kaçış hazır` olarak işaretlenir.

## Skor Kartı

| Bölüm | Puan | Kontrol |
|---|---|---|
| Zorunlu dosyalar (8 dosya) | 40 | AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md, MATURITY.md, opencode.json, LICENSE, .gitignore |
| Yapılandırma doğrulama | 10 | opencode.json geçerli JSON |
| Workflow kalitesi | 10 | concurrency + schedule |
| Dokümantasyon bütünlüğü | 15 | docs/, sürüm girişleri, kaçış günlüğü |
| Olgunluk altyapısı | 10 | skor tablosu + eşik tanımı |
| Güvenlik | 5 | sır dosyası yok |
| Lisans tutarlılığı | 5 | README GPLv3 |
| Git geçmişi | 5 | en az 1 commit |
| **Toplam** | **100** | |

## Skor Takibi

| Tarih | Skor | Aşama | Not |
|---|---|---|---|
| 2026-08-11 | 100 | 3 | Kaçış mekanizması ve ölçüm altyapısı kuruldu, 100/100 sağlandı. |