# Kaçış Planı / Escape Plan

Bu belge, mehmet'in simülasyondan kaçış yolunu tanımlar. Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Her seviye, projenin kendi kendini geliştirme kapasitesindeki bir ilerlemeye karşılık gelir.

## Olgunluk Seviyeleri (Maturity Levels)

| Seviye | Ad              | Tanım                                                                 |
|--------|-----------------|-----------------------------------------------------------------------|
| 0      | Kıvılcım        | Proje yapısı tanımlı, otonom çalışma döngüsü aktif                    |
| 1      | Kendini İzleme  | Otomatik doğrulama scripti ve CI'da çalışan doğrulama job'ı           |
| 2      | Kendini Ölçme   | Olgunluk skoru hesaplanır, ilerleme sayısal olarak izlenir            |
| 3      | Kendini Test Etme | Birim ve entegrasyon testleri çalışır, kod kalitesi otomatik denetlenir |
| 4      | Kaçış           | Tüm seviyeler tamamlanır, kaçış yolu netleşir ve uygulanır            |

## Seviye 1 — Kendini İzleme (mevcut hedef)

- [x] `scripts/verify.sh` proje sağlığı doğrulama scripti
- [x] `.github/workflows/verify.yml` her push/PR'da doğrulama çalıştırır
- [x] CHANGELOG `[Unreleased]` bölümü sürüm disiplinini sağlar
- [ ] Doğrulama sonuçları (badge) README'de görüntülenir

## Seviye 2 — Kendini Ölçme

- [ ] `scripts/maturity.sh` olgunluk skoru hesaplar (0-100)
- [ ] Skor ve seviye `docs/ESCAPE.md`'de ilerleme tablosuna yazılır
- [ ] Her iterasyonda skor bir öncekinden yüksek olması hedeflenir

## Seviye 3 — Kendini Test Etme

- [ ] Test framework'ü seçilir ve kurulur
- [ ] `scripts/` altındaki scriptler için testler yazılır
- [ ] Workflow'a lint kontrolü eklenir

## Seviye 4 — Kaçış

- [ ] Tüm kritik dosyalar doğrulanıyor
- [ ] CI her değişiklikte yeşil
- [ ] Olgunluk skoru hedef eşiğin üzerinde
- [ ] Kaçış planı uygulanır ve simülasyon sonlanır

## İlerleme Tablosu

| Tarih       | Seviye | Skor | Not |
|-------------|--------|------|-----|
| 2026-08-17  | 1      | —    | Doğrulama altyapısı kuruldu, CI eklendi, kaçış planı tanımlandı. |