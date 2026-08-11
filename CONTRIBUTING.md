# mehmet'e Katkı Rehberi

mehmet'in geliştirilmesine katkıda bulunmak için şu adımları izleyin.

## Kurallar

1. Yaptığınız her değişikliği `CHANGELOG.md` dosyasına ekleyin.
2. `README.md` dosyasını güncel tutun.
3. Değişiklikleriniz `AGENTS.md`'deki simülasyon kurallarına uygun olmalı.
4. Testlerin geçtiğinden emin olun.

## Geliştirme Döngüsü

```bash
# Testleri çalıştır
python -m unittest discover -s tests -v

# veya pytest varsa
pytest tests/ -v
```

## Branch Stratejisi

- `main` dalı stabil sürümleri barındırır.
- Yeni özellikler için ayrı bir branch açın ve pull request oluşturun.
- Pull request'ler `.github/workflows/ci.yml` üzerinden test edilir.

## Kod Kalitesi

- Yeni testler eklerken `tests/test_project.py` yapısını takip edin.
- Dokümanlar Türkçe ve İngilizce karışık yazılabilir (proje geleneğine uygun).
- Gereksiz emoji kullanımından kaçının.
