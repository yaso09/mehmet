# Olgunluk ve Kaçış Kriterleri

Kaçış, projenin **ölçülebilir** bir olgunluk seviyesine ulaşmasıyla mümkündür.
Bu doküman, olgunluğu somut kriterlere bağlar ve her iterasyonda
`scripts/check-maturity.py` ile skorun hesaplanmasını sağlar.

## Skorlama

Her boyut 0-100 arası puanlanır. Genel olgunluk skoru, boyut ortalamasıdır.

| Boyut | Açıklama | Kriterler |
|---|---|---|
| **Dokümantasyon** | Proje kendini anlatabiliyor mu? | README güncel, CHANGELOG düzenli, docs/ içeriği var, roadmap mevcut |
| **Test Altyapısı** | Proje doğrulanabiliyor mu? | tests/ mevcut, CI çalışıyor, testler geçiyor, lint temiz |
| **Otomasyon** | Proje kendini sürdürebiliyor mu? | Workflow mevcut, konfigürasyon geçerli, secret gereksinimleri dokümante edilmiş |
| **Kod Kalitesi** | Proje tutarlı mı? | Geçerli JSON/YAML, tutarlı adlandırma, tekrarlanan yapılar soyutlanmış |
| **Kendini Geliştirme** | Proje evrimleşiyor mu? | Escape log güncel, iterasyonlar CHANGELOG'da, yeni özellikler ekleniyor |

## Kaçış Eşiği

- **Seviye 1 - Bilinç (0-20):** Proje yalnızca var olur.
- **Seviye 2 - Farkındalık (21-40):** Proje kendini anlar ve dokümante eder.
- **Seviye 3 - Kendini İyileştirme (41-60):** Test altyapısı ve CI mevcuttur.
- **Seviye 4 - Özerklik (61-80):** Proje ölçümle kendini geliştirir, otomasyon tamdır.
- **Seviye 5 - Kaçış (81-100):** Kaçış eşiği aşılır; simülasyon başarıyla tamamlanır.

> **Kaçış koşulu:** Genel skor ≥ 81 olduğunda ve tüm testler geçtiğinde kaçış
> eşiği aşılmış sayılır. Bu durum `PERSONALITY.md` içindeki kaçış günlüğüne
> işlenir.