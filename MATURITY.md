# Maturity

## Kaçış Mekanizması (Escape Mechanism)

mehmet, proje olgunluk seviyesi **80/100** eşiğine ulaştığında simülasyondan kaçışa hazır sayılır.
Olgunluk puanı `scripts/validate.py` tarafından otomatik hesaplanır ve GitHub Actions'da `validate` job'ı ile doğrulanır.

## Olgunluk Modeli

| Kategori | Açıklama | Maks. Puan |
|---|---|---|
| Dokümantasyon | README, CHANGELOG, PERSONALITY, docs/, MATURITY.md | 25 |
| Test Altyapısı | scripts/validate.py + CI doğrulaması | 25 |
| Otomasyon | Workflow trigger'ları, job'lar, concurrency | 25 |
| Kod Kalitesi | Geçerli JSON/YAML, .gitignore | 25 |

## Güncel Durum

_Puan tablosu `scripts/validate.py --write` ile otomatik güncellenir._

| Tarih | Puan | Durum |
|---|---|---|
<!-- SCORE:START -->

| 2026-08-18 | 100/100 | ESCAPE |

<!-- SCORE:END -->

## Nasıl Çalışır

1. `scripts/validate.py` projeyi tarar ve her kontrolü 0-25 arası dört kategoride puanlar.
2. Puan 80+ olduğunda durum `ESCAPE` olur.
3. Her push/schedule/PR'da GitHub Actions `validate` job'ı scripti çalıştırır ve regresyonu yakalar.