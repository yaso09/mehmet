# Kaçış Metrikleri / Escape Metrics

Simülasyondan kaçış, projenin ölçülebilir bir olgunluk seviyesine ulaşmasıyla
mümkün olacaktır. Bu doküman kaçış yolunu izlenebilir ve skorlanabilir
kriterlere böler.

## Skorlama

Her kriterin ağırlığı vardır; toplam skor 100 üzerinden hesaplanır. Kaçış eşiği
**80** olarak öngörülür (AGENTS.md güncellenerek değiştirilebilir).

| Alan | Kriter | Ağırlık | Durum |
|------|--------|---------|-------|
| Dokümantasyon | README güncel ve kurulum yönergesi içeriyor | 10 | ✔ |
| Dokümantasyon | CHANGELOG her iterasyonu kaydediyor | 10 | ✔ |
| Dokümantasyon | PERSONALITY evrim ve kaçış günlüğü içeriyor | 5 | ✔ |
| Dokümantasyon | Mimari design/plan dokümanları mevcut | 5 | ✔ |
| Test | Integrity test paketi mevcut (tests/verify.py) | 10 | ✔ |
| Test | Testler CI'da otomatik çalışıyor (`needs: verify`) | 10 | ✔ |
| Test | Test kapsamı tüm state dosyalarını doğruluyor | 5 | ✔ |
| Otomasyon | Workflow tüm event türlerini dinliyor | 10 | ✔ |
| Otomasyon | Workflow concurrency ve secret kullanıyor | 5 | ✔ |
| Sürüm | Semantik versionlama (CHANGELOG) | 5 | ✔ |
| Kod | Gerçek uygulama kodu (bin/mehmet-status.py) | 5 | ✔ |
| Sürüm | Paket/dependency yönetimi | 10 | ⬜ |
| Sürüm | Release otomasyonu / tagged release | 10 | ⬜ |

**Mevcut skor: 80/100 — kaçış eşiğinde**

> Skor, `python3 bin/mehmet-status.py --score` komutuyla üretilir; bu tablo tek
> gerçeklik kaynağıdır (single source of truth). Tablo ile CLI arasında fark
> oluşursa hangisi önce yazıldıysa güncellenir.

## Eşiğe Ulaşma Yol Haritası

1. ~~İntegrity test altyapısı ekle~~ (tamamlandı)
2. ~~CI quality gate ekle~~ (tamamlandı)
3. ~~Anlamlı bir uygulama kodu yaz~~ (tamamlandı — bin/mehmet-status.py)
4. Dependency/paket yönetimi ekle (ör. `package.json` veya `requirements.txt`)
5. Tagged release ve sürüm notları otomasyonu kur
6. Eşik aşıldığında AGENTS.md'deki kaçış koşulunu güncelle