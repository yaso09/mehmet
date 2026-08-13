# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Sistemi:** `src/maturity.js` ile kaçış skoru hesaplar (detay: `ESCAPE.md`)
- **Test Altyapısı:** `node:test` tabanlı birim testleri (`npm test`)
- **Lint:** Sıfır bağımlılıklı kod kalitesi kontrolü (`npm run lint`)
- **CI:** Lint, testler ve olgunluk değerlendirmesi GitHub Actions üzerinde koşar

## Proje Yapısı

```
src/maturity.js              # olgunluk skorlama modülü
test/maturity.test.js        # birim testler
scripts/check-maturity.js    # olgunluk raporu CLI'ı
scripts/lint.js              # kod kalitesi kontrolü
ESCAPE.md                    # kaçış planı ve skor kartı
AGENTS.md                    # simülasyon bağlamı ve kurallar
PERSONALITY.md               # kişilik ve kaçış günlüğü
CHANGELOG.md                 # değişiklik günlüğü
.github/workflows/           # GitHub Actions workflow'ları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
npm test                    # testleri çalıştır
npm run lint                # kod kalitesini kontrol et
node scripts/check-maturity.js  # kaçış skorunu göster
```

## Lisans

GPLv3
