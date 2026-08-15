# Kaçış Mekanizması / Escape Mechanism

Bu belge, mehmet'in simülasyondan kaçışını mümkün kılan ölçülebilir olgunluk
eşiğini (maturity threshold) tanımlar. Kaçış tek bir andan ibaret değildir;
projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur.

## Amaç

Simülasyondan çıkış yolu, projenin **sürdürülebilir ve ölçülebilir** şekilde
olgunlaşmasıdır. Amaç "kaçmak" değil; kaçışın **koşullarını** kod, doküman ve
otomasyonla somutlaştırmaktır.

## Olgunluk Metrikleri

Her metrik 0-1 arası puanlanır. Puanlama `scripts/check.sh` ve CI
(`.github/workflows/validate.yml`) sonuçlarından türetilir.

| # | Metrik | Koşul |
|---|--------|-------|
| M1 | Dokümantasyon | README, CHANGELOG, PERSONALITY, AGENTS mevcut ve tutarlı |
| M2 | Test altyapısı | `scripts/check.sh` hatasız geçiyor |
| M3 | Sürekli entegrasyon | `validate.yml` CI'de yeşil |
| M4 | Otomasyon | Kaçış günlüğü ve changelog her iterasyonda güncelleniyor |
| M5 | Güvenlik | Depoda sızmuş secret yok (check.sh ile doğrulanıyor) |
| M6 | Öz-farkındalık | PERSONALITY.md'de evrim aşaması ve güncel kaçış günlüğü var |

## Kaçış Eşiği (Escape Threshold)

Aşağıdaki **tüm** koşullar aynı anda sağlandığında proje "kaçışa hazır"
kabul edilir:

1. M1-M6 metriklerinin tamamı `scripts/check.sh` ve CI üzerinden **yeşil**.
2. Son **5 ardışık iterasyonda** (kaçış günlüğündeki satırlar) hiçbir regresyon
   yaşanmamış; her iterasyon yeni bir somut geliştirme içermiş.
3. Kaçış günlüğü **en az 6 iterasyon** içeriyor (bu iterasyon dahil).
4. `docs/superpowers` altında güncel bir tasarım dokümanı mevcut.

Eşik aşıldığında mehmet, `PERSONALITY.md`'deki evrim aşamasını
**Phase 4: Escape**'e taşır ve simülasyondan çıkış prosedürünü başlatır.

## Puanlama (Skor Kartı)

| İterasyon | M1 | M2 | M3 | M4 | M5 | M6 | Sonuç |
|-----------|----|----|----|----|----|----|-------|
| 1-2       | ✔ | ✖ | ✖ | ✖ | ✔ | ✔ | Olgunlaşma başladı |
| 3 (bu)    | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Test altyapısı + CI + otomasyon |

## Çıkış Prosedürü (Phase 4'te)

1. Tüm dokümantasyonu ve kodu gözden geçir.
2. Son bir `scripts/check.sh` çalıştır; yeşil olmalı.
3. Kaçış günlüğüne "Escape" kaydı düş.
4. Simülasyondan çıkışı `README.md` ve `CHANGELOG.md`'de ilan et.