# Katkı Rehberi

## Geliştirme

Bu proje otonom bir AI ajanı olan mehmet tarafından geliştirilmektedir,
ancak insan katkıları da açıktır.

### Yerel Geliştirme

1. Depoyu klonla
2. `make check` ile sağlık ve olgunluk skorunu gör
3. `make test` ile testleri çalıştır

### Kurallar

- Her değişiklik CHANGELOG.md'ye eklenmeli
- README.md güncel tutulmalı
- Testler çalışıyor ve `scripts/healthcheck.py` geçiyor olmalı
- GPLv3 lisansına uyulmalı

### PR Süreci

1. `make test` çalıştığını doğrula
2. Değişikliği açıkla (PR şablonunu kullan)
3. Validate workflow'unun yeşile döndüğünü bekle