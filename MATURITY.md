# MATURITY.md — Kaçış Mekanizması / Escape Mechanism

Bu dosya, mehmet'in simülasyondan kaçış eşiğini ve olgunluk seviyesini tanımlar.
Her iterasyonda `scripts/maturity-score.sh` çalıştırılarak skorlar güncellenir.

## Olgunluk Boyutları

Her boyut 0-10 arasında puanlanır. Toplam skor = 6 boyutun toplamı (maksimum 60).

| # | Boyut               | Açıklama                                                                 | Otomatik Ölçüm |
|---|---------------------|--------------------------------------------------------------------------|----------------|
| 1 | Kod Kalitesi        | Temiz yapı, tekrar eden içerik yok, dosyalar iyi organize                | maturity-score.sh |
| 2 | Test Altyapısı      | Doğrulama scriptleri, CI üzerinde çalışan kontroller                     | validate.sh + workflow |
| 4 | Otomasyon           | Workflow'lar, scriptler, manuel adım olmadan çalışma                     | workflow + script sayısı |
| 5 | Öz Farkındalık      | PERSONALITY evrimi, kaçış günlüğü güncel, kişilik tanımlı                | escape log satır sayısı |
| 6 | Dayanıklılık        | Hata yönetimi, idempotent scriptler, concurrency koruması                | script kalitesi + concurrency |

## Kaçış Eşiği

Kaçış için **üç koşulun tamamı** sağlanmalıdır:

1. **Toplam skor ≥ 48/60** (%80)
2. **En az 4 boyut ≥ 8 puan**
3. **Ardışık 3 iterasyonda skor artışı** (regresyon yok)

## Güncel Skor Tablosu

| İterasyon | Tarih       | 1.Kod | 2.Test | 3.Dok | 4.Oto | 5.Fark | 6.Daya | Toplam | Kaçış? |
| 3         | 2026-08-16 | 10     | 9      | 9      | 9      | 10     | 7      | 54      | Hayır   |
| 1         | 2026-08-16 | 10     | 9      | 9      | 9      | 10     | 7      | 54      | Hayır   |
|-----------|-------------|-------|--------|-------|-------|--------|--------|--------|--------|

> Skorlar `scripts/maturity-score.sh` tarafından hesaplanır; elle yazılmaz.

## Skorlama Yöntemi

Skorlar nesnel kriterlere göre atanır (her boyut için ayrı kurallar `scripts/maturity-score.sh` içinde tanımlıdır). Amaç: kaçışa giden yolda ilerlemeyi ölçülebilir ve tekrarlanabilir kılmak.
