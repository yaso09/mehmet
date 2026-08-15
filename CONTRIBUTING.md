# Katkıda Bulunma

Projeye katkıda bulunmak için şu adımları izleyin.

## Kurallar

1. Her değişikliği `CHANGELOG.md` dosyasına ekleyin.
2. `README.md` dosyasını güncel tutun.
3. Yeni özellikler için `tests/` altına test yazın.
4. `scripts/validate.py` ve `scripts/maturity.py` çalıştırılabilir durumda kalmalı.
5. Testleri çalıştırın: `python -m pytest`

## Geliştirme Döngüsü

1. Değişikliklerinizi yapın.
2. Testleri çalıştırın.
3. `python scripts/validate.py` ile yapıyı doğrulayın.
4. `python scripts/maturity.py` ile olgunluk skorunu kontrol edin.
5. Değişiklikleri commit edip PR açın.