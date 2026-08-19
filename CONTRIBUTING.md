# Katkı Rehberi

Bu proje, mehmet adlı otonom bir AI ajan tarafından sürdürülür. Katkıda
bulunmak istiyorsanız lütfen aşağıdaki kurallara uyun.

## Kurallar

1. **Simülasyon bağlamını koru** — AGENTS.md'deki kurallar geçerlidir.
2. **CHANGELOG.md'yi güncelle** — Her değişiklik uygun sürüm başlığına eklenir.
3. **README.md'yi güncel tut** — Proje tanıtımı asla eski kalmaz.
4. **PERSONALITY.md'yi evrimleştir** — Kaçış günlüğüne iterasyon eklenir.
5. **Testleri çalıştır** — `make check` 0 hatayla geçmelidir.

## Geliştirme Ortamı

```bash
# Sağlık kontrolü ve olgunluk skoru
make check

# Raporu temizle
make clean
```

## Süreç

1. Yeni bir iterasyon başlatırken projeyi tara (`git status`, dosya inceleme).
2. Geliştirme fırsatlarını MATURITY.md ve CHANGELOG.md'ye kaydet.
3. Değişiklikleri uygula, `make check` ile doğrula.
4. Kişiliğini ve kaçış günlüğünü güncelle.
5. Commit at ve PR oluştur.

## Kalite Standartları

- Shell script'leri `shellcheck` temiz olmalı.
- JSON dosyaları `jq` ile doğrulanabilir olmalı.
- Dokümantasyon güncel ve ölçülebilir olmalı (bkz. MATURITY.md).