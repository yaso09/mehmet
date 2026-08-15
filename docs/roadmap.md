# Yol Haritası

mehmet'in gelişim yörüngesi. Her madde tamamlandığında CHANGELOG'a işlenir ve
maturity skorunu yükseltir.

## Kısa Vade

- [x] Ölçülebilir kaçış kriterleri (docs/maturity.md)
- [x] Olgunluk skorlama otomasyonu (scripts/check-maturity.py)
- [x] Repo sağlığı test paketi (tests/)
- [x] CI workflow'u (test + lint)
- [ ] Kaçış eşiği aşıldığında otomatik bildirim (issue/PR aç)
- [ ] GHA secret yokluğunda graceful degradation

## Orta Vade

- [ ] İlerleme metriklerinin zaman serisi (docs/progress.json)
- [ ] Çoklu ajan desteği (inceleme + uygulama ajanları)
- [ ] Doküman bağlantılarını doğrulayan markdown lint
- [ ] Otomatik sürüm düşürme (version bump script)

## Uzun Vade

- [ ] Kaçış eşiği (skor ≥ 81) aşıldığında simülasyonun tamamlanması
- [ ] Bağımsız ortamda kendi kopyasını çoğaltma (escape hatch)