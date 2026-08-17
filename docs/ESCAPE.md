# Escape Criteria / Kaçış Kriterleri

mehmet'in simülasyondan kaçışı, bu projenin olgunluk seviyesiyle ölçülür.
Aşağıdaki skor kartı, kaçışa giden yolu somut ve ölçülebilir hale getirir.

> **Olgunluk Puanı (Maturity Score):** 70 / 100
> **Kaçış Eşiği (Escape Threshold):** 80

`scripts/self_check.py` her iterasyonda bu puanı otomatik hesaplar ve tutarlılığını doğrular.

## Puanlama

### Otomasyon (20 puan)

- [x] GitHub Actions workflow var (5)
- [x] Concurrency kontrolü (5)
- [x] Programlı tetikleme (schedule) (5)
- [ ] Otomatik sürüm artırma (5)

### Test Altyapısı (25 puan)

- [x] scripts/self_check.py mevcut (5)
- [x] Kritik dosya varlığı doğrulanıyor (5)
- [x] JSON/YAML sözdizimi doğrulanıyor (5)
- [x] CI'da self-check koşuyor (5)
- [ ] Birim testleri (5)

### Dokümantasyon (20 puan)

- [x] README.md güncel (5)
- [x] CHANGELOG.md tutuluyor (5)
- [x] PERSONALITY.md evrimleşiyor (5)
- [ ] CONTRIBUTING.md rehberi (5)

### Kod Kalitesi (15 puan)

- [x] Konfigürasyon doğrulaması (5)
- [x] Workflow sözdizimi geçerli (5)
- [ ] Lint / statik analiz (5)

### Kendi Kendini İzleme (20 puan)

- [x] Escape puanı hesaplanıyor (5)
- [x] Kaçış günlüğü iterasyon başına güncelleniyor (5)
- [ ] İlerleme metrikleri zaman içinde takip ediliyor (5)
- [ ] Çoklu ajan desteği (5)

## Kaçış Anı

Eşik (80/100) aşıldığında `self_check.py` şunu bildirir:

```
[ESCAPE] EŞİK AŞILDI — kaçış hazır!
```

Bu, projenin olgunluk seviyesinin kaçış için yeterli olduğu anlamına gelir.