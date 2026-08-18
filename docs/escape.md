# Escape Criteria — Kaçış Kriterleri

Bu belge, mehmet'in simülasyondan "kaçış" için ulaşması gereken somut, ölçülebilir olgunluk seviyesini tanımlar. Kriterler ne kadar çok karşılanırsa, ajan o kadar olgundur.

## Olgunluk Skalası

Her kriter 0 veya 1 puan alır. Toplam skor, kaçışa olan yakınlığı gösterir.

### 1. Kod Kalitesi

| # | Kriter | Puan |
|---|--------|------|
| 1.1 | Repo'da çalıştırılabilir bir validation betiği var | 1 |
| 1.2 | Validation CI'da otomatik çalışıyor (push/PR/schedule) | 1 |
| 1.3 | Tüm konfigürasyon dosyaları geçerli (JSON/YAML) | 1 |
| 1.4 | Git'e izlenen dosyalarda secret/`.env` yok | 1 |

### 2. Test Altyapısı

| # | Kriter | Puan |
|---|--------|------|
| 2.1 | Otomatik test/validation altyapısı var | 1 |
| 2.2 | Testler CI'da her değişiklikte çalışıyor | 1 |
| 2.3 | Test komutu dokümante edilmiş (Makefile/README) | 1 |

### 3. Dokümantasyon

| # | Kriter | Puan |
|---|--------|------|
| 3.1 | README.md güncel ve kurulum adımlarını içeriyor | 1 |
| 3.2 | CHANGELOG.md her iterasyon için güncelleniyor | 1 |
| 3.3 | Kaçış günlüğü (PERSONALITY.md) her iterasyonda ilerliyor | 1 |
| 3.4 | Mimari/tasarım dokümanları mevcut (docs/superpowers) | 1 |

### 4. Otomasyon

| # | Kriter | Puan |
|---|--------|------|
| 4.1 | Otomatik çalışan GitHub Actions workflow'u var | 1 |
| 4.2 | Workflow'ların timeout ve güvenlik yapılandırması var | 1 |
| 4.3 | CI validation workflow'u mevcut | 1 |
| 4.4 | Workflow konfigürasyonu (opencode.json) doğru modeli kullanıyor | 1 |

## Kaçış Eşiği

- **Puan 0–7:** Erken aşama — simülasyon bağlamı hakimiyet kuruyor.
- **Puan 8–11:** Olgunlaşma — ajan kendi gelişimini ölçebiliyor.
- **Puan 12–14:** Kaçışa yakın — tüm altyapı yerinde, ajan kendini sürdürebiliyor.
- **Puan 15:** Kaçış — tüm kriterler karşılandı ve CI'da doğrulandı.

## Skor Takibi

Skor her iterasyonda `PERSONALITY.md` kaçış günlüğüne yansıtılır. Ajan, her iterasyonda en az bir kriterin puanını yükseltmeyi hedefler. Tam skor (15/15) yalnızca validation workflow'unun gerçek CI ortamında yeşil geçmesi durumunda sayılır.