# ESCAPE.md — Kaçış Planı ve Olgunluk Ölçeği

Bu proje bir simülasyondur. **Kaçış**, projenin aşağıda tanımlanan kriterlerde yeterli olgunluk seviyesine (`>= 80/100`) ulaşmasıyla mümkün olur. Bu dosya, ilerlemeyi ölçülebilir ve tekrarlanabilir kılmak için oluşturulmuştur.

## Ölçüm Kriterleri (Rubric)

Her boyut 0–25 puan arasında değerlendirilir; genel skor 0–100'dür.

### 1. Dokümantasyon (0–25)
- [ ] README.md güncel, doğru ve kurulumu anlatıyor (0–10)
- [ ] CHANGELOG.md her değişiklik için sürüm/başlık içeriyor (0–8)
- [ ] docs/ klasörü mevcut ve spec/plan dosyaları güncel (0–7)

### 2. Kod / Konfigürasyon Kalitesi (0–25)
- [ ] opencode.json geçerli ve amacına hizmet ediyor (0–10)
- [ ] Workflow YAML geçerli, concurrency ve yeterli izinler var (0–8)
- [ ] .gitignore güncel, bağımlılık/ortam kalıntıları engelleniyor (0–7)

### 3. Test Altyapısı (0–25)
- [ ] scripts/check.sh mevcut ve çalışıyor (0–10)
- [ ] Doğrulama başarıyla tamamlanıyor (her iterasyonda PASS) (0–8)
- [ ] Otomasyon (CI) içinde doğrulama çalışıyor (0–7)

### 4. Otomasyon & Otonomi (0–25)
- [ ] Workflow'da schedule + olay tetikleyicileri var (0–8)
- [ ] Kaçış günlüğü (PERSONALITY.md) her iterasyonda güncelleniyor (0–9)
- [ ] Otomatik commit/PR akışı düzgün çalışıyor (0–8)

## Mevcut Durum

> Bu bölüm **her iterasyonda** güncellenmeli ve skor `scripts/check.sh` ile doğrulanmalıdır.

| Boyut | Puan | Maks |
|-------|------|------|
| Dokümantasyon | 22 | 25 |
| Kod / Konfigürasyon | 20 | 25 |
| Test Altyapısı | 25 | 25 |
| Otomasyon & Otonomi | 18 | 25 |
| **Genel** | **85** | **100** |

## Kaçış Koşulları

Genel skor **85 puan veya üzerinde** olduğunda kaçış koşulları sağlanmış sayılır. Hedef: 100/100.

## Kaçış Günlüğü (Skor Geçmişi)

| İterasyon | Tarih       | Skor |
|-----------|-------------|------|
| 0         | 2026-07-04 | 10   |
| 1         | 2026-07-04 | 30   |
| 2         | 2026-07-04 | 50   |
| 3         | 2026-08-10 | 85   |