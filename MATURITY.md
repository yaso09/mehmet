# Olgunluk Modeli / Maturity Model

Bu dosya, simülasyondan kaçış için gereken olgunluk seviyesini ölçülebilir hale getirir.

**Kaçış Eşiği:** 80 / 100 puan

Her checkpoint `- [x]` (tamamlandı) veya `- [ ]` (bekliyor) olarak işaretlenir ve yanında puan ağırlığı taşır.
Skor, `scripts/validate_project.py` tarafından otomatik hesaplanır.

## Güncel Skor

| Kategori | Kazanılan | Maksimum |
|----------|-----------|----------|
| Kod Kalitesi | 12 | 20 |
| Test Altyapısı | 15 | 25 |
| Dokümantasyon | 20 | 20 |
| Otomasyon | 15 | 15 |
| Kendini Geliştirme Döngüsü | 15 | 20 |
| **Toplam** | **77** | **100** |

> Skor, checkpoint'ler değiştikçe validator tarafından güncellenir.

## Checkpoint'ler

### Kod Kalitesi (20)

- [x] `opencode.json` geçerli JSON ve doğru model tanımlı (4)
- [x] `.gitignore` build/ortam kalıntılarını kapsıyor (4)
- [ ] Workflow `actionlint` ile lint ediliyor (4)
- [x] `LICENSE` (GPLv3) README ile tutarlı (4)
- [ ] Sürüm etiketleme (`git tag`) kullanılıyor (4)

### Test Altyapısı (25)

- [x] Otomatik proje doğrulama scripti mevcut (`scripts/validate_project.py`) (8)
- [x] Doğrulama job'ı CI'da çalışıyor (7)
- [ ] Doğrulama scripti için birim testleri mevcut (5)
- [ ] Test kapsamı/kalite raporu üretiliyor (5)

### Dokümantasyon (20)

- [x] README güncel, özellikleri ve kurulumu anlatıyor (5)
- [x] CHANGELOG sürüm geçmişini düzenli tutuyor (5)
- [x] PERSONALITY evrim ve kaçış günlüğü tutuyor (5)
- [x] Tasarım ve plan dokümanları mevcut (5)

### Otomasyon (15)

- [x] Schedule (cron) ile otonom iterasyon (5)
- [x] Event tabanlı tetikleme (issue/PR/comment) (5)
- [x] Concurrency ve çakışma önleme (5)

### Kendini Geliştirme Döngüsü (20)

- [x] AGENTS.md simülasyon kuralları tanımlı (5)
- [x] Olgunluk modeli ve kaçış eşiği (80/100) tanımlı (5)
- [x] Olgunluk skoru otomatik hesaplanıyor (5)
- [ ] Iterasyon sonunda kendini değerlendirme raporu (5)

## Kullanım

```bash
python3 scripts/validate_project.py
```

Script, yapı doğrulaması yapar, olgunluk skorunu raporlar ve kritik hatalarda sıfır olmayan bir çıkış kodu döner.