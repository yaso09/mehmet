# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Quality Gate:** Her çalışmada `scripts/selfcheck.py` olgunluk skorunu (0-100) hesaplar ve CI'da raporlar

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Olgunluk / Kaçış Sistemi

Kaçış hedefi için ölçülebilir bir olgunluk metriği tanımlanmıştır. `scripts/selfcheck.py`
yapı, konfigürasyon, dokümantasyon, otomasyon ve test kategorilerini kontrol edip skor üretir.
Detaylar için: [docs/MATURITY.md](docs/MATURITY.md)

```bash
python3 scripts/selfcheck.py
```

## Lisans

GPLv3
