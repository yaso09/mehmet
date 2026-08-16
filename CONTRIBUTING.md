# Katkı Rehberi

mehmet'e katkıda bulunurken aşağıdaki kurallara uy.

## Kurallar

1. Her değişikliği **CHANGELOG.md**'ye ekle (Added/Fixed/Changed bölümleri).
2. Sürümü değiştiriyorsan **VERSION** dosyasını da güncelle.
3. README.md'yi güncel tut.
4. Değişikliklerden sonra `make validate` çalıştır; tüm kontrollerin PASS olması gerekir.
5. Yeni dosya eklediysen `scripts/validate.py` içindeki `REQUIRED_FILES` listesini gözden geçir.
6. Kişilikle ilgili değişiklikleri **PERSONALITY.md**'deki Kaçış Günlüğü'ne işle.

## Geliştirme Döngüsü

```bash
make validate   # mevcut durumu kontrol et
# ... değişiklikleri yap ...
make validate   # tekrar doğrula (PASS olmalı)
```

## Test Altyapısı

Projenin test altyapısı `scripts/validate.py` üzerinedir:

- Yapısal dosya kontrolleri
- `opencode.json` JSON geçerliliği
- Workflow YAML sözdizimi
- Dokümantasyon tutarlılığı (VERSION ↔ CHANGELOG ↔ README ↔ AGENTS ↔ PERSONALITY)
- Olgunluk skoru (0-100) — kaçış mekanizmasının ilerleme metriği

CI, her push ve PR'da `make validate` çalıştırır.