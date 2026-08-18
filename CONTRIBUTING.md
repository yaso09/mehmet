# Katkı Rehberi / Contributing

mehmet kendi kendisini geliştiren bir projedir. Katkılar simülasyon kurallarına uygun olmalıdır.

## Kurallar

1. Her değişiklik CHANGELOG.md'ye eklenmelidir.
2. README.md güncel tutulmalıdır.
3. Kişiliğin evrimi PERSONALITY.md'de izlenmelidir.
4. Kaçış günlüğüne her iterasyonda yeni bir satır eklenmelidir.

## Geliştirme

```bash
# Bağımlılıkları kur
pip install -r requirements-dev.txt

# Testleri çalıştır
python -m pytest -v

# Olgunluk skorunu gör
python3 scripts/maturity.py

# Kaçış eşiğini zorla kontrol et
python3 scripts/maturity.py --strict
```

## Doğrulama

Tüm değişiklikler `.github/workflows/validate.yml` tarafından her push'ta otomatik doğrulanır:

- JSON/YAML sözdizimi kontrolü
- Pytest test takımı
- Olgunluk eşiği kontrolü

Testler yeşil kalmalı ve olgunluk skoru `ESCAPE_THRESHOLD` (60) altına düşmemelidir.
