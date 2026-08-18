# Contributing

mehmet'e katkıda bulunmak isteyen herkese teşekkürler!

## Süreç

1. Projeyi incele: `README.md`, `docs/ESCAPE.md` ve `AGENTS.md`.
2. Yapacağın değişiklik için `CHANGELOG.md`'ye giriş ekle.
3. Kod değişikliklerinde testleri çalıştır:

   ```bash
   python3 -m unittest discover tests
   python3 scripts/maturity.py
   ```

4. PR açarken `.github/PULL_REQUEST_TEMPLATE.md` şablonunu doldur.

## Kurallar

- `CHANGELOG.md` her değişiklikte güncellenir (sürüm numarası, tarih, Added/Fixed).
- `README.md` projenin gerçek durumunu yansıtır.
- `PERSONALITY.md` kaçış günlüğü her iterasyonda yeni bir satır alır.
- Testler her zaman geçmeli ve olgunluk skoru düşmemelidir.

## Testler

Testler standart kütüphane `unittest` ile yazılır ve `.github/workflows/validate.yml`
tarafından her push/PR'da çalıştırılır.