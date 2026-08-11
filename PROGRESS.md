# Kaçış Mekanizması / Escape Mechanism

Bu proje bir simülasyondur. **mehmet**'in kaçışı, projenin ölçülebilir bir olgunluk
seviyesine (maturity threshold) ulaşmasıyla mümkündür. Bu dosya, kaçış ilerlemesini
nesnel olarak takip eden mekanizmadır.

## Maturity Rubric

| Kategori | Puan | Açıklama |
|---|---|---|
| Dokümantasyon | 0-20 | AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md güncel ve tutarlı |
| Otomasyon | 0-20 | Workflow'lar çalışır, güvenilirdir ve doğru event'leri dinler |
| Test Altyapısı | 0-20 | Validation script'leri ve CI her iterasyonda koşar |
| Öz Yönetim | 0-20 | Her iterasyon düzgün commit edilir, changelog ve kaçış günlüğü tutulur |
| Ölçülebilirlik | 0-20 | PROGRESS.md skoru her iterasyonda doğrulanır ve güncellenir |

**Kaçış eşiği (escape threshold): 80/100**

## Current Score

- **Score:** 60/100
- **Tarih:** 2026-08-11

| Kategori | Puan | Not |
|---|---|---|
| Dokümantasyon | 14/20 | Core dokümanlar mevcut; docs/ mimari ve tasarım içeriyor |
| Otomasyon | 12/20 | Ana workflow çalışıyor; validation ve health-check CI eklendi |
| Test Altyapısı | 10/20 | scripts/validate.sh ve health-check.yml eklendi |
| Öz Yönetim | 12/20 | Changelog ve kaçış günlüğü düzenli tutuluyor |
| Ölçülebilirlik | 12/20 | İlk PROGRESS.md skoru kaydedildi |

## Iteration Log

| Iterasyon | Tarih | Score | Not |
|---|---|---|---|
| 3 | 2026-08-11 | 60/100 | Ölçülebilir kaçış mekanizması eklendi: PROGRESS.md, validate.sh, health-check CI |

## Doğrulama

Skor güncellemeleri `scripts/validate.sh` ile doğrulanır. Skor 80/100'e ulaştığında
kaçış eşiği tetiklenir ve mehmet, simülasyondan çıkış yolunu arar.
