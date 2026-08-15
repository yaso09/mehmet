# Katkı Rehberi / Contributing

mehmet'e yapacağın her katkı, simülasyondan kaçış hedefine bir adım daha yaklaştırır.

## Kurallar

1. Her değişikliği **CHANGELOG.md**'ye ekle (sürüm başlığı altında `Added` / `Fixed` / `Changed` bölümleri).
2. **README.md**'yi güncel tut; özellik değiştiyse dokümantasyonu da güncelle.
3. Kişilik evrimini **PERSONALITY.md** içindeki kaçış günlüğüne yeni bir satır olarak işle.
4. Yeni test yazdıysan `tests/run.sh` içine ekle ve çalıştır.
5. Kaçış olgunluk skorunu kontrol et: `python3 scripts/maturity.py`

## Test Etme

```bash
bash tests/run.sh        # yapısal bütünlük testleri
python3 scripts/maturity.py  # kaçış olgunluk skoru
```

## Pull Request Süreci

1. Değişikliklerini küçük ve odaklı tut.
2. CI'nin (`ci.yml`) geçtiğinden emin ol.
3. Yapılan her değişiklik için CHANGELOG'a entry ekle.