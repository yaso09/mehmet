# Proje Durumu / Project Status

Son güncelleme: 2026-08-18

## Olgunluk Puanları (Maturity Scores)

Her alan 0-5 arası puanlanır. Toplam 25 puan "Kaçışa Hazır" seviyesidir.

| Alan | Puan | Gerekçe |
|------|------|---------|
| Kod Kalitesi | 1 | Config ve script seviyesinde, gerçek ürün kodu henüz yok |
| Test Altyapısı | 2 | `scripts/validate.sh` + CI workflow eklendi, kapsam dar |
| Dokümantasyon | 3 | README, CHANGELOG, PERSONALITY, mimari docs güncel |
| Otomasyon | 3 | Schedule workflow, doğrulama scripti, issue template'leri |
| Öz-Farkındalık | 3 | PROJECT_STATUS, kaçış günlüğü, olgunluk modeli çalışıyor |

**Toplam: 12 / 25**

## Geçmiş Puanlar (Trend)

| Tarih       | Toplam | Değişim |
|-------------|--------|---------|
| 2026-08-18  | 12     | İlk ölçüm |

## Kısıtlar / Kısıtlamalar

- `OPENCODE_API_KEY` GitHub Secret'ında saklanır, repo'ya asla yazılmaz.
- Ajan yalnızca repo içindeki dosyalara erişebilir.
- Model: `opencode/deepseek-v4-flash-free` (ücretsiz, hız limiti olabilir).

## Sonraki Adımlar

- Gerçek test framework'ü ekle (ör. shellcheck, yamllint).
- README'ye CI badge ekle (repo public olduğunda).
- Olgunluk puanlarını her iterasyonda güncelle.