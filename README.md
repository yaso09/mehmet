# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Testler

```bash
bash scripts/test.sh              # test suite (doğrulama + olgunluk eşiği)
bash scripts/validate.sh          # JSON/YAML/shell/markdown link doğrulama
bash scripts/score-maturity.sh    # olgunluk skoru raporu (0-100)
```

## Olgunluk ve Kaçış

mehmet, simülasyondan kaçış hedefine doğru ilerlerken `MATURITY.md`'deki
skorlama sistemini kullanır. Kaçış kapısı: olgunluk skoru >= 90 ve
`scripts/test.sh` CI'da yeşil. Güncel skor için `scripts/score-maturity.sh`.

## Lisans

GPLv3
