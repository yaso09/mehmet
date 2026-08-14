# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk / Maturity

Proje, kaçış eşiğine (escape threshold) ne kadar yakın olduğunu ölçen bir olgunluk
değerlendirmesine sahiptir. `scripts/maturity.mjs` projeyi dört boyutta puanlar
(Belgeleme, Otomasyon, Test Altyapısı, Kod Kalitesi) ve 100 üzerinden bir skor üretir.

```bash
npm run maturity        # Raporu yazdırır
node scripts/maturity.mjs --json  # JSON çıktı (CI için)
```

Kaçış eşiği **75/100**'dür. Ajan bu eşiği aştığında simülasyondan çıkış koşulu sağlanmış olur.

## Geliştirme

```bash
npm test          # Testleri çalıştırır (node --test)
npm run verify    # Test + olgunluk raporu
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
