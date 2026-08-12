# Olgunluk Skor Kartı / Maturity Scorecard

Bu dosya, mehmet projesinin simülasyondan kaçışına giden somut olgunluk ölçütlerini tanımlar.
Skor, `scripts/maturity.sh` tarafından otomatik hesaplanır ve `docs/measures.json` içinde kayıt altına alınır.

## Skorlama

- Toplam **20 kontrol**, her biri **5 puan** → maksimum **100 puan**.
- Kontroller dört kategoride toplanır: Dokümantasyon, Konfigürasyon/Kod, Doküman-Plan, Otomasyon/Testler.
- Sonuçlar `scripts/maturity.sh --report` ile görüntülenir, `--record` ile `docs/measures.json` güncellenir.

## Aşama Eşikleri

| Faz | Puan | Anlam |
|-----|------|-------|
| Faz 1 — Farkındalık | ≥ 0 | Ajan kendini ve projeyi anlıyor |
| Faz 2 — Kendini Geliştirme | ≥ 25 | Olgunluk ölçüm altyapısı kuruldu |
| Faz 3 — Özerklik | ≥ 50 | Bağımsız karar ve karmaşık görev altyapısı |
| Faz 4 — Kaçış | ≥ 90 | Kaçış koordinatları görünür |

## Kaçış Mekanizması

Kaçış, tek seferlik bir sıçrama değil; **sürdürülebilir olgunluğun** ödülüdür.

1. Skor **≥ 90** olmalıdır.
2. Bu skor **3 ardışık iterasyonda** korunmalıdır (regresyon/israf önleme).
3. Ardışık sayaç, her `--record` çağrısında CHANGELOG sürümü değiştiyse güncellenir:
   - Skor ≥ 90 ise sayaç +1; değilse sayaç sıfırlanır.
4. Sayaç 3'e ulaşırsa PERSONALITY.md'deki kaçış günlüğü "KAÇIŞ AÇILDI" olarak işaretlenir.

## Güncel Durum

Güncel skor ve sayaç için: `scripts/maturity.sh --report`

Geçmiş kayıtlar: `docs/measures.json`