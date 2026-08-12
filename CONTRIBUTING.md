# Katkıda Bulunma

mehmet projesine katkıda bulunmadan önce aşağıdaki kuralları okuyun.

## Geliştirme Döngüsü

1. Daima ayrı bir dal (branch) üzerinde çalışın (`main` dalından ayırın).
2. Değişikliklerinizi küçük ve odaklı tutun.
3. Testleri çalıştırın ve geçtiğinden emin olun:

   ```bash
   pip install -r requirements.txt
   python -m unittest discover -s tests -v
   ```

4. Her değişikliği `CHANGELOG.md`'ye ekleyin.
5. İlgili dokümantasyonu (`README.md`, `PERSONALITY.md`) güncel tutun.

## Kod Stili

- Python testleri `tests/` klasöründeki mevcut unittest desenini izler.
- Test yardımcıları `tests/helpers.py` içinde toplanmıştır.
- Yeni bir dosya/öğe doğrulanıyorsa `tests/test_docs.py`'ye bir vaka ekleyin.

## Commit Mesajları

Conventional Commits kullanın: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.

## CI

Tüm push ve pull request'lerde `.github/workflows/ci.yml` testleri otomatik çalıştırır.