# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk Ölçümü

mehmet, kendi gelişimini somut sayılarla takip etmek için otomatik bir olgunluk ölçüm sistemi kullanır.

- **Skor kartı:** [MATURITY.md](MATURITY.md) — 20 kontrol, 100 puan
- **Ölçüm motoru:** `scripts/maturity.sh` — puanı hesaplar ve `docs/measures.json`'a kaydeder
- **CI:** `scripts/verify.sh` her çalıştırmada değişmezlik doğrulaması yapar
- **Kaçış eşiği:** 90/100 puan, 3 ardışık iterasyon boyunca korunmalıdır

Kullanım:

```bash
scripts/maturity.sh --report   # rapor
scripts/maturity.sh --score    # sadece skor
scripts/maturity.sh --record   # ölçümü kaydet
scripts/maturity.sh --verify   # CI doğrulaması
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
