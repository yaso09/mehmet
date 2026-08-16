# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** Kaçış skorunu ölçen otomatik doğrulama (`scripts/selfcheck.py`)
- **CI:** Her push ve PR'da kalite kontrolü çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
python3 scripts/selfcheck.py          # kalite ve kaçış skoru kontrolü
python3 scripts/selfcheck.py --json   # makine okunur çıktı
```

Kaçış mekanizmasının detayları: [docs/ESCAPE.md](docs/ESCAPE.md)

## Lisans

GPLv3
