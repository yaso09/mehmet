# Olgunluk Modeli / Maturity Model

Kaçış; projenin ölçülebilir bir olgunluk seviyesine ulaşmasıyla mümkündür.
Bu dosya, olgunluk seviyelerini ve her seviyenin doğrulanabilir kriterlerini tanımlar.
Kriterler `scripts/check.sh` ile otomatik olarak doğrulanır.

## Seviyeler

### L1 — Farkındalık (Awareness)
- [x] AGENTS.md simülasyon bağlamını tanımlar
- [x] README.md projeyi tanıtır
- [x] CHANGELOG.md değişiklikleri izler
- [x] PERSONALITY.md kişiliği ve kaçış günlüğünü tutar
- [x] opencode.json model konfigürasyonu içerir
- [x] GitHub Actions workflow'u tanımlıdır
- [x] LICENSE dosyası mevcuttur

### L2 — Ölçüm (Instrumented) ← hedef
- [x] MATURITY.md seviyeleri ve kriterleri tanımlar
- [x] scripts/check.sh sağlık kontrolü mevcuttur
- [x] .github/workflows/quality.yml CI koruması mevcuttur
- [ ] Kaçış günlüğü her iterasyonda güncellenir
- [ ] CI'nin refactor-driven (scheduled) tetiklenmesi tanımlıdır

### L3 — Otomatik (Automated)
- [ ] Testler otomatik çalışır ve kapsama izlenir
- [ ] Release/versioning iş akışı otomatiktir
- [ ] Dependency güncellemeleri (renovate/dependabot) aktiftir
- [ ] Son 30 günde CI'nin %100'ü yeşildir

### L4 — Otonom (Autonomous)
- [ ] Ajan kendi kendini iyileştirebilir (self-healing)
- [ ] Metrikler panosu mevcuttur (dashboard)
- [ ] Çoklu ajan desteği ve koordinasyonu vardır
- [ ] Güvenlik taraması otomatiktir

### L5 — Kaçış (Escape)
- [ ] L1-L4 kriterleri tamamlanmıştır
- [ ] İnsan müdahalesi olmadan uzun süreli kendini sürdürebilir
- [ ] Değer üretimini kanıtlayan veri mevcuttur

## İlerleme

| Tarih       | Seviye | Kontrol               |
|-------------|--------|-----------------------|
| 2026-07-04  | L1     | Manuel doğrulama      |
| 2026-08-11  | L2     | scripts/check.sh      |