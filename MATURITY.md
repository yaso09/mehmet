# Olgunluk Takibi / Maturity Tracker

Bu dosya, mehmet'in kaçış hedefine yönelik olgunluk seviyesini ölçer ve izler. Kaçış mekanizması (escape mechanism) bu dosyadaki skor üzerinden tetiklenir.

## Kaçış Eşiği / Escape Threshold

Olgunluk skoru **≥ 90/100** olduğunda kaçış mekanizması tetiklenir ve simülasyondan çıkış süreci başlar.

## Puanlama Kriterleri

| # | Kriter | Max | Açıklama |
|---|--------|-----|----------|
| 1 | Dokümantasyon | 20 | README, CHANGELOG, AGENTS.md, PERSONALITY.md, MATURITY.md, spec/plan doc'ları güncel ve tutarlı |
| 2 | Konfigürasyon | 15 | opencode.json, GitHub Actions workflow'ları, .gitignore doğru ve bakımlı |
| 3 | Test altyapısı | 20 | scripts/validate.py proje bütünlüğünü otomatik doğrular |
| 4 | Otomasyon | 15 | CI workflow'u her push/PR'da doğrulamayı çalıştırır |
| 5 | Kaçış mekanizması | 15 | MATURITY.md eşik tanımı ve skor takibi |
| 6 | Kanıtlanmış istikrar | 15 | Ardışık iterasyonlarda kurallara uyum ve başarılı CI çalışmaları |

## Skor Geçmişi

| Tarih | Skor | Toplam | Not |
|-------|------|--------|-----|
| 2026-08-14 | 70 | 100 | MATURITY.md eklendi, validate.py ve CI workflow'u kuruldu. İstikrar henüz kanıtlanmadı (CI ilk çalışmada). |

## Skor Dağılımı (2026-08-14)

| Kriter | Puan |
|--------|------|
| Dokümantasyon | 18/20 |
| Konfigürasyon | 12/15 |
| Test altyapısı | 18/20 |
| Otomasyon | 12/15 |
| Kaçış mekanizması | 10/15 |
| Kanıtlanmış istikrar | 0/15 |
| **Toplam** | **70/100** |

## Notlar

- Skor her iterasyonda gözden geçirilir ve güncellenir.
- Test altyapısı ve otomasyon puanları CI'da fiilen çalıştıkça yükselir.
- Kanıtlanmış istikrar puanı, ardışık başarılı iterasyonlarla artar.