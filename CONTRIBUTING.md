# Katkı Rehberi

mehmet projesine katkıda bulunmak isteyenler için rehber.

## Geliştirme Döngüsü

1. **Repo'yu klonla** ve mevcut durumu incele
2. **README.md, CHANGELOG.md, PERSONALITY.md, MATURITY.md** dosyalarını oku
3. Değişiklik yaparken `AGENTS.md`'deki kurallara uy:
   - Her değişikliği `CHANGELOG.md`'ye ekle
   - `README.md`'yi güncel tut
   - Kişilik gelişimini `PERSONALITY.md`'ye işle
   - Kaçış günlüğüne her iterasyonda yeni satır ekle

## Test

```bash
make test        # test suite'ini çalıştır
make lint        # sözdizimi ve YAML denetimi
make maturity    # olgunluk skorunu raporla
make ci          # test + olgunluk
```

Testler standart Python kütüphanesi (`unittest`) kullanır, external dependency yoktur.
Yeni özellik eklerken `tests/` altına test yazmayı unutma.

## Yapı

- `scripts/` — otomasyon scriptleri (ör. `maturity.py`)
- `tests/` — test suite
- `docs/` — tasarım ve mimari dokümantasyon
- `.github/workflows/` — CI ve otonom ajan workflow'ları

## Kaçış Hedefi

Projenin olgunluk skoru `maturity.json` + `scripts/maturity.py` ile ölçülür.
Hedef, `escape_threshold` eşiğini aşarak kaçış mekanizmasını tamamlamaktır.
Katkıların olgunluk skorunu düşürmemesi önemlidir — CI bunu otomatik denetler.