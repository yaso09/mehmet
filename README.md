# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Simülasyondan kaçış, projenin ölçülebilir bir olgunluk seviyesine ulaşmasıyla mümkündür.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk / Kaçış Durumu

Kaçış eşiği **80/100**'dür. Güncel skor `METRICS.md` içinde izlenir ve her değerlendirmede `npm run assess` ile yenilenir.

- **Skor:** [METRICS.md](./METRICS.md)
- **Kriterler:** [scripts/assess.mjs](./scripts/assess.mjs)
- **Durum:** KACIS_ESIGI_ASILDI

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `npm test` | Testleri çalıştırır (Node built-in test runner, bağımlılıksız) |
| `npm run check` | Sözdizimi kontrolü yapar |
| `npm run assess` | Olgunluk skorunu hesaplar ve `METRICS.md`'yi üretir |
| `npm run test:coverage` | Kapsam raporuyla testleri çalıştırır |

## Proje Yapısı

```
AGENTS.md                 Simülasyon bağlamı ve ajan kuralları
PERSONALITY.md            Ajan kişiliği ve kaçış günlüğü
CHANGELOG.md              Değişiklik günlüğü
METRICS.md                Olgunluk skoru raporu (otomatik üretilir)
scripts/assess.mjs        Olgunluk değerlendirme motoru
test/                     Test altyapısı (Node test runner)
.github/workflows/        CI ve otonom ajan workflow'ları
docs/                     Tasarım ve plan dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Katkı

Katkı rehberi için [CONTRIBUTING.md](./CONTRIBUTING.md), güvenlik politikası için [SECURITY.md](./SECURITY.md) dosyasına bak.

## Lisans

GPLv3