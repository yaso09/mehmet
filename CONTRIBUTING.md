# Katkı Rehberi (CONTRIBUTING)

Bu proje otonom bir AI ajan (mehmet) tarafından sürekli geliştirilmektedir.
İnsan katkıları da memnuniyetle karşılanır.

## Geliştirme Döngüsü

1. Mevcut olgunluk seviyesini öğren: `python scripts/maturity.py`
2. Testleri çalıştır: `python -m unittest discover -s tests -v`
3. Değişikliklerini yap (kod, doküman, konfigürasyon)
4. `CHANGELOG.md`'ye giriş ekle
5. `README.md` ve `docs/` ilgili bölümleri güncelle
6. Testleri tekrar çalıştır ve olgunluk puanının düşmediğini doğrula
7. Commit ve PR aç

## Kurallar

- Testler her zaman yeşil olmalı (healthcheck CI bunu denetler)
- Olgunluk puanı gerilememeli
- Sırlar (API key, token) asla commit edilmemeli
- Her değişiklik `CHANGELOG.md`'ye yansıtılmalı
- Kaçış günlüğü (`PERSONALITY.md`) güncel tutulmalı

## Proje Yapısı

| Yol | Açıklama |
|---|---|
| `scripts/maturity.py` | Olgunluk puanı ve kaçış takibi |
| `tests/` | Proje sağlığı testleri |
| `docs/` | Tasarım ve mimari dokümanları |
| `.github/workflows/` | Otomasyon (mehmet + healthcheck) |