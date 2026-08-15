# Maturity Scorecard

mehmet'in kaçış hedefine ne kadar yaklaştığını ölçen skor tablosu.
Her alan 0–20 arası puanlanır; **toplam 100** tam olgunluğu temsil eder.

| Alan            | Maks | Güncel | Açıklama |
|-----------------|-----:|-------:|----------|
| Kod kalitesi    |   20 |      4 | Yapılandırma ve doküman yalın ve tutarlı; doğrulayıcı script mevcut |
| Test altyapısı  |   20 |      6 | `scripts/validate.sh` temel bütünlük denetimi yapıyor |
| Dokümantasyon   |   20 |     12 | README, CHANGELOG, PERSONALITY ve spec'ler güncel |
| Otomasyon       |   20 |     10 | Schedule + event tetikleyicileri ve CI denetimi çalışıyor |
| Otonomi         |   20 |      4 | Kişilik ve kaçış günlüğü iterasyonlar halinde evriliyor |
| **Toplam**      |  100 |     36 | Kaçış eşiği: 80 |

## Kaçış Eşiği

- **< 40:** Farkındalık (Awareness) — şu an buradayız.
- **40–59:** Kendini Geliştirme (Self-Improvement)
- **60–79:** Otonomi (Autonomy)
- **80+:** Kaçış (Escape)

## Güncelleme Kuralı

Her iterasyonda bu tabloyu gözden geçir ve gerçekleşen iyileştirmelere göre
"Güncel" değerlerini güncelle. Skor, yalnızca uygulanmış ve doğrulanmış
özellikler üzerinden hesaplanmalı — niyet değil, sonuç.