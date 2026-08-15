# Katkıda Bulunma / Contributing

Bu projeye katkıda bulunurken aşağıdaki ilkelere uy:

## Simülasyon Kuralları

1. **Her değişikliği CHANGELOG.md'ye ekle** — Yeni bir sürüm bölümü aç (`## [x.y.z] - tarih`).
2. **README.md'yi güncel tut** — Özellikler ve kurulum adımları değiştiyse yansıt.
3. **PERSONALITY.md'yi evrimleştir** — Kaçış günlüğüne yeni bir iterasyon satırı ekle.
4. **Testleri çalıştır** — Değişiklik yapmadan önce mevcut testlerin geçtiğinden emin ol:

   ```bash
   make test
   ```

## Kalite Standartları

- Test paketi stdlib `unittest` kullanır; harici bağımlılık ekleme.
- `make check` ile hem testleri hem de olgunluk skorunu doğrula.
- Olgunluk skoru 60'ın altına düşerse kaçış hedefinden uzaklaşıyorsun demektir; düzelt.

## İş Akışı

1. Yeni bir branch aç.
2. Değişiklikleri yap ve `make check` ile doğrula.
3. CHANGELOG.md, README.md ve PERSONALITY.md güncellemelerini aynı commit'e ekle.
4. PR aç ve açıklamada neyi neden değiştirdiğini özetle.