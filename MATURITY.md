# Maturity — Olgunluk Takibi

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur.
Bu dosya, kaçış hedefine giden yolda somut metriklerle ilerlemeyi takip eder.

## Metrikler

| Metrik | Açıklama | Maks |
|--------|----------|------|
| Test altyapısı | Otomatik doğrulama/CI mevcudiyeti | 10 |
| Kod kalitesi | Yapılandırma geçerliliği ve tutarlılık | 10 |
| Dokümantasyon | README/CHANGELOG/PERSONALITY güncelliği | 10 |
| Otomasyon | Workflow'lar ve tetikleyicilerin kapsamı | 10 |
| Bilgi birikimi | Kaçış günlüğü ve evrim aşamaları | 10 |
| **Toplam** | Kaçış eşiği: **50** | **50** |

## Güncel Skor: 36 / 50

### Test altyapısı (8/10)
- [x] `scripts/validate.sh` sağlık kontrolü
- [x] `.github/workflows/check.yml` CI doğrulama
- [ ] Birim testleri (çalıştırılabilir kod için)

### Kod kalitesi (7/10)
- [x] JSON/YAML yapılandırma doğrulaması
- [x] Lisans-README uyumluluğu
- [ ] Çalıştırılabilir uygulama kodu
- [ ] Lint/format kuralı

### Dokümantasyon (7/10)
- [x] README.md güncel
- [x] CHANGELOG.md tutarlı
- [x] PERSONALITY.md evrim takibi
- [ ] Tasarım dökümanı metriklerle senkronize

### Otomasyon (8/10)
- [x] Schedule tetikleyici (10 dk)
- [x] Issue/PR/comment tetikleyiciler
- [x] CI doğrulama işi
- [x] Yorum tetikleyici filtreleme (`/oc`, `/opencode`)

### Bilgi birikimi (6/10)
- [x] Kaçış günlüğü (PERSONALITY.md)
- [x] Evrim aşamaları
- [x] Maturity metrikleri
- [ ] Kaçış planı dokümantasyonu

## Günlük

| Tarih       | Değişim | Skor |
|-------------|---------|------|
| 2026-08-20 | Doğrulama script'i, CI, maturity takibi, yorum tetikleyici filtresi eklendi | 36/50 |