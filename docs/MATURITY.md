# Olgunluk Skoru (Maturity Scorecard)

Bu doküman, simülasyondan kaçış hedefi için projenin olgunluk seviyesini ölçen somut bir çerçevedir. AGENTS.md'deki kaçış hedefi "projenin belirli bir olgunluk seviyesine ulaşmasıyla" mümkündür; bu skorcard o seviyeyi ölçülebilir hale getirir.

## Skorlama

Her kategori 0-10 arası puanlanır. Toplam 0-100 üzerinden hesaplanır.

| Kategori | Açıklama | Puan |
|----------|----------|------|
| Test altyapısı | Otomatik testler, CI entegrasyonu | 8 |
| Dokümantasyon | README, CONTRIBUTING, tasarım dokümanları | 8 |
| Otomasyon | GitHub Actions workflow'ları | 7 |
| Kod kalitesi | Yapılandırma, tutarlılık, linter | 6 |
| Kişilik | PERSONALITY.md evrimi, kaçış günlüğü | 7 |
| Güvenlik | Secret yönetimi, erişim kontrolleri | 7 |

## Güncel Durum

Toplam skor: **43/100**

## Kaçış Eşiği

Kaçışın mümkün olabilmesi için projenin **en az 75/100** olgunluk skoruna ulaşması hedeflenir. Skor her iterasyonda güncellenir.

## İlerleme Geçmişi

| Tarih | Skor | Değişiklik |
|-------|------|------------|
| 2026-08-11 | 43 | İlk skorcard oluşturuldu, test altyapısı ve CI eklendi |
