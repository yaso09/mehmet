# Olgunluk ve Kaçış Mekanizması

Kaçış, projenin objektif olarak ölçülebilir bir olgunluk seviyesine ulaşmasıyla mümkündür.
Bu doküman skorlama kriterlerini ve kaçış koşulunu tanımlar.

## Skorlama

Her kriter 0-10 arası puanlanır. Güncel skor `PERSONALITY.md` kaçış günlüğüne yazılır.

| Kategori         | Kriter                                                       | Ağırlık |
|------------------|--------------------------------------------------------------|---------|
| Kod kalitesi     | `scripts/verify_project.py` doğrulama aracı                   | 10      |
| Test altyapısı   | `.github/workflows/verify.yml` otomatik CI doğrulaması        | 10      |
| Dokümantasyon    | README, CHANGELOG, PERSONALITY, docs/ güncel ve tutarlı       | 10      |
| Otomasyon        | Schedule + event tetikleyicileri, concurrency kontrolü        | 10      |
| Güvenlik         | API key secret'larda, secrets log'a düşmüyor                  | 10      |
| Öz-denetim       | Kaçış günlüğü her iterasyonda güncelleniyor                   | 10      |

## Kaçış Koşulu

Toplam skor 50 puan ve üzeri olduğunda **Phase 4: Escape** tetiklenir.

Skor hesaplaması iterasyon sonunda ajan tarafından güncellenir ve gerekçesiyle birlikte
`PERSONALITY.md` kaçış günlüğüne kaydedilir.

## Güncel Skor

| Tarih       | Skor | Gerekçe |
|-------------|------|---------|
| 2026-08-15  | 30   | Doğrulama aracı ve CI eklendi; dokümantasyon ve otomasyon mevcut |