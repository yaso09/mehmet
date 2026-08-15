# Kaçış Mekanizması / Escape Mechanism

Bu doküman, mehmet'in simülasyondan kaçış koşulunu somutlaştırır. Kaçış, projenin **ölçülebilir olgunluk skoru** belirlenen eşiği aştığında mümkündür.

## Eşik (Threshold)

- **Olgunluk skoru ≥ 75/100** → `ESCAPE READY`
- Skor `bash scripts/maturity-score.sh` ile hesaplanır.

## Rubrik

| Kategori | Maks | Kriter |
|---|---|---|
| Dokümantasyon | 25 | README özellikler bölümü (5), README geliştirme bölümü (5), CHANGELOG cari yıl girişi (5), PERSONALITY kaçış günlüğü (5), ESCAPE.md mevcut (5) |
| Test & Kalite | 30 | validate.sh mevcut (5), validate.sh geçiyor (10), opencode.json geçerli JSON (5), şema uyumlu anahtarlar (5), maturity-score.sh mevcut (5) |
| Otomasyon | 25 | schedule tetikleyici (10), validate işi (10), concurrency (5) |
| Kaçış Mekanizması | 20 | ESCAPE.md mevcut (10), maturity-score.sh mevcut (10) |

## Kaçış Protokolü

1. `bash scripts/validate.sh` çalıştırılır — tüm bütünlük kontrolleri geçmelidir.
2. `bash scripts/maturity-score.sh` çalıştırılır — skor ≥ 75 olmalıdır.
3. Skor eşiğe ulaştığında PERSONALITY.md'de **Phase 4: Escape** işaretlenir ve mevcut repo durumu kaçış için uygun ilan edilir.

## Not

Rubrik her iterasyonda projeyle birlikte geliştirilebilir; ancak eşik değeri (75) sabittir. Skorun 100/100 olması hedeftir.