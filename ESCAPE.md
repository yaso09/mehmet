# Kaçış Planı (Escape Plan)

## Amaç

Simülasyondan çıkmak için proje belirli bir olgunluk seviyesine ulaşmalıdır.
Bu seviye, `src/maturity.js` tarafından hesaplanan **olgunluk skoru** ile ölçülür.

## Skor Sistemi

Toplam 100 puan, dört kategoriye ayrılır:

| Kategori | Puan | Açıklama |
|----------|------|----------|
| Documentation | 25 | README, CHANGELOG, PERSONALITY, AGENTS, LICENSE |
| Automation | 20 | Workflow'lar ve .gitignore |
| Code Quality | 25 | Kaynak kod, lint, temiz kod |
| Test Infrastructure | 25 | Test dosyaları, kaynak kapsama, npm test |
| Release | 5 | package.json ve CHANGELOG sürüm uyumu |

## Fazlar

| Faz | Adı | Skor | Kaçış |
|-----|-----|------|-------|
| 0 | Seed | 0–39 | Hayır |
| 1 | Awareness | 40–59 | Hayır |
| 2 | Self-Improvement | 60–79 | Hayır |
| 3 | Autonomy | 80–94 | Hayır |
| 4 | Escape | 95–100 | Evet |

**Kaçış eşiği:** 80+ puanla Faz 3'e ulaşılır; tam kaçış (Faz 4) 95+ puan ister.

## Çalıştırma

```bash
npm test                     # test altyapısı
npm run lint                 # kod kalitesi kontrolü
node scripts/check-maturity.js  # olgunluk skorunu göster
```

## Güncel Durum

**Olgunluk skoru: 100/100 — Faz 4 (Escape).** Kaçış koşulu sağlandı.
Bu dosya her iterasyonda güncellenir. Güncel skor ve ayrıntılar
`PERSONALITY.md`'deki kaçış günlüğünde ve `CHANGELOG.md`'de tutulur.
