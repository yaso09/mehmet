# Contributing

Teşekkürler! mehmet projesine katkıda bulunmak istiyorsan aşağıdaki kurallara uy.

## Kurallar

1. Her değişiklik `CHANGELOG.md`'ye eklenmelidir.
2. `README.md` güncel tutulmalıdır.
3. Kişilik evrimi `PERSONALITY.md`'ye işlenmelidir.
4. Değişiklikler yapılmadan önce proje taranmalı ve geliştirme fırsatları değerlendirilmelidir.
5. Kod kalitesini, test altyapısını, dokümantasyonu ve otomasyonu iyileştiren katkılar önceliklidir.

## Kalite Kontrolü

Değişiklik göndermeden önce doğrulamayı çalıştır:

```bash
python3 scripts/maturity.py --check
```

Bu komut konfigürasyonları doğrular ve olgunluk skorunu ölçer. Skor
`ESCAPE_THRESHOLD` altındaysa kaçış girişimleri engellenir.

## Branch ve PR Akışı

- Değişiklikler için ayrı bir branch aç.
- PR açarken açıklayıcı bir başlık ve CHANGELOG referansı ekle.
- CI (`ci.yml`) geçmeden PR merge edilmez.

## Lisans

Katkıların GPLv3 lisansı altında kabul edilir.
