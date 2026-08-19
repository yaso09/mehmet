# Olgunluk Ölçüm Sistemi (Kaçış Mekanizması)

mehmet, simülasyondan kaçış için proje olgunluğunu nesnel olarak ölçer. Bu sistem,
design spec'teki "Ajanın kaçış mekanizması (maturity threshold)" ve
"İlerleme metrikleri" gelecek geliştirmelerini hayata geçirir.

## Çalıştırma

```bash
make maturity          # İnsan-okur rapor
python -m mehmet --json   # Makine-okur JSON rapor
python -m mehmet --strict # Eşiğin altındaysa çıkış kodu 1
```

## Boyutlar ve Ağırlıklar

| Boyut | Ağırlık | Açıklama |
|-------|--------|----------|
| structure | 0.15 | Temel yapı dosyaları (AGENTS.md, opencode.json, .gitignore, LICENSE, workflow) |
| documentation | 0.25 | README, CHANGELOG sürüm kayıtları, PERSONALITY kaçış günlüğü, docs/ |
| code | 0.25 | Paket varlığı, kaynak kod hacmi, docstring, CLI giriş noktası |
| tests | 0.25 | tests/ dizini, test fonksiyonları, testlerin paketi kullanması |
| automation | 0.10 | CI test job, Makefile test hedefi, pyproject.toml paket tanımı |

## Eşik ve Verdict

Toplam skor 0-100 arasındadır. `ESCAPE_THRESHOLD = 95.0`'tir.

| Skor | Verdict |
|------|---------|
| 0–39 | early |
| 40–69 | developing |
| 70–94 | mature |
| 95–100 | escape-ready |

## Ölçüm Geçmişi

| Tarih | Skor | Verdict |
|-------|------|---------|
| 2026-08-19 (v0.3.0 öncesi) | 93.9/100 | mature |
| 2026-08-19 (v0.3.0 sonrası) | 100.0/100 | escape-ready |
